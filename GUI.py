from tkinter import Entry
import PySimpleGUI as sg

from main_code import *

# name, job, limit, birthday, months_of_grace
def create_window_person():
    person_layout = [
            [sg.Text("Person Name"),sg.Input()],
            [sg.Text("Job"),sg.Input()],
            [sg.Text("Spending limit"),sg.Input()],
            [sg.Text("Birthday"),sg.Input()],
            [sg.Text("Months of grace"),sg.Input()],
            [sg.Button("confirm", key = "-ACCEPT-"), sg.Button("cancel", key= "-CLOSE-")]
            ]
            
    window_popup = sg.Window("Input Person data!", person_layout)
    while True:
        event,values = window_popup.read()
        if event == "-CLOSE-" or event == sg.WIN_CLOSED:
            window_popup.close()
            return None
        elif event == "-ACCEPT-":
                if person_input(person_layout) is not None:
                    window_popup.close()
                    return person_input(person_layout)

def create_window_stats():
    person_layout = [
            [sg.Text("Person ID"),sg.Input()],
            [sg.Button("confirm", key = "-ACCEPT-"), sg.Button("cancel", key= "-CLOSE-")]
            ]
            
    window_popup = sg.Window("choose a person!", person_layout)
    while True:
        event,values = window_popup.read()
        if event == "-CLOSE-" or event == sg.WIN_CLOSED:
            window_popup.close()
            return None
        elif event == "-ACCEPT-":
                if stats_input(person_layout) is not None:
                    window_popup.close()
                    return stats_input(person_layout)

def create_window_payment():
    payment_layout = [
            [sg.Text("Person ID"),sg.Input()],
            [sg.Text("Amount"),sg.Input()],
            [sg.Text("Date"),sg.Input()],
            [sg.Text("Venue"),sg.Input()],
            [sg.Text("Type"),sg.Input()],
            [sg.Button("confirm", key = "-ACCEPT-"), sg.Button("cancel", key= "-CLOSE-")]
            ]
            
    window_popup = sg.Window("Input Person data!", payment_layout)
    while True:
        event,values = window_popup.read()
        if event == "-CLOSE-" or event == sg.WIN_CLOSED:
            window_popup.close()
            return None
        elif event == "-ACCEPT-":
            if payment_input(payment_layout) is not None:
                window_popup.close()
                return payment_input(payment_layout)

def create_window_total_search():
    search_layout = [
            [sg.Text("Category "),sg.Input()],
            [sg.Text("Max price "),sg.Input()],
            [sg.Text("Min price"),sg.Input()],
            [sg.Text("From date "),sg.Input()],
            [sg.Text("To date "),sg.Input()],
            [sg.Text("Person  "),sg.Input()],
            [sg.Text("Venue "),sg.Input()],
            [sg.Button("confirm", key = "-ACCEPT-"), sg.Button("cancel", key= "-CLOSE-")]
            ]
            
    window_popup = sg.Window("Input search filters!", search_layout)
    while True:
        event,values = window_popup.read()
        if event == "-CLOSE-" or event == sg.WIN_CLOSED:
            window_popup.close()
            return None
        elif event == "-ACCEPT-":
                if search_input(search_layout) is not None:
                    window_popup.close()
                    return search_input(search_layout)

def stats_input(person_layout):
        person_name = person_layout[0][1].get()
        try:
            person_checked = validate_positive_int_gui(person_name)
        except pydantic.error_wrappers.ValidationError:
            return None
        return person_checked

