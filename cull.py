# %%
# pylint: disable=no-name-in-module
# sourcery skip: dont-import-test-modules
# from CullProtocolContract import CullProtocolContract
from tests import deploy_cull, initialize_deploy_account, initialize_web3_with_http_provider
from test_fixtures import get_anvil, kill_processes

# %%
pid, uri = get_anvil()
web3 = initialize_web3_with_http_provider(uri, reset_provider=False)
account = initialize_deploy_account(web3)
cull_address, cull_contract = deploy_cull(uri, account)
print(f"Cull Protocol deployed at {cull_address}")

# %%
members = [d for d in dir(cull_contract) if not d.startswith("_")]
print("contract members: " + ",".join(members))
for member in members:
    print(member)

# %%
kill_processes(pid)

# %%
