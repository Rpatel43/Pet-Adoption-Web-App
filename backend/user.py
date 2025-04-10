"""User file for API. All calls related to the user are within this file."""
from flask import Blueprint, request, jsonify

# note the blueprint!
user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/signin', methods=['POST'])
def signin():
    """Authenticate a user based off provided login info and return
    necessary response. Note we use a POST rquest for this."""

    # Make data request for user and pass
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    ######### Stub - validate login info #########
    if username and password:
        # note the success code!
        # also note we return the username for clarity AND
        # so we can include it to display on the homepage in the future per chance :)
        return jsonify({"message": "User login successful!", "username": username}), 200
    # note the error code and the fact we do not return any username
    # information so we dont give malicious users free info
    return jsonify({"error": "Missing username/password field :("}), 400
    ##############################################


@user_blueprint.route('/signup', methods=['POST'])
def signup():
    """Confirm a user signup that meets user/pass standards
    and includes all fields. Note the POST request."""

    # make data request for first and last name + user and password
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    username = data.get('username')
    password = data.get('password')
    password_confirm = data.get('password_conf')

    # note user/pass len and req for pass conf = pass
    ########## Stub - Create a new user ##########
    if not first_name or not last_name or not username or not password or not password_confirm:
        return jsonify({"error": "One of the required fields is missing information :("}), 400
    if password != password_confirm:
        return jsonify({"error": "Failed to confirm password :o"}), 400
    if len(username) < 3 or len(username) > 16:
        return jsonify({"error": "Username must be 3-16 characters."})
    if len(password) < 8 or len(password) > 32:
        return jsonify({"error": "Password must be 8-32 characters."})
    return jsonify({"message": "User successfully created",
                    "username": username}), 201
    ##############################################


#############################################################################################
### Note for signout that in our full implementation, we will need to include checks that the user
### is signed in. For now, we do not need this because its just a starter stub implementation.
#############################################################################################


@user_blueprint.route('/signout', methods=['GET'])
def signout():
    """Confirm a successful signout on button click. Notice GET method."""

    ########## Stub - Signout ##########
    return jsonify({"message": "User signed out"}), 200
    ####################################


@user_blueprint.route('/applications', methods=['GET'])
def user_applications():
    """Display list of all user applications on button click. Notice GET method."""

    #### Stub - return list of current applications for logged-in user ####
    mock_applications = [
        {"application_id": 1, "pet_id": 1, "status": "pending"},
        {"application_id": 2, "pet_id": 2, "status": "denied"},
        {"application_id": 3, "pet_id": 3, "status": "approved"},
    ]
    return jsonify({"applications": mock_applications}), 200
    #######################################################################
