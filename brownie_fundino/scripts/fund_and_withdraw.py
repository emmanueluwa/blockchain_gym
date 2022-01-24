#script used to fund and withdraw
from brownie import Fundino
from scripts.helpful_scripts import get_account

def fundino():
    fundino_me  = Fundino[-1]
    #account needed when making state changes 
    account = get_account()
    entrance_fee = fundino_me.getEntranceFee()
    print(entrance_fee)
    print(f"The current entry fee is {entrance_fee}")
    print("Funding")
    # low level transaction data sent w transactions and function calls
    fundino_me.fund({"from": account, "value": entrance_fee})

def withdraw():
    fundino_me = Fundino[-1]
    account = get_account()
    fundino_me.withdraw({"from": account})

def main():
    fundino()
    withdraw()

