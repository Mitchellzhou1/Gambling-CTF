from flask import Flask, request, jsonify
import json
from flask import Flask, render_template, request, session, url_for, redirect, make_response, jsonify
import pymysql.cursors
from app import app, get_conn
import string, random


app = Flask(__name__)

# Sample data store
data = {
    "key": None,
    "action": None,
    "args": None
}

@app.route('/userInput', methods=['POST'])
def user_input():
    try:
        data['key'] = request.json['key']
        data['action'] = request.json['action']
        data['args'] = request.json['args']
        response = data
    except KeyError:
        response = "hello"
    return jsonify(response)

@app.route('/getMoney', methods=['POST'])
def get_money():
    key = request.json.get('key', None)
    if key is not None:
        response = {"key": key}
    else:
        response = "hello"
    return jsonify(response)

@app.route('/login', methods=['GET','POST'])
def login():
    key = request.json.get('key', None)
    if key is not None:
        response = {"key": key}
    else:
        response = "hello"
    return jsonify(response)

@app.route('/getHistory', methods=['GET'])
def get_history():
    # This route takes no parameters, so no need to check for JSON input
    return jsonify("hello")


@app.route('/game')
def game():
    res = render_template('index.html', tokens=tokens)
    return res

app.secret_key = "hehe"

if __name__ == '__main__':
    app.run('0.0.0.0', 5801, debug=False)