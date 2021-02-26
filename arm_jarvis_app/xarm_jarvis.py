
import wave
import os
dirname = os.path.dirname(__file__)

import sys
sys.path.append(dirname)

from voice_recog_vosk.voice_recog import recog 

print(dirname)

from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
#cors = CORS(app)

socketio = SocketIO(app)

HTTP_SERVER_PORT = 8000
HTTP_SERVER_HOST = "localhost"

sampleRate = 44100
bitsPerSample = 16
channels = 1

numfile = 0

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

    # with open("test.wav", mode="wb") as f:
    #     f.write(genHeader() + data)
    global numfile
    global dirname
    # print(data)

    with wave.open(f"{dirname}/wavs/file_{numfile}.wav", "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(16 // 8)
        f.setframerate(44100)
        # f.setnframes(1)
        f.setcomptype("NONE", "not compressed")
        f.writeframes(genHeader() + data)
    
    print(f"file file_{numfile}.wav written")
    stt = recog(f"file_{numfile}.wav")
    print(f"reconnu: {stt}")

    # numfile += 1

    emit('audio_stream_response', stt)


@app.route('/')
def page():
    return render_template('index.html', )


if __name__ == '__main__':
    print('server launched.')
    socketio.run(app, host=HTTP_SERVER_HOST, port = HTTP_SERVER_PORT)