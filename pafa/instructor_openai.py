import instructor
from openai import OpenAI
from pydantic import Field
from instructor import OpenAISchema
from typing import Optional, Union
from enum import Enum

from pafa.react.prompt import ReAct_Prompt

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


####


class Actions(Enum):
    """Actions available for the agent."""

    GET_MAGIC_WORDS = "GET_MAGIC_WORDS"
    GET_NUM_VOWELS = "GET_NUM_VOWELS"


class Action(OpenAISchema):
    """Schema for Action takes the name of the action
    as action_type and argument for that action as action_parameter
    """

    action_type: Actions
    action_parameter: str


class ResponseObject(OpenAISchema):
    """You can either have a thought or an action or a final answer"""

    thought_or_action: Optional[Union[str, Action]]
    final_answer: Optional[str] = Field(
        ..., description="Final answer if question can be answered by you."
    )


history = """"""
question = "`How many vowels are in the first magic word of this sentence: `Hello, please help me my wauwau`"
history += f"Question: `{question}`"
system_message = {"role": "system", "content": ReAct_Prompt}
cnt = 0

while cnt < 10:
    user_message = {
        "role": "user",
        "content": history,
    }

    messages = [system_message, user_message]

    print(f"Beginning iteration {cnt}...")

    resp: ResponseObject = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=ResponseObject,
        max_retries=2,
        messages=messages,
    )

    if resp.final_answer:
        break
    elif resp.thought_or_action:
        if isinstance(resp.thought_or_action, str):
            thought = resp.thought_or_action
            history += f"\nThought: {thought}"
        elif isinstance(resp.thought_or_action, Action):
            action: Action = resp.thought_or_action
            if action.action_type == Actions.GET_MAGIC_WORDS:
                history += f"\nGet magic words of sentence: {action.action_parameter}"
                magic_words = get_magic_words(action.action_parameter)
                history += f"\Observation: Magic words: {magic_words}"
            elif action.action_type == Actions.GET_NUM_VOWELS:
                history += f"\nGet number of vowels in word: {action.action_parameter}"
                num_vowels = get_num_vowels(action.action_parameter)
                history += f"\Observation: Number of vowels: {num_vowels}"
    else:
        raise Exception("Invalid response from GPT-3")

    cnt += 1

print(history)
