from scripts.helpful_scripts import get_account
from brownie import interface, config, network

def main():
    get_weth()

def get_weth():
    """
      MINTS WETH BY DEPOSITING ETH
    """
    # abi
    # address
    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    transaction = weth.deposit({"from": account, "value": 0.1 * 10 ** 18})
    transaction.wait(1)
    print("Received 0.1 Weth")
    return transaction

