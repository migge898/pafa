import os
import openai
from openai import OpenAI
from pafa.config.config import OPENAI_API_KEY

GPT_MODEL = "gpt-3.5-turbo-0613"

client = OpenAI(api_key=OPENAI_API_KEY)
