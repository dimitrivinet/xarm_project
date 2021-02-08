from flask import Flask, render_template, request

import json
import vocal_control


app = Flask(__name__)
@app.route('/', methods = ['POST', 'GET'])
def student():
    if request.method == 'POST':
      result = json.loads(request.data)["text"] # get sentence to write
      vocal_control.write(result)                             # send sentence to program
    return render_template('webspeechdemo/webspeechdemo.html')


app.run(debug = False)