from flask import Flask, render_template, request

import json


app = Flask(__name__)
@app.route('/', methods = ['POST', 'GET'])
def student():
    if request.method == 'POST':
      result = json.loads(request.data)["text"]
      print(result)
    return render_template('webspeechdemo/webspeechdemo.html')


app.run(debug = False)