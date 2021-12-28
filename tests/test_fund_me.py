from scripts.utils import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    enterance_fee = fund_me.getEnteranceFee()
    txn = fund_me.fund({"from": account, "value": enterance_fee})
    txn.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == enterance_fee
    txn2 = fund_me.withdraw({"from": account})
    txn2.wait(1)


def test_only_owner_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
