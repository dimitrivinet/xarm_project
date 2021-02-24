
from vosk import Model, KaldiRecognizer

import os
dirname = os.path.dirname(__file__)

if not os.path.exists(dirname + "/model"):
    print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
    print("(current best model from https://alphacephei.com/vosk/models/vosk-model-fr-0.6-linto-2.2.0.zip")
    exit (1)

model = Model(dirname + "/model")
rec = KaldiRecognizer(model, 44100)