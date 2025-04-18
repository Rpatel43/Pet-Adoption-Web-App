"""File that controls all enpoints for everything related to the admin
portal and beyond, from signing in to managing services."""
import os
from sqlite3 import IntegrityError
from functools import wraps
from flask import Blueprint, request, jsonify, current_app, session, url_for
from werkzeug.utils import secure_filename
from backend.database import open_database

# blueprint for main
admin_blueprint = Blueprint('admin', __name__)

# Create folder for uploading pet photots
# root/static/uploads/ = path made with os
# PET_PHOTO_DIRECTORY = os.path.join(current_app.root_path, 'static', 'uploads')
# os.makedirs(PET_PHOTO_DIRECTORY, exist_ok=True) # exist_ok prevents error call in case
                                                # its already there

def admin_only(function):
    """Wrap for functions that ensures only admin users are capable of accessing
    certain application functions. Attached to all admin functions."""

    @wraps(function)
    def wrap(*args, **kwargs):
        """Wrap that utilizes session cookie to check if a user
        can or cannot access the management portals services."""

        if "admin_user" not in session:
            return jsonify({"error": "User is not authorized."}), 401
        return function(*args, **kwargs)
    return wrap


@admin_blueprint.route('/signin', methods=['POST'])
def admin_signin():
    """
    Manages admin sign in, ensuring login matches some currently hard
    coded login information.
    ---
    tags:
      - Admin
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
        description: Admin login successful
      400:
        description: Missing fields
      401:
        description: Invalid credentials
    """

    data = request.get_json()
    admin_username = data.get('username')
    admin_password = data.get('password')

    # Check user supplied username and pass
    if not admin_username or not admin_password:
        return jsonify({"error": "User did not provide username or password."}), 400

    # DATABASE
    database = open_database()
    cursor = database.execute("SELECT * FROM admins where username = ? AND password = ?",
                              (admin_username, admin_password))
    admin = cursor.fetchone()
    if not admin:
        return jsonify({"error": "Invalid login for admin user."}), 401

    # NOTE WE ESTABLISH THE SESSION HERE!:
    # admin_user is how we call in future to ensure we are on admin account!
    session['admin_user'] = admin_username
    return jsonify({"message": "Admin successfully logged in,", "admin": admin_username}), 200



@admin_blueprint.route('/signout', methods=['POST'])
@admin_only
def admin_signout():
    """
    Sign out the logged in admin user with a session clear.
    ---
    tags:
      - Admin
    responses:
      200:
        description: Admin signed out
      401:
        description: Unauthorized
    """
    session.pop('admin_user', None)
    return jsonify({'message': 'Admin signed out'}), 200



@admin_blueprint.route('/dashboard', methods=['GET'])
@admin_only
def admin_dashboard():
    """
    Returns all pet listings, applications, and pet types from our new fancy database o.o
    ---
    tags:
      - Admin
    responses:
      200:
        description: JSON with pets, applications, and pet_types
      401:
        description: Unauthorized
    """

    database = open_database()

    # we turn the fetchall data from database into a list of dictionaries
    # so we can turn the columns and rows into key value pairs
    # for pet types we can access with index because of thr ROW FACTORY!!!
    pets = [dict(row) for row in database.execute("SELECT * FROM pets").fetchall()]
    applications = [dict(row) for row in database.execute("SELECT * FROM applications").fetchall()]
    pet_types = [row["type"] for row in database.execute("SELECT type FROM pet_types").fetchall()]

    # RETURNGING the data
    return jsonify({"dashboard": {
        "pet_listings": pets,
        "applications": applications,
        "pet_types": pet_types
    }}), 200 # the sacred return code


