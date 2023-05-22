from flask import Flask, request
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

app = Flask(__name__)


@app.route('/', methods=['POST'])
def send_message():
    input_json = request.get_json(force=True)
    try:
        client = WebClient(token="xoxb-5243253973760-5219207849717-ep0Rj29spjpy9AEtZOO0fhec")
        result = client.chat_postMessage(
            channel='#log-analysis',
            text=input_json["summary"] + "  -->  " + input_json['text']
        )
        return result
    except SlackApiError as e:
        return "Error sending message: {}".format(e)
