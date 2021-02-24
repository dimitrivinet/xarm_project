
import sys
import os
import wave
import json

dirname = os.path.dirname(__file__)

from vosk import SetLogLevel
from voice_recog_vosk import rec


def recog(filename):
    SetLogLevel(0)

    wf = wave.open(f"{dirname}/../wavs/{filename}", "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)

    # model = Model("model")
    # rec = KaldiRecognizer(model, wf.getframerate())

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            dicti = json.loads(rec.Result())
            # print(dicti["text"])

    final_result = json.loads(rec.Result())["text"]

    print(f"reconnu: {final_result}")
