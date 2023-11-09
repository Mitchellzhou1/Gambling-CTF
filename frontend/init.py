from flask import Flask, render_template, request, session, url_for, redirect, make_response, jsonify
from app import *
import string, random, login, json, requests

rouletteVals = [('00', 'green'), ('1', 'red'), ('13', 'black'), ('36', 'red'), ('24', 'black'), ('3', 'red'),
                   ('15', 'black'), ('34', 'red'), ('22', 'black'), ('5', 'red'), ('17', 'black'), ('32', 'red'), 
                   ('20', 'black'), ('7', 'red'), ('11', 'black'), ('30', 'red'), ('26', 'black'), ('9', 'red'), 
                   ('28', 'black'), ('0', 'green'), ('2', 'black'), ('14', 'red'), ('35', 'black'), ('23', 'red'), 
                   ('4', 'black'), ('16', 'red'), ('33', 'black'), ('21', 'red'), ('6', 'black'), ('18', 'red'), 
                   ('31', 'black'), ('19', 'red'), ('8', 'black'), ('12', 'red'), ('29', 'black'), ('35', 'red'), 
                   ('10', 'black'), ('27', 'red')]

pointer = 0
tokens = 10000
userColor = ""
curr = 0 

def spinner():
    num = str(seed())
    if num == "37": num = "00"
    color = ""
    for val in rouletteVals:
        if val[0] == num:
            color = val[-1]
            break
    return color, num

def point_system(color):
    global userColor, tokens, bet
    if userColor:
        if userColor == color:
            if color == 'green': tokens = bet * 10
            else: tokens = bet * 2
        else: tokens -= bet 
        userColor = ''
        bet = 0

        
@app.route('/info', methods=['GET'])
def info():
    # Your logic to fetch and process the seeds data
    response = requests.get('http://localhost:5000/api/get-seeds')
    data = json.loads(response.text)
    latest_entries = data['latest_entries']
    seed_number_tuples = [(entry['hashed_seed'], entry['number']) for entry in latest_entries]

    # Render 'info.html' and pass the seed_number_tuples data to it
    return render_template('info.html', seed_data=seed_number_tuples[::-1])
            
@app.route('/getSeed', methods=['GET'])
def seed():
    if request.method == 'GET':
        response = requests.get('http://localhost:5000/api/get-latest-seed') #get-latest-number
        if response.ok:
           num = json.loads(response.text)['number']
           return num 
        else:
            return jsonify({"success":False, "error": "No seeds in the DB"}), 401

@app.route('/userInput', methods=['POST'])
def userInput():
    global userColor, bet
    try: 
        bet = int(request.json.get('bet_amount'))
    except ValueError:
        return jsonify({"error": "Please enter a number"}), 500

    userColor = request.json.get('user_color')
    
    # Return the color and bet amount back to the frontend
    return jsonify(color=userColor, bet_amount=bet)


@app.route('/spin')
def spin():
    global tokens, curr, bet
    color, num = spinner()
    point_system(color)
    curr += 1
    print(num, curr)
    return jsonify(number=str(num), color=color, tokens=tokens)

@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in'] and session['user']:
        return render_template('index.html', tokens=tokens)
    else: return redirect(url_for('login'))
    
app.secret_key = "he1231sajiod9832jkfjsd321ADSA2131"

if __name__ == '__main__':
    app.run('0.0.0.0', 9999, debug=True)