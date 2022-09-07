import string
import mysql.connector
from mysql.connector import Error
import pandas as pd









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


class DataBase:
    connection = create_db_connection("localhost", "root", "Archespor2", "finance")
    def __init__(self):
        pass
    

    def input_new_payment(self):
        while True:
            name = input("name: ")
            for letter in name:
                if letter not in string.ascii_letters:
                    name = ""
            if name != "":
                break
        while True:
            income = input("Monthly income: ")
            try:
                if int(income) < 0 or int(income) > 1000000000:
                    print("income has to between 0 and 1000.0000.000")
                income_tested = int(income)
                break
            except ValueError:
                print("income has to be an integer")
        while True:
            limit = input("Monthly spending limit")
            try:
                if int(limit) < 0 or int(limit) > 1000000000:
                    print("spending limit has to between 0 and 1000.0000.000")
                limit_tested = int(limit)
                break
            except ValueError:
                print("spending limit has to be an integer")

        return name, income_tested, limit_tested

    
    def get_input(self):
        
        print("commands to run 1-x 2-y 3-z etc Q to exit")
        user_input = input("Choose command to run: ")

        return user_input

    def execute_query(self, query, connect=connection):
        cursor = connect.cursor()
        try:
            cursor.execute(query)
            connect.commit()
            print("Query successful")
        except Error as err:
            print(f"Error: '{err}'")
    
    def execute_command(self, command):
        query = ""
        if command == "0":
            query = self.input_payments()
        else:
            pass
        finance_database.execute_query(query)
    
    def input_payments(self):
        name, income, limit = self.input_new_payment()
        query = f"INSERT INTO person(person_name, monthly_income, spending_limit) VALUES ({name}, {income}, {limit})"
        return query
     

finance_database = DataBase()
while True:
    command = finance_database.get_input()
    if command == "Q":
        break
    else:
        finance_database.execute_command(command)