import os
from langchain.agents import tool
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import OpenAI
from langchain_community.tools.tavily_search import TavilySearchResults


openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None or openai_api_key == "":
    raise Exception("OPENAI_API_KEY not set")


##### Tool definition #####

@tool
def get_num_vowels(word):
    """Returns the number of vowels in the given word."""
    return len([c for c in word if c in "aeiou"])

@tool
def add(list_of_numbers):
    """Accepting a list of numbers that each represent vowel counts, returns the sum of the numbers."""
    return sum(list_of_numbers)

@tool
def get_magic_words(sentence):
    """Returns the magic words in the given sentence."""
    magic_word_string = ""
    for word in sentence.split():
        if word in ["please", "thanks", "wauwau", "wizard"]:
            magic_word_string += word + " "
    return magic_word_string

tools = [get_num_vowels, add, get_magic_words]

# llm = OpenAI(model="gpt-3.5-turbo-1106", openai_api_key=openai_api_key)
llm = OpenAI()

prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke({"input": "How many vowels are in the magic words of this sentence: `Hello, please help me my wauwau`"})