from brownie import Fundino, MockV3Aggregator, network, config
from scripts.helpful_scripts import get_account

def deploy_fundino():
    account = get_account()
    # if on persistant network eg rinkebey use address else deploy mocks
    if network.show_active() != "development":
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        print(f"The active network is {network.show_active()}")
        print("Deploying Mocks...")
        #using v3 mock requires deciamls and initial ans
        mock_aggregator = MockV3Aggregator.deploy(18, 2000000000000000000000, {"from": account})
        price_feed_address = mock_aggregator.address
        print("Mocks Deployed")
        

    # pass price feed address to fundino contract
    fundino_me = Fundino.deploy(price_feed_address, {"from": account}, publish_source=config["networks"][network.show_active()].get("verify"),)
    print(f"Contract deployed to {fundino_me.address}")

def main():
    deploy_fundino()
