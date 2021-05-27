#!/usr/bin/env python3

import os
import sys
import time
import threading

from copy import deepcopy
from xarm.wrapper import XArmAPI

from robot_control.alphabet import letters_v3


dirname = os.path.dirname(os.path.realpath(__file__))
# print(dirname)


letter_functions = {"a": letters_v3.A, "b": letters_v3.B, "c": letters_v3.C, "d": letters_v3.D, "e": letters_v3.E,
                    "f": letters_v3.F, "g": letters_v3.G, "h": letters_v3.H, "i": letters_v3.I, "j": letters_v3.J,
                    "k": letters_v3.K, "l": letters_v3.L, "m": letters_v3.M, "n": letters_v3.N, "o": letters_v3.O,
                    "p": letters_v3.P, "q": letters_v3.Q, "r": letters_v3.R, "s": letters_v3.S, "t": letters_v3.T,
                    "u": letters_v3.U, "v": letters_v3.V, "w": letters_v3.W, "x": letters_v3.X, "y": letters_v3.Y,
                    "z": letters_v3.Z, " ": letters_v3.space, "Invalid": letters_v3.Invalid}

default_pos = [-375, -430]
current_pos = [0, 0]
R_THRESH = -439.877
L_THRESH = -611.823


def robot_write(arm: XArmAPI, to_write: str, ) -> bool:
    paths = list()
    for letter in to_write:
        paths.append(letter_functions.get(letter, letters_v3.Invalid)(arm))

    arm.set_pause_time(1, False)

    for path in paths:
        for pos in path:
            letters_v3.command_queue.put(pos)
            # print(pos)

    letters_v3.command_queue.join()

    arm.set_position(0, 0, 0, 0, 0, 0, 0, is_radian=False, wait=True, speed=5, mvacc=500, relative=True)

    return 0


def send_sentence(arm: XArmAPI, sentence: str, ) -> int:

    to_write = list(sentence)
    print("writing: {}".format(sentence))
    
    return robot_write(arm, to_write)


def get_last_pos(default_pos: list(), reset_pos: bool=False) -> list(): 
    current_pos = [0, 0]
    
    if reset_pos:
        current_pos = default_pos.copy()
        with open(dirname + "/current_pos.tmp", "w") as f:
            f.write(f"{default_pos[0]}\n{default_pos[1]}")
    else:
        try:
            print("opening current_pos file...")

            with open(dirname + "/current_pos.tmp", "r") as f:
                y = lambda x: float(x.rstrip("\n"))
                current_pos = list(map(y, f.readlines()[:2]))

        except FileNotFoundError:
            print("current_pos file does not exist. creating file.")
            with open(dirname + "/current_pos.tmp", "w") as f:
                f.write(f"{default_pos[0]}\n{default_pos[1]}")
            current_pos = default_pos.copy()

        except ValueError:
            print("invalid value in current_pos file. resetting current letter index.")
            with open(dirname + "/current_pos.tmp", "w+") as f:
                f.write(f"{default_pos[0]}\n{default_pos[1]}")
            current_pos = default_pos.copy()

        except:
            print("Unexpected error:", sys.exc_info()[0])
            pass


    print(f"last position: {current_pos}\n")

    return current_pos


def goto_last_pos(arm: XArmAPI, last_pos: list, ):
    speed = 50

    current_pos = deepcopy(arm.position)

    ret = arm.set_position(current_pos[0], current_pos[1], 500, current_pos[3], current_pos[4], current_pos[5], 
        radius=-1, is_radian=False, wait=True, speed=speed, mvacc=10*speed, relative=False) 
    if ret < 0:
        print('set_position, ret={}'.format(ret))
        return -1

    ret = arm.set_position(last_pos[0], last_pos[1], 500, current_pos[3], current_pos[4], current_pos[5], 
        radius=-1, is_radian=False, wait=True, speed=speed, mvacc=10*speed, relative=False)
    if ret < 0:
        print('set_position, ret={}'.format(ret))
        return -1

    ret = arm.set_position(last_pos[0], last_pos[1], 180, current_pos[3], current_pos[4], 90, 
        radius=-1, is_radian=False, wait=True, speed=speed, mvacc=10*speed, relative=False)
    if ret < 0:
        print('set_position, ret={}'.format(ret))
        return -1

    # ret = arm.set_position(last_pos[0], last_pos[1], 171.8, current_pos[3], current_pos[4], 90, 
    ret = arm.set_position(last_pos[0], last_pos[1], 172.8, current_pos[3], current_pos[4], 90, 
        radius=-1, is_radian=False, wait=True, speed=20, mvacc=200, relative=False)
    if ret < 0:
        print('set_position, ret={}'.format(ret))
        return -1

    return 0


def write_setup(arm: XArmAPI, reset_pos: bool=False) -> int:
    arm.set_world_offset([0, 0, 0, 0, 0, 0])
    time.sleep(1)

    arm.motion_enable(enable=True)
    arm.set_mode(0)
    arm.set_state(state=0)

    goto_last_pos(arm, get_last_pos(default_pos, reset_pos))

    print("arm at starting pos")
    print(arm.position)
    time.sleep(1)

    # current_yaw = deepcopy(arm.position)[5]
    # arm.set_world_offset([0, 0, 0, 180, 0.6, current_yaw])
    # arm.set_world_offset([0, 0, 0, 180, 0.6, 90])
    arm.set_world_offset([0, 0, 0, -176, 0, 90])
    time.sleep(1)

    arm.motion_enable(enable=True)
    arm.set_mode(0)
    arm.set_state(state=0)

    threading.Thread(target=letters_v3.move, args=(arm,), daemon=True).start()

    return 0


def write_exit(arm: XArmAPI, last_pos: list = None, ) -> None:
    
    #get current pos
    # print("exiting...")

    time.sleep(0.5)
    arm.set_world_offset([0, 0, 0, 0, 0, 0])
    time.sleep(1)

    if last_pos is None:
        last_pos = deepcopy(arm.position)


    try:
        with open(dirname + "/current_pos.tmp" , "w+") as f:
            to_save = f"{last_pos[0] + 5}\n{last_pos[1]}"
            print(to_save)
            print(f.write(to_save))
            print("wrote last pos to temp file.")
    except Exception as e:
        print(e)

    # arm.disconnect()
    # sys.exit(0)
