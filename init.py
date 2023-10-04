from flask import Flask, render_template, request, session, url_for, redirect, make_response
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


def testing(steps, val):
    print("steps=", steps)
    print("pointer=", pointer)
    print("val=", val)


def spinner():
    global pointer
    steps = random.randrange(0, 38)
    pointer = steps
    testing(steps, numbers[pointer])
    return numbers[pointer]


@app.route('/')
def index():
    global pointer
    number, color = spinner()
    print("number = ", number)
    print("degrees = ", degrees * pointer)
    res = render_template('index.html', number=number, degrees=degrees * pointer)
    pointer = 0
    return res


app.secret_key = 'hehe'

if __name__ == "__main__":
    app.run('0.0.0.0', 5800, debug=False)
