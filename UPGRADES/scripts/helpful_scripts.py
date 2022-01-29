from brownie import accounts, network, config
import eth_utils
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache"]


def get_account(index=None):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if network:
        return accounts[index]
    if network.show_active() in config["networks"]:
        return accounts.add(config["wallets"]["from_key"])
    if id:
        return accounts.load(id)
    return None

# e.g initializer = box.store, 1 2 3 4, encoding into bytes tells smart contract the function to call
def encode_function_data(initializer=None, *args):
    #if length of args is 0, there will be issues
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    ## we can use inbuilt brownie function
    return initializer.encode_input(*args) # bytes
