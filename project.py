import csv
import os
import sys
import pandas as pd
import tabulate
from vnstock import Vnstock

currency = "VND"

def main():
    valid_user = check_user(f"{input("Hi, please login with your user name: ")}.csv")
    print(f"Loging in as user: {valid_user[:-4]}")
    main_step(valid_user)
    
#main step and re-step with consequence_step(valid_user) if user want to continue trading    
def main_step(valid_user):
    step = input(f"What transaction you make today?\n1. Buy\n2. Sell\n3. Show me my portfolio\nAny other input to Exit program\n")
    if step == "1":
        stock = input("What you buying? ").upper()
        try:
            quantity = float(input("What's the quantity "))
            cost = float(input("What's the price "))
            buy(valid_user, stock, quantity, cost, f"cache_{valid_user}")
        except ValueError:
            print("The quantity / price must be number, please try again")
        consequence_step(valid_user)

    elif step == "2":
        stock = input("What you selling? ").upper()
        try:
            quantity = float(input("What's the quantity "))
            cost = float(input("What's the price "))
            sell(valid_user, stock, quantity, cost, f"cache_{valid_user}")
        except ValueError:
            print("The quantity / price must be number, please try again")
        consequence_step(valid_user)

    elif step == "3":
        check_portfolio(valid_user, f"cache_{valid_user}")
        consequence_step(valid_user)

    else:
        sys.exit("Exit program successful")

#recursion of step (repeat main step to user choose to continue trading or exit the program)
def consequence_step(valid_user):
    consequence_step = input(f"Anything else you want to do?\n1. Yes\n2. No, that all!\nAny other input to Exit program\n")
    if consequence_step == "1":
        main_step(valid_user)
    elif consequence_step == "2":
        sys.exit("See you tomorrow")
    else:
        sys.exit("Exit program successful")

#create new csv file / user for storage portfolio data and update header returning csv file name
def create_user(user):
    with open(user, "w",newline='') as portfolio_file:
        writer = csv.DictWriter(portfolio_file, fieldnames=["stock","quantity","cost"],)
        writer.writeheader()
    print("Creating user success")
    return user

#check whether the folder cd have the csv file name yet => if not found give user action to do (1. create the file with the inputted 2. retry prompt right user)
def check_user(user):
    file_exist = os.path.isfile(user)
    if file_exist == False:
        print("User is not exist, do you want to create new user with the inputted or try the right user name")
        step = input("1. Create new user with the inputted\n2. Retry\nAny other input to Exit program\n")
        if step == "1":
            create_user(user)
            return user
        elif step == "2":
            valid_user = check_user(f"{input("what your user?: ")}.csv")
            return valid_user
        else:
            sys.exit("Exit program successful")
    else:
        print("Login success!")
        return user

#Check existed stock in csv file => return Boolean
def check_exist_stock(user, stock):
    with open(user, "r",newline='') as portfolio_file:
        reader = csv.DictReader(portfolio_file)
        for row in reader:
            if row["stock"] == stock:
                return True
        return False

#Buy stock, if already exist in portfolio file => recalc the quantity and cost, call overwrite function, if new => append to portfolio file
def buy(portfolio, stock, quantity, cost, cache):
    if check_exist_stock(portfolio, stock):
        #Existed stock
        with open(portfolio, "r") as portfolio_file, open(cache, "w",newline='') as cache_file:
            reader = csv.DictReader(portfolio_file)
            writer = csv.DictWriter(cache_file, ["stock","quantity","cost"])
            writer.writeheader()
            for row in reader:
                try:
                    if row["stock"] == stock:
                        avg_cost = (float(quantity) * float(cost) + float(row["quantity"]) * float(row["cost"])) / (float(quantity) + float(row["quantity"]))
                        new_quantity = float(row["quantity"]) + float(quantity)
                        writer.writerow(
                        {
                            "stock": stock,
                            "quantity": new_quantity,
                            "cost": avg_cost
                        }
                    )
                        print(f"You just DCA {stock}, total quantity: {new_quantity:.2f}, average cost: {avg_cost:.2f} {currency}")
                    else:
                        writer.writerow(row)
                except IndexError:
                    pass
        overwrite(portfolio,cache)
    else:
        #New stock
        with open(portfolio, "a",newline='') as portfolio_file:
            writer = csv.DictWriter(portfolio_file, fieldnames=["stock","quantity","cost"],)
            writer.writerow(
                    {
                        "stock": stock,
                        "quantity": quantity,
                        "cost": cost
                    }
                )
            print(f"Buying {quantity:.2f} {stock} shares with price {cost:.2f} {currency}")
        

