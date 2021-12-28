#deploying solidity smart contract

from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

# importing .env into script
load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    
install_solc("0.6.0")
# compiling solidity code 
compiled_sol = compile_standard(
  {
      "language": "Solidity",
      "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
      "settings": {
          "outputSelection": {
              "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]}
          }
      },
  },
  solc_version="0.6.0",
)

#saving compiled solidity in a json file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

#getting bytecode to allow deployment
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

#get  abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# using HTTPProvider//RPC Provider(RemoteProcedureCall, aka: Set of rules for interaction) 
# to connect to ganache blockchain simulation
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x7838982b1eC9888078f71702E51B9a2C8dCC4b3C"
private_key = os.getenv("PRIVATE_KEY")

# Creating the smart contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

###1. Building the transaction ###STEPS FOR DEPLOYING CONTRACT
# Getting the latest transaction number 
nonce = w3.eth.getTransactionCount(my_address)
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce, "gasPrice": w3.eth.gas_price,}
)

###2. Signing the transaction
signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)

###3. Sending signed transaction to blockchain
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
# Good practice to wait for blovk confirmation(aka: receipt)
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

# Working with contracts [prerequisites:contract address and ABI]
simple_storage = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)

#initial favourite no.
print(simple_storage.functions.retrieve().call())

# Building a transaction to store value in contract
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1, "gasPrice": w3.eth.gas_price,}
)
#signing transaction
signed_store_transaction = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
#sending transaction
store_transaction_hash = w3.eth.send_raw_transaction(signed_store_transaction.rawTransaction)
store_transaction_receipt = w3.eth.wait_for_transaction_receipt(store_transaction_hash)

print(simple_storage.functions.retrieve().call())

