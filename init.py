import json
from flask import Flask, render_template, request, session, url_for, redirect, make_response, jsonify
import pymysql.cursors
from app import app, get_conn
import string, random

numbers = [('00', 'green'), ('1', 'red'), ('13', 'black'), ('36', 'red'), ('24', 'black'), ('3', 'red'),
           ('15', 'black'), ('34', 'red'), ('22', 'black'), ('5', 'red'),
           ('17', 'black'), ('32', 'red'), ('20', 'black'), ('7', 'red'), ('11', 'black'), ('30', 'red'),
           ('26', 'black'), ('9', 'red'), ('28', 'black'),
           ('0', 'green'), ('2', 'black'), ('14', 'red'), ('35', 'black'), ('23', 'red'), ('4', 'black'), ('16', 'red'),
           ('33', 'black'), ('21', 'red'),
           ('6', 'black'), ('18', 'red'), ('31', 'black'), ('19', 'red'), ('8', 'black'), ('12', 'red'),
           ('29', 'black'), ('35', 'red'), ('10', 'black'),
           ('27', 'red')]

degrees = 360 / len(numbers)
pointer = 0
tokens = 2000
stack = []


def testing(steps, val):
    print("steps=", steps)
    print("pointer=", pointer)
    print("val=", val)


def spinner():
    global pointer
    steps = random.randrange(0, 38)
    pointer = (pointer + steps) % 38
    #testing(steps, numbers[pointer])
    return numbers[pointer], steps


def point_system(color):
    global stack, tokens
    if stack:
        if stack[0] == color:
            if color == 'red':
                tokens *= 2
            elif color == 'black':
                tokens *= 2
            else:
                tokens *= 10
        else:
            tokens //= 5
        stack.pop(0)
    print(tokens)


@app.route('/userInput', methods=['POST'])
def userInput():
    global stack
    data = request.get_json()
    stack.append(data['user_color'])
    return jsonify(color=data)

@app.route('/spin')
def spin():
    global tokens
    (number, color), steps = spinner()
    print(number, color)
    degree = degrees * steps
    point_system(color)
    return jsonify(degrees=720 + degree, number=number, color=color, tokens=tokens)

data = {
    "key": None,
    "action": None,
    "args": None
}

"""
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
    return jsonify(response)"""

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    key = request.json.get('key', None)
    if key is not None:
        response = {"key": key}
        if key
    # return jsonify(response)
        return jsonify({"redirect": url_for('game')})

"""@app.route('/getHistory', methods=['GET'])
def get_history():
    # This route takes no parameters, so no need to check for JSON input
    return jsonify("hello")"""


@app.route('/game')
def game():
    res = render_template('index.html', tokens=tokens)
    return res

app.secret_key = "hehe"
