import json
import os
import openai
import requests
import sseclient
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored
from typing import Union, Dict, List

from pafa.react.prompt import ReAct_Answer_Prompt, ReAct_Prompt
from pafa.config.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY
GPT_MODEL = "gpt-3.5-turbo-0613"


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(
    messages, tools=None, tool_choice=None, model=GPT_MODEL
):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    body = {"model": model, "messages": messages}
    if tools is not None:
        body.update({"tools": tools})
    if tool_choice is not None:
        body.update({"tool_choice": tool_choice})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=body,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def fc(
    message: str,
    system_prompt: str,
    tools: List[Dict],
    model: str = GPT_MODEL,
    tool_choice: Union[Dict, None] = None,
    cnt: int = 0,
):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message},
    ]
    body = {
        "model": model,
        "messages": messages,
        "tools": tools,
        "tool_choice": tool_choice if tool_choice else "auto",
    }
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=body,
        )
        tool_call = response.json()["choices"][0]["message"]["tool_calls"][0]

        function_name = tool_call["function"]["name"]
        function_args = json.loads(tool_call["function"]["arguments"])
        return function_name, function_args
    except AttributeError as err:
        print(f"Exception: ", {response.json()["choices"][0]["message"]})
        cnt += 1
        if cnt > 2:
            raise Exception("Error getting tool name and arguments!")
        return fc(
            message,
            f"{system_prompt}.\nCALL A TOOL!.",
            tools,
            model,
        )


def stream_complete(message: str, system_prompt: str, model: str = GPT_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message},
    ]

    body = {"model": model, "messages": messages, "stream": True}
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            stream=True,
            headers=headers,
            json=body,
        )

        client = sseclient.SSEClient(response)
        for event in client.events():
            if event.data != "[DONE]":
                content = event.data["choices"][0]["message"]["content"]
                if content:
                    yield content
    except Exception as e:
        print(e)
        exit(-1)


