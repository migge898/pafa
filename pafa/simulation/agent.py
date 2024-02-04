import json
import instructor
from openai import OpenAI
from pydantic import Field
from instructor import OpenAISchema
from typing import Dict, List
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
    try:
        with open(f"simulated/namespaces/{namespace}/{pod}.txt", "r") as log_file:
            return log_file.read()
    except FileNotFoundError:
        return f"Pod {pod} not found in namespace {namespace}. To change the namespace, use the action get_pods with the new namespace."


class States(Enum):
    """States available for the agent."""

    QUESTION = "QUESTION"
    THOUGHT = "THOUGHT"
    ACTION = "ACTION"
    OBSERVATION = "OBSERVATION"
    FINAL_ANSWER = "FINAL_ANSWER"


class Thought(OpenAISchema):
    """Thought schema contains text for the thought and a boolean indicating if the final answer can be reached"""

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
    """Actions available for the agent."""

    get_pods = "get_pods"
    get_logs = "get_logs"


class Action(OpenAISchema):
    """Schema for Action takes the name of the action
    as action_type and the corresponding parameter as action_parameter
    """

    action_type: Actions
    action_parameter: str


def chat_completion_request(
    message: str,
    system_prompt: str = ReAct_Prompt,
    model: str = "gpt-3.5-turbo",
    response_model: OpenAISchema = None,
    seed = 42069,
    max_retries = 2,
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

def update_usage_stats(
    resp: OpenAISchema, history: str, call_id: str, usage_stats: Dict
):
    raw_resonse = resp._raw_response.usage
    if call_id not in usage_stats:
        usage_stats[call_id] = {}
        usage_stats[call_id]["history"] = history
        usage_stats[call_id]["input_token"] = raw_resonse.prompt_tokens
        usage_stats[call_id]["output_token"] = raw_resonse.completion_tokens
        usage_stats[call_id]["total_tokens"] = raw_resonse.total_tokens

    # cost calculation from https://openai.com/pricing using gpt-3.5-turbo-1106
    usage_stats["total_input_tokens"] = sum(
        [usage_stats[call_id]["input_token"] for call_id in usage_stats]
    )
    usage_stats["total_output_tokens"] = sum(
        [usage_stats[call_id]["output_token"] for call_id in usage_stats]
    )
    usage_stats["total_tokens"] = sum(
        [usage_stats[call_id]["total_tokens"] for call_id in usage_stats]
    )
    usage_stats["estimated_cost_dollar"] = (
        usage_stats["total_input_tokens"] * 0.0010
        + usage_stats["total_output_tokens"] * 0.002
    )

def main():
    current_state = States.QUESTION
    alert = read_alert("BugTicketServiceOverloaded")
    history = """"""
    question = "Question: What is the root cause and a possible solution for this alert:\n`" + json.dumps(alert, indent=4) + "`"
    completion_cnt = 0
    usage_stats = {}
    namespace = "unknown"
    while completion_cnt < 10:
        print(f"Current State: {current_state}, Count: {completion_cnt}")
        match current_state:
            case States.QUESTION:
                history += f"Question: `{question}`"
                current_state = States.THOUGHT
            case States.THOUGHT:
                thought: Thought = chat_completion_request(history, response_model=Thought)
                completion_cnt += 1
                # update_usage_stats(thought, history, f"thought{cnt}", usage_stats)
                if thought.reached_final_answer:
                    history += f"\nThought: {thought.thought}\nFinal Answer: True"
                    current_state = States.FINAL_ANSWER
                else:
                    history += f"\nThought: {thought.thought}"
                    current_state = States.ACTION
            case States.ACTION:
                action: Action = chat_completion_request(history, response_model=Action)
                completion_cnt += 1
                # update_usage_stats(action, history, f"action{cnt}", usage_stats)
                if action.action_type == Actions.get_pods:
                    namespace = action.action_parameter
                    history += f"\nAction: get_pods[{action.action_parameter}]"
                    log_entries = get_pods(namespace)
                    history += f"\nObservation:\n{log_entries}"
                elif action.action_type == Actions.get_logs:
                    podname = action.action_parameter
                    history += f"\nAction: get_logs[{action.action_parameter}]"
                    log_entries = get_logs(podname, namespace)
                    history += f"\nObservation:\n{log_entries}"
                current_state = States.OBSERVATION
            case States.OBSERVATION:
                current_state = States.THOUGHT
            case States.FINAL_ANSWER:
                final_answer: FinalAnswer = chat_completion_request(
                    history, response_model=FinalAnswer, system_prompt=ReAct_Answer_Prompt
                )
                completion_cnt += 1
                # update_usage_stats(final_answer, history, f"final_answer{cnt}", usage_stats)
                print(f"History:\n{history}")
                print(f"Final Answer:\n")
                print("Root Cause:", final_answer.root_cause)
                print("Solution:", final_answer.solution)
                print("Evidence:", final_answer.evidence)
                with open("usage_stats.json", "w") as f:
                    json.dump(usage_stats, f, indent=4)
                break

        

if __name__ == "__main__":
    
    main()