def search_input(search_layout):
        category = search_layout[0][1].get()
        max_price = search_layout[1][1].get()
        min_price = search_layout[2][1].get()
        date_old = search_layout[3][1].get()
        date_new = search_layout[4][1].get()
        person_id = search_layout[5][1].get()
        venue = search_layout[6][1].get()
        try:
            if category == "":
                category_checked = None
            else:
                category_checked = validate_words_gui(category)
        except pydantic.error_wrappers.ValidationError:
            return None
        try:
            if venue == "":
                venue_checked = None
            else:
                venue_checked = validate_words_gui(venue)
        except pydantic.error_wrappers.ValidationError:
            return None
        try:
            if max_price == "":
                max_price_checked = None
            else:
                max_price_checked = validate_positive_int_gui(max_price)
        except pydantic.error_wrappers.ValidationError:
            return None
        try:
            if min_price == "":
                min_price_checked = None
            else:
                min_price_checked = validate_positive_int_gui(min_price)
        except pydantic.error_wrappers.ValidationError:
            return None
        try:
            if date_old == "":
                date_old_checked = None
            else:
                date_old_checked = validate_date_gui(date_old)
        except pydantic.error_wrappers.ValidationError:
            sg.popup(custom_text= "'From date' has to be yyyy-mm-dd format")
            return None
        try:
            if date_new == "":
                date_new_checked = None
            else:
                date_new_checked = validate_date_gui(date_new)
        except pydantic.error_wrappers.ValidationError:
            sg.popup(custom_text= "'Up to date' has to be yyyy-mm-dd format")
            return None
        try:
            if person_id == "":
                person_id_checked = None
            else:
                person_id_checked = validate_positive_int_gui(person_id)
        except pydantic.error_wrappers.ValidationError:
            return None
        return category_checked, max_price_checked, min_price_checked, date_old_checked, date_new_checked, person_id_checked, venue_checked

def person_input(person_layout):
    # name, job, limit, birthday, months_of_grace
        name = person_layout[0][1].get()
        job = person_layout[1][1].get()
        limit = person_layout[2][1].get()
        birthday = person_layout[3][1].get() 
        months_of_grace = person_layout[4][1].get()

        try:
            name_checked = validate_words_gui(name)
        except pydantic.error_wrappers.ValidationError:
            return None
        try:
            limit_checked = validate_positive_int_gui(limit)
        except pydantic.error_wrappers.ValidationError:
            return None
        try:
            grace_checked = validate_positive_int_gui(months_of_grace)
        except pydantic.error_wrappers.ValidationError:
            return None
        try:
            job_checked = validate_words_gui(job)
        except pydantic.error_wrappers.ValidationError:
            return None
        try:
            birthday_checked = validate_date_gui(birthday)
        except pydantic.error_wrappers.ValidationError:
            sg.popup(custom_text= "date has to be yyyy-mm-dd format")
            return None

        return name_checked, job_checked, limit_checked, birthday_checked, grace_checked

def payment_input(person_layout):
        person_id = person_layout[0][1].get()
        amount = person_layout[1][1].get()
        date = person_layout[2][1].get()
        venue = person_layout[3][1].get()
        buy_type = person_layout[4][1].get()

        try:
            id_checked = validate_positive_int_gui(person_id)
        except pydantic.error_wrappers.ValidationError:
            return None
        try:
            date_checked = validate_date_gui(date)
        except (pydantic.error_wrappers.ValidationError, ValidationErr):
            sg.popup(custom_text= "date has to be yyyy-mm-dd format")
            return None
        try:
            amount_checked = validate_positive_int_gui(amount)
        except pydantic.error_wrappers.ValidationError:
            return None
        try:
            type_checked = validate_words_gui(buy_type)
        except pydantic.error_wrappers.ValidationError:
            return None
        try:
            venue_checked = validate_words_gui(venue)
        except pydantic.error_wrappers.ValidationError:
            return None

        return id_checked, amount_checked, date_checked, venue_checked, type_checked

