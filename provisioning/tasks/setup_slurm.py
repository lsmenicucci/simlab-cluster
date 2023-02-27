from pyinfra import host, logger, operations
from pyinfra.api import facts, operation
from pyinfra.facts.server import Which, KernelVersion, Selinux, Command
from pyinfra.facts import files
from pathlib import Path

# Parameters
munge_key_path = "/etc/munge/munge.key"

www = host.get_fact(Which, command='wwctl')
assert www is not None, "Could not find wwctl command"

operations.dnf.packages(
        name="Install dnf plugins, required for powertools",
        packages=["dnf-plugins-core"],
        present=True)

operations.server.shell(name="Enable powertools",commands=["dnf config-manager --set-enabled powertools"])

operations.dnf.packages(
    name="Install slurm packages",
    packages=["slurm", "slurm-slurmctld", "slurm-slurmdbd", "munge"],
    present=True)

# Create munge user
operations.server.group("munge", present=True, system=True)
operations.server.user("munge", present=True, system=True, ensure_home=False)

# Ensure munge key
file_stat = host.get_fact(files.File, munge_key_path)

if (file_stat == None):
    gen_cmd = "create-munge-key"
    operations.server.shell(name="Generate munge key", commands=[gen_cmd])


operations.systemd.service("munge", running=True, enabled=True)
operations.systemd.service("slurmctld", running=True, enabled=True)
operations.systemd.service("slurmdbd", running=True, enabled=True)

