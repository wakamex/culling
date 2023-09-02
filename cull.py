# %%
from eth_typing import URI
import CullProtocolContract as contract

# %%
for d in dir(contract):
    if not d.startswith("_"):
        print(d)


# %%
from test_fixtures.deploy_cull import deploy_cull, initialize_deploy_account, initialize_web3_with_http_provider
from test_fixtures.local_chain import local_chain

# %%
web3 = initialize_web3_with_http_provider(URI("http://localhost:8545"), reset_provider=False)
account = initialize_deploy_account(web3)
deploy_cull(_local_chain, account)

# %%
