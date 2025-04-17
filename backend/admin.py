rayna
rspiky_
Online



Group DM


Search

chat
March 12, 2025

Clouds — 3/12/2025 5:34 PM
Id say we each want to do
1 persona
1 scenario for said persona
3 user stories each (can be for any or multiple personas)
some features we might want

Then we can wrap up the rest in lab and after
March 13, 2025

QT. saoud — 3/13/2025 3:39 PM
sounds good
[3:42 PM]
i am finishing lab 6 in the library and then coming to lab a little late

rayna — 3/13/2025 4:07 PM
i’m also running a bit late

Clouds — 3/13/2025 9:01 PM
Just messaging to let everyone know the milestone is fully complete and submitted

Ronit Patel — 3/13/2025 9:11 PM
Sounds good thanks
March 27, 2025

Clouds — 3/27/2025 10:31 PM
Just submitted the milestone, changed up the figma prototype a bit to include animal profiles so we met all the requirements
April 3, 2025

rayna — 4/3/2025 3:12 PM
just letting you guys know that i won’t be in lab today because im sick. lmk what i should do for the milestone

Clouds — 4/3/2025 3:21 PM
Np, we just have to draw some diagrams so we'll let you know which one you need to do during or after lab
[3:21 PM]
otherwise you can pick which one you want to do now, is also fine
[3:23 PM]
Im going to do the sequence diagrams because theres multiple of those but any of the other ones you just need to do 1 diagram

rayna — 4/3/2025 3:44 PM
ok, thanks

Clouds — 4/3/2025 4:15 PM
You can do the Use Case Diagram. You can either add your completed drawing file to the repo in the docs folder on the feature branch or you can send it to the groupchat and ill put it in for you

rayna — 4/3/2025 7:31 PM
finished the use case diagram. i'll send it here
[7:31 PM]

usecasediagram.drawio
6.24 KB

Ronit Patel — 4/3/2025 7:44 PM

er-pet-adoption.drawio
19.98 KB

seq-01-login.drawio
3.10 KB

seq-02-application.drawio
3.09 KB

Clouds — 4/3/2025 8:07 PM
Thanks ill get everything in the repo and submit soon

Clouds — 4/3/2025 11:09 PM
Milestone is submitted, just a reminder that next weeks milestone requires us to code up our apps api so we are going to want to get a headstart early next week
April 10, 2025

Clouds — 4/10/2025 2:47 AM
Hey all, sorry for the late message but just wanted to let everyone know what im thinking for this milestone; ive completed about 90% of the mock-based api (besides tests). after going over it and starting some work on it earlier this week I realized its just one of those things that is way easier if one person works on it. im thinking for class tomorrow we give each person a file or two to modify the comments/docstrings to better reflect what they would write and slowly push parts of the file to the repo so everyone gets good credit for this milestone. Ill put the main files in here now so if you want to start doing this pushing before class tomorrow feel free. just let the group know which you are taking so we dont overlap it. ill attach the files to this message (besides tests because ill do that one). Ill also put in the requirements and yml so for now this is all everyone needs to pick from
"""File that controls all enpoints for everything related to the admin
portal and beyond, from signing in to managing applications."""
from flask import Blueprint, request, jsonify

# blueprint for main
admin_blueprint = Blueprint('admin', __name__)
Expand
admin.py
5 KB
"""Main file for API. Handles blueprints and starting the app up."""
from flask import Flask
from user import user_blueprint
from pets import pets_blueprint
from admin import admin_blueprint
Expand
main.py
2 KB
"""Contains all endpoints related to pet search and application process
that will be accessed by non-administrative users."""
from flask import Blueprint, request, jsonify

# blueprint for main
pets_blueprint = Blueprint('pets', __name__)
Expand
pets.py
3 KB
"""User file for API. All calls related to the user are within this file."""
from flask import Blueprint, request, jsonify

# note the blueprint!
user_blueprint = Blueprint('user', __name__)
Expand
user.py
4 KB

Clouds — 4/10/2025 9:12 PM
Could someone approve my merge request please?

Clouds — 4/10/2025 9:58 PM
Milestone is all set, pipeline works and tests work good
April 15, 2025

Clouds — 4/15/2025 8:33 PM
if one or multiple of you have a chance soon, upon up a feature branch off of develop and put 1 or multiple of these into it and submit a pull request to merge with develop. I made some minor changes so the app could handle a picture for the animals. thanks
"""File that controls all enpoints for everything related to the admin
portal and beyond, from signing in to managing applications."""
from flask import Blueprint, request, jsonify

