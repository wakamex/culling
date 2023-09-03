from eth_typing import URI
from typing import cast

from test_fixtures import local_chain
from deploy_cull import deploy_cull, initialize_deploy_account, initialize_web3_with_http_provider
from web3 import HTTPProvider


def test_cull(local_chain):
    """Deploy the Cull Protocol."""
    web3 = initialize_web3_with_http_provider(local_chain, reset_provider=False)
    account = initialize_deploy_account(web3)
    cull_address, cull_contract = deploy_cull(local_chain, account)
    print(f"{cull_address=}")
    print(f"{cull_contract=}")
