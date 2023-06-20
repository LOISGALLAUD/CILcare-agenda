"""
db_cursor.py

This module contains the DBCursor class.
It will be used to interact with the database.
"""

#------------------------------------------------------------------------------#

import random
import sqlite3 as sql
from datetime import datetime

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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                archived BOOLEAN NOT NULL,
                description TEXT,
                expiration_date DATE
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS operators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                archived BOOLEAN NOT NULL
            );
        """)

        # Join table between operators and qualifications
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS operator_qualification (
                operator_id INTEGER,
                qualification_id INTEGER,
                FOREIGN KEY (operator_id) REFERENCES operators(id),
                FOREIGN KEY (qualification_id) REFERENCES qualifications(id)
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS `users` (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                archived BOOLEAN NOT NULL,
                description TEXT
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

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS animal_type (
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

    def get_operators(self, qualification_id:int=None) -> list:
        """
        Returns the operators with the given criteria.
        """
        query = """
            SELECT operators.id, operators.name, operators.archived
            FROM operators
            LEFT JOIN operator_qualification ON operators.id = operator_qualification.operator_id
            LEFT JOIN qualifications ON operator_qualification.qualification_id = qualifications.id
            WHERE qualifications.id = ?
        """
        self.cursor.execute(query, (qualification_id,))
        rows = self.cursor.fetchall()
        return [
            {"id": row[0], "name": row[1], "archived": row[2]} for row in rows
        ]

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
                SELECT * FROM `qualifications` WHERE `name` = ?;
            """, (qualification,))
        rows = self.cursor.fetchall()
        qualifications = [
            {
                'id': row[0],
                'name': row[1],
                'archived': row[2],
                'description': row[3],
                'expiration_date': row[4]
            }
            for row in rows
        ]
        return qualifications



    def get_equipments(self, name:str=None) -> list:
        """
        Returns the equipments.
        """
        if name is None:
            self.cursor.execute("""
                SELECT * FROM `equipment`;
            """)
        else:
            self.cursor.execute("""
                SELECT * FROM `equipment` WHERE `name` = ?;
            """, (name,))
        rows = self.cursor.fetchall()
        equipments = [
            {
                'id': row[0],
                'name': row[1],
                'archived': row[2],
                'description': row[3]
            }
            for row in rows
        ]
        return equipments

    def set_random_values(self) -> bool:
        """
        Sets random values in the database.
        """

        qualifications = [
            {
                "name": 'Qualification A',
                "archived": random.randint(0, 1),
                "description": 'Description A',
                "expiration_date": datetime.now()
            },
            {
                "name": 'Qualification B',
                "archived": random.randint(0, 1),
                "description": 'Description B',
                "expiration_date": datetime.now()
            },
            {
                "name": 'Qualification C',
                "archived": random.randint(0, 1),
                "description": 'Description C',
                "expiration_date": datetime.now()
            }
        ]

        for qualification in qualifications:
            query = """INSERT INTO qualifications
            (name, archived, description, expiration_date)
            VALUES (?, ?, ?, ?)"""
            values = (
                qualification["name"],
                qualification["archived"],
                qualification["description"],
                qualification["expiration_date"].strftime("%d/%m/%Y")
            )
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
            self.cursor.execute(query, values)
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
            query = "INSERT INTO operators (name, archived) VALUES (?, ?)"
            values = (
                operator['name'],
                operator['archived']
            )
            self.cursor.execute(query, values)
            self.connection.commit()

        operator_qualifications = [
            {
                'operator_id': 1,
                'qualification_id': 2
            },
            {
                'operator_id': 2,
                'qualification_id': 2
            },
            {
                'operator_id': 3,
                'qualification_id': 3
            }
        ]

        for operator_qualification in operator_qualifications:
            query = """INSERT INTO operator_qualification
            (operator_id, qualification_id) VALUES (?, ?)"""
            values = (
                operator_qualification['operator_id'],
                operator_qualification['qualification_id']
            )
            self.cursor.execute(query, values)
            self.connection.commit()


        equipments = [
            {'name': 'Equipment1', 'archived': random.choice([1, 0]),
             "description": 'Lorem ipsum dolor sit amet'},
            {'name': 'Equipment2', 'archived': random.choice([1, 0]),
             "description": 'Consectetur adipiscing elit'},
            {'name': 'Equipment3', 'archived': random.choice([1, 0]),
             "description": 'Sed do eiusmod tempor incididunt'},
        ]

        for equipment in equipments:
            query = """INSERT INTO equipment (name, archived, description)
            VALUES (?, ?, ?)"""
            values = (
                equipment['name'],
                equipment['archived'],
                equipment['description']
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
            self.cursor.execute(query, values)
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
            self.cursor.execute(query, values)
            self.connection.commit()

    def close_connection(self) -> bool:
        """
        Ferme la session MySQL.
        """
        self.connection.close()
        return True
