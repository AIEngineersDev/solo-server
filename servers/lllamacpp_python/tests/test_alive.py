import pytest_container
from .conftest import MS
import tenacity
import os

CONTAINER_IMAGES = [MS]

def test_etc_os_release_present(auto_container: pytest_container.container.ContainerData):
    assert auto_container.connection.file("/etc/os-release").exists

@tenacity.retry(stop=tenacity.stop_after_attempt(5), wait=tenacity.wait_exponential())
def test_alive(auto_container: pytest_container.container.ContainerData, host):
    host.run_expect([0],f"curl http://localhost:{auto_container.forwarded_ports[0].host_port}",).stdout.strip()
