import json
import instructor
from openai import OpenAI
from pydantic import Field
from instructor import OpenAISchema
from typing import Dict, List
from enum import Enum

from pafa.react.prompt import ReAct_Answer_Prompt, ReAct_Prompt

# Enables `response_model`
client = instructor.patch(OpenAI())


### tools implementation
def get_num_vowels(word):
    """Returns the number of vowels in the given word."""
    return len([c for c in word if c in "aeiou"])


def get_magic_words(sentence):
    """Returns the magic words in the given sentence."""
    magic_word_string = ""
    for word in sentence.split():
        if word in ["please", "thanks", "wauwau", "wizard"]:
            magic_word_string += word + " "
    return magic_word_string


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

    final_answer: str


class Actions(Enum):
    """Actions available for the agent."""

    get_magic_words = "get_magic_words"
    get_num_vowels = "get_num_vowels"


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
        max_retries=2,
        messages=messages,
    )


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


current_state = States.QUESTION
history = """"""
question = "`How many vowels are in the first magic word of this sentence: `Hello, please help me my wauwau`"
system_message = {"role": "system", "content": ReAct_Prompt}
cnt = 0
usage_stats = {}

while cnt < 10:
    match current_state:
        case States.QUESTION:
            history += f"Question: `{question}`"
            current_state = States.THOUGHT
        case States.THOUGHT:
            thought: Thought = chat_completion_request(history, response_model=Thought)
            update_usage_stats(thought, history, f"thought{cnt}", usage_stats)
            if thought.reached_final_answer:
                history += f"\nThought: {thought.thought}\nFinal Answer:"
                current_state = States.FINAL_ANSWER
            else:
                history += f"\nThought: {thought.thought}"
                current_state = States.ACTION
        case States.ACTION:
            action: Action = chat_completion_request(history, response_model=Action)
            update_usage_stats(action, history, f"action{cnt}", usage_stats)
            if action.action_type == Actions.get_magic_words:
                history += f"\nAction: Call get_magic_words with parameter: {action.action_parameter}"
                magic_words = get_magic_words(action.action_parameter)
                history += f"\nObservation: {magic_words}"
            elif action.action_type == Actions.get_num_vowels:
                history += f"\nAction: Call get_num_vowels with parameter: {action.action_parameter}"
                num_vowels = get_num_vowels(action.action_parameter)
                history += f"\nObservation: {num_vowels}"
            current_state = States.OBSERVATION
        case States.OBSERVATION:
            current_state = States.THOUGHT
        case States.FINAL_ANSWER:
            # final_answer: FinalAnswer = chat_completion_request(
            #     history, response_model=FinalAnswer, system_prompt=ReAct_Answer_Prompt
            # )
            # update_usage_stats(final_answer, history, f"final_answer{cnt}", usage_stats)
            print(f"History:\n{history}")

            with open("usage_stats.json", "w") as f:
                json.dump(usage_stats, f, indent=4)
            break

    cnt += 1
