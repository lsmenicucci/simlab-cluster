from pyinfra.operations import server, dnf, files, systemd
from pyinfra import host, logger
from pyinfra.api import facts, operation
from pyinfra.facts.server import Which, KernelVersion, Selinux, Command
from pathlib import Path

www = host.get_fact(Which, command='wwctl')
assert www is not None, "Could not find wwctl command installed"

# Configure system
selinux = host.get_fact(Command, "getenforce")

if (selinux != "Disabled"):
    files.line(
        name="Disable SELinux",
        path="/etc/selinux/config",
        line=r"SELINUX=*.",
        replace="SELINUX=disabled")

    server.reboot(name="Rebooting machine", delay=3, reboot_timeout=300)


# Configure warewulf
systemd.service(
    name="Enable warewulf service",
    service="warewulfd",
    enabled=True,
    running=True)

config_filepath = Path("/usr/local/etc/warewulf").joinpath("warewulf.conf")
#config_filepath = Path("/etc/warewulf").joinpath("warewulf.conf")


# Edit network configuration

def replace_wwconfig(actual, target):
    files.line(
        path=config_filepath.as_posix(),
        name="Edit warewulf subnet configuration",
        line=actual,
        replace=target)

replace_wwconfig(r"^ipaddr:*.",         "ipaddr: 10.0.1.1")
replace_wwconfig(r"^network:*.",        "network: 10.0.1.0")
replace_wwconfig(r"^  range start:*.",  "  range start: 10.0.1.2")
replace_wwconfig(r"^  range end:*.",    "  range end: 10.0.1.100")

# Ensure kernel headers
dnf.packages(
    name="Ensure kernel devel files",
    packages=["kernel-devel","kernel-headers"],
    present=True
)

server.shell(
    name="Generate possibly configuration files",
    commands=["wwctl configure --all"])

# server.shell(
#     name="Pull centos linux VNFS container",
#     commands=["wwctl container import docker://warewulf/centos-7 centos-7 --setdefault"])

server.shell(
    name="Build VNFS for container centos-7",
    commands=["wwctl container build centos-7"])

host_kernel = host.get_fact(KernelVersion)

server.shell(
    name="Import host kernel",
    commands=[f"wwctl kernel import {host_kernel}"])