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

        # if tables are empty, fill them with random values
        if self.cursor.execute("SELECT COUNT(*) FROM `users`").fetchone()[0] == 1:
            self.set_random_values()

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
                `password` TEXT NOT NULL
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS operators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                archived BOOLEAN NOT NULL,
                qualification_id INTEGER,
                FOREIGN KEY (qualification_id) REFERENCES qualifications(id)
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
                INSERT INTO `users` (`username`, `password`)
                VALUES ('admin', 'admin');
            """)
        return True

    def get_users(self, username:str=None) -> list:
        """
        Returns the user(s) with the given username.
        """
        if username is None:
            self.cursor.execute("""
                SELECT * FROM `users`;
            """)
        else:
            self.cursor.execute("""
                SELECT * FROM `users` WHERE `username` = ?;
            """, (username,))

        rows = self.cursor.fetchall()
        users = [
            {
                'id': row[0],
                'username': row[1],
                'password': row[2]
            }
            for row in rows
        ]
        return users

    def get_operators(self, name:str=None) -> list:
        """
        Returns the user with the given username.
        """
        if name is None:
            self.cursor.execute("""
                SELECT * FROM `operators`;
            """)
        else:
            self.cursor.execute("""
                SELECT * FROM `operators` WHERE `name` = ?;
            """, (name,))
        rows = self.cursor.fetchall()
        operators = [
            {
                'id': row[0],
                'name': row[1],
                'archived': row[2],
                'qualification_id': row[3]
            }
            for row in rows
        ]
        return operators

    def get_qualifications(self, qualification:str=None) -> list:
        """
        Returns the qualifications.
        """
        if qualification is None:
            self.cursor.execute("""
                SELECT * FROM `qualifications`;
            """)
        else:
            self.cursor.execute("""
                SELECT * FROM `qualifications` WHERE `qualification` = ?;
            """, (qualification,))
        rows = self.cursor.fetchall()
        qualifications = [
            {
                'id': row[0],
                'qualification': row[1]
            }
            for row in rows
        ]
        return qualifications

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
            {'username': 'User1', 'password': 'password1',
             'qualification_id': random.randint(1, len(qualifications))},

            {'username': 'User2', 'password': 'password2',
             'qualification_id': random.randint(1, len(qualifications))},

            {'username': 'User3', 'password': 'password3',
             'qualification_id': random.randint(1, len(qualifications))},
        ]

        for user in users:
            if self.get_users(user['username']) != []:
                continue
            query = "INSERT INTO users (username, password) VALUES (?, ?)"
            values = (
                user['username'],
                user['password']
            )
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

        operators = [
            {'name': 'Operator1', 'archived': random.choice([1, 0]),
             'qualification_id': random.randint(1, 3)},

            {'name': 'Operator2', 'archived': random.choice([1, 0]),
             'qualification_id': random.randint(1, 3)},

            {'name': 'Operator3', 'archived': random.choice([1, 0]),
             'qualification_id': random.randint(1, 3)},
        ]

        for operator in operators:
            query = "INSERT INTO operators (name, archived, qualification_id) VALUES (?, ?, ?)"
            values = (
                operator['name'],
                operator['archived'],
                operator['qualification_id']
            )
            self.cursor.execute(query, values)
            self.connection.commit()


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

    def close_connection(self) -> bool:
        """
        Ferme la session MySQL.
        """
        self.connection.close()
        return True
