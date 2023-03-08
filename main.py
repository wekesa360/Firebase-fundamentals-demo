import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, jsonify, request

cred = credentials.Certificate('./key.json')
firebase_app = firebase_admin.initialize_app(cred)

app = Flask(__name__)
db = firestore.client()

@app.route('/api/users', methods=['GET'])
def get_users():
    users_ref = db.collection('users')
    users = [doc.to_dict() for doc in users_ref.get()]
    return jsonify(users), 200

@app.route('/api/users', methods=['POST'])
def create_user():
    user_data = request.json
    users_ref = db.collection('users')
    user_ref = users_ref.document()
    user_ref.set(user_data)
    user_data['id'] = user_ref.id
    return jsonify(user_data), 201

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user_ref = db.collection('users').document(user_id)
    user_data = user_ref.get()
    if user_data.exists:
        return jsonify(user_data.to_dict()), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.json
    user_ref = db.collection('users').document(user_id)
    user_ref.update(user_data)
    return jsonify({'message': 'User updated successfully'}), 200

@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_ref = db.collection('users').document(user_id)
    user_ref.delete()
    return jsonify({'message': 'User deleted successfully'}), 200

if __name__ == '__main__':
    app.run()