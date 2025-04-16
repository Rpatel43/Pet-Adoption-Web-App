"""Test file for this iteration of stub/mock API. Includes tests for all possible
code outcomes out of admin.py, pets.py, and user.py."""
# pylint: disable=W0621
import pytest
from backend.main import build_app


@pytest.fixture
def test_client():
    """Creates client for testing purposes."""
    app = build_app()
    app.config['TESTING'] = True
    # Ensure that each test gets its own fresh client,
    # and global state (e.g., pet_types in admin/pets) is not shared.
    with app.test_client() as this_client:
        yield this_client


#############################
# admin.py endpoint tests :)
#############################


@pytest.mark.parametrize("payload, status, expected_key, expected_value", [
    ({"username": "admin", "password": "admin123"}, 200, "message", "Admin login success"),
    ({"username": "bad", "password": "creds"}, 401, "error", "Invalid admin login")
])
def test_admin_signin(test_client, payload, status, expected_key, expected_value):
    """Test code properly responds to both successful admin sign in and bad sign in."""

    response = test_client.post('/api/admin/signin', json=payload)
    data = response.get_json()
    value = data.get(expected_key, "")

    # check for correct status code
    assert response.status_code == status

    # check we get correct expected dict key
    assert expected_key in data

    # check that message or error contains expected response value
    assert expected_value in value


def test_admin_dashboard(test_client):
    """Tests that admin dashboard contains all expected data, including prebuilt Dog and Cat."""

    response = test_client.get('/api/admin/dashboard')
    dashboard = response.get_json().get("dashboard", {})

    # check status code
    assert response.status_code == 200

    # Assure that pet listings and applications are lists
    # and assure that the dashboard pet types contain dogs and cats
    # without any influence.
    assert isinstance(dashboard.get("pet_listings"), list)
    assert isinstance(dashboard.get("applications"), list)
    assert dashboard.get("pet_types") == ["Dog", "Cat"]


@pytest.mark.parametrize("endpoint, payload, status, expected_key", [
    ('/api/admin/pet', {"name": "Bella", "type": "Dog", "sex": "F", "bio": "Friendly pet",
                        "health_info": "healthy", "size": "Small", "weight": "20lbs",
                        "status": "Available", "picture": "bella.png"}, 201, "message"),
    ('/api/admin/pet', {}, 400, "error")
])
def test_admin_add_pet(test_client, endpoint, payload, status, expected_key):
    """
    Tests that admin add pet works as intended when 1. all info provided
    2. not all fields provided
    """

    response = test_client.post(endpoint, json=payload)
    data = response.get_json()

    # assert correct status code
    assert response.status_code == status

    # make sure we get proper message or error key depending on if valid add pet
    assert expected_key in data


@pytest.mark.parametrize("pet_id, payload, status, expected_key", [
    (1, {"name": "Shiny new name"}, 200, "message"),
    (1, {}, 400, "error")
])
def test_admin_edit_pet(test_client, pet_id, payload, status, expected_key):
    """
    Tests that admin pet edit works as intended when 1. we actually edit pet info
    2. provide no new edits
    """
    # note how we call route with pet id
    response = test_client.put(f'/api/admin/pet/{pet_id}', json=payload)
    data = response.get_json()

    # status code check
    assert response.status_code == status

    # assert message / error
    assert expected_key in data


def test_admin_delete_pet(test_client):
    """Tests that we successfully delete a pet listing when provide an ID"""

    # just define it locally
    pet_id = 1
    # note inclusion of pet id in route
    response = test_client.delete(f'/api/admin/pet/{pet_id}')
    data = response.get_json()

    # status code check
    assert response.status_code == 200

    # note function should contain data of pet id after delete
    assert data.get("pet_id") == pet_id


def test_admin_view_applications(test_client):
    """Asserts that admins get proper data when they go to view applications."""

    response = test_client.get('/api/admin/applications')
    data = response.get_json()

    # status code
    assert response.status_code == 200

    # Check that appilcations are in data AND that its a list
    assert "applications" in data
    assert isinstance(data["applications"], list)


@pytest.mark.parametrize("app_id, payload, status, expected_key", [
    (1, {"status": "approved"}, 200, "message"),
    (1, {}, 400, "error")
])
def test_admin_update_application(test_client, app_id, payload, status, expected_key):
    """
    Tests that when an admin updates an application, it goes through properly
    or fails if not updated properly.
    """

    # note the application id
    response = test_client.put(f'/api/admin/application/{app_id}', json=payload)
    data = response.get_json()

    # check status code
    assert response.status_code == status

    # make sure message or error based on corectness
    assert expected_key in data


@pytest.mark.parametrize("url, payload, status, expected_key", [
    ("/api/admin/pettypes", {"type": "Birds"}, 201, "message"),
    ("/api/admin/pettypes", {}, 400, "error"),
    ("/api/admin/pettypes", {"type": "Dog"}, 409, "error"),
])
def test_admin_pet_type_operations(test_client, url, payload, status, expected_key):
    """Tests that our pet type operations return proper keys and status codes."""

    response = test_client.post(url, json=payload)
    data = response.get_json()

    # make sure there is data
    assert response is not None

    # status code check again wow
    assert response.status_code == status

    # Make sure key works as intended. Note 409 return for repeat
    assert expected_key in data


