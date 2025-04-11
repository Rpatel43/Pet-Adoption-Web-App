"""Contains all endpoints related to pet search and application process
that will be accessed by non-administrative users."""
from flask import Blueprint, request, jsonify

# blueprint for main
pets_blueprint = Blueprint('pets', __name__)

@pets_blueprint.route('/pets', methods=['GET'])
def get_pets():
    """function that controls the web-apps gathering of the list of pets,
    filtered or unfiltered based on user request."""

    # default to no pet type selected
    pet_type = request.args.get('type', None)

    # Stub - return a mock list of pets, filtering by type if provided
    pets_list = [
        {"id": 1, "name": "Dakota", "type": "Dog"},
        {"id": 2, "name": "Sylvester", "type": "Cat"}
    ]
    # if the user wants a specific type of pet, filter and return pets of
    # that tpye. Otherwise, return ALL pets.
    if pet_type:
        filtered = [pet for pet in pets_list if pet['type'] == pet_type]
        return jsonify({"pets": filtered}), 200
    return jsonify({"pets": pets_list}), 200

@pets_blueprint.route('/pet/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    """Function that uses petid to route and gather ALL relevant
    information that will be displayed on a pets profile page.
    Note how we track petid for routing."""

    # Stub - return mock details for a pet
    pet = {
        "id": pet_id,
        "name": "Winston",
        "type": "Cat",
        "sex": "M",
        "bio": "Very friendly cat.",
        "health_info": "Healthy/Vaccinated",
        "size": "Small",
        "weight": "12lbs"
    }
    return jsonify({"pet": pet}), 200

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