# blueprint for main
admin_blueprint = Blueprint('admin', __name__)
Expand
admin.py
5 KB
"""Contains all endpoints related to pet search and application process
that will be accessed by non-administrative users."""
from flask import Blueprint, request, jsonify

# blueprint for main
pets_blueprint = Blueprint('pets', __name__)
Expand
pets.py
3 KB
"""Test file for this iteration of stub/mock API. Includes tests for all possible
code outcomes out of admin.py, pets.py, and user.py."""
# pylint: disable=W0621
import pytest
from backend.main import build_app
Expand
test_api.py
13 KB
NEW
[8:35 PM]
i also just made a pull request for adding an iter of the db; approve that first and then make your feature branch (edited)
April 17, 2025

QT. saoud — 2:55 PM
is this the milestone for today
NEW
[2:55 PM]
and is there a lab also we have to complete
NEW

Clouds — 2:56 PM
That was some early stuff, i've just about completed the milestone
NEW
[2:56 PM]
Im going to send iterations of files for everyone to submit piece by piece to the github so the progression is there
NEW

QT. saoud — 3:02 PM
okay that sounds good
NEW

Clouds — 3:23 PM
I apologize in advance for this series of messages. I am going to put all of the py file that you guys will submit (the same ones you worked on last milestone). They go from oldest at the top to newest at bottom. Make a feature branch off of DEVELOP for each one (id put a varying amount of time between each push to make it more 'authenitc') and open a PULL REQUEST for merging to develop. Do not put in another file until your previous pull request has been fulfilled by someone else. Feel free to change comments/style, but ensure nothing violates pylint. Easiest way to do thi is to have everyone do it at the same time so we are not waiting for PR approvals.
NEW
[3:23 PM]
Forwarded
adding wrap w/ session
"""File that controls all enpoints for everything related to the admin
portal and beyond, from signing in to managing services."""

from functools import wraps
from flask import Blueprint, request, jsonify, session


# blueprint for main
admin_blueprint = Blueprint('admin', __name__)


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
@admin_only
def admin_signin():
    """Manages admin sign in, ensuring login matches some currently hard
    coded login information."""

    data = request.get_json()
    admin_username = data.get('username')
    admin_password = data.get('password')

    # Stub - check admin login info
    # for now we use hard coded results until we can
    # put admin login data in its own table in db
    if admin_username == "admin" and admin_password == "admin123":
        return jsonify({"message": "Admin login success", "admin": admin_username}), 200
    return jsonify({"error": "Invalid admin login"}), 401


@admin_blueprint.route('/dashboard', methods=['GET'])
@admin_only
def admin_dashboard():
    """Contains all neccessary data that the admin may or may not
    need access to when using the management portal."""

    # Stub - return fake dashboard data
    # note we include pet types but we may not need it here;
    # not really sure so just throwing it in with its default values
    dashboard_data = {
        "pet_listings": [],
        "applications": [],
        "pet_types": ["Dog", "Cat"]
    }
    return jsonify({"dashboard": dashboard_data}), 200


@admin_blueprint.route('/pet', methods=['POST'])
@admin_only
def add_pet():
    """Controls management's abiltiy to add new pet listings."""

    data = request.get_json()
    data_fields = ['name', 'type', 'sex', 'bio', 'health_info', 'size', 'weight', 'picture']
    is_missing = [field for field in data_fields if field not in data or not data[field]]
    if is_missing:
        return jsonify({"error": f"Missing fields: {', '.join(is_missing)}"}), 400
    # Stub - add a new pet listing
    return jsonify({"message": "Pet added", "pet": data}), 201


@admin_blueprint.route('/pet/<int:pet_id>', methods=['PUT'])
@admin_only
def edit_pet(pet_id):
    """Controls management's ability to edit an existing pet listing."""

    data = request.get_json()

    # Stub - edit an existing pet listing
    # note 'data' will be fleshed out to include every bit of info for
    # pet profile after we include DB
    if data:
        return jsonify({"message": "Pet updated", "pet_id": pet_id, "updates": data}), 200
    return jsonify({"error": "Invalid update data"}), 400


@admin_blueprint.route('/pet/<int:pet_id>', methods=['DELETE'])
@admin_only
def delete_pet(pet_id):
    """Controls management's ability to delete existing pet listings."""
    # Stub - delete a pet listing
    # more to come when Db is put in
    return jsonify({"message": "Pet deleted", "pet_id": pet_id}), 200


