# import pandas to work with dataframe and printed in the table.
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

# variables I am going to need for input_used_per_week
# To print the table in the terminal. 
# Fetched from Pandas.
dataframe_stack = pd.DataFrame(stack.get_all_records())
col_list_stack = dataframe_stack["Used per week"].values.tolist()

# variables i am goin to need for amount_remain_update
# This will be used after the project to develop the app further.
dataframe_content = pd.DataFrame(stack.get_all_records())
dataframe_storage = pd.DataFrame(stack.get_all_records())
dataframe_remain = pd.DataFrame(remain.get_all_records())


# get the values from the worksheet variables.
# create a function later on
stack_list = stack.get_all_values()
consume_list = consume.get_all_values()
remain_list = remain.get_all_values()
budget_list = budget.get_all_values()

# the value worksheets in to dataframe with pandas
# This will be used after the project to develop the app further.
df_stack = pd.DataFrame(stack_list)
df_consume = pd.DataFrame(consume_list)
df_remain = pd.DataFrame(remain_list)
df_budget = pd.DataFrame(budget_list)

# Welcomes the app.
def welcome_app():
    """
    This function will welcome the user.
    Validate the data
    Or exit the app if the user decides not to continue.
    """
    print('Welcome to the house food stack app\n')
    start = input('Will you like to start?\n Only yes or no allowed\n')
    while True:
        if start == 'yes':
            main()
        elif start == 'no':
            print('App will exit\n')
            exit()
            return False
        else:
            validate_start(start)
            print('Please try again...\n')
            welcome_app()
    return start

# Validates the input from welcome app.
def validate_start(data):
    """
    The function is to validate input.
    The input given must be strings. Yes or no answer.
    Other than that, an error will appear in the terminal.
    """
    try:
        if data != 'yes':
            raise ValueError(
                f'you provided {data}')
    except ValueError as e:
        print(
            f'Yes or no is required, other valus is not permited. You provided {data}.\n')
        print('Please try again...\n')
        welcome_app()
        return False
    return True


# Clear the cells.
def clear_cell(cell_target, sheet):
    """
    The function will clear the old cells from the worksheet.
    The update function will also update cells.
    """
    sheet.batch_clear([cell_target])


# Print table and instructions
def print_instructions():
    """
    Instructions are added for a better understanding of the app.
    
    """
    print('Please have the terminal as max with as possible because')
    print('it will show all the table.')
    print('The input area will be below the table.\n')
    print('Please write 22 numbers separated by a comma.')
    print("For the purpose of the project, I'll leave an example\n")
    print('2,5,1,2,4,7,0,4,0,3,2,1,0,1,1,1,0,4,3,0,0,45\n')
    

# Inputs the numbers
def input_used_per_week():
    """
    While loop for the user until the input data is correct
    This function should input the numbers to the terminal.
    Contains the validation function.
    """
    while True:
        data_per_week = input('Enter your numbers here:\n')
        data_per_week_list = data_per_week.split(",")
        if validate_input(data_per_week_list):
            break
    return data_per_week_list

# Validate the numbers from the input.
# Code from Code Institute modules.
def validate_input(data):
    """
    The function is to validate input.
    Input given can not be strings.
    Input must be 22 numbers. Less or more will show an error.
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
        print(
            f'Other than number, other valus is not permited. Your data is {e}\n')
        return False
    return True


# This code was created together with Kevin, CI tutor.
# Upadtes the the sheets
def update_sheet(data, cell_target, sheet):
    """
    Function to convert our used per week in to list
    Change the empy list with the inputed numbers
    This will always update the sheet, erase the old numbers.
    """
    print(f'updating {sheet}...\n')
    cell_list = sheet.range(cell_target)
    cell_values = data

    for i, val in enumerate(cell_values):
        cell_list[i].value = val

    sheet.update_cells(cell_list)
    print(f'{sheet} updated successfully\n')

# Clears the list got it from the pandas.
def transform_numbers_and_clear(value, col_list):
    """
    This function is to get all numbers from the list, erase there values
    and change itth the new input values, if needed.
    The reason for this is because data from the sheet came as an
    empty list of strings.
    For purpose of the project,
    is created to show the knowledge adquiered but you dont need it,
    because the update function will erase the data and store the new one.
    """
    numbers = [int(numbers) for numbers in value]
    col_list.clear()
    col_list = []
    col_list.append(numbers)
    for x in col_list:
        new_numbers = x
    return new_numbers


# The "zip" was taken from CI modules.
def collect_update_remain_sheet(column_numbers):
    """
    This function will collect, do mathematical ecuation
    and return the number to place in Amount remain cell in the remain sheet.
    Positive numbers indicates there is still food stack left.
    Negative numbers indicates storage is empty and/or
    extra was bought during the week.
    """
    col_list_storage = dataframe_stack["Amount in storage"].values.tolist()
    col_list_content = dataframe_content["Content"].values.tolist()
    remain_numbers = []
    mult_content = []
    for used, content in zip(column_numbers, col_list_content):
        multiplication = used * content
        mult_content.append(multiplication)
    for storage, mult in zip(col_list_storage, mult_content):
        subtraction = storage - mult
        remain_numbers.append(subtraction)
    return remain_numbers

# Changes int64 to float
def change_int_to_float():
    """
    All the numbers coming from the list of price is an int64.
    We need to convert to float and then divided by 10.
    For the estimate_budget function to work.
    """
    col_list_price = dataframe_stack["Price €"].values.tolist()

    dataframe_stack["Price €"] = dataframe_stack["Price €"].astype("float")
    quotients = []
    for number in col_list_price:
        quotients.append(number / 10)
    return quotients

# The "zip" was taken from CI modules.
def estimate_budget(column_numbers):
    """
    Het the numbers from Google sheet
    Function to estimate budget and return the value.
    """
    float_num = change_int_to_float()
    col_list_content = dataframe_content["Content"].values.tolist()
    col_list_portion = dataframe_stack["Portions"].values.tolist()
    budget_numbers = []
    mult_num = []
    price_num = []
    for used, portion in zip(column_numbers, col_list_portion):
        multiplication = used * portion
        mult_num.append(multiplication)
    for price, mult in zip(float_num, mult_num):
        mult = price * mult
        price_num.append(mult)
    for content, division in zip(col_list_content, price_num):
        div = division / content
        budget_numbers.append(div)
    return budget_numbers

# Runs the app except the welcome app.
def main():
    """
    This function will run all the function, if yes was inputed, except the
    welcome_app().
    """
    clear_cell('J2:J23', stack)
    clear_cell('G2:G23', remain)
    clear_cell('I2:I23', budget)
    print(dataframe_stack)
    print_instructions()
    input_num = input_used_per_week()
    used_week_numbers = transform_numbers_and_clear(input_num, col_list_stack)
    remain_num = collect_update_remain_sheet(used_week_numbers)
    budget_numbers = estimate_budget(used_week_numbers)
    update_sheet(used_week_numbers, 'J2:J23', stack)
    update_sheet(remain_num, 'G2:G23', remain)
    update_sheet(budget_numbers, 'I2:I23', budget)
    print('You have finished. All sheet are up to date')
    print('The app will exit now.')
    exit()

# Welcome_app is here to avoid infinite loop. Bug fix
welcome_app()
main()
