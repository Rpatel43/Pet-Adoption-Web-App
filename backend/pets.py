"""Contains all endpoints related to pet search and application process
that will be accessed by non-administrative users."""
# pylint: disable=E0611
from sqlite3 import Error
from flask import Blueprint, request, jsonify, session
from backend.database import open_database
from backend.user import user_only

# blueprint for main
pets_blueprint = Blueprint('pets', __name__)

@pets_blueprint.route('/pets', methods=['GET'])
def get_pets():
    """
    function that controls the web-apps gathering of the list of pets,
    filtered or unfiltered based on user request.
    ---
    tags:
      - Pets
    parameters:
      - in: query
        name: type
        schema:
          type: string
        description: Filter by pet type
    responses:
      200:
        description: JSON object with \"pets\" array
        content:
          application/json:
            schema:
              type: object
              properties:
                pets:
                  type: array
                  items:
                    $ref: '#/components/schemas/Pet'
      500:
        description: Database error
    """

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
    """
    Function that uses petid to route and gather ALL relevant
    information that will be displayed on a pets profile page.
    Note how we track petid for routing.
    ---
    tags:
      - Pets
    parameters:
      - in: path
        name: pet_id
        schema:
          type: integer
        required: true
        description: ID of the pet
    responses:
      200:
        description: A single pet object
        content:
          application/json:
            schema:
              type: object
              properties:
                pet:
                  $ref: '#/components/schemas/Pet'
      404:
        description: Pet not found
      500:
        description: Database error
    """

    database = open_database()
    row = database.execute(
        "SELECT * FROM pets WHERE id = ?", (pet_id,)
    ).fetchone()

    if not row:
        return jsonify({"error": "Pet listing not found"}), 404
    # return dict of row for data formatting
    return jsonify({"pet": dict(row)}), 200

@pets_blueprint.route('/pet/<int:pet_id>/application', methods=['POST'])
@user_only
def submit_user_application(pet_id):
    """
    Checks that the user submitted an application that contains
    data in all fields. Return message if True else error.
    Note how we track petid for routing.
    ---
    tags:
      - Applications
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
            required:
              - application_response
            properties:
              application_response:
                type: string
                description: \"Why you’d make a great owner\"
    responses:
      201:
        description: Application created
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                application_id:
                  type: integer
      400:
        description: Missing application_response
      401:
        description: Unauthorized
      500:
        description: Database error
    """

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
    """
    Returns list of pet types. This is going to be used
    for the dropdown menu we create for the user to filter by
    animal type.
    ---
    tags:
      - Pets
    responses:
      200:
        description: JSON object with \"pet_types\" array
        content:
          application/json:
            schema:
              type: object
              properties:
                pet_types:
                  type: array
                  items:
                    type: string
      500:
        description: Database error
    """

    database = open_database()
    # try-exc again
    try:
        cursor = database.execute("SELECT type FROM pet_types")
        pet_types = [row["type"] for row in cursor.fetchall()]
    except Error as err:
        return jsonify({"error": f"db error: {err}"}), 500
    return jsonify({"pet_types": pet_types}), 200
