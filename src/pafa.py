import json
import sys
import pymsteams
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def respond():
    # first print the json, then store it in file "message.json" and send a webhook to microsoft teams with the json
    print(request.json)
    # with open('message.json', 'w') as outfile:
    #     json.dump(request.json, outfile)

    # message = pymsteams.connectorcard(ms_teams_webhook_url)
    # # make json to string
    # message.text(json.dumps(request.json))
    # # convert to team readable
    
    # # send webhook
    # message.send()
    return Response(status=200)

if __name__ == '__main__':

    # message = pymsteams.connectorcard("https://evoilade.webhook.office.com/webhookb2/03f3c5a1-ce75-4979-b78a-6ab9c7555521@a65e9058-ba4d-481d-b114-5eba2e0684e2/IncomingWebhook/64e1276c26bc4a3d9b83f1d5dfca7afa/bc610f64-2f72-48a6-ab4a-44c8053fa395")
    # message.text("Hello reality!")

    # # send webhook
    # message.send()

    print(sys.executable)