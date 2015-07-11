import os, sys
import json, httplib, urllib2
import requests
import re

from urlparse import urlparse
from flask import Flask, request
from twilio.rest import TwilioRestClient
from twilio.rest.resources import Connection
from twilio.rest.resources.connection import PROXY_TYPE_HTTP

# proxy_url = os.environ.get("http_proxy")
# host, port = urlparse(proxy_url).netloc.split(":")
# Connection.set_proxy_info(host, int(port), proxy_type=PROXY_TYPE_HTTP)

app = Flask(__name__)
port = int(os.getenv('VCAP_APP_PORT', 8080))

# connect to Twilio and start a call
TWILIO_ACCOUNT_SID = "ACd99405ba17278687dc0166b0f17d8f88" 
TWILIO_AUTH_TOKEN = "b87ffa0dcf11287fb04d1d854012f95a" 

# set up parse to receive the call 
PARSE_APP_ID = "HkyPWNWp8ifnCeQIkSgNIAfqWgeOtq3fsDcgAiOs"
PARSE_REST_API_KEY = "aoLJq2DPuz0rF0Kmxz520zPq4tpKkk6U1wW28Nvj"

@app.route('/')
def hello_world():
    print "this should be in the log"
    return 'Hello World! I am running on port ' + str(port)


@app.route('/makeCall', methods=['GET', 'POST'])
def make_call():
    print 'Making a phone call to +61419190104'
    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    call = client.calls.create(
        to="+61419190104",
        from_="+61281884735",
        url="http://coffeenomad.com.au/conversation.xml"
    )
    return 'Making a phone call to +61419190104'


@app.route('/handleRecording', methods=['GET', 'POST'])
def handle_recording():
    return "Handling recording"


@app.route('/handleTranscription', methods=['GET', 'POST'])
def transcribe_audio():
    transcription = request.values.get('TranscriptionText')
    weight = re.findall('\d+', transcription)[0] # just take the first array if multiple numbers
    url = "https://api.parse.com/1/classes/metrics"
    data = {'weight': weight}

    headers = {
       'X-Parse-Application-Id': PARSE_APP_ID,
       'X-Parse-REST-API-Key': PARSE_REST_API_KEY,
       'Content-Type': 'application/json'
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print "post was: %s" % r.content
    return "Sucessfully added patient data"

if __name__ == '__main__':
    app.run(debug=True)

