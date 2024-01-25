# get alerts from http://localhost:9090/api/v1/alerts and save each in ../alertdata/<alertname>.json

import json
import sys
import requests

def main():
    # get reqest  http://localhost:9090/api/v1/alerts

    x = requests.get('http://localhost:9090/api/v1/alerts')

    json_data = json.loads(x.text)

    if x.status_code == 200 and 'data' in json_data and 'alerts' in json_data['data']:
        alerts = json_data['data']['alerts']

        # Loop through each alert and save it to a file
        for alert in alerts:
            alertname = alert['labels']['alertname']
            filename = f"alertdata/{alertname}.json"

            with open(filename, 'w') as file:
                json.dump(alert, file, indent=4)

            print(f"Alert '{alertname}' saved to {filename}")
    else:
        print("Failed to fetch alerts from Prometheus API.")


if __name__ == '__main__':
    main()
