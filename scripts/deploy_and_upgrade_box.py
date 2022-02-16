from scripts.helpful_scripts import encode_function_data, get_account, upgrade_contract
from brownie import (
    config,
    network,
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
)


def deploy_and_upgrade_box():
    account = get_account()
    print(f"Deploying to {network.show_active()}")

    box = Box.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    proxyAdmin = ProxyAdmin.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )

    # initializer = box.store, 1
    boxEncodedInitializerFunction = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxyAdmin.address,
        boxEncodedInitializerFunction,
        {"from": account, "gas_limit": 1000000},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )

    print(f"Proxy deployed to {proxy}, you can now upgrade to V2!")

    proxyBox = Contract.from_abi("Box", proxy.address, Box.abi)
    proxyBox.store(1, {"from": account})

    # Upgrade
    boxV2 = BoxV2.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    upgradeTransaction = upgrade_contract(
        account, proxy, boxV2.address, proxyAdminContract=proxyAdmin
    )

    print("Proxy has been updated!")
    proxyBox = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxyBox.increment({"from": account})
    print(proxyBox.retrieve())


def main():
    deploy_and_upgrade_box()