@admin_blueprint.route('/applications', methods=['GET'])
... (59 lines left)
Collapse
admin.py
6 KB
NEW
[3:23 PM]
Forwarded
directory for pet photos
"""File that controls all enpoints for everything related to the admin
portal and beyond, from signing in to managing services."""
import os
from functools import wraps
from flask import Blueprint, request, jsonify, current_app, session
Expand
admin.py
6 KB
NEW
[3:23 PM]
Forwarded
some db functionality for signin and session for login check AND signout
"""File that controls all enpoints for everything related to the admin
portal and beyond, from signing in to managing services."""
import os
from functools import wraps
from flask import Blueprint, request, jsonify, current_app, session
from .database import open_database
Expand
admin.py
7 KB
NEW
[3:23 PM]
Forwarded
finished iteration of admin
"""File that controls all enpoints for everything related to the admin
portal and beyond, from signing in to managing services."""
import os
from sqlite3 import IntegrityError
from functools import wraps
from flask import Blueprint, request, jsonify, current_app, session, url_for
Expand
admin.py
11 KB
NEW
[3:24 PM]
Forwarded
signup database integration
"""User file for API. All calls related to the user are within this file."""
from sqlite3 import IntegrityError
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from .database import open_database
Expand
user.py
5 KB
NEW
[3:24 PM]
Forwarded
login functionallity implemented
"""User file for API. All calls related to the user are within this file."""
from sqlite3 import IntegrityError
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from .database import open_database
Expand
user.py
5 KB
NEW
[3:24 PM]
Forwarded
finished implementing functions
"""User file for API. All calls related to the user are within this file."""
from sqlite3 import IntegrityError
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from .database import open_database
Expand
user.py
5 KB
NEW
[3:24 PM]
Forwarded
Added wrap for login detection for certain features
"""User file for API. All calls related to the user are within this file."""
from sqlite3 import IntegrityError
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from .database import open_database
Expand
user.py
5 KB
NEW
[3:24 PM]
Forwarded
add session api enpoint to check login status
"""User file for API. All calls related to the user are within this file."""
from sqlite3 import IntegrityError
from functools import wraps
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from .database import open_database
Expand
user.py
6 KB
NEW
[3:25 PM]
Forwarded
pets get pets and get pet
"""Contains all endpoints related to pet search and application process
that will be accessed by non-administrative users."""
from sqlite3 import Error
from flask import Blueprint, request, jsonify
from .database import open_database

# blueprint for main
pets_blueprint = Blueprint('pets', __name__)

@pets_blueprint.route('/pets', methods=['GET'])
def get_pets():
    """function that controls the web-apps gathering of the list of pets,
    filtered or unfiltered based on user request."""

    # default to no pet type selected
    pet_type = request.args.get('type')

    database = open_database()
    # apply filter by checking for pet_type
    try:
        if pet_type:
            cursor = database.execute("SELECT * FROM pets WHERE type = ?", (pet_type,))
        else:
            cursor = database.execute("SELECT * FROM pets")
        # dict form
        pets = [dict(row) for row in cursor.fetchall()]
    except Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    return jsonify({"pets": pets}), 200

