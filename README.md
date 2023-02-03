![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome BrianRosenkranz,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **August 17, 2021**

## Reminders

* Your code must be placed in the `run.py` file
* Your dependencies must be placed in the `requirements.txt` file
* Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

-----
Happy coding!




bugs
1) The values from my csv file came empty. Solution create a new csv file and new repository.
2) Pandas came with the wrong values because it function. Solution was the atrributre together wiht gspread. pd.dataframe(value.gett all records)** corregir aca
3)The numbers from the data frame must be a list. to list and also the one from the input.
4) list inside a list after retrieving the numbers in the input and appending it to list from the sheet. sol: for in iterate. and update the columns
5)Just updated stack, not all of them. Function to update all when called