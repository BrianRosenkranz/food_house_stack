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

# variables i am goin to need for input_used_per_week
dataframe_stack = pd.DataFrame(stack.get_all_records())
col_list_stack = dataframe_stack["Used per week"].values.tolist()

# variables i am goin to need for amount_remain_update
dataframe_content = pd.DataFrame(stack.get_all_records())
dataframe_storage = pd.DataFrame(stack.get_all_records())
dataframe_remain = pd.DataFrame(remain.get_all_records())


# get the values from the worksheet variables.
#create a function later on
stack_list = stack.get_all_values()
consume_list = consume.get_all_values()
remain_list = remain.get_all_values()
budget_list = budget.get_all_values()

# the value worksheets in to dataframe with pandas
#erase if no need at the end of the project
df_stack = pd.DataFrame(stack_list)
df_consume = pd.DataFrame(consume_list)
df_remain = pd.DataFrame(remain_list)
df_budget = pd.DataFrame(budget_list)


def welcome_app():
    print('Welcome to the house food stack app\n')
    start= input('Will you like to start?')


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
        print("For the purpose of the project, I'll leave an example")
        print('2,5,1,2,4,7,0,4,0,3,2,1,0,1,1,1,0,4,3,0,0,45')
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


def transform_numbers_and_clear(value, col_list):
    """
    This function is to get all numbers from the list, erase there values
    and change it wiht the new input values, if needed.
    The reason for this is because data from the sheet came as an empty list of strings.
    For purpose of the project, is created to show the knowledge adquiered but you dont need it,
    because the update function will erase the data and store the new one.
    """
    numbers=[int(numbers) for numbers in value]
    col_list.clear()
    col_list=[]
    col_list.append(numbers)
    for x in col_list:
        new_numbers=x
    return new_numbers



def collect_update_remain_sheet(column_numbers):
    """
    This function will collect, do mathematical ecuation
    and return the number to place in Amount remain cell in the remain sheet.
    Positive numbers indicates there is still food stack
    Negative numbers indicates storage is empty and extra was bought during the week.
    """
    # numbers to mult
    col_list_storage = dataframe_stack["Amount in storage"].values.tolist()# numbers to subtract
    col_list_content = dataframe_content["Content"].values.tolist()
    remain_numbers=[]
    mult_content=[]
    for used, content in zip(column_numbers, col_list_content):
        multiplication= used  * content
        mult_content.append(multiplication)
    for storage, mult in zip(col_list_storage, mult_content):
        subtraction= storage - mult
        remain_numbers.append(subtraction)
    return remain_numbers

def change_int_to_float():
    """
    All the numbers coming from the list of price is an int64.
    We need to convert to float and then divided by 10.
    For the estimate_budget function to work.
    """

    col_list_price = dataframe_stack["Price €"].values.tolist()
    #print(dataframe_stack["Price €"].dtype)
    dataframe_stack["Price €"]=dataframe_stack["Price €"].astype("float")
    quotients = []
    for number in col_list_price:
        quotients.append(number / 10)
    return quotients

def estimate_budget(column_numbers):
    """
    Function to estimate budget.
    """
    float_num = change_int_to_float()
    col_list_content = dataframe_content["Content"].values.tolist()
    col_list_portion = dataframe_stack["Portions"].values.tolist()
    budget_numbers = []
    mult_num = []
    price_num = []
    for used, portion in zip(column_numbers, col_list_portion):
        multiplication= used  * portion
        mult_num.append(multiplication)
    for price, mult in zip(float_num, mult_num):
        mult= price * mult
        price_num.append(mult)
    for content, division in zip(col_list_content, price_num):
        div= division / content
        budget_numbers.append(div)
    return budget_numbers

def main():
    """
    This function will take all the function and start the programm,
    """
    welcome_app()
    input_num = input_used_per_week()
    used_week_numbers = transform_numbers_and_clear(input_num, col_list_stack)
    remain_num = collect_update_remain_sheet(used_week_numbers)
    budget_numbers=estimate_budget(used_week_numbers)
    update_sheet(used_week_numbers, 'J2:J23',stack)
    update_sheet(remain_num,'G2:G23',remain)
    update_sheet(budget_numbers,'J2:J23',budget)



welcome_app()