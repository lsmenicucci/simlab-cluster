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

config_filepath = Path("/usr/local/etc/warewulf").joinpath("warewulf.conf")
#config_filepath = Path("/etc/warewulf").joinpath("warewulf.conf")

# Edit network configuration

def replace_wwconfig(actual, target):
    files.line(
        path=config_filepath.as_posix(),
        name="Edit warewulf subnet configuration",
        line=actual,
        replace=target)


def setup_wwnet(subnet: str):
    assert len(subnet.split(".")) == 4, "Expected a subnet of the form xxx.xxx.xxx.xxx"
    prefix = ".".join(subnet.split(".")[:3])

    replace_wwconfig(r"^ipaddr:*.",         f"ipaddr: {prefix}.1")
    replace_wwconfig(r"^network:*.",        f"network: {prefix}.0")
    replace_wwconfig(r"^  range start:*.",  f"  range start: {prefix}.2")
    replace_wwconfig(r"^  range end:*.",    f"  range end: {prefix}.100")


setup_wwnet("10.1.1.1")

server.shell(
    name="Generate possibly configuration files",
    commands=["wwctl configure --all"])


# Add firewall rules
for service_name in ["warewulf", "tftp", "nfs"]:
    server.shell(
        name=f"Add service '{service_name}' to firewall",
        commands=[f"firewall-cmd --permanent --add-service {service_name}"])

server.shell(name="Restart firewall", commands=["firewall-cmd --reload"])

# Enable & start system service
systemd.service(
    name="Enable and start warewulf service",
    service="warewulfd",
    enabled=True,
    running=True)
