from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpers import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from web3 import Web3


def deploy_fundme():
    

    #if on persistent otherwise deploy MOCKS
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else: 
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    account = get_account()

    print(account)

    fundme = FundMe.deploy(price_feed_address, {"from": account}, publish_source=config["networks"][network.show_active()].get("verify"),)

    print(f"Account deployed to {fundme.address}")
    return fundme

def main():
    deploy_fundme()