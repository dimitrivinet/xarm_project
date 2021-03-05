
import os
import sys
import signal
import unicodedata

dirname = os.path.dirname(os.path.realpath(__file__))
# print(dirname)
sys.path.append(dirname)

import writing
from arm_init import robot_start

_arm = None

def sigint_handler(sig, frame):
        print("\nSIGINT Captured, terminating")        
        if _arm:
            _arm.arm.set_state(state=4)

            if _arm.current_mode == "writing":
                writing.write_exit(_arm.arm)

            _arm.arm.disconnect()
        sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

class Arm():
    def __init__(self):
        self.current_mode = "none"
        self.arm = robot_start()
        global _arm
        _arm = self

        print("\nxarm initialized.\n")

    def write(self, to_write: str) -> int:
        to_write = sentence_normalize(to_write)
        print(f"to write: {to_write}")
        if self.current_mode != "writing":
            writing.write_setup(self.arm)
        self.current_mode = "writing"
        writing.robot_write(self.arm, to_write)




def sentence_normalize(sentence: str) -> str:
    sentence = ''.join((c for c in unicodedata.normalize(
        'NFD', sentence) if unicodedata.category(c) != 'Mn'))

    sentence = sentence.lower()
    return sentence