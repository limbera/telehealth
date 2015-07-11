import os, sys
import json, httplib, urllib2

from twilio.rest import TwilioRestClient
from flask import Flask, request

class Logger(object):
    def __init__(self, filename="error.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

sys.stdout = Logger("error.log")


app = Flask(__name__)

# On Bluemix, get the port number from the environment variable VCAP_APP_PORT
# When running this app on the local machine, default the port to 8080
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
    #print call.sid
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


@app.route('/handleRecording', methods=['GET', 'POST'])
def handle_recording():
    return "yes"
    # recording_url = request.values.get('RecordingUrl', None)

    # #print request
    # #recording_url = "http://coffeenomad.com.au/down_to_cases.wav"

    # connection = httplib.HTTPSConnection('api.parse.com', 443)
    # connection.connect()

    # # upload the file to Parse.com /files/ dir 
    # data = urllib2.urlopen(recording_url).read();
    # connection.request('POST', '/1/files/audio.wav',  data, {
    #    "X-Parse-Application-Id": PARSE_APP_ID,
    #    "X-Parse-REST-API-Key": PARSE_REST_API_KEY,
    #    'Content-Type': "audio/x-wav"
    # })
    # result = json.loads(connection.getresponse().read())

    # connection = httplib.HTTPSConnection('api.parse.com', 443)
    # connection.connect()
    # connection.request('POST', '/1/classes/audio_recording', json.dumps({
    #        "transcription": "Testing",
    #        "audio_file": {
    #          "name": result['name'],
    #          "__type": "File"
    #        }
    #      }), {
    #        "X-Parse-Application-Id": PARSE_APP_ID,
    #        "X-Parse-REST-API-Key": PARSE_REST_API_KEY,
    #        "Content-Type": "application/json"
    #      })
    # result = json.loads(connection.getresponse().read())
    # print result
    # return 'File successfully uploaded' + str(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)

# if __name__ == '__main__':
#     app.debug = True
#     app.run()

