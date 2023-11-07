from flask import Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['roulette']
users_collection = db['users']

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()

    # Ensure required fields are present
    if 'username' not in data or 'password' not in data or 'password2' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if the username already exists
    existing_user = users_collection.find_one({'username': data['username']})
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400

    # Hash the password
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=16)

    # Create a new user document
    new_user = {
        'username': data['username'],
        'password': hashed_password,
        'balance': 2000
    }

    # Insert the new user into the collection
    users_collection.insert_one(new_user)

    return jsonify({'message': 'User added successfully'}), 201


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    # Ensure required fields are present
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required'}), 400

    # Find the user in the database
    user = users_collection.find_one({'username': data['username']})
    if user and check_password_hash(user['password'], data['password']):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


if __name__ == '__main__':
    app.run(debug=True)
