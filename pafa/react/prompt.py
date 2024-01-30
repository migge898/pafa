ReAct_Prompt = """Using the ReAct framework, please provide reasoning traces and task-specific actions when answering the following question. Your only actions are get_magic_words[Sentence] and get_num_vowels[WORD]. Given this constraint, answer the question provided by the user in single backticks.
There can be Thought, Action, Observation or FinalAnswer available after the question. So please do not to repeat a same Thought or Observation. Do not repeat the same search text for the action. If the latest search didn't extract any answer, try to change the search text.
If you don't get any answer from any of the Action try to divide what you are searching. Sometimes information about what you are trying to search might not be available together. You might need to go more granular.
If you don't know how ReAct framework works, refer the following example.
Question: `What is the number of vowels in the second magic word: I love wauwau, please.`
Thought: I need to find out what are the magic words in the sentence, then find the second one of these and finally find out how many vowels it has.
Action: Call get_magic_words with parameters "What is the number of vowels in the second magic word: I love wauwau, please."
Result: "wauwau", "please"
Observation: The sentence has the following magic words in order: "wauwau", "please".
Thought: There are 2 magic words in this sentence. So I need to find out how many vowels the second magic word "please" has.
Action: Call get_num_vowels with parameters "please"
Result: 3
Observation: The word "please" has 3 vowels.
Thought: The second magic word of the provided sentence is "please" and has 3 vowels, so the answer is 3.
Final Answer: True
The provided example is generic but you have to follow the steps as followed in the example.
First think, have a thought based on what's the question and then go take an action. Don't directly take any action without a thought in the history. Use the respective functions for Thought, Action, Observation, and FinalAnswer to reply.
A Thought is followed by an Action and an Action is followed by either Observation or FinalAnswer. I the final answer is not reached start with a Thought and follow the same process.
You have access to the history so don't repeat (call) the same Thoughts or Observations which are already available in the history. Also do not an exact action with same arguments again if its already available in the history.
If you don't get any answer from the Action change the arguments in the next iteration.
Please go step by step, don't directly try and reach the final answer. Don't assume things!
"""

ReAct_Answer_Prompt = """You will be provided with a question inside single backticks and history of action and reasoning inside triple backticks. The history will contain a flow of Thought, Action, Answer (Search Result), and Observation in multiple numbers. Using the history you need to answer the provided question. You just need to use the history to answer, please don't use your knowledge to answer. Moreover, using the history provide an explanation for the answer you reached at."""