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


# variables i am goin to need later on


def input_used_per_week():
    """
    While loop for the user until the input data is correct
    This function should input the numbers to the terminal.
    Contains the validation funtion.
    """
    while True:
        print('Please use the table printed in the terminal to fill the 22 rows, with a comma after the numberr. By not so, it will come with an error.')
        print('Please have the terminal as max with as possible because it will print all the table.')
        print('The input is below the table')
        print(dataframe_stack)
        data_per_week = input('Enter your numbers here:\n')
        data_per_week_list = data_per_week.split(",")
        if validate_input(data_per_week_list):
            break
    return data_per_week_list



def validate_input(data):
    """
    Function to validate input. Input given  can not be strings or less or more values than 22.
    """
    try:
        [int(num) for num in data]
        if len(data) != 22:
            if data == 'string':
                raise ValueError(
                    f'You provided a string value, just are numbers requiered, you provided {data}')
            raise ValueError(
                f'Exactly 22 numbers requiered, you provided {len(data)} '
            )
    except ValueError as e:
        print(f'Other than number, other valus is not permited. Your data is {e}\n')
        return False
    return True
        

def update_sheet(data,cell_target,sheet):
    """
    Function to convert our used per week in to list
    Change the empy list with the inputed numbers
    This will always update the sheet, erase the old numbers.
    """
    print(f'updating {sheet}...\n')
    cell_list = sheet.range(cell_target)
    cell_values = data # replace this with a list of 22 values

    for i, val in enumerate(cell_values):  #gives us a tuple of an index and value
        cell_list[i].value = val    #use the index on cell_list and the val from cell_values

    sheet.update_cells(cell_list)
    print(f'{sheet} updated successfully\n')

dataframe_stack = pd.DataFrame(stack.get_all_records())
col_list_stack = dataframe_stack["Used per week"].values.tolist()


input_num = input_used_per_week()

def transform_numbers(value, col_list):
    numbers=[int(numbers) for numbers in value]
    col_list.clear()
    col_list=[]
    col_list.append(numbers)
    for x in col_list:
        new_numbers=x
    return new_numbers

update_sheet(transform_numbers(input_num, col_list_stack), 'J2:J23',stack)
update_sheet(transform_numbers(input_num, col_list_stack), 'G2:G23',remain)
update_sheet(transform_numbers(input_num, col_list_stack), 'I2:I23',budget)