from cProfile import label
from turtle import left
from winreg import QueryInfoKey
import pydantic_constrained_types as cons
import pydantic
import string
import psycopg2
import sqlalchemy as sql
import matplotlib.pyplot as plt
import pandas as pd

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

def create_engine_config():
    params = config()
    hostname, database_name, user, password = params["host"], params["database"], params["user"], params["password"]
    engine = sql.create_engine(f'postgresql+psycopg2://{user}:{password}@{hostname}/{database_name}')
    return engine

def return_plot_job(dataframe,plot_type = "bar", title_window = ""):

    dataframe.plot(x = dataframe.columns[0], y =[dataframe.columns[1],dataframe.columns[2]],kind = plot_type, title = title_window)
    plt.show()

class DataBase:
    engine = create_engine_config()
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
    
    def job_stats(self, variant = 'yearly'):
        #long term spendings, rent etc
        query1 = """
        select person.job as Job, sum(long_term_spending.amount*long_term_spending.times)/count(distinct person.person_name) as spending FROM person
INNER JOIN long_term_spending ON long_term_spending.person_id = person.person_id
WHERE DATE_PART('day', now() - start_date::timestamp) <= 365
Group by job;
        """
        #everyday spendings
        query2 = """
        select person.job as Job, (sum(spendings.amount))/count(distinct person.person_name) as spending 
		FROM person
INNER JOIN spendings ON spendings.person_id = person.person_id
WHERE DATE_PART('day', now() - spending_date::timestamp) <= 365
Group by job;
        """
        #income per job
        query3 = """
    select person.job as Job, (sum(incomes.amount))/count(distinct person.person_name) as incomes FROM person
INNER JOIN incomes ON incomes.person_id = person.person_id
WHERE DATE_PART('day', now() - income_date::timestamp) <= 365
Group by job;
    """
        
        incomes = pd.read_sql_query(query3, self.engine)
        long_spend = pd.read_sql_query(query1, self.engine)
        dt = pd.read_sql_query(query2, self.engine)
        dt.spending = dt.spending + long_spend.spending
        dt['total income'] = incomes.incomes
        if variant == 'y':
            return_plot_job(dt, title_window ='Average yearly income and spending for jobs')
        elif variant == 'm':
            dt.spending = dt.spending.map(lambda p: p/12)
            dt['total income'] = dt['total income'].map(lambda p: p/12)
            return_plot_job(dt, title_window ='Average monthly income and spending for jobs')
        elif variant == 'd':
            dt.spending = dt.spending.map(lambda p: p/365)
            dt['total income'] = dt['total income'].map(lambda p: p/365)
            return_plot_job(dt, title_window ='Average daily income and spending for jobs')

    def money_stats(self):
        #long term spendings, rent etc
        query1 = """
        select person.person_id as id, 
sum(long_term_spending.amount*long_term_spending.times)/count(distinct person.person_id) as spending
FROM person
LEFT OUTER JOIN long_term_spending ON long_term_spending.person_id = person.person_id
WHERE DATE_PART('day', now() - start_date::timestamp) <= 365
GROUP BY person.person_id;
        """
        #everyday spendings
        query2 = """
        select person.person_id as id, (sum(spendings.amount))/count(distinct person.person_name) as spending 
		FROM person
INNER JOIN spendings ON spendings.person_id = person.person_id
WHERE DATE_PART('day', now() - spending_date::timestamp) <= 365
GROUP BY person.person_id;
        """
        #income per job
        query3 = """
    select person.person_id as id, (sum(incomes.amount))/count(distinct person.person_name) as incomes FROM person
INNER JOIN incomes ON incomes.person_id = person.person_id
WHERE DATE_PART('day', now() - income_date::timestamp) <= 365
GROUP BY person.person_id;
    """
        incomes = pd.read_sql_query(query3, self.engine)
        long_spend = pd.read_sql_query(query1, self.engine)
        long_spend = long_spend.set_index('id')
        dt = pd.read_sql_query(query2, self.engine)
        dt = dt.join(long_spend.spending, 'id',rsuffix='_l')
        dt['total spending'] = dt.spending.fillna(0) + dt.spending_l.fillna(0)
        dt = dt.drop('spending', axis=1)
        dt = dt.drop('spending_l', axis=1)
        dt['income'] = incomes.incomes
        dt['money saved'] = dt.income - dt["total spending"]
        dt.income = dt.income.map(lambda p: p/12)
        dt = dt.drop('total spending', axis=1)
        return_plot_job(dt,title_window= 'Money saved compared to monthly income')
    
    def category_stats(self):
        query = """
        select category, sum(spendings.amount) as amount
		FROM spendings
WHERE DATE_PART('day', now() - spending_date::timestamp) <= 365
Group by category;
        """
        dt = pd.read_sql_query(query, self.engine)
        dt.plot(x = dt.columns[0], y =dt.columns[1],kind = 'bar', title='Spending per category')
        plt.show()

    def venue_stats(self):
        query = """
        select venue, sum(spendings.amount) as amount
		FROM spendings
WHERE DATE_PART('day', now() - spending_date::timestamp) <= 365
Group by venue
ORDER BY amount DESC
LIMIT 10;
        """
        dt = pd.read_sql_query(query, self.engine)
        dt.plot(x = dt.columns[0], y =dt.columns[1],kind = 'bar', title="top 10 venues by spending")
        plt.show()
