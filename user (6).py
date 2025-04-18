"""User file for API. All calls related to the user are within this file."""
from sqlite3 import IntegrityError
from functools import wraps
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from .database import open_database

# note the blueprint!
user_blueprint = Blueprint('user', __name__)


def user_only(function):
    """Wrap that only allows signed in users to access certain content."""
    @wraps(function)
    def wrapped(*args, **kwargs):
        """Wrap that utilizes session and user_id to ensure a user is logged in"""
        if "user_id" not in session:
            return jsonify({"error": "You must be logged in for this feature."}), 401
        return function(*args, **kwargs)
    return wrapped

@user_blueprint.route('/signin', methods=['POST'])
def signin():
    """
    Authenticate a user based off provided login info and return
    necessary response. Note we use a POST rquest for this.
    ---
    tags:
      - Users
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [username, password]
            properties:
              username: { type: string }
              password: { type: string }
    responses:
      200:
        description: Login successful
      400:
        description: Missing fields
      401:
        description: Invalid credentials
    """

    # Make data request for user and pass
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing username or password."}), 400

    # DB
    database = open_database()
    row = database.execute("SELECT id, password FROM users WHERE username = ?",
                           (username,)).fetchone()
    if not row or not check_password_hash(row["password"], password):
        return jsonify({"error": "Invalid login."}), 401

    # NOTE session established here
    session["user_id"] = row["id"]
    session["username"] = username

    return jsonify({"message": "User successfully logged in!",
                    "username": username}), 200



@user_blueprint.route('/signup', methods=['POST'])
def signup():
    """
    Confirm a user signup that meets user/pass standards
    and includes all fields. Note the POST request.
    ---
    tags:
      - Users
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [first_name, last_name, username, password, password_conf]
            properties:
              first_name: { type: string }
              last_name:  { type: string }
              username:   { type: string, minLength: 3, maxLength: 16 }
              password:   { type: string, minLength: 8, maxLength: 32 }
              password_conf: { type: string }
    responses:
      201:
        description: User created
      400:
        description: Validation error
      409:
        description: Username already exists
    """

    # make data request for first and last name + user and password
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    username = data.get('username')
    password = data.get('password')
    password_confirm = data.get('password_conf')

    if not first_name or not last_name or not username or not password or not password_confirm:
        return jsonify({"error": "One of the required fields is missing information :("}), 400
    if password != password_confirm:
        return jsonify({"error": "Failed to confirm password :o"}), 400
    if len(username) < 3 or len(username) > 16:
        return jsonify({"error": "Username must be 3-16 characters."}), 400
    if len(password) < 8 or len(password) > 32:
        return jsonify({"error": "Password must be 8-32 characters."}), 400


    # hash+salt password
    protected_password = generate_password_hash(password)

    # database
    database = open_database()
    # Cannot have duplicate usernames; catch it now
    try:
        database.execute(
            "INSERT INTO users (username, first_name, last_name, password) VALUES (?, ?, ?, ?)",
            (username, first_name, last_name, protected_password)
        )
        database.commit()
    except IntegrityError:
        return jsonify({"error": "Username taken."}), 409

    return jsonify({"message": "New user created",
                    "username": username}), 201

#############################################################################################
### Note for signout that in our full implementation, we will need to include checks that the user
### is signed in. For now, we do not need this because its just a starter stub implementation.
#############################################################################################
# ^^^ now we do it

@user_blueprint.route('/signout', methods=['POST'])
@user_only
def signout():
    """
    Confirm a successful signout on button click.
    ---
    tags:
      - Users
    responses:
      200:
        description: Signed out
      401:
        description: Unauthorized
    """

    # just pop from session so they lose access
    session.pop("user_id", None)
    session.pop("username", None)
    return jsonify({"message": "User signed out"}), 200



@user_blueprint.route('/applications', methods=['GET'])
@user_only
def user_applications():
    """
    Display list of all user applications on button click. Notice GET method.
    ---
    tags:
      - Applications
    responses:
      200:
        description: JSON object with “applications” array
        content:
          application/json:
            schema:
              type: object
              properties:
                applications:
                  type: array
                  items:
                    $ref: '#/components/schemas/Application'
      401:
        description: Unauthorized
    components:
      schemas:
        Application:
          type: object
          properties:
            application_id:      { type: integer }
            user_id:             { type: integer }
            pet_id:              { type: integer }
            status:              { type: string }
            application_response:{ type: string }
    """

    database = open_database()
    # collect all applications for user
    rows = database.execute("SELECT * FROM applications WHERE user_id = ?",
                            (session["user_id"],)).fetchall()

    # put them in list(dict) form
    applications = [dict(row) for row in rows]
    return jsonify({"applications": applications}), 200


@user_blueprint.route("/session", methods=['GET'])
def active_user():
    """
    Endpoint that will be used to check when a user is or is not logged in.
    Useful for adaptive homepage that needs to know when youre logged in or not.
    ---
    tags:
      - Users
    responses:
      200:
        description: Current user info
        content:
          application/json:
            schema:
              type: object
              properties:
                user:
                  oneOf:
                    - type: null
                    - type: object
                      properties:
                        id:       { type: integer }
                        username: { type: string }
    """

    # If user no longer logged in, mark it
    if "user_id" not in session:
        return jsonify({"user": None}), 200

    # otherwise, maintain session
    return jsonify({"user": {
        "id": session["user_id"],
        "username": session["username"]
    }}), 200
