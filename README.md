# Prometheus Alert Fixer Agent (PAFA)

This Python application is designed to seamlessly integrate with a Kube-Prometheus cluster. Deployed within the cluster, the app actively listens for incoming alerts and employs advanced techniques, including Large Language Models (LLM) and prompt engineering, to swiftly analyze and formulate resolutions. The end user is then promptly notified via Microsoft Teams, ensuring a streamlined and efficient alert management process.

# Latest Version 0.1.0
First ReAct-agent in `pafa/openai_test`. With a dummy question it shall be demonstraded that the [ReAct](https://arxiv.org/abs/2210.03629) Framework can work.
Also [instructor](https://github.com/jxnl/instructor) is tested to make the coding process more easy and safer working with ChatGPT Responses.
Goal: Make it stable, that no errors occur.

# Future Version 1.0.0
The ReAct-Agent will be adjusted to work with Prometheus Alert Data and Logs.
Nice-To-Have: App gets containerized and tested with a cluster.

# Future Version 2.0.0
Depeding on complexity and time, some features of [RCAgent](https://arxiv.org/abs/2310.16340) are getting implemented.