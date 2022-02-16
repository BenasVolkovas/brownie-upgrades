from brownie import accounts, network, config
import eth_utils

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache", "hardhat", "ganache-local"]

# Get account depending on active network chain
def get_account(index=None, id=None):
    if index:
        return accounts[index]

    if id:
        return accounts.load(id)

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    # Default
    return accounts.add(config["wallets"]["from_key"])


# initializer=box.store, 1
def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


def upgrade_contract(
    account,
    proxy,
    newImplementationAddress,
    proxyAdminContract=None,
    initializer=None,
    *args
):
    transaction = None
    if proxyAdminContract:
        if initializer:
            encodedFunctionCall = encode_function_data(initializer, *args)
            transaction = proxyAdminContract.upgradeAndCall(
                proxy.address,
                newImplementationAddress,
                encodedFunctionCall,
                {"from": account},
            )
        else:
            transaction = proxyAdminContract.upgrade(
                proxy.address,
                newImplementationAddress,
                {"from": account},
            )
    else:
        if initializer:
            encodedFunctionCall = encode_function_data(initializer, *args)
            transaction = proxy.upgradeToAndCall(
                newImplementationAddress, encodedFunctionCall, {"from": account}
            )
        else:
            transaction = proxy.upgradeTo(newImplementationAddress, {"from", account})

    transaction.wait(1)
    return transaction
