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


# variables i am goin to need later on

dataframe = pd.DataFrame(stack.get_all_records())
col_list = dataframe["Used per week"].values.tolist()
# variables i am goin to need later on


def input_used_per_week():
    """
    This function should input the numbers to the terminal,
    """
    print('Please use the table printed in the terminal to fill the 22 rows, with a comma after the numberr. By not so, it will come with an error.')
    print('Please have the terminal as max with as possible because it will print all the table.')
    print('The input is below the table')
    print(dataframe)
    data_per_week = input('Enter your numbers here:\n')
    data_per_week_list = data_per_week.split(",")
    validate_input(data_per_week_list)


def validate_input(data):
    """
    Function to validate input. Input given  can not be strings or less or more values than 22.
    """
    try:
        if len(data) != 22:
            if data == 'string':
                raise ValueError(
                    f'You provided a string value, just are numbers requiered, you provided {data}')
            raise ValueError(
                f'Exactly 22 numbers requiered, you provided {len(data)} '
            )
    except ValueError as e:
        print(
            f'Other than number, other valus is not permited. Your data is {e}\n')


input_used_per_week()
