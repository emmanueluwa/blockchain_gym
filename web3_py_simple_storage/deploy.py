#deploying solidity smart contract

from solcx import compile_standard, install_solc
import json

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
              "*": {"*": ["abi", "metadata", "evn.bytecode", "evm.sourceMap"]}
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
