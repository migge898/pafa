import json
import os
import random
import time

from pafa.simulation.constants import Pairings, DEFAULT_POD_LIST
from pafa.simulation.helpers import (
    convert_date_millis_to_iso_z,
    convert_pod_list_to_text,
)


def get_pods(namespace: str):
    try:
        with open(
            f"simulated/namespaces/{namespace}/pod-list.json", "r"
        ) as namespace_file:
            pod_list = json.load(namespace_file)
            return convert_pod_list_to_text(pod_list)
    except FileNotFoundError:
        return f"Namespace {namespace} not found."


def get_logs(pod: str, namespace: str):
    try:
        with open(f"simulated/namespaces/{namespace}/{pod}.txt", "r") as log_file:
            return log_file.read()
    except FileNotFoundError:
        return f"Pod {pod} not found in namespace {namespace}."


def generate_pod_log(pod: str, start_time_millis: int, num_rows: int):
    def generate_timestamps():
        timestamps = []
        current_time = start_time_millis
        for _ in range(num_rows):
            # Every log entry differs between 1 and 10 minutes
            delta = random.randint(1, 10) * 1000 * 60
            current_time += delta
            timestamps.append(current_time)
        # Converting timestamps to format like: "2024-01-22T18:44:03.692166958Z"
        timestamps = map(
            lambda x: convert_date_millis_to_iso_z(x),
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
            case "messengersvc":
                result = Pairings.generate_messenger_svc(num_rows, 0.05)
            case "playerstatssvc":
                result = Pairings.generate_player_stats_svc(num_rows, 0.05)
        return result

    # bugticketsvc-main-0  ->  bugticketsvc
    pod_kind = pod.split("-")[0]
    assert pod_kind in [
        "bugticketsvc",
        "paymentsvc",
        "userauthsvc",
        "messengersvc",
        "playerstatssvc",
    ]
    log_entries = []
    # Pairings structure like [("INFO", 3 new open tickets for tag: client"),...]
    pairings = generate_level_message_pairs(pod_kind)
    times = generate_timestamps()

    # Log should look like this, but in JSON: t=2024-01-22T18:44:03.692166958Z level=info msg="State cache has been initialized"
    for i in range(num_rows):
        level, msg = pairings[i][0], pairings[i][1]
        log_entries.append({"time": times[i], "lvl": level, "msg": msg})

    # lambda func that converts log element to single line text
    convert_to_text = lambda x: f't={x["time"]} level={x["lvl"]} msg="{x["msg"]}"'
    log_entries = list(map(convert_to_text, log_entries))
    return log_entries


def generate_namespace(namespace: str, pod_list: dict = DEFAULT_POD_LIST):
    def init_namespace():

        # generate dir
        try:
            os.makedirs(f"simulated/namespaces/{namespace}", exist_ok=False)
            with open(
                f"simulated/namespaces/{namespace}/pod-list.json", "w"
            ) as namespace_file:
                json.dump(pod_list, namespace_file, indent=4)
        except FileExistsError:
            print(f"Namespace {namespace} already exists.")

    def save_pod_log(pod: str, log: list[str]):
        with open(f"simulated/namespaces/{namespace}/{pod}.txt", "w") as log_file:
            log_file.write("\n".join(log))

    assert namespace not in os.listdir(
        "simulated/namespaces"
    ), "Namespace already exists"
    assert "services" in pod_list, "services key not found in pod_list"

    init_namespace()
    for pod in pod_list["services"]:
        # Calculate a random start time for the logs
        start_time = (time.time() + random.randint(1, 60000)) * 1000
        num_rows = 10
        pod_log = generate_pod_log(pod["name"], start_time, num_rows)
        save_pod_log(pod["name"], pod_log)


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
    print(get_logs("messengersvc-main-0", "test-000"))