from brownie import accounts, network, config


def get_account():
    if network.show_active == "development":
        acc = accounts[0]
    else:
        acc = accounts.add(config["wallets"]["from_key"])
    return acc
