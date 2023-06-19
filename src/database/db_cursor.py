"""
db_cursor.py

This module contains the DBCursor class.
It will be used to interact with the database.
"""

#------------------------------------------------------------------------------#

import random
import sqlite3 as sql

#------------------------------------------------------------------------------#

class DBCursor:
    """
    DBCursor class.

    It will be used to interact with the database.
    It will be able to return information or modify
    values in the database.
    """
    def __init__(self, app) -> None:
        self.loggers = app.loggers
        self.connection = None
        self.cursor = None
        self.setup_connection()
        self.setup_tables()
        self.setup_admin()
        self.set_random_values()
        self.show_tables()

    def setup_connection(self) -> bool:
        """
        Connects to the database.
        """
        self.connection = sql.connect("./data/cilcare.sqlite")
        self.cursor = self.connection.cursor()
        return True

    def setup_tables(self) -> bool:
        """
        Creates the tables if they don't exist.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS `qualifications` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `qualification` TEXT NOT NULL
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS `users` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `username` TEXT NOT NULL UNIQUE,
                `password` TEXT NOT NULL,
                `qualification_id` INTEGER,
                FOREIGN KEY (`qualification_id`) REFERENCES `qualifications` (`id`)
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS study (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                archived BOOLEAN NOT NULL,
                client_id INT,
                animal_type VARCHAR(255),
                animal_count INT,
                description TEXT,
                FOREIGN KEY (client_id) REFERENCES client(id)
            );
            """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS series (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                study_id INT,
                name VARCHAR(255),
                number INT,
                ears VARCHAR(255),
                FOREIGN KEY (study_id) REFERENCES study(id)
            );""")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS client (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL
            );
            """)

        return True

    def setup_admin(self) -> bool:
        """
        Creates the admin user if it doesn't exist.
        """
        self.cursor.execute("""
            SELECT * FROM `users` WHERE `username` = 'admin';
        """)
        if self.cursor.fetchone() is None:
            self.cursor.execute("""
                INSERT INTO `users` (`username`, `password`, `qualification_id`)
                VALUES ('admin', 'admin', NULL);
            """)
        return True

    def get_user(self, username: str) -> tuple:
        """
        Returns the user with the given username.
        """
        self.cursor.execute("""
            SELECT * FROM `users` WHERE `username` = ?;
        """, (username,))
        return self.cursor.fetchone()

    def set_random_values(self) -> bool:
        """
        Sets random values in the database.
        """
        qualifications = ['Qualification A', 'Qualification B', 'Qualification C']

        for qualification in qualifications:
            query = "INSERT INTO qualifications (qualification) VALUES (?)"
            values = (qualification,)
            self.cursor.execute(query, values)
            self.connection.commit()

        users = [
        {'username': 'User1',
         'password': 'password1',
         'qualification_id': random.randint(1, len(qualifications))},

        {'username': 'User2',
         'password': 'password2',
         'qualification_id': random.randint(1, len(qualifications))},

        {'username': 'User3',
         'password': 'password3',
         'qualification_id': random.randint(1, len(qualifications))},
        ]

        for user in users:
            query = "INSERT INTO users (username, password, qualification_id) VALUES (?, ?, ?)"
            values = (
                user['username'],
                user['password'],
                user['qualification_id']
            )
            # Verify if the user already exists
            if self.get_user(user['username'])[1] == user['username']:
                continue
            self.cursor.execute(query, values)
            self.connection.commit()

        clients = ['Client A', 'Client B', 'Client C']
        random.shuffle(clients)

        for client_name in clients:
            query = "INSERT INTO client (name) VALUES (?)"
            values = (client_name,)
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()

        # Générer des valeurs aléatoires pour la table "study"
        studies = [
            {'name': 'Study 1',
             'archived': random.choice([True, False]),
             'animal_type': 'Cat', 'animal_count': random.randint(1, 10),
             'description': 'Lorem ipsum dolor sit amet'},

            {'name': 'Study 2',
             'archived': random.choice([True, False]),
             'animal_type': 'Dog', 'animal_count': random.randint(1, 10),
             'description': 'Consectetur adipiscing elit'},

            {'name': 'Study 3',
             'archived': random.choice([True, False]),
             'animal_type': 'Rabbit',
             'animal_count': random.randint(1, 10),
             'description': 'Sed do eiusmod tempor incididunt'},
        ]

        for study in studies:
            query = """INSERT INTO study
            (name, archived, client_id, animal_type, animal_count, description)
            VALUES (?, ?, ?, ?, ?, ?)"""
            values = (
                study['name'],
                study['archived'],
                random.randint(1, len(clients)),
                study['animal_type'],
                study['animal_count'],
                study['description']
            )
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()

        # Générer des valeurs aléatoires pour la table "series"
        series = [
            {'name': 'Series 1', 'number': random.randint(1, 5),
             'ears': random.choice(['Two', 'Four'])},
            {'name': 'Series 2', 'number': random.randint(1, 5),
             'ears': random.choice(['Two', 'Four'])},
            {'name': 'Series 3', 'number': random.randint(1, 5),
             'ears': random.choice(['Two', 'Four'])},
        ]

        for series_data in series:
            query = "INSERT INTO series (study_id, name, number, ears) VALUES (?, ?, ?, ?)"
            values = (
                random.randint(1, len(studies)),
                series_data['name'],
                series_data['number'],
                series_data['ears']
            )
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()

    def show_tables(self) -> bool:
        """
        Shows the tables.
        """
        self.cursor.execute("""
            SELECT * FROM `users`;
        """)
        self.loggers.log.debug(self.cursor.fetchall())

        self.cursor.execute("""
            SELECT * FROM `qualifications`;
        """)
        self.loggers.log.debug(self.cursor.fetchall())

        self.cursor.execute("""
            SELECT * FROM `study`;
        """)
        self.loggers.log.debug(self.cursor.fetchall())

    def close_connection(self) -> bool:
        """
        Ferme la session MySQL.
        """
        self.connection.close()
        return True
