from scripts.helpful_scripts import encode_function_data, get_account, upgrade_contract
from brownie import (
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    exceptions,
)
import pytest


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

    boxV2 = BoxV2.deploy({"from": account})
    proxyBox = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    print("proxyBox = ", proxyBox)

    with pytest.raises(exceptions.VirtualMachineError):
        proxyBox.increment({"from": account})

    upgrade_contract(account, proxy, boxV2.address, proxyAdminContract=proxyAdmin)
    assert proxyBox.retrieve() == 0
    proxyBox.increment({"from": account})
    assert proxyBox.retrieve() == 1
