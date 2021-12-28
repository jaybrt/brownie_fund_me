from brownie import FundMe, MockV3Aggregator, network, config
from scripts.utils import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def deploy_fund_me():
    account = get_account()
    # pass price feed address to fundme contract
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # set contract address to value stored in config
        price_feed_address = config["networks"][network.show_active][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        # set price feed address to address of deployed mock contract
        price_feed_address = MockV3Aggregator[-1].address
        print("Mocks deployed")

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get(
            "verify"
        ),  # verify code if its a live network
    )
    print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fund_me()
