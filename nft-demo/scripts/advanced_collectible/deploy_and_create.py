from scripts.helpful_scripts import get_account, OPENSEA_URL, get_contract
from brownie import AdvancedCollectible, network, config

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"

def deploy_and_create():
    account = get_account()
    ## opensea market place currently works w rinkeby, prep for mocks to rinkeby or deployed contracts
    advanced_collectible = AdvancedCollectible.deploy(
      get_contract("vrf_coordinator"),
      get_contract("link_token"),
      config["networks"][network.show_active()]["key_hash"],
      config["networks"][network.show_active()]["fee"],
      {"from": account},
      )

def main():
    deploy_and_create()
