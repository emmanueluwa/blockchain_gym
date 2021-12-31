from brownie import accounts, config, SimpleStorage, network

# nice architecture to have all deployment logic in individual function
def deploy_simple_storage():
    ##using ganache built-in local accounts 
    account = get_account()
    #using brownie to deploy contract, stating which account is being used to deploy it, transaction function so change is made to 
    #blockchain
    simple_storage = SimpleStorage.deploy({"from": account})
    #call(view) function, no change made, no from account value needed
    stored_value = simple_storage.retrieve()
    print(stored_value)
    # using the store function in contract to changed stored value in contract
    transaction = simple_storage.store(15, {"from": account})
    # Good practice to wait for block confirmation(aka: receipt)
    transaction.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print("Updated stored value: " + str(updated_stored_value))



    ###Ways to access account
    ##encrypted command line
    # account = accounts.load("codecamp")
    # print(account)
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)

def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])




# defining a function to run 
def main():
    deploy_simple_storage()
