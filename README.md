# Flask-Firebase CRUD API
This is a simple Flask API that uses Firebase Firestore as a data store to perform CRUD (Create, Read, Update, Delete) operations on a collection of users.

## **Requirements**
- Python 3.x
- Flask
- Firebase Admin SDK
## **Installation**
1. Clone this repository to your local machine.
2. Install the required dependencies using pip:

    ```
    pip install -r requirements.txt
    ```
3. Add your Firebase service account credentials to the project directory as  `key.json`. You can obtain these credentials by creating a new Firebase project and generating a new private key from the Firebase console.
4. Start the Flask development server:

    ```
        flask run
    ```

5. The API should now be available at `http://localhost:5000`.
## **Endpoints**
- `GET /api/users`: Retrieve all users from the database.
- `POST /api/users`: Create a new user in the database.
- `GET /api/users/<user_id>`: Retrieve a specific user by ID.
- `PUT /api/users/<user_id>`: Update a specific user by ID.
- `DELETE /api/users/<user_id>`: Delete a specific user by ID.

All data is sent and received in JSON format.

## **Examples**

To create a new user:


    POST /api/users
    {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "age": 30
    }

To retrieve all users:


    GET /api/users

To retrieve a specific user by ID:


    GET /api/users/abc123

To update a specific user by ID:


    PUT /api/users/abc123
    {
        "age": 31
    }

To delete a specific user by ID:


    DELETE /api/users/abc123
