from brownie import Fundino, MockV3Aggregator, network, config
from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS

def deploy_fundino():
    account = get_account()
    # if on persistant network eg rinkebey use address else deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        
        
    # pass price feed address to fundino contract
    fundino_me = Fundino.deploy(price_feed_address, {"from": account}, publish_source=config["networks"][network.show_active()].get("verify"),)
    print(f"Contract deployed to {fundino_me.address}")
    return fundino_me

def main():
    deploy_fundino()
