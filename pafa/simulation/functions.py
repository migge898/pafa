import datetime
import json
import os
import random

from pafa.simulation.constants import Pairings, DEFAULT_POD_LIST

def get_pods(namespace: str):
    pass


def get_logs(pod: str):
    pass


# TODO: Change timestamp to be non millis
def generate_pod_log(
    namespace: str, pod: str, start_time_millis: str, num_rows: int, **kwargs
):
    def generate_timestamps():
        timestamps = []
        current_time = int(start_time_millis)
        for _ in range(num_rows):
            # Every log entry differs between 1 and 10 seconds
            delta = random.randint(1, 10) * 1000
            current_time += delta
            timestamps.append(current_time)
        timestamps = map(
            lambda x: str(datetime.datetime.utcfromtimestamp(x / 1000)) + "Z",
            timestamps,
        )
        return list(timestamps)
    def generate_level_message_pairs(pod_kind: str):
        result = []
        match pod_kind:
            case "bugticketsvc":
                result = Pairings.generate_bug_ticket_svc(num_rows, 0.05)
            case "paymentsvc":
                result = Pairings.generate_payment_svc(num_rows, 0.05)
            case "userauthsvc":
                result = Pairings.generate_user_auth_svc(num_rows, 0.05)
            case "messagersvc":
                result = Pairings.generate_message_svc(num_rows, 0.05)
            case "playerstatssvc":
                result = Pairings.generate_player_stats_svc(num_rows, 0.05)
        return result

    # bugticketsvc-main-0  ->  bugticketsvc
    pod_kind = pod.split("-")[0]
    assert pod_kind in [
        "bugticketsvc",
        "paymentsvc",
        "userauthsvc",
        "messagersvc",
        "playerstatssvc",
    ]
    log_entries = []
    times = generate_timestamps()

    # Log should look like this, but in JSON: t=2024-01-22T18:44:03.692166958Z level=info msg="State cache has been initialized"
    for i in range(num_rows):
        log_entries.append({"timestamp": times[i], "level": None, "msg": None})

    return generate_timestamps()


def generate_namespace(namespace: str):
    def init_namespace():
        pod_list = DEFAULT_POD_LIST

        # generate dir
        os.makedirs(f"simulated/namespaces/{namespace}", exist_ok=False)
        with open(
            f"simulated/namespaces/{namespace}/pod-list.json", "w"
        ) as namespace_file:
            json.dump(pod_list, namespace_file, indent=4)

    init_namespace()
    # TODO: generate pods with DEFAULT_POD_LIST["services"][i]["name"]
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

    with open(f"simulated/alerts/{alertname}.json", "w") as alert_file:
        json.dump(alert_json, alert_file, indent=4)


if __name__ == "__main__":
    # generate_alert(
    #     description="BugTicketservice in namespace test-000 is using 65% of CPU.",
    #     alertname="BugTicketServiceOverloaded",
    #     namespace="test-000",
    #     pod="bugticketsvc-main-0",
    #     active_at_time="2023-12-21T09:33:16.095364684Z",
    # )
    # generate_namespace("test-000")

    # a = generate_pod_log(
    #     namespace="test-000",
    #     pod="bugticketsvc-main-0",
    #     start_time_millis="1706828197476",
    #     num_rows=3,
    # )
    res = Pairings.generate_bug_ticket_svc(5, 0.05)
    [print(x) for x in res]