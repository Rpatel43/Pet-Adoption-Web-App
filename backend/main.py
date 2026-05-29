"""Main file for API. Handles blueprints and starting the app up."""
from os import makedirs, environ, path
from secrets import token_hex
try:
    from flasgger import Swagger
except ImportError:
    Swagger = None
from flask import Flask, request, make_response
from backend.user import user_blueprint
from backend.pets import pets_blueprint
from backend.admin import admin_blueprint
from backend.database import init_application


def build_app():
    """Instantiates the application before we run it."""

    app = Flask(__name__, instance_relative_config=True)

    # Make an instance folder for the database to live
    try:
        makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Config key and db
    # NOTE we generate a key locally if we dont have access to github secrets
    app.config["SECRET_KEY"] = environ.get("SECRET_KEY") or token_hex(32)
    app.config["DATABASE"] = path.join(app.instance_path, "pet_adoption_website.db")

    # some secutiry features for session
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_HTTPONLY"] = True

    upload_dir = path.join(app.root_path, 'static', 'uploads')
    makedirs(upload_dir, exist_ok=True)
    app.config['PET_PHOTO_DIRECTORY'] = upload_dir


    if Swagger:
        Swagger(app)

    configure_cors(app)
    init_application(app)

    # blueprint registration for all of our module files
    # note the seperate prefix for admin so they have a seperate portal
    app.register_blueprint(user_blueprint, url_prefix='/api')
    app.register_blueprint(pets_blueprint, url_prefix='/api')
    app.register_blueprint(admin_blueprint, url_prefix='/api/admin')


    @app.route('/')
    def homepage():
        """Homepage route. We create this in main because it is our landing page and is
        where we want the user to hit first when they enter the web app."""
        return {"message": "Welcome to the homepage! :)"}, 200


    return app


def configure_cors(app):
    @app.after_request
    def add_cors_headers(response):
        origin = request.headers.get('Origin')
        if origin:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        return response

    @app.route('/api', methods=['OPTIONS'])
    @app.route('/api/<path:path>', methods=['OPTIONS'])
    def preflight(path=None):
        response = make_response('', 204)
        origin = request.headers.get('Origin')
        if origin:
            response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        return response


if __name__ == '__main__':
    application = build_app()
    application.run(
        host='0.0.0.0',
        port=int(environ.get('PORT', 5000)),
        debug=environ.get('FLASK_DEBUG', '0') in ('1', 'true', 'True')
    )
