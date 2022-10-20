from tkinter import Entry
import PySimpleGUI as sg
import pandas as pd


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
            [sg.Button("", key="-JOB-"),sg.Text("Job stats")],
            [sg.Button("", key="-CURRENT-"),sg.Text("Available money")],
            [sg.Button("", key="-CATEGORY-"),sg.Text("Category stats")],
            [sg.Button("", key="-VENUE-"),sg.Text("Popular venues")],
            [sg.Button("", key="-PERSONAL-"),sg.Text("Personal summary")],
            [sg.Button("cancel", key= "-CLOSE-")]
            ]
            
    window_popup = sg.Window("choose a person!", person_layout)
    while True:
        event,values = window_popup.read()
        if event == "-CLOSE-" or event == sg.WIN_CLOSED:
            window_popup.close()
            return None
        elif event == "-JOB-":
            window_popup.close()
            return "-JOB-"
        elif event == "-CURRENT-":
            window_popup.close()
            return "-CURRENT-"
        elif event == "-CATEGORY-":
            window_popup.close()
            return "-CATEGORY-"
        elif event == "-VENUE-":
            window_popup.close()
            return "-VENUE-"
        elif event == "-PERSONAL-":
            window_popup.close()
            return "-PERSONAL-"


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

def result_text_window(result):

    layout = [
                [sg.Multiline(default_text=result,size=(70,20))],
                [sg.Button("close",key="-EXIT-")]
                ]
    result_window = sg.Window("Results", layout)
    while True:
        event, values = result_window.read()
        if event == "-EXIT-" or event == sg.WIN_CLOSED:
            result_window.close()
            break

def stat_date_choice():
    layout = [
        [sg.Button("yearly", key = "-Y-")],
        [sg.Button("monthly", key = "-M-")],
        [sg.Button("daily", key = "-D-")]
    ]
    choice_window = sg.Window("Choose time format!", layout)
    while True:
        event, values = choice_window.read()
        if event == "-Y-" or event == sg.WIN_CLOSED:
            choice_window.close()
            return 'y'
        elif event == "-M-":
            choice_window.close()
            return 'm'
        elif event == "-D-":
            choice_window.close()
            return 'd'

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
            popup = create_window_total_search()
            if popup is not None:
                category_checked, max_price_checked, min_price_checked, date_old_checked, date_new_checked, person_id_checked, venue_checked = popup
                query = finance_database.apply_filters_gui(category_checked, max_price_checked, min_price_checked, date_old_checked, date_new_checked, person_id_checked, venue_checked)
                dt = pd.read_sql_query(query,finance_database.engine)
                dt_str = dt.to_string()
                result_text_window(dt_str)
        
        if event == "-USERS-":
            query = "SELECT * FROM person"
            dt = pd.read_sql_query(query,finance_database.engine)
            result_text_window(dt)
            
        
        if event == "-STATS-":
            popup = create_window_stats()
            if popup is not None:
                if popup == "-JOB-":
                    variant = stat_date_choice()
                    finance_database.job_stats(variant)
                if popup == "-CURRENT-":
                    finance_database.money_stats()
                if popup == "-CATEGORY-":
                    finance_database.category_stats()
                if popup == "-VENUE-":
                    finance_database.venue_stats()
                if popup == "-PERSONAL-":
                    pass



main_window()