#sell stock, recalc quantity, call overwrite function, log the profit/loss into a txt file to keep track
def sell(portfolio, stock, quantity, price, cache):
    if check_exist_stock(portfolio, stock):
        with open(portfolio, "r") as portfolio_file, open(cache, "w",newline='') as cache_file:
            reader = csv.DictReader(portfolio_file)
            writer = csv.DictWriter(cache_file, ["stock","quantity","cost"])
            writer.writeheader()
            for row in reader:
                try:
                    if row["stock"] == stock:
                        if float(row["quantity"]) == float(quantity): #if sold out => not update the row in cache
                            pass
                        else:
                            writer.writerow(
                            {
                                "stock": stock,
                                "quantity": str(float(row["quantity"]) - float(quantity)),
                                "cost": row["cost"]
                            }
                    )
                        profit = (float(quantity) * (float(price)-float(row["cost"])))
                        print(f"You sold {quantity:.2f} {stock} at price {price:.2f} {currency}=> Realized profit/(loss) of {profit:.2f} {currency}")
                    else:
                        writer.writerow(row)
                except IndexError:
                    pass
        overwrite(portfolio,cache)
    else:
        #action when try to sell not existing stock
        print("You can't sell something you don't have (The next update will include derivatives)")


#Overwrite function to take data from cache file and then paste it to the 1st argument file, after that delete the cache file
def overwrite(portfolio, cache):
    with open(portfolio, "w",newline='') as updated_portfolio_file, open(cache, "r") as cache_file:
        writer = csv.writer(updated_portfolio_file)
        for row in csv.reader(cache_file):
            try:
                is_blank_row = row[1]
                writer.writerow(row)
            except IndexError:
                pass
    os.remove(cache)

#print out the current portfolio and unrealized gain/(loss)
def check_portfolio(portfolio, cache):
    portfolio_list = []

    #read portfolio file to list out the stock ID
    with open(portfolio, "r") as portfolio_file:
        reader = csv.reader(portfolio_file)
        for row in reader:
            if row[0] =="stock":
                pass
            else:
                portfolio_list.append(row[0])
    
    #using vnstock to find current price and return with a list of current price in order
    portfolio_current_price =  (Vnstock(show_log=False).stock().trading.price_board(symbols_list= portfolio_list)["match"]["match_price"]).tolist()   
    
    #add the current price list, calculated profit column in portfolio file and output is a cache file 
    df = pd.read_csv(portfolio)
    df["current price"] = portfolio_current_price
    df["unrealized profit/(loss)"] = ((df["current price"] - df["cost"]) * df["quantity"])
    df["unrealized(%) profit/(loss)"] = ((1 - (df["current price"] / df["cost"])) * 100)
    #fill word if can't found current price
    df["current price"] = df["current price"].fillna("Stock not marketable")
    df["unrealized profit/(loss)"] = df["unrealized profit/(loss)"].fillna("Stock not marketable")
    df["unrealized(%) profit/(loss)"] = df["unrealized(%) profit/(loss)"].fillna("Stock not marketable")
    #save into the file as output cache
    df.to_csv(cache, index=False)
    
    with open(cache, "r") as cache_file:
        reader = csv.reader(cache_file)
        print("Here is your current portfolio:")
        print(tabulate.tabulate(reader, headers="firstrow", tablefmt="outline"))
    #remove the cache file
    os.remove(cache)

if __name__ == "__main__":
    main()