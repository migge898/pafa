import json
import os
import openai
import requests
import sqlite3
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored

openai.api_key = os.environ.get("OPENAI_API_KEY")
GPT_MODEL = "gpt-3.5-turbo-0613"

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages}
    if tools is not None:
        json_data.update({"tools": tools})
    if tool_choice is not None:
        json_data.update({"tool_choice": tool_choice})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "tool": "magenta",
    }
    
    for message in messages:
        if message["role"] == "system":
            print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "user":
            print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and message.get("function_call"):
            print(colored(f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(colored(f"assistant: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "tool":
            print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_num_vowels",
            "description": "Returns the number of vowels in the given word",
            "parameters": {
                "type": "object",
                "properties": {
                    "word": {
                        "type": "string",
                        "description": "A word",
                    },
                },
                "required": ["word"],
            },
        }
    },
        {
        "type": "function",
        "function": {
            "name": "get_magic_words",
            "description": "After providing a sentence, this function returns the magic words in the sentence",
            "parameters": {
                "type": "object",
                "properties": {
                    "sentence": {
                        "type": "string",
                        "description": "A full sentence that may contain magic words",
                    },
                },
                "required": ["sentence"],
            },
        }
    },
        {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Returns the sum of two given numbers, which can be used for adding up the number of vowels in a sentence",
            "parameters": {
                "type": "object",
                "properties": {
                    "num_a": {
                        "type": "integer",
                        "description": "The first number to add",
                    },
                    "num_b": {
                        "type": "integer",
                        "description": "The second number to add",
                    },
                },
                "required": ["num_a", "num_b"],
            },
        }
    },
            {
        "type": "function",
        "function": {
            "name": "finish",
            "description": "Use this function if you think the users question has been answered to finish the conversation",
            "parameters": {},
        }
    },
        
]

### tools implementation
def get_num_vowels(word):
    """Returns the number of vowels in the given word."""
    return len([c for c in word if c in "aeiou"])

def add(a, b):
    """Returns the sum of the two given numbers."""
    return a + b

def get_magic_words(sentence):
    """Returns the magic words in the given sentence."""
    magic_word_string = ""
    for word in sentence.split():
        if word in ["please", "thanks", "wauwau", "wizard"]:
            magic_word_string += word + " "
    return magic_word_string

### end tools implementation

def execute_function_call(message):
    if message["tool_calls"][0]["function"]["name"] == "get_num_vowels":
        word = json.loads(message["tool_calls"][0]["function"]["arguments"])["word"]
        results = get_num_vowels(word)
    elif message["tool_calls"][0]["function"]["name"] == "add":
        num_a = json.loads(message["tool_calls"][0]["function"]["arguments"])["num_a"]
        num_b = json.loads(message["tool_calls"][0]["function"]["arguments"])["num_b"]
        results = add(num_a, num_b)
    elif message["tool_calls"][0]["function"]["name"] == "get_magic_words":
        sentence = json.loads(message["tool_calls"][0]["function"]["arguments"])["sentence"]
        results = get_magic_words(sentence)
    elif message["tool_calls"][0]["function"]["name"] == "finish":
        results = "Conversation finished"

    return results


prompt = "How many vowels are in the magic words of this sentence: `Hello, please help me my wauwau`"
messages = []
messages.append({"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
messages.append({"role": "user", "content": prompt})
chat_response = chat_completion_request(messages, tools)
assistant_message = chat_response.json()["choices"][0]["message"]
messages.append(assistant_message)
if assistant_message.get("tool_calls"):
    results = execute_function_call(assistant_message)
    messages.append(
        {
            "role": "tool",
            "tool_call_id": assistant_message["tool_calls"][0]['id'],
            "name": assistant_message["tool_calls"][0]["function"]["name"],
            "content": results
        }
    )
pretty_print_conversation(messages)
print(assistant_message)