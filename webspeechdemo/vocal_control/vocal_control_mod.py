#!/usr/bin/env python3

from vocal_control.alphabet import letters_v3
from copy import deepcopy
from xarm.wrapper import XArmAPI
from icecream import ic
# ic.enable()
ic.disable()

import vocal_control.writing as writing

import threading
import time
import os
import signal
import sys
import unicodedata
# import arm_init

current_mode = "none"

def execute(arm: XArmAPI, command: str) -> int:
    global current_mode
    try:
        sentence = sentence_normalize(command)
        # ic(sentence)
        sentence = sentence.split("ecri")
        # ic(sentence)
        sentence = sentence[1][2:] + " "
        print(f"to write: {sentence}")
        if current_mode != "writing":
            writing.write_setup(arm)
        current_mode = "writing"
        writing.write(arm, sentence)
    except IndexError:
        print("mot clé non trouvé")
    except Exception as e:
        print(e)


def sentence_normalize(sentence: str) -> str:
    sentence = ''.join((c for c in unicodedata.normalize(
        'NFD', sentence) if unicodedata.category(c) != 'Mn'))

    sentence = sentence.lower()
    ic(sentence)
    return sentence
                

if __name__ == "__main__":
    writing.write("dummy", "a")


