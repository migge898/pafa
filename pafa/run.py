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

    # message = ""
    # message.text("Hello reality!")

    # # send webhook
    # message.send()

    print(sys.executable)
