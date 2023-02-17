"""Module containing pure functions to retrieve general information from Docker containers."""

from typing import Any, Dict, List, Optional

import docker  # type: ignore[import]
from docker.models.containers import Container  # type: ignore[import]

from emulation_system.compose_file_creator import Service


def get_volumes(container: Container) -> Optional[List[Dict[str, Any]]]:
    """Gets a list of volumes for a docker container.

    Returns None if no volumes exist
    """
    return [mount for mount in container.attrs["Mounts"] if mount["Type"] == "volume"]


def get_mounts(container: Container) -> Optional[List[Dict[str, Any]]]:
    """Gets a list of mounts for a docker container.

    Returns None if no mounts exist
    """
    return [mount for mount in container.attrs["Mounts"] if mount["Type"] == "bind"]


def get_container(service: Optional[Service]) -> Optional[Container]:
    """Gets Docker Container object from local Docker dameon based off of passed Service object.

    Specifically looks for a container with same name as passed Service object.
    """
    if service is None:
        return None
    else:
        return docker.from_env().containers.get(service.container_name)


def get_containers(services: Optional[List[Service]]) -> Optional[List[Container]]:
    """Gets a list of containers based off of passed list."""
    if services is None:
        return None
    else:
        return [get_container(service) for service in services]


def exec_in_container(container: Container, command: str) -> str:
    """Runs a command in passed docker container and returns command's output."""
    api_client = docker.APIClient()
    exec_id = api_client.exec_create(container.id, command)["Id"]
    return api_client.exec_start(exec_id).decode().strip()