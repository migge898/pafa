import json
import openai
from openai import OpenAI
from typing import List, Dict, Union

# TODO: Change deprecated function to tools in every name and OpenAI-API usage

class FunctionCall:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def __call__(
        self,
        message: str,
        system_prompt: str,
        functions: List[Dict],
        model: str,
        function_call: Union[Dict, None] = None,
        cnt: int = 0,
    ):
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ]
            client = OpenAI()
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                functions=functions,
                function_call=function_call if function_call else "auto"
            )
            print(response)
            function_call = response.choices[0].message.function_call
            function_name = function_call.get("name")
            function_args = json.loads(function_call.get("arguments"))
            return function_name, function_args
        except AttributeError as err:
            # print(f"Exception: ", {response.choices[0].get("message")})
            cnt += 1
            if cnt > 2:
                raise Exception("Error getting function name and arguments!")
            return self.__call__(
                message,
                f"{system_prompt}.\nCALL A FUNCTION!.",
                functions,
                model,
            )


if __name__ == "__main__":
    from pafa.config.config import OPENAI_API_KEY
    from pafa.react.prompt import ReAct_Prompt
    from pafa.react.schemas import Functions

    fc = FunctionCall(OPENAI_API_KEY)
    print("here")
    fn, fa = fc(
        "Question: `How many vowels are in the first magic word of this sentence: `Hello, please help me my wauwau`",
        ReAct_Prompt,
        Functions.functions,
        "gpt-3.5-turbo-16k",
    )
    print(f"Function Name: {fn}")
    print(f"Function Arguments: {json.dumps(fa, indent=4)}")