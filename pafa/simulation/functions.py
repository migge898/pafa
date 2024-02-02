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
    def generate_level_message_pairs(pod_kind: str):
        result = []
        # 90% of the time, the number of tickets is between 10 and 30, otherwise it's between 31 and 100
        ticket_num = lambda: random.randint(10, 30) if random.random() < 0.9 else random.randint(31, 100)
        tag = lambda: random.choice("paymentservice", "client", "launcher", "misc")
        # cpu over 10, 20 or 30
        cpu_usage = lambda: random.choice([10, 20, 30])
        infos = lambda x: filter(lambda x: x[0] == "INFO", x)
        warns = lambda x: filter(lambda x: x[0] == "WARN", x)
        # returns a list of weights for the pairings like: 3 * [0.95] + 2 * [0.05] = [0.95, 0.95, 0.95, 0.05, 0.05]
        weights_gen = lambda pairings, warn_weight: len(list(infos(pairings))) * [(1 - warn_weight)] + len(list(warns(pairings))) * [warn_weight]
        match pod_kind:
            case "bugticketsvc":
                pairings = [
                    ("INFO", f"{ticket_num()} new open tickets for tag: {tag()}"),
                    ("INFO", f"{ticket_num()} tickets have been closed for tag: {tag()}"),
                    ("INFO", f"{ticket_num()// 3} tickets have been reopened for tag: {tag()}"),
                    ("INFO", f"{ticket_num()// 2} tickets have been assigned for tag: {tag()}"),
                    ("INFO", f"{ticket_num()} tickets have been unassigned for tag: {tag()}"),
                    ("INFO", f"{ticket_num()} tickets have been resolved for tag: {tag()}"),
                    ("WARN", f"{ticket_num()// 5} tickets have not been resolved for more than 3 days: {tag()}"),
                    ("WARN", f"CPU usage of this pod over {cpu_usage()}%."),
                ]
                result = random.choices(pairings, k=num_rows, weights=weights_gen(pairings, 0.05))
            case "paymentsvc":
                pass
            case "userauthsvc":
                pass
            case "messagersvc":
                pass
            case "playerstatssvc":
                pass

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
    ticket_num = lambda: random.randint(10, 30) if random.random() < 0.9 else random.randint(31, 100)
    tag = lambda: random.choice(["paymentservice", "client", "launcher", "misc"])
    cpu_usage = lambda: random.choice([10, 20, 30])
    infos = lambda x: filter(lambda x: x[0] == "INFO", x)
    warns = lambda x: filter(lambda x: x[0] == "WARN", x)
    # returns a list of weights for the pairings
    weights_gen = lambda pairings, warn_weight: len(list(infos(pairings))) * [(1 - warn_weight)] + len(list(warns(pairings))) * [warn_weight]
    pairings = [
        ("INFO", f"{ticket_num()} new open tickets for tag: {tag()}"),
        ("INFO", f"{ticket_num()} tickets have been closed for tag: {tag()}"),
        ("INFO", f"{ticket_num()// 3} tickets have been reopened for tag: {tag()}"),
        ("INFO", f"{ticket_num()// 2} tickets have been assigned for tag: {tag()}"),
        ("INFO", f"{ticket_num()} tickets have been unassigned for tag: {tag()}"),
        ("INFO", f"{ticket_num()} tickets have been resolved for tag: {tag()}"),
        ("WARN", f"{ticket_num()// 5} tickets have not been resolved for more than 3 days: {tag()}"),
        ("WARN", f"CPU usage of this pod over {cpu_usage()}%."),
    ]
    # result = random.choices(pairings, k=30, weights=[0.95, 0.05])
    # [print(element) for element in result]
    print(weights_gen(pairings, 0.05))
    # filter pairings for warn