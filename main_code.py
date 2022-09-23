import pydantic_constrained_types as cons
import pydantic
import string
import psycopg2

from datetime import datetime, date
from xml.dom import ValidationErr
from configparser import ConfigParser



class PositiveInt(pydantic.BaseModel):
    id: cons.PositiveInt
    
class JustLetters(pydantic.BaseModel):
    id: cons.constr(min_length=3, max_length=15)

class Date(pydantic.BaseModel):
    d: date = None

def validate_positive_int_gui(number):

        income = PositiveInt(id=number)
        income_tested = income.id
        if income_tested < 1000000000:
            return income_tested

def validate_words_gui(word:str):
            name = JustLetters(id=word)
            for char in name.id:
                if char not in string.ascii_letters:
                    name = ""
            if name != "":
                name_tested = name.id.lower()
                return name_tested

def validate_date_gui(date_input:str):
    if date_input != "today":
        date_ = Date(d=date_input)
        if date_.d > datetime(1980,1,1).date():
            date_tested = date_.d
            return date_tested
        raise ValidationErr
    else:
        date_tested = date.today()
        return date_tested

def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def create_db_connection():
        connection = None
        try:
            params = config()
            connection = psycopg2.connect(**params)
                    
            print("Database connection successful")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return connection


class DataBase:
    connection = create_db_connection()
    def __init__(self):
        pass

    def execute_query(self, query, connect=connection):
        cursor = connect.cursor()
        try:
            cursor.execute(query)
            connect.commit()
            print("Query successful")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
    
    def execute_gui_command(self, command):
        
        if command == "0":
            query = self.insert_person_gui()
            self.execute_query(query)
        elif command =="1":
            query = self.insert_payment_gui()
            self.execute_query(query)
        elif command == "2":
            query = self.apply_filters_gui()
            result = self.read_query(query)
            for item in result:
                print(item)
        elif command =="3":
            self.return_advice_gui()
    
    def insert_person_gui(self, name, job, limit, birthday, months_of_grace):
        name = f"'{name}'"
        job = f"'{job}'"
        birthday = f"'{birthday}'"
        query = f"INSERT INTO person(person_name, job, spending_limit, birthday, months_of_grace_period) VALUES ({name}, {job}, {limit}, {birthday},{months_of_grace})"
        return query
    
    def insert_payment_gui(self,person_id, amount, date, venue, payment_type):
        payment_type = f"'{payment_type}'"
        venue = f"'{venue}'"
        date = f"'{date}'"
        query = f"INSERT INTO spendings(person_id, amount, spending_date, venue, category) VALUES({person_id}, {amount}, {date}, {venue}, {payment_type})"
        return query

    def apply_filters_gui(self,type_specified, price_specified_high, price_specified_low,
         date_specified_old, date_specified_new, person_specified, venue_specified):
        
        if type_specified is not None:
            type_query = f"category = '{type_specified}' and "
        else:
            type_query = ""

        if venue_specified is not None:
            venue_query = f"venue = '{venue_specified}' and "
        else:
            venue_query = ""

        if price_specified_high is not None:
            price_query_high = f"amount < {price_specified_high} and "
        else:
            price_query_high = ""

        if price_specified_low is not None:
            price_query_low = f"amount > {price_specified_low} and "
        else:
            price_query_low = ""

        if date_specified_old is not None:
            date_query_old = f"spending_date > '{date_specified_old}' and "
        else:
            date_query_old = ""

        if date_specified_new is not None:
            date_query_new = f"spending_date < '{date_specified_new}' and "
        else:
            date_query_new = ""

        if person_specified is not None:
            person_query = f"person_id = {person_specified}"
        else:
            person_query = ""

        query = (f"SELECT * FROM spendings WHERE {type_query}{venue_query}{price_query_high}"
        f"{price_query_low}{date_query_old}{date_query_new}{person_query};")

        if query.endswith(" and ;"):
            query = query[:-5]
        if query.endswith(" WHERE ;"):
            query = """SELECT * 
            FROM spendings
            ORDER BY spending_date DESC
            LIMIT 100;"""

        print(f"statemnt sent to database: {query}")
        return query

    def read_query(self, query, connecto=connection):
        cursor = connecto.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def filter_for_user(self, user):
        last_month = date.today().replace(month=date.today().month-1)
        query = f"SELECT * FROM payment WHERE person_id = {user} and date > '{last_month}'"
        return query
    
    def query_user_info(self, user):
        query = f"SELECT monthly_income, spending_limit, person_name FROM person WHERE person_id = {user}"
        return query

    def return_advice_gui(self, user):
        spending = self.get_user_spending(user)
        user_name, monthly_income, spending_limit = self.get_user_personal_data(user)
        total = self.user_total_spending(spending)
        return_string = f"{user_name}, you have spent {total} PLN in the last 30 days\n"
        if total > spending_limit:
            return_string += (f"You disregarded your spending limit by {total- spending_limit} PLN\n")
        return_string += (f"You spent {total/monthly_income*100:.1f}% of your monthly income\n")
        return return_string

    def get_user_spending(self, user):
        query = self.filter_for_user(user)
        data = self.read_query(query)
        spending_temp_dict = {}
        for item in data:
            try:
                spending_temp_dict[item[4]] += item[3]
            except KeyError:
                spending_temp_dict[item[4]] = item[3]
        return spending_temp_dict
    
    def get_user_personal_data(self, user):
        query_for_user = self.query_user_info(user)
        user_data = self.read_query(query_for_user)
        monthly_income = user_data[0][0]
        spending_limit = user_data[0][1]
        user_name = user_data[0][2]
        return user_name, monthly_income, spending_limit

    def user_total_spending(self, spending):
        total_spent = 0
        for key in spending:
            total_spent += spending[key]
        
        return total_spent
