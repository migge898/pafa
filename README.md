# Prometheus Alert Fixer Agent (PAFA)
This Python application is designed to seamlessly integrate with a Kube-Prometheus cluster at the end. Deployed within the cluster, the app actively listens for incoming alerts and employs advanced techniques, including Large Language Models (LLM) and prompt engineering, to swiftly analyze and formulate resolutions. The end user is then promptly notified via Microsoft Teams, ensuring a streamlined and efficient alert management process.
The current development focuses on the agent implementation and will therefore run only locally.

# Config
To get the agent running rename the file `.env-template` to `.env` and insert your OpenAI key and the webhook-url of your Microsoft Teams channel, where you want to receive the output of the agent (the latter disabled at version 0.1.0).

# Latest Version 1.0.0
The ReAct-Agent will be adjusted to work with Prometheus Alert Data and Logs.
Nice-To-Have: App gets containerized and tested with a cluster.

# Future Version 2.0.0
Depending on complexity and time, some features of [RCAgent](https://arxiv.org/abs/2310.16340) are getting implemented.