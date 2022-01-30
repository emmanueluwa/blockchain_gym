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


def upgrade(
  account,
  proxy,
  new_implementation_address,
  proxy_admin_contract=None,initializer=None,
  *args
):
  transaction = None
  if proxy_admin_contract:
      if initializer:
          encoded_function_call = encode_function_data(initializer, *args)
          transaction = proxy_admin_contract.upgradeAndCall(
              proxy.address,
              new_implementation_address,
              encoded_function_call,
              {"from": account},
          )
      else:
          transaction = proxy_admin_contract.upgrade(
              proxy.address, new_implementation_address, {"from": account}
          )
  else:
      #if no proxy admin contract
      if initializer:
          encoded_function_call = encode_function_data(initializer, *args)
          # we can call directly from proxy contract
          transaction = proxy.upgradeToAndCall(
              new_implementation_address, encoded_function_call, {"from": account}
          )
      else:
          transaction = proxy.upgradeTo(new_implementation_address, {"from": account})
  return transaction
