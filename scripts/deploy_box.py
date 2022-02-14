from scripts.helpful_scripts import encode_function_data, get_account
from brownie import network, Box, ProxyAdmin, TransparentUpgradeableProxy, Contract


def deploy_box():
    account = get_account()
    print(f"Deploying to {network.show_active()}")

    box = Box.deploy({"from": account})
    proxyAdmin = ProxyAdmin.deploy({"from": account})

    # initializer = box.store, 1
    boxEncodedInitializerFunction = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxyAdmin.address,
        boxEncodedInitializerFunction,
        {"from": account, "gas_limit": 1000000},
    )

    print(f"Proxy deployed to {proxy}, you can now upgrade to V2!")

    proxyBox = Contract.from_abi("Box", proxy.address, Box.abi)
    proxyBox.store(1, {"from": account})
    print(proxyBox.retrieve())


def main():
    deploy_box()
