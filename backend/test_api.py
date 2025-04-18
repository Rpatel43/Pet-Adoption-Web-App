"""Test suite for the pet adoption API (Human-AI collaborative)."""
# pylint: disable=W0621
import io
import pytest
from flask import url_for # pylint: disable=W0611
from backend.main import build_app
from backend.database import init_database, open_database

@pytest.fixture
def test_client(tmp_path):
    """Initialize app, fresh database, and seed basic data."""

    # create new db file
    db_file = tmp_path / "test.db"

    app = build_app()
    app.config['TESTING']  = True
    app.config['DATABASE'] = str(db_file)

    with app.app_context():

        init_database()
        db = open_database()
        db.execute(
            """INSERT INTO pets
               (name, type, sex, bio, health_info, size, weight, status, picture)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ("Dakota", "Dog", "F", "Friendly dog", "Healthy", "Medium", "20lbs", "Available", "")
        )
        db.execute(
            """INSERT INTO pets
               (name, type, sex, bio, health_info, size, weight, status, picture)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ("Sylvester", "Cat", "M", "Playful cat", "Healthy", "Small", "12lbs", "Available", "")
        )
        db.commit()

    with app.test_client() as client:
        yield client

##################
# Admin enpoints #
##################

def test_admin_dashboard_requires_auth(test_client):
    """Ensure /dashboard is protected before login."""
    resp = test_client.get('/api/admin/dashboard')
    assert resp.status_code == 401
    assert 'error' in resp.get_json()

@pytest.mark.parametrize("payload,status", [
    ({'username': 'admin', 'password': 'admin123'}, 200),
    ({'username': 'admin'}, 400),
    ({}, 400)
])
def test_admin_signin_validations(test_client, payload, status):
    """Cover signin success, missing fields, and invalid credentials."""
    resp = test_client.post('/api/admin/signin', json=payload)
    assert resp.status_code == status
    data = resp.get_json()
    if status == 200:
        assert data.get('message', '').startswith('Admin')
    else:
        assert 'error' in data

def test_admin_add_pet_edge_cases(test_client):
    """Test file upload endpoint with edge cases."""
    # not logged in
    data = {'name': 'B', 'type': 'Dog', 'sex': 'F', 'bio': 'x',
            'health_info': 'h', 'size': 'S', 'weight': '5lbs', 'status': 'A'}
    dummy = (io.BytesIO(b''), '')
    resp = test_client.post('/api/admin/pet',
                            data={**data, 'picture': dummy},
                            content_type='multipart/form-data')
    assert resp.status_code == 401
    # login and missing picture
    test_client.post('/api/admin/signin',
                     json={'username': 'admin', 'password': 'admin123'})
    resp2 = test_client.post('/api/admin/pet',
                             data=data,
                             content_type='multipart/form-data')
    assert resp2.status_code == 400

#################
# Pet endpoints #
#################
def test_get_pets_and_filters(test_client):
    """Verify pets listing and filter behavior."""
    # No filter returns two
    resp = test_client.get('/api/pets')
    data = resp.get_json()
    assert resp.status_code == 200
    assert len(data['pets']) == 2
    # Non-existent type -> empty list
    resp2 = test_client.get('/api/pets?type=Bird')
    assert resp2.status_code == 200
    data2 = resp2.get_json()
    assert isinstance(data2['pets'], list) and len(data2['pets']) == 0

def test_get_pet_not_found(test_client):
    """Fetch a non-existent pet should 404."""
    resp = test_client.get('/api/pet/999')
    assert resp.status_code == 404
    assert 'error' in resp.get_json()

##################
# User endpoints #
##################

def test_user_signup_and_login_flow(test_client):
    """End-to-end signup, session, and logout."""
    signup = {'first_name': 'A', 'last_name': 'B',
              'username': 'userX', 'password': 'pass1234', 'password_conf': 'pass1234'}
    r1 = test_client.post('/api/signup', json=signup)
    assert r1.status_code == 201
    # Duplicate username
    r1b = test_client.post('/api/signup', json=signup)
    assert r1b.status_code == 409
    # Short password
    bad = signup.copy()
    bad['password'] = bad['password_conf'] = 'short'
    r2 = test_client.post('/api/signup', json=bad)
    assert r2.status_code == 400
    # Login
    r3 = test_client.post('/api/signin', json={'username': 'userX', 'password': 'pass1234'})
    assert r3.status_code == 200
    # Check session
    r4 = test_client.get('/api/session')
    assert r4.get_json()['user']['username'] == 'userX'
    # Logout
    r5 = test_client.post('/api/signout')
    assert r5.status_code == 200
    # Now session is None
    r6 = test_client.get('/api/session')
    assert r6.get_json()['user'] is None

def test_application_without_login(test_client):
    """Ensure user cannot apply when not signed in."""
    resp = test_client.post('/api/pet/1/application', json={'application_response': 'hi'})
    assert resp.status_code == 401

@pytest.mark.usefixtures('test_client')
def test_valid_application_submission(test_client):
    """After login, application submission should succeed."""
    signup = {'first_name': 'C', 'last_name': 'D', 'username':
              'userY', 'password': 'pass5678', 'password_conf': 'pass5678'}
    test_client.post('/api/signup', json=signup)
    test_client.post('/api/signin', json={'username': 'userY', 'password': 'pass5678'})
    resp = test_client.post('/api/pet/1/application',
                            json={'application_response': 'I care deeply'})
    data = resp.get_json()
    assert resp.status_code == 201
    assert 'application_id' in data
