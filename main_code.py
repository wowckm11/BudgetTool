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
        while True:
            try:
                name = JustLetters(id=input("Name: "))
                for char in name.id:
                    if char not in string.ascii_letters:
                        name = ""
                if name != "":
                    name_tested = name.id
                    break
            except pydantic.error_wrappers.ValidationError:
                print("name has to contain only letters and have length from 3 to 15 characters")

        while True:
            try:
                income = PositiveInt(id=input("Monthly income: "))
                income_tested = income.id
                break
            except pydantic.error_wrappers.ValidationError:
                print("you have to input a positive integer")

            
        while True:
            try:
                limit = PositiveInt(id=input("Monthly spending limit: "))
                limit_tested = limit.id
                break
            except pydantic.error_wrappers.ValidationError:
                print("you have to input a positive integer")
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
        query = ""
        if command == "0":
            query = self.insert_person()
        elif command =="1":
            query = self.insert_payment()
        else:
            pass
        finance_database.execute_query(query)
    
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

        while True:
            try:
                person_id = PositiveInt(id=input("database user id: "))
                person_id_tested = person_id.id
                break
            except pydantic.error_wrappers.ValidationError:
                print("you have to input a positive integer")

        while True:
            try:
                date = Date(id=input("date of purchase "))
                if date.id > datetime(1980,1,1).date():
                    date_tested = date.id
                    break
                print("you have to input a valid date")
            except pydantic.error_wrappers.ValidationError:
                print("you have to input a valid date")
        
        while True:
            try:
                amount = PositiveInt(id=input("amount spent: "))
                amount_tested = amount.id
                break
            except pydantic.error_wrappers.ValidationError:
                print("you have to input a positive integer")
        
        while True:
            try:
                payment_type = JustLetters(id=input("purchase category: "))
                for char in payment_type.id:
                    if char not in string.ascii_letters:
                        payment_type = ""
                if payment_type != "":
                    payment_type_tested = payment_type.id
                    break
            except pydantic.error_wrappers.ValidationError:
                print("type has to contain only letters and have length from 3 to 15 characters")

            

        return person_id_tested, date_tested, amount_tested, payment_type_tested
            

finance_database = DataBase()
while True:
    command = finance_database.get_input()
    if command == "Q":
        break
    else:
        finance_database.execute_command(command)