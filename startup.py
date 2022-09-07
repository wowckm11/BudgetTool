import mysql.connector
from mysql.connector import Error
import pandas as pd
pw = "Archespor2"


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database = db_name)
                
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


create_person_table = """
CREATE TABLE person (
  person_id INT PRIMARY KEY,
  person_name TEXT NOT NULL,
  monthly_income INT NOT NULL,
  spending_limit INT
);
"""

create_payment_table = """
CREATE TABLE payment (
  payment_id INT PRIMARY KEY,
  person INT,
  date DATE NOT NULL,
  amount INT NOT NULL,
  type TEXT
);
"""

alter_payment = """
ALTER TABLE payment
ADD FOREIGN KEY(person_id)
REFERENCES person(person_id)
ON DELETE SET NULL;
"""

pop_person = """
INSERT INTO person VALUES
(1,  'Maciej', '9000', '2000'),
(2, 'Oliwia', '2400','2000'),
(3, 'Blazej', '3500','1500');
"""

pop_payment = """
INSERT INTO payment VALUES
(1, 1, 2020-08-20, 350, 'equipment')
(2, 1, 2020-08-21, 450, 'food')
(3, 1, 2020-08-22, 150, 'growth')
(4, 2, 2020-08-23, 650, 'equipment')
(5, 2, 2020-08-20, 350, 'food')
(6, 2, 2020-08-21, 450, 'growth')
(7, 3, 2020-08-22, 150, 'equipment')
(8, 3, 2020-08-23, 650, 'food')
"""
connection = create_server_connection("localhost", "root", pw)
create_database_query = "CREATE DATABASE finance"
create_database(connection, create_database_query)
connection = create_db_connection("localhost", "root", pw, "finance")
execute_query(connection, create_person_table)
execute_query(connection, create_payment_table)
execute_query(connection, alter_payment)
execute_query(connection, pop_person)
execute_query(connection, pop_payment)
