from scripts.helpful_scripts import encode_function_data, get_account
from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, Contract


def test_proxy_delegates_calls():
    account = get_account()
    box = Box.deploy({"from": account})
    proxyAdmin = ProxyAdmin.deploy({"from": account})
    boxEncodedInitializerFunction = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxyAdmin.address,
        boxEncodedInitializerFunction,
        {"from": account, "gas_limit": 1000000},
    )

    proxyBox = Contract.from_abi("Box", proxy.address, Box.abi)

    assert proxyBox.retrieve() == 0
    proxyBox.store(1, {"from": account})
    assert proxyBox.retrieve() == 1
