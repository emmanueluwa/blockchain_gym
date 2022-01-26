from brownie import network, config, accounts, MockV3Aggregator, Contract, VRFCoordinatorMock, LinkToken, interface

#comma, names of networks
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "genache-local"]

def get_account(index=None, id=None):
    # accounts[0]
    # accounts.add("env")
    # accounts.load("id")
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])

contract_to_mock = {"eth_usd_price_feed": MockV3Aggregator, "vrf_coordinator": VRFCoordinatorMock, "link_token": LinkToken,}

# get a contract based on whether its deployed as a mock or if its a real contract
def get_contract(contract_name):
    """This function: Grab contract addresses from brownie config if defined, otherwise, 
    it will deploy a mock version of the contract, and return that contract. 
  
      Args:
          contract_name (string)

      Returns:
          brownie.network.contract.ProjectContract: The most recently deployed version
          of this contract.
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            # same as MockV3.. .length
            deploy_mocks()
        contract = contract_type[-1]
        # same as doing MockV3Aggre..[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        ## we need address and abi
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
        #MockV3Aggregator abi
    return contract


DECIMALS = 8
INITIAL_VALUE = 200000000000

def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Deployed")

def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000): #0.1 LINK
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    transaction = link_token.transfer(contract_address, amount, {"from": account})
    # same as above but using brownie interface instead
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # transaction = link_token_contract.transfer(contract_address, amount, {"from": account})
    transaction.wait(1)
    print("Fund contract")
    return transaction
