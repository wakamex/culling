"""Test fixture for deploying local anvil chain and initializing hyperdrive"""
import subprocess
import time
from typing import Iterator

import pytest

# fixture arguments in test function have to be the same as the fixture name
# pylint: disable=redefined-outer-name


@pytest.fixture(scope="function")
def local_chain() -> Iterator[str]:
    """Launches a local anvil chain for testing. Kills the anvil chain after.

    Returns
    -------
    Iterator[str]
        Yields the local anvil chain url
    """
    anvil_port = 9999
    host = "127.0.0.1"  # localhost

    # Assuming anvil command is accessible in path
    # running into issue with contract size without --code-size-limit arg

    # Using context manager here seems to make CI hang, so explicitly killing process at the end of yield
    # pylint: disable=consider-using-with
    anvil_process = subprocess.Popen(
        ["anvil", "--host", "127.0.0.1", "--port", str(anvil_port), "--code-size-limit", "9999999999"]
    )

    local_chain_ = "http://" + host + ":" + str(anvil_port)

    # Hack, wait for anvil chain to initialize
    time.sleep(0.1)

    yield local_chain_

    # Kill anvil process at end
    anvil_process.kill()
