import pytest
from project import main_step, create_user, check_exist_stock
import csv
import os

def test_main_step(monkeypatch):
    #check wheter the program exit when type unknown command 
    with pytest.raises(SystemExit):
        monkeypatch.setattr('builtins.input', lambda _: "4")
        main_step("valid_user")
    
    with pytest.raises(SystemExit):
        monkeypatch.setattr('builtins.input', lambda _: "One")
        main_step("valid_user")
    
def test_create_user():
    #check to see the function create a csv file and return it name
    assert create_user("kien.csv") == "kien.csv"
    assert os.path.exists("kien.csv")

def test_check_exist_stock():
    with open("kien.csv", "w", newline='') as test_file:
        writer = csv.DictWriter(test_file, fieldnames=["stock", "quantity", "cost"])
        writer.writeheader()
        writer.writerow({"stock": "MBB", "quantity": 1000, "cost": 20000})
        writer.writerow({"stock": "TCB", "quantity": 500, "cost": 10000})
    #check if run true with existed and non-existed stock
    assert check_exist_stock("kien.csv", "MBB") == True
    assert check_exist_stock("kien.csv", "ABC") == False