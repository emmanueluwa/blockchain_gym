from brownie import (
    network,
    accounts,
    config
)

LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "ganache",
    "development",
    "hardhat"
]
NON_FORKED_LOCAL_BLOCKCHAIN = ["mainnet-fork"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])

contract_to_mock = {"link_token": LinkToken, "vrf_coordinator": VRFCoordinatorMock}

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    if network.show_active() in config["networks"]:
      return accounts.add(config["wallets"]["from_key"])
    return None


#if mock should be used or an actual contract
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

# used to deploy mocks to testnet
def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks...")
    account = get_account()

