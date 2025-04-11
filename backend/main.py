"""Main file for API. Handles blueprints and starting the app up."""
from flask import Flask
from backend import user, pets, admin
from user import user_blueprint
from pets import pets_blueprint
from admin import admin_blueprint


def build_app():
    """Instantiates the application before we run it."""

    app = Flask(__name__)

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


if __name__ == '__main__':
    application = build_app()
    application.run(debug=True)
