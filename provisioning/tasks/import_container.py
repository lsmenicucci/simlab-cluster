from pyinfra import host, logger
from pyinfra.operations import server
from pathlib import Path

container_name = "simlab"
docker_uri = f"docker-daemon://{container_name}:latest"

server.shell(
	name="Import container from docker",
	commands=[f"wwctl container import {docker_uri} -bfuv"])

