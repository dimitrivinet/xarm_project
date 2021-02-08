#!/usr/bin/env python3

import pyaudio
import speech_recognition as sr
import sys
import time

from contextlib import contextmanager
from ctypes import CFUNCTYPE, c_char_p, c_int, cdll



ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)

def record_and_recognize():
    with noalsaerr():
        r = sr.Recognizer()
        mic = sr.Microphone()

        # print(mic)
        # print(sr.Microphone.list_microphone_names())

    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            print("\nsay something (im giving up on you)")
            audio = r.listen(source, timeout=10, phrase_time_limit=6)

        print("done recording. recognizing...\n")
        return(r.recognize_google(audio, language="fr-FR"))
    except:
        print("Message non reconnu")
        return "erreur"


def test():
    msg = ""
    while True:
        while msg != "a":
            msg = input(
                "Entrer a pour lancer une reconnaissance de voix, quit pour quitter\n")
            if msg == "quit":
                sys.exit(0)
        output = record_and_recognize()
        print("output: {}".format(output))
        msg = ""


def return_sentence():
    msg = ""
    output = ""
    while msg != "ok":
        print("Initialisation...")
        output = record_and_recognize()
        print("output: {}\n".format(output))
        # msg = input(
        #     "Entrer ok pour retourner ce message, ou autre chose pour réessayer\n")
        msg = "ok"
    print("message enregistré\n")
    return output.lower()


# test()
