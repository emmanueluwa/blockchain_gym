from brownie import network, config, accounts 

def get_account():
    #choose account based on if the network is in dev mode or not
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
