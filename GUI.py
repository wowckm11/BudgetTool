from distutils.cmd import Command
from tkinter import Entry
import PySimpleGUI as sg
import os.path
from main_code import *

def create_window_person():
    person_layout = [
            [sg.Text("Person Name"),sg.Input()],
            [sg.Text("Monthly Income"),sg.Input()],
            [sg.Text("Spending limit"),sg.Input()],
            [sg.Button("confirm", key = "-ACCEPT-"), sg.Button("cancel", key= "-CLOSE-")]
            ]
            
    window_popup = sg.Window("Input Person data!", person_layout)
    while True:
        event,values = window_popup.read()
        if event == "-CLOSE-":
            window_popup.close()
            return None
        elif event == "-ACCEPT-":
                if person_input(person_layout) is not None:
                    window_popup.close()
                    return person_input(person_layout)

def create_window_payment():
    payment_layout = [
            [sg.Text("Person ID"),sg.Input()],
            [sg.Text("Date"),sg.Input()],
            [sg.Text("Amount"),sg.Input()],
            [sg.Text("Type"),sg.Input()],
            [sg.Button("confirm", key = "-ACCEPT-"), sg.Button("cancel", key= "-CLOSE-")]
            ]
            
    window_popup = sg.Window("Input Person data!", payment_layout)
    while True:
        event,values = window_popup.read()
        if event == "-CLOSE-":
            window_popup.close()
            return None
        elif event == "-ACCEPT-":
                if payment_input(payment_layout) is not None:
                    window_popup.close()
                    return payment_input(payment_layout)

def person_input(person_layout):
        person_name = person_layout[0][1].get()
        monthly_income = person_layout[1][1].get()
        spending_limit = person_layout[2][1].get()
        try:
            person_checked = validate_positive_int_gui(person_name)
        except pydantic.error_wrappers.ValidationError:
            return None
        try:
            income_checked = validate_positive_int_gui(monthly_income)
        except pydantic.error_wrappers.ValidationError:
            return None
        try:
            spending_checked = validate_positive_int_gui(spending_limit)
        except pydantic.error_wrappers.ValidationError:
            return None
        return person_checked, income_checked, spending_checked

def payment_input(person_layout):
        person_id = person_layout[0][1].get()
        date = person_layout[1][1].get()
        amount = person_layout[2][1].get()
        buy_type = person_layout[3][1].get()
        try:
            id_checked = validate_positive_int_gui(person_id)
        except pydantic.error_wrappers.ValidationError:
            return None
        try:
            date_checked = validate_positive_int_gui(date)
        except pydantic.error_wrappers.ValidationError:
            sg.popup(custom_text= "date has to be yyyy-mm-dd format")
            return None
        try:
            amount_checked = validate_positive_int_gui(amount)
        except pydantic.error_wrappers.ValidationError:
            return None
        try:
            type_checked = validate_positive_int_gui(buy_type)
        except pydantic.error_wrappers.ValidationError:
            return None
        return id_checked, date_checked, amount_checked, type_checked


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
                person_name, monthly_income, spending_limit = popup
                query = finance_database.insert_person_gui(person_name, monthly_income, spending_limit)
                finance_database.execute_query(query)
                sg.popup(custom_text= "Person entry added succesfuly", no_titlebar=True)
        
        if event == "-PAYMENT-":
            popup = create_window_payment()
            if popup is not None:
                id_checked, date_checked, amount_checked, type_checked = popup
                query = finance_database.insert_payment_gui(id_checked, date_checked, amount_checked, type_checked)
                finance_database.execute_query(query)
                sg.popup(custom_text= "Payment entry added succesfuly", no_titlebar=True)

main_window()