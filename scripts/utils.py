from brownie import accounts, network, config, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 18
STARTING_PRICE = 4000


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        acc = accounts[0]
    else:
        acc = accounts.add(config["wallets"]["from_key"])
    return acc


def deploy_mocks():
    # create mock price feed contract on development network
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks")
    if (
        len(MockV3Aggregator) <= 0
    ):  # only deploy new mock if one hasn't been deployed before
        MockV3Aggregator.deploy(
            DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_account()}
        )
