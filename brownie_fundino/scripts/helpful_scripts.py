from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "genache-local"]

DECIMALS = 18
STARTING_PRICE = 2000

def get_account():
    #choose account based on if the network is in dev mode or not
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    # only us mock if there isn't one already, it is a list of mocks deployed therefore
    if len(MockV3Aggregator) <= 0:
        #using v3 mock requires deciamls and initial ans
        MockV3Aggregator.deploy(DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_account()})
    print("Mocks Deployed")