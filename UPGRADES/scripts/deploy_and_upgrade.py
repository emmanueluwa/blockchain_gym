from scripts.helpful_scripts import get_account, encode_function_data
from brownie import network, Box, ProxyAdmin, TransparentUpgradeableProxy, Contract

def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    #implementation contract
    box = Box.deploy({"from": account})

    # setting contract as proxy admin
    proxy_admin = ProxyAdmin.deploy({"from": account})

    # connecting to proxy, 1. encode initialiser function
    initializer = box.store, 1
    #calling function for transparent upgradeable proxy, function empty = no initializer
    box_encoded_initializer_function = encode_function_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        #helps to add gas limit
        {"from": account, "gas_limit": 1000000},
    )
    print(f"Proxy deployed to {proxy}, you can now upgrade to v2!")
    #proxy address could change, assigning proxy address the abi of box contract e.g pointer in C
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    transaction_store = proxy_box.store(1, {"from": account})
    transaction_store.wait(1)

    # upgrading from v1 to v2 w increment function
    


