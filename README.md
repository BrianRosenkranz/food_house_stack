






bugs
1) The values from my csv file came empty. Solution create a new csv file and new repository.
2) Pandas came with the wrong values because it function. Solution was the atrributre together wiht gspread. pd.dataframe(value.gett all records)** corregir aca
3)The numbers from the data frame must be a list. to list and also the one from the input.
4) list inside a list after retrieving the numbers in the input and appending it to list from the sheet. sol: for in iterate. and update the columns
5)Just updated stack, not all of them. Function to update all when called
6) for the estimate budget the number from stock sheet was retrieve as int and when converted to float, it was just adding a ,0. The solution was changing the google sheet formats and divided wiht python by 10.
7)Everytime there is a validation process, the instrucction and the table was printed. To fixed this a new function was created.
8)Infinite loop with the welcome_app function. Solution. Taking the function out of main() and placing the welcome app funcion.
9) By creating a new function to print the instruccions and the table, the table cells were not clearing. To solve i put the print table statement in the main function.


91: E501 line too long (90 > 79 characters)
140: E501 line too long (100 > 79 characters)
146: E501 line too long (82 > 79 characters) because of indentation.