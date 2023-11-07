from app import *
import string, random
from flask import Flask, make_response, request, flash, session, jsonify
import re

def validEmail(email):
    regex = "^[a-zA-Z0-9-_!#$%&'*+-/=?^_`{|}~']+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    return re.search(regex, email)

@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        if request.method == "POST":
            username = request.json.get('usr')
            password = request.json.get('pwd')
            if authenticate(username, password):
                session['logged_in'] = True 
                session['user'] = username  
                return jsonify({"success":True, "redirect": url_for('index')})
            else:
                return jsonify({"error": "Incorrect username/password", "success":False})

def authenticate(username, password):
    # Auth with DB
    # prepared statements
    return False

@app.route('/logout', methods = ["POST"])
def logout():
    session['email'] = ''
    session['logged_in'] = False 
    return render_template('login.html')
