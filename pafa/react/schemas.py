import json
from typing import List, Union
from pydantic import BaseModel
from instructor import OpenAISchema
from enum import Enum


class Actions(Enum):
    """Actions available for the agent.
    Only SearchKB action is available
    """

    SEARCH_KB = "SearchKB"


class Action(OpenAISchema):
    """Schema for Action takes the name of the action
    as action_type and argument for that action as search_text
    """

    action_type: Actions
    search_text: str


class Thought(OpenAISchema):
    """Thought scheama contains text for the thought"""

    thought_text: str


class Observation(OpenAISchema):
    """Observation schema contains text for the observation being made"""

    observation_text: str


class FinalAnswer(OpenAISchema):
    reached_final_answer: bool


class Exit(OpenAISchema):
    exit: bool

class Functions:
    functions = [ 
        {
            "name": "Action",
            "description": "Search for a particular text in the knowledge base.",
            "parameters": Action.model_json_schema(),
        },
        {
            "name": "Thought",
            "description": "Generate a thought text with past history.",
            "parameters": Thought.model_json_schema(),
        },
        {
            "name": "Observation",
            "description": "Generate an observation text with past history.",
            "parameters": Observation.model_json_schema(),
        },
        {
            "name": "FinalAnswer",
            "description": "Based on the history tell if the final answer can be reached",
            "parameters": FinalAnswer.model_json_schema(),
        },
        {
            "name": "Exit",
            "description": "Exit the process",
            "parameters": Exit.model_json_schema(),
        },
    ]

if __name__ == "__main__":
    print(json.dumps(Functions.functions, indent=4))
    exit()