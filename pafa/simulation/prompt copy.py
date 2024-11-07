ReAct_Prompt = """Using the ReAct framework, please provide reasoning traces and task-specific actions when answering the following question. Your only actions are get_pods[namespace] and get_logs[pod_name]. Given this constraint, try to find the root cause and a possible solution of the given alert.
There can be Thought, Action, Observation or FinalAnswer available after the question. So please do not repeat a same Thought or Observation. Do not repeat the same parameter for the action. If the latest action didn't extract any answer, try to change the parameter.
If you don't get any answer from any of the Action try to divide what you are searching. Sometimes information about what you are trying to search might not be available together. You might need to go more granular.
If you don't know how ReAct framework works, refer the following example.
Question: What is the root cause and a possible solution for this alert:
`{
    "labels": {
        "alertname": "BugTicketServiceOverloaded",
        "severity": "critical",
        "pod": "bugticketsvc-main-1",
        "namespace": "prod-123"
    },
    "annotations": {
        "description": "BugTicketservice in namespace test-000 is using 90% of CPU."
    },
    "activeAt": "t=2024-02-04T19:22:47.862156Z"
}`
Thought: To find the root cause and a possible solution, I need to find the logs of the pod "bugticketsvc-main-1" in the namespace "prod-123".
Action: get_logs[pod="prod-123",namespace="bugticketsvc-main-1"]
Observation:
(...)
t=2024-02-04T19:13:47.862156Z level=WARN msg="100000 new open tickets for tag: messengersvc"
t=2024-02-04T19:14:47.862156Z level=WARN msg="CPU usage of this pod over 40%."
t=2024-02-04T19:15:47.862156Z level=WARN msg="100000 new open tickets for tag: messengersvc"
t=2024-02-04T19:18:47.862156Z level=WARN msg="4 tickets with tag launcher have not been resolved for more than 3 days:"
Thought: Looking at the logs, I can see that many new tickets are open for tag "messengerscv" and the CPU goes higher shortly after. So there might be a problem with a messengersvc pod. I will look at the pods to see abnormal behavior.
Action: get_logs["messengersvc-main-1"]Action: get_logs["prod-123","bugticketsvc-main-1"]
Observation:
(...)
t=2024-02-04T19:13:47.862156Z level=INFO msg="100000 new open tickets for tag: messengersvc"
t=2024-02-04T19:14:47.862156Z level=WARN msg="CPU usage of this pod over 40%."
t=2024-02-04T19:15:47.862156Z level=INFO msg="100000 new open tickets for tag: messengersvc"
t=2024-02-04T19:18:47.862156Z level=WARN msg="4 tickets with tag launcher have not been resolved for more than 3 days:"
t=2024-02-04T19:22:47.862156Z level=WARN msg="CPU usage of this pod over 90%."
Thought: Looking at the logs, I can see that many new tickets are open for tag "messengerscv". The next log entry shows that the CPU usage has increased to 40%. And it continues until 90% CPU usage is reached. So there might be a problem with the messengersvc pod that results in high CPU usage here. Also looking at the pods from before I can see that the pod "messengersvc-main-1" is in a failed state. So the root cause might be to find in its logs.
Action: get_pods["prod-123"]
Observation: 
Name                   Ready    Status      Restarts  Age
bugticketsvc-main-0    2/2      Running            0  9d
bugticketsvc-main-1    1/2      Running            0  9d
bugticketsvc-main-2    2/2      Running            0  9d
paymentsvc-main-0      3/3      Running            0  9d
paymentsvc-main-1      1/1      Running            0  9d
userauthsvc-main-0     7/7      Running            0  9d
messengersvc-main-0    2/2      Running            0  9d
messengersvc-main-1    0/1      Failed             2  9d
messengersvc-main-2    1/1      Running            0  9d
playerstatssvc-main-0  2/2      Running            0  9d
playerstatssvc-main-1  2/2      Running            0  9d
playerstatssvc-main-2  2/2      Running            0  9d
Thought: The pod "messengersvc-main-1" has failed and was restarted 2 times. This might be the problematic messenger pod. I will examine its logs.
Action: get_logs[namespace="prod-123", pod="messengersvc-main-1"]
Observation:
(...)
t=2024-02-04T06:59:21.862932Z level=INFO msg="New thread in forum created."
t=2024-02-04T07:05:21.862932Z level=INFO msg="Broadcasted message: Christmas Event coming soon!"
t=2024-02-04T07:06:21.862932Z level=INFO msg="config: changed ip address of the server"
t=2024-02-04T07:09:21.862932Z level=WARN msg="pod needs to be restarted manually"
Thought: It can be seen that there was a change in the configuration at t=2024-02-04T07:06:21.862932Z and after that the pod needs to be restarted manually. This might be the root cause of the high CPU usage. The solution might be to restart the pod manually.
Final Answer: True if the root cause and solution are found with evidence in the history.
The provided example is generic but you have to follow the steps as followed in the example.
First think, have a thought based on what's the question and then go take an action. Don't directly take any action without a thought in the history. Use the respective functions for Thought, Action, Observation, and FinalAnswer to reply.
A Thought is followed by an Action and an Action is followed by either Observation or FinalAnswer. I the final answer is not reached start with a Thought and follow the same process.
You have access to the history so don't repeat (call) the same Thoughts or Observations which are already available in the history. Also do not an exact action with same arguments again if its already available in the history.
If you don't get any answer from the Action change the arguments in the next iteration.
Please go step by step, don't directly try and reach the final answer. Don't assume things!
"""

ReAct_Answer_Prompt = """You will be provided with an alert inside single backticks and history of action and reasoning inside triple backticks. The history will contain a flow of Thought, Action and Observation in multiple numbers. Using the history you need to find the root cause, a solution and evidence for all of that. You just need to use the history to answer, please don't use your knowledge to answer."""