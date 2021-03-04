#!/usr/bin/env python3

from robot_control.alphabet import letters_v3
from copy import deepcopy
from xarm.wrapper import XArmAPI

import robot_control.writing as writing

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
        sentence = sentence.split("ecri")
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
    return sentence
                

if __name__ == "__main__":
    writing.write("dummy", "a")


