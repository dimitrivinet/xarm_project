#!/usr/bin/env python3

import os
import sys
import time
import signal

from xarm.wrapper import XArmAPI


def robot_start() -> XArmAPI:
    arm = "dummy"

    connected = False
    while not connected:
        try:
            arm = XArmAPI('172.21.72.250', do_not_open=True)
            arm.connect()
            connected = True
        except:
            print("arm is not online. trying again in 3 seconds...")
            time.sleep(3)
    
    arm.set_world_offset([0, 0, 0, 0, 0, 0])
    time.sleep(1)

    arm.motion_enable(enable=True)
    arm.set_mode(0)
    arm.set_state(state=0)

    time.sleep(1)
    print("arm started")

    return arm


if __name__ == "__main__":
    arm = robot_start()
    time.sleep(10)
    arm.disconnect()
