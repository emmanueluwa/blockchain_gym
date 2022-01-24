from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fundino
from brownie import network, accounts, exceptions
import pytest

def test_can_fund_and_withdraw():
    account = get_account()
    fundino_me = deploy_fundino()
    entrance_fee = fundino_me.getEntranceFee()
    transaction = fundino_me.fund({"from": account, "value": entrance_fee})
    transaction.wait(1)
    assert fundino_me.addressToAmountFunded(account.address) == entrance_fee
    transaction2 = fundino_me.withdraw({"from": account})
    transaction2.wait(1)
    assert fundino_me.addressToAmountFunded(account.address) == 0

def test_only_owner_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    fundino_me = deploy_fundino()
    scammer = accounts.add()
    #letting test know that we are expecting a virtual machine revert
    with pytest.raises(exceptions.VirtualMachineError):
        fundino_me.withdraw({"from": scammer})
