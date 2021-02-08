#!/usr/bin/env python3

from flask import Flask, render_template, request
from xarm.wrapper import XArmAPI

import threading
import json
import sys
import signal
import time

from vocal_control.arm_init import start as robot_start
from vocal_control.vocal_control_mod import execute as robot_execute



def sigint_handler(sig, frame):
    print("\nSIGINT Captured, terminating")
    if arm:
        arm.set_state(state=4)
        arm.disconnect()
    sys.exit(0)


app = Flask(__name__)
@app.route('/', methods = ['POST', 'GET'])
def student():
    if request.method == 'POST':
        result = json.loads(request.data)["text"]   # get sentence to write
        try:
            print(result)
            robot_execute(result)                     # send sentence to program
        except Exception as e:
            print(e)
            pass

    return render_template('webspeechdemo/webspeechdemo.html')



arm = "dummy"

signal.signal(signal.SIGINT, sigint_handler)

connected = False
while not connected:
    try:
        arm = XArmAPI('172.21.72.250', do_not_open=True)
        arm.connect()
        connected = True
    except:
        print("arm is not online. trying again in 3 seconds...")
        time.sleep(3)

app_init = threading.Thread(target= app.run, kwargs={"debug":False, })
app_init.start()

robot_start(arm)

app_init.join()