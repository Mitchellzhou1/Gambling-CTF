from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Connect to MongoDB
CLIENT = MongoClient('mongodb://localhost:27017/')
DB = CLIENT['roulette']
USER_COLLECTION = DB['users']
SEEDS_COLLECTION = DB['seeds']
BET_POOL_NO = 0


# Register route
@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()

    # Ensure required fields are present
    if 'username' not in data or 'password' not in data or 'password2' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if the username already exists
    existing_user = USER_COLLECTION.find_one({'username': data['username']})
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400

    # Hash the password
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=16)

    # Create a new user document
    new_user = {
        'username': data['username'],
        'password': hashed_password,
        'tokens': 2000
    }

    # Insert the new user into the collection
    USER_COLLECTION.insert_one(new_user)

    return jsonify({'message': 'User added successfully'}), 201


# Login route
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    # Ensure required fields are present
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required'}), 400

    # Find the user in the database
    user = USER_COLLECTION.find_one({'username': data['username']})
    if user and check_password_hash(user['password'], data['password']):
        return jsonify({'message': 'Login successful', 'tokens': 2000}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


# Route to fetch the latest seed
@app.route('/api/get-latest-seed', methods=['GET'])
def get_latest_seed():
    # Check if there are any documents in the collection
    if SEEDS_COLLECTION.count_documents({}) > 0:

        # Fetch the latest seed
        latest_entry = SEEDS_COLLECTION.find_one(sort=[("_id", -1)])

        # convert to str to jsonify
        latest_entry['_id'] = str(latest_entry['_id'])
        return jsonify(latest_entry), 200

    else:
        return jsonify({'error': 'No seeds in the DB'}), 401


# Route to fetch latest 100 seeds for provability page
@app.route('/api/get-seeds', methods=['GET'])
def get_seeds():
    # Check if there are any documents in the collection
    if SEEDS_COLLECTION.count_documents({}) > 0:

        # Fetch the latest seed
        latest_entries = SEEDS_COLLECTION.find().sort("_id", -1).limit(100)

        latest_entries_list = []

        for entry in latest_entries:
            # convert to str to jsonify
            entry['_id'] = str(entry['_id'])
            latest_entries_list.append(entry)

        return jsonify({"latest_entries": latest_entries_list}), 200

    else:
        return jsonify({'error': 'No seeds in the DB'}), 401


@app.route('/api/place-bets', methods=['POST'])
def place_bet():
    global BET_POOL_NO

    data = request.get_json()

    # Ensure required fields are present
    if 'username' not in data or 'bet' not in data or 'color' not in data:
        return jsonify({'error': 'Username, bet and color are required'}), 400

    # Find the user in the database
    user = USER_COLLECTION.find_one({'username': data['username']})
    if user:
        print(f'{BET_POOL_NO.value}')
        pool_collection = DB[f"POOL{BET_POOL_NO.value}"]

        user_in_pool = pool_collection.find_one({'username': data['username']}) == data['username']
        if user_in_pool:
            return jsonify({'error': 'User cannot place the bet twice'}), 401

        # Create a new bet document
        new_bet = {
            'username': data['username'],
            'color': data['color'],
            'bet': data['bet']
        }

        # Insert the new bet into the pool
        pool_collection.insert_one(new_bet)
        return jsonify({'message': 'Successfully placed the bet'}), 200
    else:
        return jsonify({'error': 'User does not exist'}), 401


def run_flask(pool_number):
    global BET_POOL_NO
    BET_POOL_NO = pool_number
    app.run(debug=False)
