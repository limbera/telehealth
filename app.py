import os, sys
import json, httplib, urllib2
from twilio.rest import TwilioRestClient
from flask import Flask, request

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


@app.route('/makeCall')
def make_call():
    print 'Making a phone call to +61419190104'
    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    call = client.calls.create(
        url="http://coffeenomad.com.au/conversation.xml",
        to="+61419190104",
        from_="+61281884735"
    )
    return 'Making a phone call to +61419190104'


@app.route('/handleTranscription', methods=['GET', 'POST'])
def transcribe_audio():
    transcription_text = request.values.get('TranscriptionText')
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/classes/metrics', json.dumps({
           "weight": transcription_text,
           "phone": To,
         }), {
           "X-Parse-Application-Id": PARSE_APP_ID,
           "X-Parse-REST-API-Key": PARSE_REST_API_KEY,
           "Content-Type": "application/json"
         })
    return "Sucessfully added patiend data"

