from unicodedata import category
import random
from datetime import date, timedelta

from main_code import DataBase

new_database = DataBase()
def add_random_spendings(number_of_entries):
    for i in range(number_of_entries):
        person = random.randint(1,8)
        amount = random.randint(50,650)
        date_ = random.randint(-360,0)
        ven = random.randint(1,2)
        categ = random.randint(1,6)

        category_ = {1:"food",2:"equipment",3:"transport",4:"fun",5:"education",6:"investment"}
        venue = {"food1": "biedronka","food2": "lidl", "equipment":"amazon","transport1":"uber","transport2":"train","fun1":"club","fun2":"sports center","education":"Coursera","investment":"etoro"}
        if category_[categ] == "food" or category_[categ] == "transport" or category_[categ] == "fun":
            ven_ = category_[categ]+str(ven)
        else: ven_ = category_[categ]
        date_conv = date.today()
        date_conv += timedelta(days = date_)
        date_new = date_conv.isoformat()
        query = f"INSERT INTO spendings(person_id,amount,spending_date,venue,category) VALUES({person},{amount},'{date_new}','{venue[ven_]}','{category_[categ]}')"
        new_database.execute_query(query)


def add_incomes():
    for i in range(1,9):
        person = i
        income_source = 'job'
        if i == 3 or i == 5 or i == 7:
            amount = 25000
        if i == 4 or i == 6 :
            amount = 7000
        if i == 1 or i ==2 or i == 8:
            amount = 12000
        for f in range(13):
            inc_date = date.fromisoformat('2022-09-10')
            inc_date -= timedelta(days=f*30)
            query = f"INSERT INTO incomes(person_id,amount,income_date,income_source) VALUES({person},{amount},'{inc_date}','{income_source}')"
            new_database.execute_query(query)

def add_random_incomes():
    for i in range(1,9):
        person = i
        income_source = 'side'
        if i == 3 or i == 5 or i == 7:
            amount = 500
        if i == 4 or i == 6 :
            amount = 1500
        if i == 1 or i ==2 or i == 8:
            amount = 2500
        for f in range(13):
            if random.randint(1,4) == 1:
                inc_date = date.fromisoformat('2022-09-10')
                inc_date -= timedelta(days=f*30)
                query = f"INSERT INTO incomes(person_id,amount,income_date,income_source) VALUES({person},{amount},'{inc_date}','{income_source}')"
                new_database.execute_query(query)

def add_random_longterm():
    for i in range(1,9):
        person = i
        
        amount = random.randint(800,1000)
        times = random.randint(5,12)
        for f in range(13):
            if random.randint(1,8) == 1:
                dues = random.randint(1,4)
                dues_period = "quaterly" if dues == 1 else "Month"
                inc_date = date.fromisoformat('2022-09-10')
                inc_date -= timedelta(days=f*30)
                query = f"INSERT INTO long_term_spending(person_id,dues_period,amount,times,start_date) VALUES({person},'{dues_period}',{amount},{times},'{inc_date}')"
                new_database.execute_query(query)

def add_random_goals():
    for i in range(1,9):
        person = i
        goal_name = {1:"car",4:"plane",3:"private cinema",2:"house"}
        goal = random.randint(1,4)
        price = goal * 1000000
        query = f"INSERT INTO goals(person_id,goal_name,price,is_complete) VALUES({person},'{goal_name[goal]}',{price},False)"
        new_database.execute_query(query)

add_random_spendings(1200)