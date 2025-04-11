"""File that controls all enpoints for everything related to the admin
portal and beyond, from signing in to managing applications."""
from flask import Blueprint, request, jsonify

# blueprint for main
admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/signin', methods=['POST'])
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
def add_pet():
    """Controls management's abiltiy to add new pet listings."""

    data = request.get_json()
    data_fields = ['name', 'type', 'sex', 'bio', 'health_info', 'size', 'weight']
    is_missing = [field for field in data_fields if field not in data or not data[field]]
    if is_missing:
        return jsonify({"error": f"Missing fields: {', '.join(is_missing)}"}), 400
    # Stub - add a new pet listing
    return jsonify({"message": "Pet added", "pet": data}), 201


@admin_blueprint.route('/pet/<int:pet_id>', methods=['PUT'])
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
def delete_pet(pet_id):
    """Controls management's ability to delete existing pet listings."""
    # Stub - delete a pet listing
    # more to come when Db is put in
    return jsonify({"message": "Pet deleted", "pet_id": pet_id}), 200


@admin_blueprint.route('/applications', methods=['GET'])
def view_applications():
    """Grabs list of all currently submitted pet applications."""

    # Stub - return a list of all submitted applications
    applications = []
    return jsonify({"applications": applications}), 200


@admin_blueprint.route('/application/<int:app_id>', methods=['PUT'])
def update_application(app_id):
    """Allows management to update the status of an application.
    Note how we need to take in the application ID."""

    data = request.get_json()

    # Stub - update the status of an application (approve or reject)
    if data:
        return jsonify({"message": "Application updated",
                        "application_id": app_id, 
                        "status": data.get("status")}), 200
    return jsonify({"error": "Invalid data"}), 400


# a mock to use for our pet_type funcs
pet_types = ["Dog", "Cat"]


@admin_blueprint.route('/pettypes', methods=['POST'])
def admin_add_pet_type():
    """ Admin endpoint to add a new pet type.
    Expects a JSON input of { "type": "new_type" }"""

    data = request.get_json()
    new_type = data.get("type") # <-- why json input is important

    # Stub - test adding a new type
    if not new_type:
        return jsonify({"error": "Missing pet type"}), 400
    if new_type.lower() in (pet_type.lower() for pet_type in pet_types):
        return jsonify({"error": "That pet type exists already!"}), 409
    pet_types.append(new_type)
    return jsonify({"message": "Pet type added",
                    "pet_types": pet_types}), 201


@admin_blueprint.route('/pettypes/<string:pet_type>', methods=['DELETE'])
def admin_delete_pet_type(pet_type):
    """Admin endpoint to delete an existing pet type."""

    # Stub - Attmept removal of pet type
    if pet_type not in pet_types:
        return jsonify({"error": "Pet type not found"}), 404
    pet_types.remove(pet_type)
    return jsonify({"message": "Pet type deleted", "pet_types": pet_types}), 200
