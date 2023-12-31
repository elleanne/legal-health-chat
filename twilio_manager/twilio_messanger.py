import os
from twilio.rest import Client
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from preprocess.query import preprocess_query
from model import get_response

app = Flask(__name__)

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
server_number = os.environ['SERVER_PHONE_NUMBER']
client = Client(account_sid, auth_token)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    req_values = request.values

    ## send to preprocessing
    user_data = preprocess_query(req_values)

    ## send preprocessed data to api -> gpt
    response_text = get_response(user_data, 15)
    response_text += ' \nThis is not legal advice, consult a lawyer for your question.'

    # Start our TwiML response
    resp = MessagingResponse()
    resp.message(response_text)

    return str(resp)

def run_server():
    app.run()