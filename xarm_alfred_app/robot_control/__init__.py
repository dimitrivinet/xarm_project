
import os
import sys
import signal
import unicodedata
import threading
import queue

dirname = os.path.dirname(os.path.realpath(__file__))
# print(dirname)
sys.path.append(dirname)

import writing
from arm_init import robot_start


rasa_command_queue = queue.Queue()


""" 
    RASA message codes: 

    #1xx informational response – the request was received, print response
    #2xx successful – the request was successfully received, understood, and accepted; action necessary
    #3xx api error – intent recognition or entity extraction unsuccessful
"""

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

class Arm(threading.Thread):
    def __init__(self):
        super().__init__(self)
        self.current_mode = "none"
        self.arm = robot_start()
        global _arm
        _arm = self

        print("\nxarm initialized.\n")

    def run(self):
        command = ""
        code= ""
        while True:
            command = rasa_command_queue.get(block=True, timeout=None)
            code = command[0:4]

            if code == "#101":
                continue
            elif code == "#201":
                self.write(command[25:-1])
            elif code == "#202":
                self.grab(command[37:])

            rasa_command_queue.task_done()            


    def write(self, to_write: str) -> int:
        to_write = sentence_normalize(to_write)
        print(f"to write: {to_write}")
        if self.current_mode != "writing":
            writing.write_setup(self.arm)
        self.current_mode = "writing"
        writing.robot_write(self.arm, to_write)
    
    def grab(self, to_grab: str) -> int:
        pass



def sentence_normalize(sentence: str) -> str:
    sentence = ''.join((c for c in unicodedata.normalize(
        'NFD', sentence) if unicodedata.category(c) != 'Mn'))

    sentence = sentence.lower()
    return sentence