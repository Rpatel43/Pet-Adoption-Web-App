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

    # Admin data table
    # Notes
    # - UNIQUE username
    database.execute(
        """
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
        """
    )

    # Admin initial data
    # setup cursor
    cursor = database.execute("SELECT COUNT(*) AS count FROM admins;")
    # if no admin login exists:
    if cursor.fetchone()["count"] == 0:
        database.execute(
            "INSERT INTO admins (username, password) VALUES (?, ?)",
            ("admin", "admin123")
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


    # Default Pet listings initial data
    cursor = database.execute("SELECT COUNT(*) AS count FROM pets;")
    if cursor.fetchone()["count"] == 0:
        default_pets = [
            (
                "Loki", "Cat", "M",
                "Devil cat during the day, a pair of floating eye balls at night. He will eat your Doritos", # pylint: disable=line-too-long
                "Healthy",
                "Large", "13 lbs",
                "Available",
                "/static/uploads/loki.jpg"
            ),
            (
                "Molly", "Dog", "F",
                "The sweetest old girl. Terrified of thunderstorms and will hide behind random objects (you can still see her)", # pylint: disable=line-too-long
                "Healthy, has arthritis",
                "Medium/large", "56 lbs",
                "Available",
                "/static/uploads/Molly.png"
            ),
            (
                "Chiliman", "Cat", "M",
                "1 yr old. Cuddly. Loves freeze dried minnows and touching absolutely everything you own.", # pylint: disable=line-too-long
                "Healthy, neutered.",
                "Small", "10 lbs",
                "Available",
                "/static/uploads/chiliman.jpg"
            ),
            (
                "Mustang", "Cat", "F",
                "9 yr old. Independent outdoor cat who loves to bring gifts and purr loudly to show her love.", # pylint: disable=line-too-long
                "Healthy.",
                "Medium", "8 lbs",
                "Available",
                "/static/uploads/mustang.jpg"
            ),
            (
                "Lily", "Cat", "F",
                "7 yr old. You receive a flurry of happy meow greeting when she sees you, she loves to nap in the sun along side you.", # pylint: disable=line-too-long
                "Healthy.",
                "Large", "14 lbs",
                "Available",
                "/static/uploads/lily.jpg"
            ),
            (
                "Annie", "Dog", "F",
                "8 yr old. Loves playing and is extremely friendly, loves to snuggle in your lap.", # pylint: disable=line-too-long
                "Healthy, has seizure condition.",
                "Medium", "40 lbs",
                "Available",
                "/static/uploads/annie.jpg"
            )
        ]
        for pet in default_pets:
            database.execute(
                """
                INSERT INTO pets
                  (name, type, sex, bio, health_info, size, weight, status, picture)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                pet
            )

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
