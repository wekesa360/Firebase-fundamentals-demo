import firebase_admin
from firebase_admin import credentials, auth, db
from flask import Flask, jsonify, request, session
import os

cred = credentials.Certificate('./key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fundamentals-demo-default-rtdb.asia-southeast1.firebasedatabase.app'
})

app = Flask(__name__)
app.secret_key = os.urandom(54)

app.config['FIREBASE_ADMIN_APP'] = firebase_admin.get_app()

@app.route('/api/signup', methods=['POST'])
def signup():
    email = request.json['email']
    password = request.json['password']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    gender = request.json['gender']

    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=first_name
        )
        session['user'] = user.uid
        db.reference(f'users/{user.uid}').set(
            {
            'first_name': first_name,
            'last_name': last_name,
            'email': user.email,
            'gender': gender
            }
        )
        return jsonify({'message': 'Account created successfully.'}), 201
    except Exception as e:
        return jsonify({'message': f'There was an issue creating your account: {e}'}), 40


@app.route('/api/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    app = app.config['FIREBASE_ADMIN_APP']
    auth = firebase_admin.auth
    
    user = auth.get_user_by_email(email, password)
    try:
        decoded_token = auth.verify_id_token(user.id_token)
        user = auth.get_user(decoded_token['uid'])
        session['user'] = user.uid
        return jsonify({'message': 'Login successful'}), 200
    except Exception as e:
        return jsonify({'message': f'Invalid credentials {e}'}), 401
    

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'message': 'Logout successful.'}), 200


@app.route('/api/profile', methods=['GET'])
def profile():
    if 'user' in session:
        user = auth.get_user(session['user'])
        user_data = db.reference(f'users/{user.uid}').get()
        return jsonify({'email': user.email, 
                        'first_name': user_data['first_name'],
                        'last_name': user_data['last_name'],
                        'gender': user_data['gender'] }), 200
    else:
        return jsonify({'message': 'You are not logged in'}), 401
    


if __name__ == '__main__':
    app.run()
