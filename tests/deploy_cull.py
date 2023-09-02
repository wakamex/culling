"""Functions to initialize hyperdrive using web3"""

from eth_account.account import Account
from eth_account.signers.local import LocalAccount
from eth_typing import Address, ChecksumAddress
from ethpy.base import (
    deploy_contract,
    deploy_contract_and_return,
    get_transaction_logs,
    initialize_web3_with_http_provider,
    load_all_abis,
    smart_contract_transact,
)
from fixedpointmath import FixedPoint
from web3 import Web3
from web3.contract.contract import Contract

# TODO these functions should eventually be moved to `ethpy/hyperdrive`, but leaving
# these here for now to be used by tests while we figure out how to parameterize
# initial hyperdrive conditions


def initialize_deploy_account(web3: Web3) -> LocalAccount:
    """Initializes the local anvil account to deploy everything from.

    Arguments
    ---------
    web3 : Web3
        web3 provider object

    Returns
    -------
    LocalAccount
        The LocalAccount object
    """
    # TODO get private key of this account programmatically
    # https://github.com/delvtech/elf-simulations/issues/816
    # This is the private key of account 0 of the anvil pre-funded account
    account_private_key = (
        "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
    )
    account: LocalAccount = Account().from_key(account_private_key)
    # Ensure this private key is actually matched to the first address of anvil
    assert web3.eth.accounts[0] == account.address
    return account


def deploy_cull(
    rpc_url: str, deploy_account: LocalAccount
) -> tuple[ChecksumAddress, Contract]:
    """Deploy Culling Contract."""
    abi_folder = "out/"
    abis, bytecodes = load_all_abis(abi_folder, return_bytecode=True)
    web3 = initialize_web3_with_http_provider(rpc_url, reset_provider=False)
    deploy_account_addr = Web3.to_checksum_address(deploy_account.address)

    base_token_contract_addr, base_token_contract = deploy_contract_and_return(
        web3,
        abi=abis["ERC20Mintable"],
        bytecode=bytecodes["ERC20Mintable"],
        deploy_account_addr=deploy_account_addr,
    )

    # deploy Cull Protocol
    abi = abis["CullProtocol"]
    args = [base_token_contract_addr, int(0.05 * 1e18)]
    bytecode = bytecodes["CullProtocol"]

    cull_address, cull_contract = deploy_contract_and_return(
        web3=web3,
        abi=abi,
        bytecode=bytecode,
        deploy_account_addr=deploy_account_addr,
    args=args
    )
    # contract = web3.eth.contract(abi=abi, bytecode=bytecode)
    # tx_hash = contract.constructor(*args).transact({"from": deploy_account_addr, "gas": 720449})
    # tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    # assert (cull_address := tx_receipt["contractAddress"])
    # cull_contract = web3.eth.contract(address=cull_address, abi=abi)
    return cull_address, cull_contract
