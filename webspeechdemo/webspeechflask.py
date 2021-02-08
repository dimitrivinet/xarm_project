from flask import Flask, render_template, request

import threading
import json
import vocal_control
from vocal_control.vocal_control_mod import write as robot_write
from vocal_control.vocal_control_mod import start as start_robot


app = Flask(__name__)
@app.route('/', methods = ['POST', 'GET'])
def student():
    if request.method == 'POST':
        result = json.loads(request.data)["text"]   # get sentence to write
        try:
            print(result)
            robot_write(result)                     # send sentence to program
        except Exception as e:
            print(e)
            pass

    return render_template('webspeechdemo/webspeechdemo.html')


app_init = threading.Thread(target= app.run, kwargs={"debug":False, })
app_init.start()

start_robot()

app_init.join()