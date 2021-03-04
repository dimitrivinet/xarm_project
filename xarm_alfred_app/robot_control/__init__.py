
import os
import sys
import signal

dirname = os.path.dirname(__file__)
# print(dirname)
sys.path.append(dirname)

from arm_init import robot_start

_arm = "dummy"

def sigint_handler(sig, frame):
        print("\nSIGINT Captured, terminating")
        try:
            if _arm:
                _arm.set_state(state=4)
                _arm.disconnect()
            sys.exit(0)
        except AttributeError as e:
            sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

class Arm():
    def __init__(self):
        self.arm = robot_start()
        global _arm
        _arm = robot_start

        print("\nxarm initialized.\n")