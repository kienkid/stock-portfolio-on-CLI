# MY STOCK PORTFOLIO
#### Video Demo:  <https://youtu.be/haZ0zeL2He8>
#### Description:

**Welcome to My Stock Portfolio!**

This program is your personal assistant for managing, buying, selling, and tracking the profit/loss of your Vietnam stocks portfolio in real-time through command line interface (CLI).
This is my final project on CS50P course.

## Getting Started

1. **Run the Program**:
    - To start to program, first cd to your "database storage folder" and run the project.py file through a CLI with python3
    - First the program will ask for the database name. This will correspond to a CSV file having the same name which will store your portfolio data in the "database storage folder".
    - Simply input your username. If there isn't a CSV file with that name in the "database storage folder", you'll have the option to create a new database with the inputted name or retry.

2. **Login**:
    - If the username (database name) exists, you'll be logged in directly and proceed to main options.
    - If not, you can try a different name or create a new database with your desired username.
    - If you choose to create new database, a new csv file will be created with that inputted username and logged in with that username.

## Main Options

1. **Buy**:
    - Enter the stock code (for current price observation, please enter 3 letter code for Vietnam stocks), quantity, and price.
    - If the stock already exists in the database, the new buying quantity will be plus with the current quantity, and the average cost will be recalculated.
    - The database will be updated with the new information.

2. **Sell**:
    - Input the stock code, quantity, and price.
    - If the stock exists in the database, the selling quantity will be subtracted with the current quantity, and the realized profit/loss will be calculated and displayed.

3. **Show My Current Portfolio**:
    - This option prints out your current portfolio/database in a table.
    - It will show name, quantity, cost, current price (using the `vnstock` library to extract the nearest market price), absolute and percentage profit/loss figures (the programs will calculated it base on current price, cost and quantity) columns.

## How it Works

- All data is stored in a CSV file named after your username.
- Each buy and sell action updates the relevant information in a new cache CSV file called "cache_username" and then using it to overwrite the current "username" file. After that it will delete the cache file.
- The "Show My Current Portfolio" option find the latest market prices and gives you a snapshot of your holdings and performance.
- Exit the program by input any other keys when choosing options. 

**Note**: The program is just a beginning, further update will arrives in foreseen future if i have time, or maybe i will convert it into a application program. idk, let the future answer ==][==
