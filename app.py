from GUI import *
from main_code import *

finance_database = DataBase()
main_window()
while True:
    command = finance_database.get_input()
    if command == "Q":
        break
    else:
        finance_database.execute_command(command)