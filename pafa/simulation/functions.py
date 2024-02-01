import json


def get_pods(namespace: str):
    pass


def get_logs(pod: str):
    pass


def generate_pod_logs(namespace: str, pod: str, start_time: str, end_time: str):
    pass


def generate_alert(
    description: str, alertname: str, namespace: str, pod: str, active_at_time: str
):
    alert_json = {
        "labels": {
            "alertname": alertname,
            "severity": "critical",
            "pod": pod,
            "namespace": namespace,
        },
        "annotations": {
            "description": description,
        },
        "activeAt": active_at_time,
    }

    # write json to path simulated/alerts/

    with open(f"simulated/alerts/{alertname}.json", "w") as alert_file:
        json.dump(alert_json, alert_file)


if __name__ == "__main__":
    assert get_pods("error") == "The namespace error does not exist."
