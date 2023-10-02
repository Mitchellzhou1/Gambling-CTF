from flask import Flask, render_template, request, session, url_for, redirect, make_response
import pymysql.cursors
from app import app, get_conn
import string, random

@app.route('/')
def index():
    numbers = [('00', 'green'), ('27', 'red'), ('10', 'black'), ('35', 'red'), ('29', 'black'), ('12', 'red'), ('8', 'black'), ('19', 'red'),
               ('31', 'black'), ('18', 'red'), ('6', 'black'), ('21', 'red'), ('33', 'black'), ('16', 'red'), ('4', 'black'), ('23', 'red'),
               ('35', 'black'), ('14', 'red'), ('2', 'black'), ('0', 'red'), ('28', 'black'), ('9', 'red'), ('26', 'black'), ('30', 'red'),
               ('11', 'black'), ('7', 'red'), ('20', 'black'), ('32', 'red'), ('17', 'black'), ('5', 'red'), ('22', 'black'), ('34', 'red'),
               ('15', 'black'), ('3', 'red'), ('24', 'black'), ('36', 'red'), ('13', 'black'), ('1', 'red'), ('00', 'green')]


    res = make_response(render_template('index.html'))
    return res


app.secret_key = 'Q3I3Pm1lc3NpQ3I3Pm1lc3NpQ3I3Pm1lc3Np123hehe'

if __name__ == "__main__":
    app.run('0.0.0.0', 5800, debug=False)