@pets_blueprint.route('/pet/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    """Function that uses petid to route and gather ALL relevant
    information that will be displayed on a pets profile page.
    Note how we track petid for routing."""

    database = open_database()
    row = database.execute(
        "SELECT * FROM pets WHERE id = ?", (pet_id,)
    ).fetchone()

    if not row:
        return jsonify({"error": "Pet listing not found"}), 404
    # return dict of row for data formatting
    return jsonify({"pet": dict(row)}), 200

@pets_blueprint.route('/pet/<int:pet_id>/application', methods=['POST'])
def submit_user_application(pet_id):
    """Checks that the user submitted an application that contains
    data in all fields. Return message if True else error.
    Note how we track petid for routing."""

    data = request.get_json()

    # Stub - accept and record a pet adoption application IF all fields complete
    if not data or "pet_id" not in data:
        return jsonify({"error": "Invalid application data"}), 400
    return jsonify({"message": "Application submitted",
                    "application": data,
                    "pet_id_received": pet_id}), 201

# define pet initial types for method use
pet_types = ['Dog', 'Cat']

@pets_blueprint.route("/pettypes", methods=['GET'])
def get_pet_types():
    """Returns list of pet types. This is going to be used
    for the dropdown menu we create for the user to filter by
    animal type."""
    return jsonify({"pet_types": pet_types}), 200
Collapse
pets.py
3 KB
NEW
[3:25 PM]
Forwarded
all funcs implemented
"""Contains all endpoints related to pet search and application process
that will be accessed by non-administrative users."""
from sqlite3 import Error
from flask import Blueprint, request, jsonify, session
from .database import open_database

# blueprint for main
pets_blueprint = Blueprint('pets', __name__)

@pets_blueprint.route('/pets', methods=['GET'])
def get_pets():
    """function that controls the web-apps gathering of the list of pets,
    filtered or unfiltered based on user request."""

    # default to no pet type selected
    pet_type = request.args.get('type')

    database = open_database()
    # apply filter by checking for pet_type
    try:
        if pet_type:
            cursor = database.execute("SELECT * FROM pets WHERE type = ?", (pet_type,))
        else:
            cursor = database.execute("SELECT * FROM pets")
        # dict form
        pets = [dict(row) for row in cursor.fetchall()]
    except Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    return jsonify({"pets": pets}), 200

@pets_blueprint.route('/pet/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    """Function that uses petid to route and gather ALL relevant
    information that will be displayed on a pets profile page.
    Note how we track petid for routing."""

    database = open_database()
    row = database.execute(
        "SELECT * FROM pets WHERE id = ?", (pet_id,)
    ).fetchone()

    if not row:
        return jsonify({"error": "Pet listing not found"}), 404
    # return dict of row for data formatting
    return jsonify({"pet": dict(row)}), 200

@pets_blueprint.route('/pet/<int:pet_id>/application', methods=['POST'])
def submit_user_application(pet_id):
    """Checks that the user submitted an application that contains
    data in all fields. Return message if True else error.
    Note how we track petid for routing."""

    data = request.get_json()

    submission = data.get("application_response")
    if not submission:
        return jsonify({"error": "No app. response submitted"}), 400
    user_id = session.get("user_id")

    # DB
    database = open_database()
    # try-exc in case cursor/commit fails
    try:
        cursor = database.execute(
            """INSERT INTO applications
            (user_id, pet_id, status, application_response)
            VALUES (?, ?, 'pending', ?)""",
            (user_id, pet_id, submission)
        )
        database.commit()
    except Error as err:
        return jsonify({"error": f"database error: {err}"}), 500
    return jsonify({
        "message": "application submitted",
        "application_id": cursor.lastrowid
    }), 201

# define pet initial types for method use
# pet_types = ['Dog', 'Cat'] retired

@pets_blueprint.route("/pettypes", methods=['GET'])
def get_pet_types():
    """Returns list of pet types. This is going to be used
    for the dropdown menu we create for the user to filter by
    animal type."""

    database = open_database()
    # try-exc again
    try:
        cursor = database.execute("SELECT type FROM pet_types")
        pet_types = [row["type"] for row in cursor.fetchall()]
    except Error as err:
        return jsonify({"error": f"db error: {err}"}), 500
    return jsonify({"pet_types": pet_types}), 200
Collapse
pets.py
4 KB
NEW
[3:25 PM]
Forwarded
add wrapper from user
"""Contains all endpoints related to pet search and application process
that will be accessed by non-administrative users."""
from sqlite3 import Error
from flask import Blueprint, request, jsonify, session
from .database import open_database
from .user import user_only
Expand
pets.py
4 KB
NEW
[3:25 PM]
Forwarded
add swagger to pets
"""Contains all endpoints related to pet search and application process
that will be accessed by non-administrative users."""
from sqlite3 import Error
from flask import Blueprint, request, jsonify, session
from .database import open_database
from .user import user_only
Expand
pets.py
6 KB
[3:25 PM]
Forwarded
add swagger to admin
"""File that controls all enpoints for everything related to the admin
portal and beyond, from signing in to managing services."""
import os
from sqlite3 import IntegrityError
from functools import wraps
from flask import Blueprint, request, jsonify, current_app, session, url_for
Expand
admin.py
15 KB
[3:25 PM]
Forwarded
add swagger to user
"""User file for API. All calls related to the user are within this file."""
from sqlite3 import IntegrityError
from functools import wraps
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from .database import open_database
Expand
user.py
8 KB
[3:26 PM]
Forwarded
final iterations of each primary py file
"""File that controls all enpoints for everything related to the admin
portal and beyond, from signing in to managing services."""
import os
from sqlite3 import IntegrityError
from functools import wraps
from flask import Blueprint, request, jsonify, current_app, session, url_for
Expand
admin.py
15 KB
"""Contains all endpoints related to pet search and application process
that will be accessed by non-administrative users."""
from sqlite3 import Error
from flask import Blueprint, request, jsonify, session
from backend.database import open_database
from backend.user import user_only
Expand
pets.py
6 KB
"""User file for API. All calls related to the user are within this file."""
from sqlite3 import IntegrityError
from functools import wraps
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database import open_database
Expand
user.py
8 KB
NEW
[3:27 PM]
This final iterations chunk is what should be in the repo at the end of the day
NEW
[3:27 PM]
For your guys' files. I will take care of the other files and pushing them. Make sure to put these files in "backend" folder
NEW

Clouds
I apologize in advance for this series of messages. I am going to put all of the py file that you guys will submit (the same ones you worked on last milestone). They go from oldest at the top to newest at bottom. Make a feature branch off of DEVELOP for each one (id put a varying amount of time between each push to make it more 'authenitc') and open a PULL REQUEST for merging to develop. Do not put in another file until your previous pull request has been fulfilled by someone else. Feel free to change comments/style, but ensure nothing violates pylint. Easiest way to do thi is to have everyone do it at the same time so we are not waiting for PR approvals.

Clouds — 3:28 PM
Please read this before doing anything with these files
NEW

QT. saoud — 4:03 PM
i am pretty sure i just did first one (edited)
NEW
[4:04 PM]
i need sm to do the pull
NEW


Message Clouds, Ronit Patel, QT. saoud
﻿



to select
;
"""File that controls all enpoints for everything related to the admin
portal and beyond, from signing in to managing services."""
import os
from sqlite3 import IntegrityError
from functools import wraps
from flask import Blueprint, request, jsonify, current_app, session, url_for
from werkzeug.utils import secure_filename
from .database import open_database

# blueprint for main
admin_blueprint = Blueprint('admin', __name__)

# Create folder for uploading pet photots
# root/static/uploads/ = path made with os
PET_PHOTO_DIRECTORY = os.path.join(current_app.root_path, 'static', 'uploads')
os.makedirs(PET_PHOTO_DIRECTORY, exist_ok=True) # exist_ok prevents error call in case
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
    """Manages admin sign in, ensuring login matches some currently hard
    coded login information."""

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
    """Sign out the logged in admin user with a session clear."""
    session.pop('admin_user', None)
    return jsonify({'message': 'Admin signed out'}), 200



@admin_blueprint.route('/dashboard', methods=['GET'])
@admin_only
def admin_dashboard():
    """Returns all pet listings, applications, and pet types from our new fancy database o.o"""

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
    """Controls management's abiltiy to add new pet listings."""

    # first make sure the data fields are present in the form
    data_fields = ['name', 'type', 'sex', 'bio', 'health_info', 'size', 'weight', 'status']
    for field in data_fields:
        if not request.form.get(field):
            return jsonify({"error": f"missing data field: {field}"}), 400

    # then we validate the image and save it to our directory
    if "picture" not in request.files:
        return jsonify({"error": "No picture uploaded :L"}), 400
    picture = request.files['picture'] # grab the picture data

    # use secure filename for safety and convenience features
    filename = secure_filename(picture.filename)

    # put photo in directory
    file_desination = os.path.join(PET_PHOTO_DIRECTORY, filename)
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
    """Controls management's ability to edit an existing pet listing."""

    # Data grab and verify all fields present on edit
    data = request.get_json() or {} # if there is somehow an empty pet listing
    required_fields = ["name", "type", "sex", "bio", "health_info",
                       "size", "weight", "status", "picture"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"missing field(s): {", ".join(missing_fields)}"}), 400

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
    """Controls management's ability to delete existing pet listings."""

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
    """Grabs list of all currently submitted pet applications."""

    database = open_database()
    # same dict row trick as earlier
    applications = [dict(row) for row in database.execute("SELECT * FROM applications").fetchall()]

    return jsonify({"applications": applications}), 200


@admin_blueprint.route('/application/<int:app_id>', methods=['PUT'])
@admin_only
def update_application(app_id):
    """Allows management to update the status of an application.
    Note how we need to take in the application ID."""

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
    """ Admin endpoint to add a new pet type.
    Expects a JSON input of { "type": "new_type" }"""

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
    """Admin endpoint to delete an existing pet type."""

    database = open_database()
    cursor = database.execute("DELETE FROM pet_types WHERE type = ?", (pet_type,))
    database.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": "Pet type does not exist"}), 404
    pet_types = [row["type"] for row in database.execute("SELECT type FROM pet_types").fetchall()]

    return jsonify({"message": "Pet type deleted",
                    "pet_types": pet_types}), 200