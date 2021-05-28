import os
import sys

dirname = os.path.dirname(os.path.realpath(__file__))

if dirname == "":
    print("error: dirname empty")
    sys.exit(0)

print(dirname)
sys.path.append(dirname)


import wave
import requests
import argparse
import threading

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# from voice_recog_vosk.voice_recog import recog 
import azure.cognitiveservices.speech as speechsdk
speech_config = speechsdk.SpeechConfig(subscription="b6aeeece6e0c404d8390528985e1a213", region="francecentral")
speech_config.speech_recognition_language="fr-FR"

parser = argparse.ArgumentParser(description='A.L.F.R.E.D., robotic assistant.')
parser.add_argument('-n', '--no-robot', action='store_true', help="don't connect to the xArm")
parser.add_argument('-r', '--reset-pos', action='store_true', help="reset the current position to default for writing mode")
#TODO: this ^
args = parser.parse_args()
# print(args.no_robot)

NO_ROBOT = args.no_robot
RESET_POS = args.reset_pos

if not NO_ROBOT:
    import robot_control


arm = "dummy"


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
#cors = CORS(app)

socketio = SocketIO(app, logger=False, engineio_logger=False, allow_upgrades=False)

socketio.init_app(app, cors_allowed_origins="*")

HTTP_SERVER_PORT = 8080
HTTP_SERVER_HOST = "0.0.0.0"

sampleRate = 44100
bitsPerSample = 16
channels = 1
        

def send_rasa(message: str) -> str:
    r = requests.post("http://rasa:5005/webhooks/rest/webhook", json={"sender": "alfred_user", "message": message})
    return r.json()[0]["text"]

def genHeader():
    global sampleRate
    global bitsPerSample
    global channels

    datasize = 2000*10**6
    o = bytes("RIFF",'ascii')                                               # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(4,'little')                               # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE",'ascii')                                              # (4byte) File type
    o += bytes("fmt ",'ascii')                                              # (4byte) Format Chunk Marker
    o += (16).to_bytes(4,'little')                                          # (4byte) Length of above format data
    o += (1).to_bytes(2,'little')                                           # (2byte) Format type (1 - PCM)
    o += (channels).to_bytes(2,'little')                                    # (2byte)
    o += (sampleRate).to_bytes(4,'little')                                  # (4byte)
    o += (sampleRate * channels * bitsPerSample // 8).to_bytes(4,'little')  # (4byte)
    o += (channels * bitsPerSample // 8).to_bytes(2,'little')               # (2byte)
    o += (bitsPerSample).to_bytes(2,'little')                               # (2byte)
    o += bytes("data",'ascii')                                              # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4,'little')                                    # (4byte) Data size in bytes
    return o

@socketio.on('message')
def handle_message(data):
    if type(data) == str:
        print('from client: ' + data)
    else:
        print(data)

@socketio.on('connect')
def connect():
    print("client connected")

@socketio.on('audio_stream')
def handle_stream(data):
    # print(data)
    # print("end of byte stream")

    global numfile
    global dirname

    with wave.open(f"{dirname}/wavs/file_0.wav", "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(16 // 8)
        f.setframerate(44100)
        # f.setnframes(1)
        f.setcomptype("NONE", "not compressed")
        f.writeframes(genHeader() + data)
    
    print(f"file written")
    print(f"recognizing...")

    audio_input = speechsdk.AudioConfig(filename=f"{dirname}/wavs/file_0.wav")
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    
    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
        emit('audio_stream_response', result.text)
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

    print("_" * 16)
    print("")

    rasa_response = send_rasa(stt)
    # print(rasa_response)
    emit('rasa_response', rasa_response[5:])

    if not NO_ROBOT:
        robot_control.rasa_command_queue.put(rasa_response)

    # to_write = extract_to_write(rasa_response)
    # if arm != "dummy" and to_write != -1:
    #     arm.write(to_write)

@socketio.on('manual_stream')
def handle_manual_stream(data):
    print(f"user: {data}")

    rasa_response = send_rasa(data)
    print(f"rasa: {rasa_response}")

    emit('rasa_response', rasa_response[5:])

    if not NO_ROBOT:
        robot_control.rasa_command_queue.put(rasa_response)

    # to_write = extract_to_write(rasa_response)
    # if arm != "dummy" and to_write != -1:
    #     arm.write(to_write)

@app.route('/')
def page():
    return render_template('index.html', )


if __name__ == '__main__':

    print('server launched.\n')

    if not NO_ROBOT:
        arm = robot_control.Arm(reset_pos=RESET_POS, daemon=True, )
        arm.start()

    socketio.run(app, host=HTTP_SERVER_HOST, port = HTTP_SERVER_PORT,)