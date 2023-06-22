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
                description TEXT
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
                expiration_date DATE,
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
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                archived BOOLEAN NOT NULL,
                description TEXT
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                archived BOOLEAN NOT NULL,
                description TEXT
            );
            """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS room_equipment (
            room_id INTEGER,
            equipment_id INTEGER,
            FOREIGN KEY (room_id) REFERENCES rooms (id),
            FOREIGN KEY (equipment_id) REFERENCES equipments (id)
        );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS studies (
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
                FOREIGN KEY (study_id) REFERENCES studies(id)
            );""")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL
            );
            """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS animal_types (
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
        Returns the operator(s) with the given username.
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
                'archived': row[2]
            }
            for row in rows
        ]
        return operators

    def get_qualified_operators(self, qualification_id:int=None) -> list:
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
            {
                "id": row[0],
                "name": row[1],
                "archived": row[2]
            } for row in rows
        ]

    def get_expiration_date(self, operator_id:int, qualification_id:int) -> str:
        """
        Returns the expiration date of the operator's qualification.
        """
        self.cursor.execute("""
            SELECT expiration_date FROM operator_qualification
            WHERE operator_id = ? AND qualification_id = ?;
        """, (operator_id, qualification_id))
        self.connection.commit()
        return self.cursor.fetchone()[0]

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
                'description': row[3]
            }
            for row in rows
        ]
        return qualifications

    def get_animal_types(self, animal_type_name:str=None) -> list:
        """
        Returns the animal type(s) with the given name.
        """
        if animal_type_name is None:
            self.cursor.execute("""
                SELECT * FROM `animal_types`;
            """)
        else:
            self.cursor.execute("""
                SELECT * FROM `animal_types` WHERE `name` = ?;
            """, (animal_type_name,))

        rows = self.cursor.fetchall()
        animal_types = [
            {
                'id': row[0],
                'name': row[1]
            }
            for row in rows
        ]
        return animal_types

    def get_rooms(self, room_name:str=None) -> list:
        """
        Returns the equipments.
        """
        if room_name is None:
            self.cursor.execute("""
                SELECT * FROM `rooms`;
            """)
        else:
            self.cursor.execute("""
                SELECT * FROM `rooms` WHERE `name` = ?;
            """, (room_name,))
        rows = self.cursor.fetchall()
        rooms = [
            {
                'id': row[0],
                'name': row[1],
                'archived': row[2],
                'description': row[3]
            }
            for row in rows
        ]
        return rooms

    def get_equipments(self, equipment_name:str=None) -> list:
        """
        Returns the equipments.
        """
        if equipment_name is None:
            self.cursor.execute("""
                SELECT * FROM `equipments`;
            """)
        else:
            self.cursor.execute("""
                SELECT * FROM `equipments` WHERE `name` = ?;
            """, (equipment_name,))
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

    def insert_room(self, name:str, archived:int, description:str) -> bool:
        """
        Inserts a room in the database.
        """
        self.cursor.execute("""
            INSERT INTO `rooms` (`name`, `archived`, `description`)
            VALUES (?, ?, ?);
            """, (name, archived, description))
        self.connection.commit()
        return True

    def insert_qualification(self, name:str, archived:int,
                             description:str) -> bool:
        """
        Inserts a qualification in the database.
        """
        self.cursor.execute("""
            INSERT INTO `qualifications` (`name`, `archived`, `description`)
            VALUES (?, ?, ?);
            """, (name, archived, description))
        self.connection.commit()
        return True

    def insert_operator(self, name:str, archived:int) -> bool:
        """
        Inserts an operator in the database.
        """
        self.cursor.execute("""
            INSERT INTO `operators` (`name`, `archived`)
            VALUES (?, ?);
            """, (name, archived))
        self.connection.commit()
        return True

    def insert_link_operator_qualification(self, operator_id:int, qualification_id:int,
                                            expiration_date:datetime.date) -> bool:
        """
        Inserts a link operator qualification in the database.
        """
        self.cursor.execute("""
            INSERT INTO `operator_qualification` (`operator_id`, `qualification_id`, `expiration_date`)
            VALUES (?, ?, ?);
            """, (operator_id, qualification_id, expiration_date))
        self.connection.commit()
        return True

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
            (name, archived, description)
            VALUES (?, ?, ?)"""
            values = (
                qualification["name"],
                qualification["archived"],
                qualification["description"]
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
            query = "INSERT INTO clients (name) VALUES (?)"
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
                'qualification_id': 2,
                'expiration_date': datetime.strptime("22/09/2003", '%d/%m/%Y').date()
            },
            {
                'operator_id': 2,
                'qualification_id': 2,
                'expiration_date': datetime.strptime("02/04/2002", '%d/%m/%Y').date()
            },
            {
                'operator_id': 3,
                'qualification_id': 3,
                'expiration_date': datetime.strptime("02/04/2023", '%d/%m/%Y').date()
            }
        ]

        for operator_qualification in operator_qualifications:
            query = """INSERT INTO operator_qualification
            (operator_id, qualification_id, expiration_date) VALUES (?, ?, ?)"""
            values = (
                operator_qualification['operator_id'],
                operator_qualification['qualification_id'],
                operator_qualification["expiration_date"].strftime("%d/%m/%Y")
            )
            self.cursor.execute(query, values)
            self.connection.commit()

        room_equipments = [
            {
                'room_id': 1,
                'equipment_id': 2,
            },
            {
                'room_id': 2,
                'equipment_id': 1,
            },
            {
                'room_id': 3,
                'equipment_id': 3,
            }
        ]

        for room_equipment in room_equipments:
            query = """INSERT INTO room_equipment
            (room_id, equipment_id) VALUES (?, ?)"""
            values = (
                room_equipment['room_id'],
                room_equipment['equipment_id']
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
            query = """INSERT INTO equipments (name, archived, description)
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
            query = """INSERT INTO studies
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

        animal_types = ['Dog', 'Cat', 'Bird', 'Fish', 'Rabbit']

        for animal_type in animal_types:
            query = "INSERT INTO animal_types (name) VALUES (?)"
            values = (animal_type,)
            self.cursor.execute(query, values)
            self.connection.commit()

        rooms = [
            {
                'name': 'Room A',
                'archived': random.choice([0, 1]),
                'description': 'Description A'
            },
            {
                'name': 'Room B',
                'archived': random.choice([0, 1]),
                'description': 'Description B'
            },
            {
                'name': 'Room C',
                'archived': random.choice([0, 1]),
                'description': 'Description C'
            }
        ]

        for room in rooms:
            query = "INSERT INTO rooms (name, archived, description) VALUES (?, ?, ?)"
            values = (room['name'], room['archived'], room['description'])
            self.cursor.execute(query, values)
            self.connection.commit()

    def close_connection(self) -> bool:
        """
        Ferme la session MySQL.
        """
        self.connection.close()
        return True
