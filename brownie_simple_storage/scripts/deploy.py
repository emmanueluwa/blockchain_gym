from brownie import accounts, config 

# nice architecture to have all deployment logic in individual function
def deploy_simple_storage():
    ##using ganache built-in local accounts 
    account = accounts[0]
    print(account)
    ##encrypted command line
    # account = accounts.load("codecamp")
    # print(account)
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)


# defining a function to run 
def main():
    deploy_simple_storage()
