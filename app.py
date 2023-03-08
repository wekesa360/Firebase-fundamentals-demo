# Import required packages
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, jsonify, request

#Initialize Firebase Admin SDK with service account credentials
cred = credentials.Certificate('./key.json')
firebase_app = firebase_admin.initialize_app(cred)

#Create Flask app and Firestore client
app = Flask(__name__)
db = firestore.client()

@app.route('/api/users', methods=['GET'])
def get_users():
    """Endponint to retrieve all users from Firestore database."""
    # Retrieve all documents from the 'users' collection and convert them to a list of dictionaries
    users_ref = db.collection('users')
    users = [doc.to_dict() for doc in users_ref.get()]
    # Return a JSON response with the list of users and a 200 OK status code
    return jsonify(users), 200

@app.route('/api/users', methods=['POST'])
def create_user():
    """Endpoint to create a new user in a Firestore database."""
    # Retrieve user data from the request body of a JSON object
    user_data = request.json
    # Create a new document in the 'users' collection and set the data
    users_ref = db.collection('users')
    user_ref = users_ref.document()
    user_ref.set(user_data)
    # Add the document ID to the user data and return the updated user data with a 201 Created status code
    user_data['id'] = user_ref.id
    return jsonify(user_data), 201

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Endpoint to retrieve a single user from  Firestore database."""
    # Retrieve the document with the specified user ID from the 'users' collection
    user_ref = db.collection('users').document(user_id)
    user_data = user_ref.get()
    # Check if the document exists and return the user data as a JSON response  with 20 OK code, or return a 404 Not found status code.
    if user_data.exists:
        return jsonify(user_data.to_dict()), 200
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Endpoint to update a single user in Firestore database."""
    # Retrieve updated user data from the request body as a JSON object
    user_data = request.json
    # Update the document with hte specified user ID in the 'users' collection
    user_ref = db.collection('users').document(user_id)
    user_ref.update(user_data)
    # Return a JSOn response with a message and a 200 OK status code
    return jsonify({'message': 'User updated successfully'}), 200

@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Endpoint to delete a single user"""
    # Delete the document with the specified user ID from the 'users' collection
    user_ref = db.collection('users').document(user_id)
    user_ref.delete()
    #Return a JSON response with a message and 200 OK status code
    return jsonify({'message': 'User deleted successfully'}), 200

# If script is being executed as the main program
if __name__ == '__main__':
    app.run()