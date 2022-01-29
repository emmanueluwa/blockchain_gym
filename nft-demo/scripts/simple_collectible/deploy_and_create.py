from scripts.helpful_scripts import get_account, OPENSEA_URL
from brownie import SimpleCollectible

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"

def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    transaction = simple_collectible.createCollectible(sample_token_uri, {"from": account})
    transaction.wait(1)
    print(f"nft can now be viewed at {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter() - 1)}")
    print("Please wait up to 20mins, and hit the refresh metadata button.")
    return simple_collectible

def main():
    deploy_and_create()
