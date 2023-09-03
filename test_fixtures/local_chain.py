"""Test fixture for deploying local anvil chain and initializing hyperdrive"""
import os
import signal
import selectors
import subprocess
import time
from typing import Iterator, Tuple
from eth_typing import URI

import pytest

# fixture arguments in test function have to be the same as the fixture name
# pylint: disable=redefined-outer-name


class PgrepWrapper:
    """Wrapper for `pgrep`."""

    def __init__(self, pid):
        self.pid = pid

    def kill(self):
        """Kill the process."""
        try:
            os.kill(self.pid, signal.SIGTERM)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            print(f"Could not kill process {self.pid}: {exc}")

    def __repr__(self):
        return f"{self.pid}"


def pgrep(process) -> list[PgrepWrapper]:
    """Return the output of `pgrep` for the given process."""
    try:
        result = subprocess.run(["pgrep", process], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        pids = result.stdout.strip().split("\n")
        return [PgrepWrapper(int(pid)) for pid in pids]
    except subprocess.CalledProcessError as exc:
        raise ValueError(f"Could not find process {process}") from exc


def kill_processes(pids):
    """Kill processes."""
    if not isinstance(pids, list):
        pids = [pids]
    for pid_str in pids:
        try:
            pid = int(pid_str)
            os.kill(pid, signal.SIGTERM)  # or signal.SIGKILL
        except Exception as exc:
            raise ValueError(f"Could not kill process {pid_str}: {exc}") from exc


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

    pids, uri = get_anvil(host, anvil_port)
    time.sleep(0.1)  # Hack, wait for anvil chain to initialize
    yield uri
    kill_processes(pids)  # Kill anvil process at end


def read_output(pipe, buffer_list):
    """Read output from a pipe."""
    while chunk := pipe.read(1):
        decoded_chunk = chunk.decode("utf-8")
        print(decoded_chunk, end="")
        buffer_list.append(decoded_chunk)
        buffer_str = "".join(buffer_list)
        if "Listening on" in buffer_str or "Address already in use" in buffer_str:
            break  # End of streams


def get_anvil(host: str = "127.0.0.1", port=9999) -> Tuple[int, URI]:
    """Get anvil."""
    # pylint: disable=consider-using-with
    sel = selectors.DefaultSelector()
    stdout, stderr = [], []

    process = subprocess.Popen(["anvil", "--host", host, "--port", str(port), "--accounts", "1", "--code-size-limit", "9999999999"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)

    # Register the selector to poll for "read" readiness on stdout and stderr
    sel.register(process.stdout, selectors.EVENT_READ, lambda: read_output(process.stdout, stdout))  # type: ignore
    sel.register(process.stderr, selectors.EVENT_READ, lambda: read_output(process.stderr, stderr))  # type: ignore

    while True:
        # Wait for at least one of the pipes to be ready for reading
        for key, _ in sel.select():
            key.data()

        # Check if anvil has started
        if "Listening on" in "".join(stdout):
            print("Started anvil on process ", end="")
            break

        # Check if anvil is already running
        if "Address already in use" in "".join(stderr):
            print("Connected to existing anvil on process ", end="")
            break

    print(pid := pgrep("anvil")[0].pid)
    return pid, URI(f"http://{host}:{port}")
