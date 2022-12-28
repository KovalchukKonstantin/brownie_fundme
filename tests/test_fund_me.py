from scripts.helpers import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fundme
from brownie import network, accounts, exceptions
import pytest

def test_can_fund_and_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")

    account = get_account()
    fundme = deploy_fundme()
    entrance_fee = fundme.getEntranceFee() + 100
    tx = fundme.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fundme.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fundme.withdraw({"from": account})
    tx2.wait(1)
    assert fundme.addressToAmountFunded(account.address) == 0

def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")

    account = get_account()
    fundme = deploy_fundme()
    bad_account = accounts.add()
    with pytest.raises(Exception):
        fundme.withdraw({"from": bad_account})
    #fundme.withdraw({"from": account})