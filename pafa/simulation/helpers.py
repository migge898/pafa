import datetime

import tabulate


def convert_date_millis_to_iso_z(date_millis: int) -> str:
    """Converts a date string to ISO format with Z at the end."""
    converted_date = str(datetime.datetime.utcfromtimestamp(date_millis / 1000).isoformat() + "Z")
    return converted_date


def convert_pod_list_to_text(pod_list: dict) -> str:
    """Converts a podlist JSON to a multi-line text like a table."""
    assert "services" in pod_list, "services key not found in pod_list"
    data = []
    for pod in pod_list["services"]:
        data.append(
            [
                pod["name"],
                pod["ready"],
                pod["status"],
                pod["restarts"],
                pod["age"],
            ]
        )
    headers = ["Name", "Ready", "Status", "Restarts", "Age"]
    table = tabulate.tabulate(data, headers, tablefmt="plain")
    return table


if __name__ == "__main__":
    assert "2024-02-02T17:21:15.204000Z" == convert_date_millis_to_iso_z(1706894475204)
    # print(datetime.datetime.utcnow().isoformat())
    print(convert_date_millis_to_iso_z(1706894475204))