def main_window():
    file_list_column = [
        [
            sg.Button("", key= "-PERSON-"),
            sg.Text("add person"),
            
            sg.Button("", key= "-PAYMENT-"),
            sg.Text("add payment"),

            sg.Button("", key= "-SEARCH-"),
            sg.Text("search through payments"),

            sg.Button("", key= "-STATS-"),
            sg.Text("print user stats"),

            sg.Button("", key= "-USERS-"),
            sg.Text("print users"),

            # sg.Button("", key= "-POP-"),
            # sg.Text("populate database"),

            # sg.Button("", key= "-RESET-"),
            # sg.Text("RESET database"),
        ],
    ]

    layout = [
        [
            sg.Column(file_list_column),
        ]
    ]

    window = sg.Window("Budgeting tool", layout)

    finance_database = DataBase()
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            window.close()
            break

        if event == "-PERSON-":
            popup = create_window_person()
            if popup is not None:
                name, job, limit, birthday, months_of_grace = popup
                query = finance_database.insert_person_gui(name, job, limit, birthday, months_of_grace)
                finance_database.execute_query(query)
                sg.popup(custom_text= "Person entry added succesfuly", no_titlebar=True)
        
        if event == "-PAYMENT-":
            popup = create_window_payment()
            if popup is not None:
                id_checked, amount_checked, date_checked, venue_checked, type_checked = popup
                query = finance_database.insert_payment_gui(id_checked, amount_checked, date_checked, venue_checked, type_checked)
                finance_database.execute_query(query)
                sg.popup(custom_text= "Payment entry added succesfuly", no_titlebar=True)
        
        if event == "-SEARCH-":
            search_results = ""
            popup = create_window_total_search()
            if popup is not None:
                category_checked, max_price_checked, min_price_checked, date_old_checked, date_new_checked, person_id_checked, venue_checked = popup
                query = finance_database.apply_filters_gui(category_checked, max_price_checked, min_price_checked, date_old_checked, date_new_checked, person_id_checked, venue_checked)
                for item in finance_database.read_query(query):
                    search_results += f"{item}\n"
                sg.popup(search_results)
        
        if event == "-USERS-":
            search_results = "ID / NAME / INCOME / LIMIT\n"
            query = "SELECT * FROM person"
            for item in finance_database.read_query(query):
                search_results += f"{item}\n"
            sg.popup(search_results)
        
        if event == "-STATS-":
            popup = create_window_stats()
            if popup is not None:
                sg.popup(finance_database.return_advice_gui(popup))

        # if event == "-POP-":
        #     pop_person = """
        #         INSERT INTO person(person_name, monthly_income, spending_limit) 
        #         VALUES
        #         ('Maciej', '9000', '2000'),
        #         ('Oliwia', '2400','2000'),
        #         ('Blazej', '3500','1500');
        #         """
        #     pop_payment = """
        #         INSERT INTO payment(person_id, date, amount, type) 
        #         VALUES
        #         ( 1, '2020-08-20', 350, 'equipment'),
        #         ( 1, '2020-08-21', 450, 'food'),
        #         ( 1, '2020-08-22', 150, 'growth'),
        #         ( 2, '2020-08-23', 650, 'equipment'),
        #         ( 2, '2020-08-20', 350, 'food'),
        #         ( 2, '2020-08-21', 450, 'growth'),
        #         ( 3, '2020-08-22', 150, 'equipment'),
        #         ( 3, '2020-08-23', 650, 'food'),
        #         ( 1, '2020-08-20', 650, 'equipment'),
        #         ( 1, '2020-08-21', 150, 'food'),
        #         ( 1, '2020-08-22', 2150, 'growth'),
        #         ( 2, '2020-08-23', 62130, 'equipment'),
        #         ( 2, '2020-08-20', 320, 'food'),
        #         ( 2, '2020-08-21', 450, 'growth'),
        #         ( 3, '2020-08-22', 1150, 'equipment'),
        #         ( 3, '2020-08-23', 6150, 'food')"""

        #     finance_database.execute_query(pop_person)
        #     finance_database.execute_query(pop_payment)
        
        # if event == "-RESET-":
        #     finance_database.execute_query("DROP TABLE payment")
        #     finance_database.execute_query("DROP TABLE person")
        #     create_person_table = """
        #     CREATE TABLE person (
        #     person_id INT PRIMARY KEY AUTO_INCREMENT,
        #     person_name TEXT NOT NULL,
        #     monthly_income INT NOT NULL,
        #     spending_limit INT
        #     );
        #     """

        #     create_payment_table = """
        #     CREATE TABLE payment (
        #     payment_id INT PRIMARY KEY AUTO_INCREMENT,
        #     person_id INT,
        #     date DATE,
        #     amount INT,
        #     type TEXT,
        #     FOREIGN KEY (person_id) REFERENCES person(person_id)
        #     );
        #     """
        #     finance_database.execute_query(create_person_table)
        #     finance_database.execute_query(create_payment_table)
main_window()