def test_admin_delete_pet_type_success(test_client):
    """Tests that deleting a pet type works as intended when it goes through."""

    # Delete Cat from default list
    response = test_client.delete('/api/admin/pettypes/Cat')
    data = response.get_json()

    # status code
    assert response.status_code == 200

    # check to make sure we deleted cat (very sad)
    assert "Cat" not in data.get("pet_types", [])


def test_admin_delete_pet_type_failure(test_client):
    """Tests that when we try to delete a non-existent pet type that it doesnt work."""

    response = test_client.delete('/api/admin/pettypes/NonExistent')
    data = response.get_json()

    # 404 does not exist response code
    assert response.status_code == 404

    # check for error key
    assert "error" in data


#############################
# pets.py endpoint tests :D
#############################


def test_get_pets_no_filter(test_client):
    """Tests that the app correctly returns all pets when no filter selected."""

    response = test_client.get('/api/pets')
    data = response.get_json()

    # response code
    assert response.status_code == 200

    # make sure data is present
    assert "pets" in data

    # make sure all pets present (only have two rn)
    assert len(data["pets"]) == 2


def test_get_pets_filter(test_client):
    """tests that pet filter data is properly fetched"""

    # note how we have filtered by dogs
    response = test_client.get('/api/pets?type=dog')
    data = response.get_json()

    # status code check
    assert response.status_code == 200

    # check data present
    assert "pets" in data

    # check that pet filter works as intended
    for pet in data["pets"]:
        assert pet["type"] == "dog"


def test_get_pet(test_client):
    """Checks that API correctly fetches pet data by ID"""

    # note petid and its route
    pet_id = 1
    response = test_client.get(f'/api/pet/{pet_id}')
    data = response.get_json()

    # status code
    assert response.status_code == 200

    # assert data
    assert "pet" in data

    # make sure data is gathered right by pet and id
    assert data["pet"]["id"] == pet_id

    # Check to make sure pet image works as intended
    pet = data["pet"]
    assert "picture" in pet
    assert isinstance(pet["picture"], str)
    assert pet["picture"] != ""


@pytest.mark.parametrize("payload, status, expected_key", [
    ({"pet_id": 1, "applicant": "User123", "comments": "I love this pet"}, 201, "message"),
    ({}, 400, "error")
])
def test_submit_user_application(test_client, payload, status, expected_key):
    """Tests that a user application is correctly submitted with some sample data."""

    # note pet ID in route
    pet_id = 1
    response = test_client.post(f'/api/pet/{pet_id}/application', json=payload)
    data = response.get_json()

    # check status code
    assert response.status_code == status

    # Make sure message is there
    assert expected_key in data


def test_get_pet_types(test_client):
    """Check that pet types are fetched with correct data"""

    response = test_client.get('/api/pettypes')
    data = response.get_json()

    # status code
    assert response.status_code == 200

    # check pet types are present and the data is Dog and Cat
    assert "pet_types" in data
    assert data["pet_types"] == ["Dog", "Cat"]


# -----------------------------------------------------------------------------
# USER ENDPOINTS TESTS (user.py)
# -----------------------------------------------------------------------------


@pytest.mark.parametrize("payload, status, key, text", [
    ({"username": "testuser", "password": "testpass"}, 200, "message", "User login successful!"),
    ({}, 400, "error", "")
])
def test_user_signin(test_client, payload, status, key, text):
    """Tests that user sign in is verified/rejected."""

    response = test_client.post('/api/signin', json=payload)
    data = response.get_json()

    # status code
    assert response.status_code == status

    # Check that sign in is correct and passes reqs
    assert key in data
    if text:
        assert text in data[key]


@pytest.mark.parametrize("payload, status, key", [
    (
        {"first_name": "Test", "last_name": "User", "username": "newuser",
         "password": "strongpassword", "password_conf": "strongpassword"},
        201, "message"
    ),
    (
        {"last_name": "User", "username": "newuser", "password": "strongpassword",
         "password_conf": "strongpassword"},
        400, "error"
    ),
    (
        {"first_name": "Test", "last_name": "User", "username": "newuser",
         "password": "strongpassword", "password_conf": "differentpassword"},
        400, "error"
    ),
    (
        {"first_name": "Test", "last_name": "User", "username": "ab",
         "password": "strongpassword", "password_conf": "strongpassword"},
        400, "error"
    ),
    (
        {"first_name": "Test", "last_name": "User", "username": "validusername",
         "password": "short", "password_conf": "short"},
        400, "error"
    ),
])
def test_user_signup(test_client, payload, status, key):
    """Checks all facets of user signup to make sure correct result
    is returned if nnot all criteria met."""

    response = test_client.post('/api/signup', json=payload)
    data = response.get_json()

    # status code
    assert response.status_code == status

    # assert proper return
    assert key in data


def test_user_signout(test_client):
    """Ensures user signout goes through as expected."""
    response = test_client.get('/api/signout')
    data = response.get_json()

    assert response.status_code == 200

    assert "message" in data
    assert "signed out" in data["message"]


def test_user_applications(test_client):
    """Ensures user application fetches pending applications and data"""

    response = test_client.get('/api/applications')
    data = response.get_json()

    # status code
    assert response.status_code == 200

    # Ensure applications in list and that the data is in list format
    assert "applications" in data
    assert isinstance(data["applications"], list)
