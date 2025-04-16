"""Database for the pet adoption website. contains all neccessary data tables and preload values."""
import sqlite3
from flask import current_app, g
import click

def open_database():
    """Opens database connection if a link is not already established.
    Utilizes 'g' import to make possible."""

    # if connection dne yet:
    if 'database' not in g:
        g.database = sqlite3.connect(
            # retrieves path to database file
            current_app.config['DATABASE'],
            # converts returned values to python data types
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # make rows in database behave like dictionaries
        g.database.row_factory = sqlite3.Row

    return g.database


def close_database(error=None): # pylint: disable=unused-argument
    """Closes the connection of the database. We pop the connection
    to either get it, or none, and close if need be."""
    connection = g.pop('database', None)
    if connection is not None:
        connection.close()


def init_database():
    """Initialize the database with all neccessary tables and pre-config data"""

    database = open_database()

    # User data table
    # Notes
    # - notice how username must be unique
    # - notice how we mark id to auto increment and as primary key
    # - note text cannot be null
    database.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            password TEXT NOT NULL
        );
        """
    )

    # Pets data table
    # Notes
    # - note id primary key / auto increment
    # - note name and type cannot be null
    database.execute(
        """
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            sex TEXT,
            bio TEXT,
            health_info TEXT,
            size TEXT,
            weight TEXT,
            status TEXT,
            picture TEXT
        );
        """
    )

    # Application data table
    # Notes
    # - Foreign keys ensure that we are assigning an application
    # to an existing user and pet listing
    database.execute(
        """
        CREATE TABLE IF NOT EXISTS applications (
            application_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            pet_id INTEGER NOT NULL,
            status TEXT,
            application_response TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(pet_id) REFERENCES pets(id)
        );
        """
    )

    # Pet types data table
    # Notes
    # - Make sure type is UNIQUE so we do not have duplicate types
    database.execute(
        """
        CREATE TABLE IF NOT EXISTS pet_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL UNIQUE
        );
        """
    )

    # Pet Types initial data
    # set up cursor and row of access
    cursor = database.execute("SELECT COUNT(*) as count FROM pet_types;")
    row = cursor.fetchone()
    # note we can access row like this because of our row factory that we made earlier
    if row["count"] == 0:
        # insert Cat and Dog types into pet_types on init
        database.execute("INSERT INTO pet_types (type) VALUES (?)", ("Dog",))
        database.execute("INSERT INTO pet_types (type) VALUES (?)", ("Cat",))
    # commit to db
    database.commit()


def init_application(app):
    """Registers our database with the flask application."""
    # Enables an auto-closedown of the database to clearn up the database connection
    app.teardown_appcontext(close_database)
    # adds our init database command below
    app.cli.add_command(init_database_command)


@click.command('init-database')
def init_database_command():
    """Clears the database and refreshes it with new tables and values."""
    # initializes the database
    init_database()
    click.echo("database successfully initialized.")