def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "tool": "magenta",
    }

    for message in messages:
        if message["role"] == "system":
            print(
                colored(
                    f"system: {message['content']}\n", role_to_color[message["role"]]
                )
            )
        elif message["role"] == "user":
            print(
                colored(f"user: {message['content']}\n", role_to_color[message["role"]])
            )
        elif message["role"] == "assistant" and message.get("function_call"):
            print(
                colored(
                    f"assistant: {message['function_call']}\n",
                    role_to_color[message["role"]],
                )
            )
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(
                colored(
                    f"assistant: {message['content']}\n", role_to_color[message["role"]]
                )
            )
        elif message["role"] == "tool":
            print(
                colored(
                    f"function ({message['name']}): {message['content']}\n",
                    role_to_color[message["role"]],
                )
            )


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
        },
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
        },
    },
    {
        "type": "function",
        "function": {
            "name": "Thought",
            "description": "Generate a thought text with past history.",
            "parameters": {
                "type": "object",
                "properties": {
                    "thought_text": {
                        "type": "string",
                        "description": "What your thought is",
                    },
                },
                "required": ["thought_text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "Observation",
            "description": "Generate an observation text with past history.",
            "parameters": {
                "type": "object",
                "properties": {
                    "observation_text": {
                        "type": "string",
                        "description": "Your observation",
                    },
                },
                "required": ["observation_text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "Exit",
            "description": "Exit the process",
            "parameters": {
                "type": "object",
                "properties": {
                    "exit": {
                        "type": "boolean",
                        "description": "Exit",
                    },
                },
                "required": ["sentence"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "FinalAnswer",
            "description": "Based on the history tell if the final answer can be reached",
            "parameters": {
                "type": "object",
                "properties": {
                    "reached_final_answer": {
                        "type": "boolean",
                        "description": "Reached Final Answer",
                    },
                },
                "required": ["reached_final_answer"],
            },
        },
    },
]


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


### end tools implementation


# def execute_function_call(message):
#     function_name = message["tool_calls"][0]["function"]["name"]
#     function_args = json.loads(message["tool_calls"][0]["function"]["arguments"])
#     if function_name == "get_num_vowels":
#         word = function_args["word"]
#         results = get_num_vowels(word)
#     elif function_name == "get_magic_words":
#         sentence = function_args["sentence"]
#         results = get_magic_words(sentence)

#     return results


def execute_function_call(function_name, function_args):
    if function_name == "get_num_vowels":
        word = function_args["word"]
        results = get_num_vowels(word)
    elif function_name == "get_magic_words":
        sentence = function_args["sentence"]
        results = get_magic_words(sentence)

    return results


# prompt = "How many vowels are in the magic words of this sentence: `Hello, please help me my wauwau`"
# messages = []
# messages.append(
#     {
#         "role": "system",
#         "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous.",
#     }
# )
# messages.append({"role": "user", "content": prompt})
# chat_response = chat_completion_request(messages, tools)
# assistant_message = chat_response.json()["choices"][0]["message"]
# messages.append(assistant_message)
# if assistant_message.get("tool_calls"):
#     results = execute_function_call(assistant_message)
#     messages.append(
#         {
#             "role": "tool",
#             "tool_call_id": assistant_message["tool_calls"][0]["id"],
#             "name": assistant_message["tool_calls"][0]["function"]["name"],
#             "content": results,
#         }
#     )
# pretty_print_conversation(messages)
# print(assistant_message)


# history = """"""
# question = "How many vowels are in the first magic word of this sentence: `Hello, please help me my wauwau"
# history += f"Question: `{question}`\nThought:"
# system_message = {"role": "system", "content": ReAct_Prompt}
# cnt = 0

# messages = [system_message, {"role": "user", "content": history}]


# # limit number of iterations
# while cnt < 10:
#     print(f"Beginning iteration {cnt}...")

#     response = chat_completion_request(messages, tools)
#     assistant_message = response.json()["choices"][0]["message"]

#     # This content only exists if the assistant is not calling a tool, otherwise it is null
#     content = assistant_message.get("content")

#     if assistant_message.get("tool_calls"):
#         results = execute_function_call(assistant_message)
#         messages.append(
#             {
#                 "role": "tool",
#                 "tool_call_id": assistant_message["tool_calls"][0]["id"],
#                 "name": assistant_message["tool_calls"][0]["function"]["name"],
#                 "content": results,
#             }
#         )
#     elif content:
#         history += f"\n{content}"
#         if "finalanswer" in content.lower():
#             break
#         messages.append(
#             {
#                 "role": "assistant",
#                 "content": content,
#             }
#         )

#     else:
#         raise Exception("Invalid response from GPT-3")

#     cnt += 1

####################


def reAct(question: str):
    history = """"""
    history_calls = []

    def agent(
        question: Union[str, None],
        function_name: Union[str, None],
        function_arguments: Union[Dict, None],
        history: str = """""",
        false_counts: int = 0,
    ):
        if false_counts >= 4:
            return history, history_calls
        if question:
            history += f"Question: `{question}`"
            fn, fa = fc(history, ReAct_Prompt, tools, GPT_MODEL)
            history_calls.append({"fn": fn, "fa": fa})
            print(f"""Function: {fn} | Arguments: {fa}""")
            print(f"History: {history}")
            return agent(None, fn, fa, history)
        else:
            ACTIONS = ["get_num_vowels", "get_magic_words"]
            if function_name in ACTIONS:
                answer = execute_function_call(function_name, function_arguments)
                history += f"\nAction: Call {function_name} with parameters '{function_arguments}'"
                history += f"\nResult: {answer}"
                print("Result: ", answer)
                print(f"History: {history}")
                fn, fa = fc(history, ReAct_Prompt, tools, GPT_MODEL)
                print(f"""Function: {fn} | Arguments: {fa}""")
                history_calls.append({"fn": fn, "fa": fa})
                return agent(None, fn, fa, history)
            elif function_name == "Thought":
                history += f"\nThought: {function_arguments.get('thought_text')}"
                print(f"History: {history}")
                fn, fa = fc(history, ReAct_Prompt, tools, GPT_MODEL)
                print(f"""Function: {fn} | Arguments: {fa}""")
                history_calls.append({"fn": fn, "fa": fa})
                return agent(None, fn, fa, history)
            elif function_name == "Observation":
                history += f"""\nObservation: {function_arguments.get('observation_text')}
                """
                print(f"History: {history}")
                fn, fa = fc(history, ReAct_Prompt, tools, GPT_MODEL)
                print(f"""Function: {fn} | Arguments: {fa}""")
                history_calls.append({"fn": fn, "fa": fa})
                return agent(None, fn, fa, history)
            elif function_name == "Exit":
                return history, history_calls
            elif function_name == "FinalAnswer":
                history += f"""\nFinal Answer: {function_arguments.get('reached_final_answer')}
                """
                print(f"History: {history}")
                if function_arguments.get("reached_final_answer"):
                    print(f"Inside Final Answer Returning")
                    return history, history_calls
                else:
                    false_counts += 1
                    if false_counts > 4:
                        return history, history_calls
                    else:
                        fn, fa = fc(
                            history,
                            ReAct_Prompt,
                            tools,
                            GPT_MODEL,
                        )
                        history_calls.append({"fn": fn, "fa": fa})
                        return agent(None, fn, fa, history, false_counts)
            else:
                print(f"ERROR: Called unavailable function. Terminating Agent!")
                return history, history_calls

    history, history_calls = agent(question, None, None, history)
    message = f"""Question: `{question}` History: ```{history}```
    """
    final_answer = ""
    # for msg in stream_complete(message, ReAct_Answer_Prompt, GPT_MODEL):
    #     final_answer += msg
    #     clear_terminal()
    #     print(final_answer, end="", flush=True)
    #     sleep(0.1)
    print("#################################################")

    
    messages = [
        {"role": "system", "content": ReAct_Answer_Prompt},
        {"role": "user", "content": message}
    ]
    response = chat_completion_request(messages=messages)
    clear_terminal()
    print(response.json())


####################
reAct(
    "How many vowels are in the first magic word of this sentence: `Hello, please help me my wauwau"
)
