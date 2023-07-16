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
                constraint_value INTEGER CHECK (constraint_value IN (1, 2, NULL)),
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
                client_name VARCHAR(255),
                animal_type_id INT,
                number INT,
                description TEXT,
                deleted BOOLEAN DEFAULT 0,
                FOREIGN KEY (animal_type_id) REFERENCES animal_types(id)
            );
            """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS serial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                study_id INT,
                name VARCHAR(255),
                number INT,
                ears VARCHAR(255),
                FOREIGN KEY (study_id) REFERENCES studies(id)
            );""")

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS animal_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                description TEXT
            );
            """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                study_name VARCHAR(255) NOT NULL,
                archived BOOLEAN NOT NULL,
                animal_type_id INTEGER,
                description TEXT,
                FOREIGN KEY (animal_type_id) REFERENCES animal_types(id)
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                study_id INTEGER,
                series_id INTEGER,
                operator_id INTEGER,
                room_id INTEGER,
                equipment_id INTEGER,
                animal_type_id INTEGER,
                start_date DATETIME,
                end_date DATETIME,
                description TEXT,
                FOREIGN KEY (study_id) REFERENCES studies(id),
                FOREIGN KEY (series_id) REFERENCES series(id),
                FOREIGN KEY (operator_id) REFERENCES operators(id),
                FOREIGN KEY (room_id) REFERENCES rooms(id),
                FOREIGN KEY (equipment_id) REFERENCES equipments(id),
                FOREIGN KEY (animal_type_id) REFERENCES animal_types(id)
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

    def get_rooms(self, room_name:str=None, room_id:int=None) -> list:
        """
        Returns the equipments.
        """
        if room_name is None and room_id is None:
            self.cursor.execute("""
                SELECT * FROM `rooms`;
            """)
        elif room_id is not None:
            self.cursor.execute("""
                SELECT * FROM `rooms` WHERE `id` = ?;
            """, (room_id,))
        elif room_name is not None:
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
                'constraint': row[3],
                'description': row[4]
            }
            for row in rows
        ]
        return equipments

    def get_templates(self, study_name:str=None) -> list:
        """
        Returns the templates.
        """
        if study_name is None:
            self.cursor.execute("""
                SELECT * FROM `templates`;
            """)
        else:
            self.cursor.execute("""
                SELECT * FROM `templates` WHERE `study_name` = ?;
            """, (study_name,))
        rows = self.cursor.fetchall()
        templates = [
            {
                'id': row[0],
                'study_name': row[1],
                'archived': row[2],
                'animal_type_id': row[3],
                'description': row[4]
            }
            for row in rows
        ]
        return templates

    def get_room_equipment(self, eqpt_id:int) -> list:
        """
        Returns the room of the given equipment.
        """
        self.cursor.execute("""
            SELECT room_id FROM room_equipment WHERE equipment_id = ?
        """, (eqpt_id,))
        self.connection.commit()
        return self.cursor.fetchone()[0]

    def get_studies(self, study_name:str=None) -> list:
        """
        Returns the studies.
        """
        if study_name is None:
            self.cursor.execute("""
                SELECT * FROM `studies`;
            """)
        else:
            self.cursor.execute("""
                SELECT * FROM `studies` WHERE `name` = ?;
            """, (study_name,))
        rows = self.cursor.fetchall()
        studies = [
            {
                'id': row[0],
                'name': row[1],
                'archived': row[2],
                'client_name': row[3],
                'animal_type_id': row[4],
                'number': row[5],
                'description': row[6],
                'deleted': row[7]
            }
            for row in rows
        ]
        return studies

    def get_serials(self, study_id:int) -> list:
        """
        Returns the serials.
        """
        self.cursor.execute("""
            SELECT * FROM `serial` WHERE `study_id` = ?;
        """, (study_id,))
        rows = self.cursor.fetchall()
        serials = [
            {
                'id': row[0],
                'study_id': row[1],
                'name': row[2],
                'number': row[3],
                'ears': row[4]
            }
            for row in rows
        ]
        return serials

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

    def insert_equipment(self, name:str, archived:int, constraint:str,
                            description:str) -> bool:
        """
        Inserts an equipment in the database.
        """
        self.cursor.execute("""
            INSERT INTO `equipments` (`name`, `archived`, `constraint_value`, `description`)
            VALUES (?, ?, ?, ?);
            """, (name, archived, constraint, description))
        self.connection.commit()
        return True

    def insert_link_room_equipment(self, equipment_id:int, room_id:int) -> bool:
        """
        Inserts a link equipment room in the database.
        """
        self.cursor.execute("""
            INSERT INTO `room_equipment` (`equipment_id`, `room_id`)
            VALUES (?, ?);
            """, (equipment_id, room_id))
        self.connection.commit()
        return True

    def insert_animal_type(self, name:str, description:str) -> bool:
        """
        Inserts an animal type in the database.
        """
        self.cursor.execute("""
            INSERT INTO `animal_types` (`name`, `description`)
            VALUES (?, ?);
            """, (name, description))
        self.connection.commit()
        return True

    def insert_template(self, study_name:str, archived:bool,
                        animal_type_id:int, description:str) -> bool:
        """
        Inserts a template in the database.
        """
        self.cursor.execute("""
            INSERT INTO `templates` (`study_name`, `archived`, `animal_type_id`, `description`)
            VALUES (?, ?, ?, ?);
            """, (study_name, archived, animal_type_id, description))
        self.connection.commit()
        return True

    def insert_task(self, study_id:int, series_id:int, operator_id:int,
                    room_id:int, equipment_id:int, animal_type_id:int,
                    start_date:datetime, end_date:datetime, description:str) -> bool:
        """
        Inserts a task in the database.
        """
        self.cursor.execute("""
            INSERT INTO `tasks` (`study_id`, `series_id`, `operator_id`, `room_id`, `equipment_id`, `animal_type_id`, `start_date`, `end_date`, `description`)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (study_id, series_id, operator_id, room_id, equipment_id, animal_type_id, start_date, end_date, description))
        self.connection.commit()
        return  True

    def insert_study(self, name:str, archived:bool, client_name:str,
                     animal_type_id:int, number:int, description:str) -> bool:
        """
        Inserts a study in the database.
        Returns its id.
        """
        self.cursor.execute("""
            SELECT id FROM `studies` WHERE `name` = ?;
        """, (name,))
        if self.cursor.fetchone() is not None:
            self.safe_delete_study(name)

        print(name, archived, client_name, animal_type_id, number, description)
        self.cursor.execute("""
            INSERT INTO `studies` (`name`, `archived`, `client_name`, `animal_type_id`, `number`, `description`)
            VALUES (?, ?, ?, ?, ?, ?);
            """, (name, archived, client_name, animal_type_id, number, description))
        self.connection.commit()

        return self.cursor.lastrowid

    def insert_serial(self, study_id:int, name:str, number:int, ears:str) -> bool:
        """
        Inserts a serial in the database.
        """
        self.cursor.execute("""
            INSERT INTO `serial` (`study_id`, `name`, `number`, `ears`)
            VALUES (?, ?, ?, ?);
            """, (study_id, name, number, ears))
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
             'archived': 0,
             'animal_type_id': 2, 'number': random.randint(1, 10),
             'description': 'Lorem ipsum dolor sit amet'},

            {'name': 'Study 2',
             'archived': random.choice([True, False]),
             'animal_type_id': 1, 'number': random.randint(1, 10),
             'description': 'Consectetur adipiscing elit'},

            {'name': 'Study 3',
             'archived': random.choice([True, False]),
             'animal_type_id': 3,
             'number': random.randint(1, 10),
             'description': 'Sed do eiusmod tempor incididunt'},
        ]

        for study in studies:
            query = """INSERT INTO studies
            (name, archived, client_name, animal_type_id, number, description)
            VALUES (?, ?, ?, ?, ?, ?)"""
            values = (
                study['name'],
                study['archived'],
                "Client " + study['name'],
                study['animal_type_id'],
                study['number'],
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
            query = "INSERT INTO serial (study_id, name, number, ears) VALUES (?, ?, ?, ?)"
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

    def safe_delete_study(self, study_name:str) -> bool:
        """
        Deletes a study in the database.
        """
        self.cursor.execute("""
            UPDATE `studies` SET `deleted` = 1 WHERE `name` = ?;
        """, (study_name,))
        self.connection.commit()
        return True

    def close_connection(self) -> bool:
        """
        Ferme la session MySQL.
        """
        self.connection.close()
        return True
