
import sys
import os
import wave
import json

dirname = os.path.dirname(__file__)
if __name__ == "__main__":
    sys.exit("This is useless on its own :D")

from vosk import SetLogLevel
from voice_recog_vosk import rec


def recog(filename):
    SetLogLevel(0)
    filepath = f"{dirname}/../wavs/{filename}"

    wf = wave.open(filepath, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)

    # model = Model("model")
    # rec = KaldiRecognizer(model, wf.getframerate())

    temp_result = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            temp_result += json.loads(rec.Result())["text"]
            # print(temp_result)

    final_result = json.loads(rec.Result())["text"]

    if os.path.exists(filepath):
        os.remove(filepath)

    # print(f"reconnu: {final_result}")
    return final_result if final_result != "" else temp_result
