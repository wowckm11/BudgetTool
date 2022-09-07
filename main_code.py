from datetime import datetime
import string
from xml.dom import ValidationErr
import mysql.connector
from mysql.connector import Error
import pandas as pd
import pydantic_constrained_types as cons
import pydantic


class PositiveInt(pydantic.BaseModel):
    id: cons.PositiveInt
    
class JustLetters(pydantic.BaseModel):
    id: cons.constr(min_length=3, max_length=15)

class Date(pydantic.BaseModel):
    id: pydantic.PastDate






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
    

    def input_new_person(self):
        
        name_tested = validate_words("Person name: ")
        income_tested = validate_positive_int("Monthly input: ")
        limit_tested = validate_positive_int("Monthly spending limit: ")
        return name_tested, income_tested, limit_tested

    
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

        if command == "0":
            query = self.insert_person()
            finance_database.execute_query(query)
        elif command =="1":
            query = self.insert_payment()
            finance_database.execute_query(query)
        elif command == "2":
            query = self.input_filters
            finance_database.read_query(query)
        
    
    def insert_person(self):
        name, income, limit = self.input_new_person()
        name = f'"{name}"'
        query = f"INSERT INTO person(person_name, monthly_income, spending_limit) VALUES ({name}, {income}, {limit})"
        return query
     
    def insert_payment(self):
        person_id, date, amount, payment_type = self.input_new_payment()
        payment_type = f'"{payment_type}"'
        date = f'"{date}"'
        query = f"INSERT INTO payment(person_id, date, amount, type) VALUES({person_id}, {date}, {amount}, {payment_type})"
        return query
    
    def input_new_payment(self):

        person_id_tested = validate_positive_int("Person ID number: ")
        date_tested = validate_date("Date of purchase: ")
        amount_tested = validate_positive_int("Cost: ")
        payment_type_tested = validate_words("Category: ")

        return person_id_tested, date_tested, amount_tested, payment_type_tested

    def input_filters(self):
        query = ""
        return query

    def read_query(connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as err:
            print(f"Error: '{err}'")

def validate_positive_int(message:str):
    while True:
        try:
            income = PositiveInt(id=input(message))
            income_tested = income.id
            if income_tested < 1000000000:
                return income_tested
            else:
                print("invalid input")
        except pydantic.error_wrappers.ValidationError:
            print("invalid input")

def validate_words(message:str):
    while True:
        try:
            name = JustLetters(id=input(message))
            for char in name.id:
                if char not in string.ascii_letters:
                    name = ""
            if name != "":
                name_tested = name.id
                return name_tested
        except pydantic.error_wrappers.ValidationError:
            print("invalid input")

def validate_date(message:str):
    while True:
        try:
            date = Date(id=input(message))
            if date.id > datetime(1980,1,1).date():
                date_tested = date.id
                return date_tested
            print("date is only accepted in yyyy-mm-dd format")
        except pydantic.error_wrappers.ValidationError:
            print("date is only accepted in yyyy-mm-dd format")
        


finance_database = DataBase()
while True:
    command = finance_database.get_input()
    if command == "Q":
        break
    else:
        finance_database.execute_command(command)