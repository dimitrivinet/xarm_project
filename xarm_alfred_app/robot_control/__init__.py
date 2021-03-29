
import os
import sys
import signal
import unicodedata
import threading
import queue
import time
import numpy as np

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
    def __init__(self, reset_pos=False, daemon=True):
        threading.Thread.__init__(self, daemon=daemon)
        self.current_mode = "none"
        self.arm = robot_start()
        self.reset_pos=reset_pos
        self.speed = 50
        self.isGrabbing = False

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
                self.write(command[30:-1])
            elif code == "#202":
                self.grab(command[37:])
            elif code == "#401":
                self.eeg_control(command[5:])
            elif code == "#402":
                self.hand_control(command[5:])

            rasa_command_queue.task_done()            


    def write(self, to_write: str) -> int:
        to_write = sentence_normalize(to_write)
        print(f"to write: {to_write}")
        if self.current_mode != "writing":
            writing.write_setup(self.arm, self.reset_pos)
        self.current_mode = "writing"
        writing.robot_write(self.arm, to_write)
    
    def grab(self, to_grab: str) -> int:
        pass

    def eeg_control(self, direction: str) -> int:
        if self.current_mode != "eeg":
            eeg_setup(self.arm,self.speed)
            self.current_mode = "eeg"


        if direction == "LEFT":
            ret = self.arm.set_position(60, 0, 0, 0, 0, 0, 
            radius=-1, is_radian=False, wait=False, speed=self.speed, mvacc=10*self.speed, relative=True)
            if ret < 0:
                print('set_position, ret={}'.format(ret))
                return -1

        elif direction == "RIGHT":
            ret = self.arm.set_position(-60, 0, 0, 0, 0, 0,  
            radius=-1, is_radian=False, wait=False, speed=self.speed, mvacc=10*self.speed, relative=True)
            if ret < 0:
                print('set_position, ret={}'.format(ret))
                return -1
        else:
            pass

    def hand_control(self, command: str,) -> int:
        print(f" COMMAND : {command}")
        if self.current_mode != "eeg":
            eeg_setup(self.arm, self.speed)
            self.current_mode = "eeg"
            # self.arm.set_pause_time(0.5, False)

        try:
            
            parameters = command.split(" ")
            hand_speed = float(parameters[0])
            hand_angle = float(parameters[1])
            hand_gesture = parameters[2]
        except Exception as e:
            print(e)
            return        

        print(f"PARAMETERS : {hand_speed}, {hand_angle}, {hand_gesture}")
        if hand_gesture == "GRAB" and not self.isGrabbing:
            print("IS GRABBING")
            self.arm.set_gripper_position(380, speed = 2500, auto_enable=True)
            self.isGrabbing = True
        elif hand_gesture != "GRAB" and self.isGrabbing:
            self.arm.set_gripper_position(600, speed = 2500, auto_enable=True)
            self.isGrabbing = False

        dist_mul = 14
        x = np.cos(hand_angle)*dist_mul
        y = np.sin(hand_angle)*dist_mul
        new_speed = min(750, hand_speed * 5000)
        new_acc = 5000

        if hand_speed > 0.01:
            ret = self.arm.set_position(x, 0, y, 0, 0, 0, 
            radius=3, is_radian=False, wait=False, speed=new_speed, mvacc=new_acc, relative=True)
            if ret < 0:
                print('set_position, ret={}'.format(ret))
                return -1



def sentence_normalize(sentence: str) -> str:
    sentence = ''.join((c for c in unicodedata.normalize(
        'NFD', sentence) if unicodedata.category(c) != 'Mn'))

    sentence = sentence.lower()
    return sentence

def eeg_setup(arm, speed):
    arm.set_world_offset([0, 0, 0, 0, 0, 0])
    time.sleep(1)

    arm.motion_enable(enable=True)
    arm.set_mode(0)
    arm.set_state(state=0)

    ret = arm.set_position(0, -227.8, 643.9, 0, -90, 90, 
        radius=-1, is_radian=False, wait=True, speed=speed, mvacc=10*speed, relative=False)
    if ret < 0:
        print('set_position, ret={}'.format(ret))
        return -1