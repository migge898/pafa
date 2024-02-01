import datetime
import json
import os
import random

DEFAULT_POD_LIST = {
    "services": [
        {
            "name": "bugticketsvc-main-0",
            "ready": "2/2",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "bugticketsvc-main-1",
            "ready": "2/2",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "bugticketsvc-main-2",
            "ready": "2/2",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "paymentsvc-main-0",
            "ready": "3/3",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "paymentsvc-main-1",
            "ready": "1/1",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "userauthsvc-main-0",
            "ready": "7/7",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "messagersvc-main-0",
            "ready": "2/2",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "messagersvc-main-1",
            "ready": "1/1",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "messagersvc-main-2",
            "ready": "1/1",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "playerstatssvc-main-0",
            "ready": "2/2",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "playerstatssvc-main-1",
            "ready": "2/2",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
        {
            "name": "playerstatssvc-main-2",
            "ready": "2/2",
            "status": "Running",
            "restarts": 0,
            "age": "9d",
        },
    ]
}


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

    a = generate_pod_log(
        namespace="test-000",
        pod="bugticketsvc-main-0",
        start_time_millis="1706828197476",
        num_rows=3,
    )
    print(a)
