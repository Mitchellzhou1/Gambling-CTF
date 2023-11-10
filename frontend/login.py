from datetime import timedelta
from app import *
import string, random
from flask import Flask, make_response, request, flash, session, jsonify
import requests 
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
           y user = request.json.get('usr')
            pwd = request.json.get('pwd')
            backend_url = 'http://localhost:5000/api/login'
            response = requests.post(backend_url, json={'username': user, 'password': pwd})

            if response.ok:
                session['logged_in'] = True 
                session['user'] = user  
                app.permanent_session_lifetime = timedelta(minutes=30)
                return jsonify({"success":True, "redirect": url_for('index')})
            else:
                return jsonify({"success":False, "error": "Incorrect username/password"})
            
        
@app.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        if request.method == "POST":
            user = request.json.get('usr')
            pwd1 = request.json.get('pwd1')
            pwd2 = request.json.get('pwd2')
            backend_url = 'http://localhost:5000/api/register'
            response = requests.post(backend_url, json={'username': user, 'password': pwd1, 'password2':pwd2})

            if response.ok:
                session['logged_in'] = True 
                session['user'] = user  
                app.permanent_session_lifetime = timedelta(minutes=30)
                return jsonify({"redirect": url_for('index')})
            else:
                return jsonify({"success":False, "error": "Username already exists"})

@app.route('/logout', methods = ["POST"])
def logout():
    session['user'] = ''
    session['logged_in'] = False 
    return jsonify({"redirect": url_for('login')})
