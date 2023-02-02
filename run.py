# import pandas to work with dataframe
import pandas as pd
# import gspreads to work with google sheets and API
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPE_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)
# get the spread sheet
SHEET = GSPREAD_CLIENT.open("house_food_stack")
# get the worksheets in to variables
stack = SHEET.worksheet("stack")
consume = SHEET.worksheet("consume")
remain = SHEET.worksheet("remain")
budget = SHEET.worksheet("budget")
# get the values from the worksheet variables.
stack_list = stack.get_all_values()
consume_list = consume.get_all_values()
remain_list = remain.get_all_values()
budget_list = budget.get_all_values()

# the value worksheets in to dataframe with pandas
df_stack = pd.DataFrame(stack_list)
df_consume = pd.DataFrame(consume_list)
df_remain = pd.DataFrame(remain_list)
df_budget = pd.DataFrame(budget_list)




dataframe = pd.DataFrame(stack.get_all_records())


def input_used_per_week():
    """
    This function should input the numbers to the terminal,
    """
    print('Please use the table printed in the terminal to fill the 22 rows. By not so, it will come with an error.')
    print('Please have the terminal as max with as possible because it will print all the table.')
    print('The input is below the table')
    print(dataframe)
    data_per_week= input('Enter your numbers here:\n')
    print(f'The information provided is: {data_per_week}')

    

input_used_per_week()