# pylint: disable=invalid-name
"""A web3.py Contract class for the CullProtocol contract."""
from __future__ import annotations
from typing import Any, cast
from eth_typing import ChecksumAddress
from web3.contract.contract import Contract, ContractFunction, ContractFunctions
from web3.exceptions import FallbackNotFound


class APR(ContractFunction):
    """ContractFunction for the APR method."""

    # pylint: disable=arguments-differ
    def __call__(self) -> "APR":
        super().__call__()
        return self

    # TODO: add call def so we can get return types for the calls
    # def call()


class YEAR_IN_SECONDS(ContractFunction):
    """ContractFunction for the YEAR_IN_SECONDS method."""

    # pylint: disable=arguments-differ
    def __call__(self) -> "YEAR_IN_SECONDS":
        super().__call__()
        return self

    # TODO: add call def so we can get return types for the calls
    # def call()


class AddHolder(ContractFunction):
    """ContractFunction for the addHolder method."""

    # pylint: disable=arguments-differ
    def __call__(self, _holder: str) -> "AddHolder":
        super().__call__(_holder)
        return self

    # TODO: add call def so we can get return types for the calls
    # def call()


class Cull(ContractFunction):
    """ContractFunction for the cull method."""

    # pylint: disable=arguments-differ
    def __call__(self) -> "Cull":
        super().__call__()
        return self

    # TODO: add call def so we can get return types for the calls
    # def call()


class CullInterval(ContractFunction):
    """ContractFunction for the cullInterval method."""

    # pylint: disable=arguments-differ
    def __call__(self) -> "CullInterval":
        super().__call__()
        return self

    # TODO: add call def so we can get return types for the calls
    # def call()


class HolderIndex(ContractFunction):
    """ContractFunction for the holderIndex method."""

    # pylint: disable=arguments-differ
    def __call__(self, input0: str) -> "HolderIndex":
        super().__call__(input0)
        return self

    # TODO: add call def so we can get return types for the calls
    # def call()


class HolderList(ContractFunction):
    """ContractFunction for the holderList method."""

    # pylint: disable=arguments-differ
    def __call__(self, input0: int) -> "HolderList":
        super().__call__(input0)
        return self

    # TODO: add call def so we can get return types for the calls
    # def call()


class NextCullTime(ContractFunction):
    """ContractFunction for the nextCullTime method."""

    # pylint: disable=arguments-differ
    def __call__(self) -> "NextCullTime":
        super().__call__()
        return self

    # TODO: add call def so we can get return types for the calls
    # def call()


class RemoveHolder(ContractFunction):
    """ContractFunction for the removeHolder method."""

    # pylint: disable=arguments-differ
    def __call__(self, _holder: str) -> "RemoveHolder":
        super().__call__(_holder)
        return self

    # TODO: add call def so we can get return types for the calls
    # def call()


class Token(ContractFunction):
    """ContractFunction for the token method."""

    # pylint: disable=arguments-differ
    def __call__(self) -> "Token":
        super().__call__()
        return self

    # TODO: add call def so we can get return types for the calls
    # def call()


class CullProtocolContractFunctions(ContractFunctions):
    """ContractFunctions for the CullProtocol contract."""

    APR: APR
    YEAR_IN_SECONDS: YEAR_IN_SECONDS
    addHolder: AddHolder
    cull: Cull
    cullInterval: CullInterval
    holderIndex: HolderIndex
    holderList: HolderList
    nextCullTime: NextCullTime
    removeHolder: RemoveHolder
    token: Token


class CullProtocolContract(Contract):
    """A web3.py Contract class for the CullProtocol contract."""

    def __init__(self, web3_instance, address: ChecksumAddress | None = None, abi=Any) -> None:
        self.w3 = web3_instance
        self.abi = abi
        # TODO: make this better, shouldn't initialize to the zero address, but the Contract's init
        # function requires an address.
        self.address = address if address else cast(ChecksumAddress, "0x0000000000000000000000000000000000000000")
        try:
            # Initialize parent Contract class
            super().__init__(address=address)
        except FallbackNotFound:
            print("Fallback function not found. Continuing...")

    # TODO: add events
    # events: ERC20ContractEvents
    functions: CullProtocolContractFunctions
