# Prometheus Alert Fixer Agent (PAFA)
This Python application is designed to seamlessly integrate with a Kube-Prometheus cluster at the end. Deployed within the cluster, the app actively listens for incoming alerts and employs advanced techniques, including Large Language Models (LLM) and prompt engineering, to swiftly analyze and formulate resolutions. The end user is then promptly notified via Microsoft Teams, ensuring a streamlined and efficient alert management process.
The current development focuses on the agent implementation and will therefore run only locally.

# Config
To get the agent running rename the file `.env-template` to `.env` and insert your OpenAI key.
