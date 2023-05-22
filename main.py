import http.client
import json
from flask import Flask,jsonify,request

app=Flask(__name__)
@app.route("/")

def hi():
    return "my API call"

@app.route('/post', methods=["POST"])

def testpost():
     input_json = request.get_json(force=True)
     dictToReturn = {'text':input_json['text']}
     return jsonify(dictToReturn)
