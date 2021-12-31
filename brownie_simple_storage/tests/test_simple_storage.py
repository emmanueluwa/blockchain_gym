from brownie import SimpleStorage, accounts

def test_deployed():
    ## Arrange
    account = accounts[0]

    ## Act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0

    ## Assert
    assert starting_value == expected

def test_updating_storage():
    ## Arrange
    account = accounts[0]
    # part of setup and not what is being tested
    simple_storage = SimpleStorage.deploy({"from": account})

    ## Act
    expected = 101
    simple_storage.store(expected, {"from": account})

    ## Assert
    assert expected == simple_storage.retrieve()
