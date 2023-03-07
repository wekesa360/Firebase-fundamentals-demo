import firebase_admin
from firebase_admin import credentials, auth, db
from flask import Flask, jsonify, request, session
import os

cred = credentials.Certificate('./cred.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fundamentals-demo-default-rtdb.asia-southeast1.firebasedatabase.app'
})

app = Flask(__name__)
app.secret_key = os.urandom(54)


@app.route('/api/signup', methods=['POST'])
def signup():
    email = request.json['email']
    password = request.json['password']
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        session['user'] = user.uid
        return jsonify({'message': 'Account created successfully.'}), 201
    except Exception as e:
        return jsonify({'message': f'There was an issue creating your account: {e}'}), 40


@app.route('/api/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    try:
        user = auth.get_user_by_email(email)
        auth.sign_in_with_email_and_password(email, password)
        session['user'] = user.uid
        return jsonify({'message': 'Login successful'}), 200
    except Exception as e:
        return jsonify({'message': f'Invalid credentials {e}'}), 401
    
    
        
