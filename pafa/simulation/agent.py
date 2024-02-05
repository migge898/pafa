import json
import instructor
from openai import OpenAI
from pydantic import Field
from instructor import OpenAISchema
from typing import Dict, List, Optional
from enum import Enum

from pafa.simulation.prompt import ReAct_Answer_Prompt, ReAct_Prompt
from pafa.simulation.helpers import convert_pod_list_to_text

# Enables `response_model`
client = instructor.patch(OpenAI())


### tools implementation
def get_pods(namespace: str):
    try:
        with open(
            f"simulated/namespaces/{namespace}/pod-list.json", "r"
        ) as namespace_file:
            pod_list = json.load(namespace_file)
            return convert_pod_list_to_text(pod_list)
    except FileNotFoundError:
        return f"Namespace {namespace} not found."


def get_logs(pod: str, namespace: str):
    if namespace == "unknown":
        return "Namespace is not set."
    try:
        with open(f"simulated/namespaces/{namespace}/{pod}.txt", "r") as log_file:
            return log_file.read()
    except FileNotFoundError:
        return f"[ERR] Pod {pod} not found in namespace {namespace}. Check if the provided namespace is correct."


class States(Enum):
    """States available for the agent."""

    QUESTION = "QUESTION"
    THOUGHT = "THOUGHT"
    ACTION = "ACTION"
    OBSERVATION = "OBSERVATION"
    FINAL_ANSWER = "FINAL_ANSWER"


class Thought(OpenAISchema):
    """Thought schema contains text for the thought and a boolean indicating if the final answer can be reached.
    To find the root cause only consider the log entries to events that happened before the alert was active.
    Try to find hints in the logs that might indicate that the root cause is in another pod or service.
    Try to find recent changes in the logs that might indicate the root cause.
    """

    thought: str
    reached_final_answer: bool


class FinalAnswer(OpenAISchema):
    """With the help of history, answer the question of the beginning in a text."""

    root_cause: str = Field(
        ...,
        description="The root cause of the alert.",
    )
    solution: str = Field(
        ...,
        description="The solution to fix the alert given the history.",
    )
    evidence: str = Field(
        ...,
        description="The evidence found in history to support the solution. This can be a log entry and or a part of an observation like status, restarts etc.",
    )


class Actions(Enum):
    """Actions available for the agent.
    get_pods: Change the namespace and list pods with their names, status, restarts, and age
    get_logs: Get the logs before the alert of a pod in the current namespace. The logs may show that the root cause is in another pod.
    """

    get_pods = "get_pods"
    get_logs = "get_logs"


class Action(OpenAISchema):
    """Schema for Action takes the name of the action
    as action_type and the namespace. If the action_type is get_logs, it also takes the pod_name.
    """

    action_type: Actions
    namespace: str
    pod_name: Optional[str] = None


def chat_completion_request(
    message: str,
    system_prompt: str = ReAct_Prompt,
    model: str = "gpt-3.5-turbo",
    response_model: OpenAISchema = None,
    seed=42069,
    max_retries=2,
):
    user_message = {
        "role": "user",
        "content": message,
    }

    system_message = {
        "role": "system",
        "content": system_prompt,
    }

    messages = [system_message, user_message]

    return client.chat.completions.create(
        model=model,
        response_model=response_model,
        max_retries=max_retries,
        messages=messages,
        seed=seed,
    )


def read_alert(alertname: str):
    with open(f"simulated/alerts/{alertname}.json", "r") as alert_file:
        return json.load(alert_file)


def get_total_tokens(resp: OpenAISchema):
    raw_resonse = resp._raw_response.usage
    return raw_resonse.total_tokens


def agent(
    id: str, alertname: str = "BugTicketServiceOverloaded", model: str = "gpt-3.5-turbo"
):
    result = {
        "id": id,
        "results": {
            "root_cause_pred": None,
            "solution_pred": None,
            "evidence_pred": None,
            "tokens": 0,
            "error": None,
            "completion_cnt": 0,
        },
    }
    error = "No error"
    tokencount = 0
    current_state = States.QUESTION
    alert = read_alert(alertname)
    history = """"""
    question = (
        "Question: What is the root cause and a possible solution for this alert:\n`"
        + json.dumps(alert, indent=4)
        + "`"
    )
    completion_cnt = 0
    usage_stats = {}
    namespace = "unknown"
    try:
        while completion_cnt < 10:
            print(f"Current State: {current_state}, Count: {completion_cnt}")
            match current_state:
                case States.QUESTION:
                    history += f"Question: `{question}`"
                    current_state = States.THOUGHT
                case States.THOUGHT:
                    thought: Thought = chat_completion_request(
                        history, response_model=Thought, model=model
                    )
                    completion_cnt += 1
                    tokencount += get_total_tokens(thought)
                    if thought.reached_final_answer:
                        history += f"\nThought: {thought.thought}\nFinal Answer: True"
                        current_state = States.FINAL_ANSWER
                    else:
                        history += f"\nThought: {thought.thought}"
                        current_state = States.ACTION
                case States.ACTION:
                    action: Action = chat_completion_request(history, response_model=Action)
                    tokencount += get_total_tokens(action)
                    completion_cnt += 1
                    if action.action_type == Actions.get_pods:
                        namespace = action.namespace
                        history += f"\nAction: get_pods[{action.namespace}]"
                        log_entries = get_pods(namespace)
                        history += f"\nObservation:\n{log_entries}"
                    elif action.action_type == Actions.get_logs:
                        podname = action.pod_name
                        namespace = action.namespace
                        history += (
                            f"\nAction: get_logs[namespace={namespace}, pod={podname}]"
                        )
                        log_entries = get_logs(podname, namespace)
                        history += f"\nObservation:\n{log_entries}"
                    current_state = States.OBSERVATION
                case States.OBSERVATION:
                    current_state = States.THOUGHT
                case States.FINAL_ANSWER:
                    break
        if current_state != States.FINAL_ANSWER:
            error = "Final answer not reached"
        final_answer: FinalAnswer = chat_completion_request(
            history,
            response_model=FinalAnswer,
            system_prompt=ReAct_Answer_Prompt,
            model=model,
        )
        tokencount += get_total_tokens(final_answer)
        completion_cnt += 1
    except Exception as e:
        error = str(e)
    print("Finished with id:", id)
    result["results"]["root_cause_pred"] = final_answer.root_cause
    result["results"]["solution_pred"] = final_answer.solution
    result["results"]["evidence_pred"] = final_answer.evidence
    result["results"]["tokens"] = tokencount
    result["results"]["error"] = error
    result["results"]["completion_cnt"] = completion_cnt

    return result, history

if __name__ == "__main__":

    agent()