@admin_blueprint.route('/pet', methods=['POST'])
@admin_only
def add_pet():
    """
    Controls management's abiltiy to add new pet listings.
    ---
    tags:
      - Admin
    requestBody:
      required: true
      content:
        multipart/form-data:
          schema:
            type: object
            required: [name,type,sex,bio,health_info,size,weight,status,picture]
            properties:
              name:        { type: string }
              type:        { type: string }
              sex:         { type: string }
              bio:         { type: string }
              health_info: { type: string }
              size:        { type: string }
              weight:      { type: string }
              status:      { type: string }
              picture:
                type: string
                format: binary
    responses:
      201:
        description: Pet created
      400:
        description: Validation error or missing file
      401:
        description: Unauthorized
    """

    # first make sure the data fields are present in the form
    data_fields = ['name', 'type', 'sex', 'bio', 'health_info', 'size', 'weight', 'status']
    for field in data_fields:
        if not request.form.get(field):
            return jsonify({"error": f"missing data field: {field}"}), 400

    # then we validate the image and save it to our directory
    if "picture" not in request.files:
        return jsonify({"error": "No picture uploaded :L"}), 400

    upload_dir = current_app.config['PET_PHOTO_DIRECTORY']
    picture = request.files['picture'] # grab the picture data

    # use secure filename for safety and convenience features
    filename = secure_filename(picture.filename)

    # put photo in directory
    file_desination = os.path.join(upload_dir, filename)
    picture.save(file_desination)

    # we need the url for the database so grab it now
    picture_url = url_for('static', filename=f"uploads/{filename}")

    # DATAbase
    database = open_database()
    cursor = database.execute(
        """INSERT INTO pets (name, type, sex, bio, health_info, size, weight, status, picture)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (request.form['name'], request.form['type'], request.form['sex'],
         request.form['bio'], request.form['health_info'], request.form['size'],
         request.form['weight'], request.form['status'], picture_url)
    )
    database.commit()

    return jsonify({"message": "Pet added:",
                    "pet_id": cursor.lastrowid,
                    "picture_url": picture_url}), 201



@admin_blueprint.route('/pet/<int:pet_id>', methods=['PUT'])
@admin_only
def edit_pet(pet_id):
    """
    Controls management's ability to edit an existing pet listing.
    ---
    tags:
      - Admin
    parameters:
      - in: path
        name: pet_id
        schema:
          type: integer
        required: true
        description: ID of the pet
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [name, type, sex, bio, health_info, size, weight, status, picture]
            properties:
              name:        { type: string }
              type:        { type: string }
              sex:         { type: string }
              bio:         { type: string }
              health_info: { type: string }
              size:        { type: string }
              weight:      { type: string }
              status:      { type: string }
              picture:     { type: string }
    responses:
      200:
        description: Pet updated
      400:
        description: Missing fields
      401:
        description: Unauthorized
    """

    # Data grab and verify all fields present on edit
    data = request.get_json() or {} # if there is somehow an empty pet listing
    required_fields = ["name", "type", "sex", "bio", "health_info",
                       "size", "weight", "status", "picture"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"missing field(s): {', '.join(missing_fields)}"}), 400

    # database update
    database = open_database()
    database.execute(
        """
        UPDATE pets
            SET name = ?,
                type = ?,
                sex = ?,
                bio = ?,
                health_info = ?,
                size = ?,
                weight = ?,
                status = ?,
                picture = ?
        WHERE id = ?
        """,
        (
            data['name'], data['type'], data['sex'],
            data['bio'], data['health_info'], data['size'],
            data['weight'], data['status'], data['picture'], pet_id
        )
    )

    database.commit()
    return jsonify({"message": "pet information updated",
                    "pet_id": pet_id}), 200


@admin_blueprint.route('/pet/<int:pet_id>', methods=['DELETE'])
@admin_only
def delete_pet(pet_id):
    """
    Controls management's ability to delete existing pet listings.
    ---
    tags:
      - Admin
    parameters:
      - in: path
        name: pet_id
        schema:
          type: integer
        required: true
    responses:
      200:
        description: Pet deleted
      401:
        description: Unauthorized
    """

    database = open_database()
    # note the comma so sqlite gets its one-element tuple
    # it does not like if you do not have the comma (trust me)
    database.execute("DELETE FROM pets WHERE id = ?", (pet_id,))
    database.commit()

    return jsonify({"message": "Pet listing deleted",
                    "pet_id": pet_id}), 200


@admin_blueprint.route('/applications', methods=['GET'])
@admin_only
def view_applications():
    """
    Grabs list of all currently submitted pet applications.
    ---
    tags:
      - Admin
    responses:
      200:
        description: JSON with “applications” array
      401:
        description: Unauthorized
    """

    database = open_database()
    # same dict row trick as earlier
    applications = [dict(row) for row in database.execute("SELECT * FROM applications").fetchall()]

    return jsonify({"applications": applications}), 200


@admin_blueprint.route('/application/<int:app_id>', methods=['PUT'])
@admin_only
def update_application(app_id):
    """
    Allows management to update the status of an application.
    Note how we need to take in the application ID.
    ---
    tags:
      - Admin
    parameters:
      - in: path
        name: app_id
        schema:
          type: integer
        required: true
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [status]
            properties:
              status: { type: string, enum: ['pending','approved','denied'] }
    responses:
      200:
        description: Application updated
      400:
        description: Missing status
      401:
        description: Unauthorized
    """

    data = request.get_json() or {} # if empty
    status = data.get("status")
    if not status:
        return jsonify({"error": "No status :("}), 400

    # db time
    database = open_database()
    database.execute(
        """
        UPDATE applications
            SET status = ?
        WHERE application_id = ?
        """,
        (
            status, app_id)
        )
    database.commit()

    return jsonify({"message": "Application status updated",
                    "application_id": app_id,
                    "status": status}), 200


# a mock to use for our pet_type funcs
# pet_types = ["Dog", "Cat"] gone but not forgotten o7


@admin_blueprint.route('/pettypes', methods=['POST'])
@admin_only
def admin_add_pet_type():
    """ 
    Admin endpoint to add a new pet type.
    Expects a JSON input of { "type": "new_type" }
    ---
    tags:
      - Admin
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [type]
            properties:
              type: { type: string }
    responses:
      201:
        description: Pet type added
      400:
        description: Missing type
      409:
        description: Duplicate type
    """

    data = request.get_json() or {} # if empty
    new_type = data.get("type") # <-- why json input is important
    if not new_type:
        return jsonify({"error": "Missing pet type"}), 400

    # database woot
    database = open_database()
    # we do not want to crete duplicate pet types so we will catch it here
    # with sqlite's integrity error
    try:
        database.execute("INSERT INTO pet_types (type) VALUES (?)", (new_type,))
        database.commit()
    except IntegrityError:
        return jsonify({"error": "Pet type already exists o.o"}), 409

    # same line from dashboard thanks to the almighty row factory
    pet_types = [row["type"] for row in database.execute("SELECT type FROM pet_types").fetchall()]
    return jsonify({"message": "Added pet type",
                    "pet_types": pet_types}), 201



@admin_blueprint.route('/pettypes/<string:pet_type>', methods=['DELETE'])
@admin_only
def admin_delete_pet_type(pet_type):
    """
    Admin endpoint to delete an existing pet type.
    ---
    tags:
      - Admin
    parameters:
      - in: path
        name: pet_type
        schema:
          type: string
        required: true
    responses:
      200:
        description: Pet type deleted
      404:
        description: Not found
      401:
        description: Unauthorized
    """

    database = open_database()
    cursor = database.execute("DELETE FROM pet_types WHERE type = ?", (pet_type,))
    database.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": "Pet type does not exist"}), 404
    pet_types = [row["type"] for row in database.execute("SELECT type FROM pet_types").fetchall()]

    return jsonify({"message": "Pet type deleted",
                    "pet_types": pet_types}), 200
