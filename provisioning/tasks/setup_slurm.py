from collections import defaultdict
from pyinfra import host, logger, operations
from pyinfra.api import FactBase, facts, operation
from pyinfra.facts.server import Which, KernelVersion, Selinux, Command
from pyinfra.facts import files
from pathlib import Path

# Parameters
munge_key_path = "/etc/munge/munge.key"
slurm_files = [
    "/etc/slurm/slurm.conf",
    "/etc/slurm/slurmbd.conf",
    "/etc/munge/munge.key"
]

# Check
www = host.get_fact(Which, command='wwctl')
assert www is not None, "Could not find wwctl command"

# Utils
def create_ww_overlay(name, files):
    files_ps = [ Path(f) for f in files ]
    dirs = set()
    for file in files_ps:
        cur = file.parent
        while cur.as_posix() != "/":
            dirs.add(cur.as_posix())
            cur = cur.parent

    dirs = sorted(dirs)

    cmds = [f"wwctl overlay create {name}"]
    cmds += [f"wwctl overlay mkdir {name} {dirc}" for dirc in dirs]
    cmds += [f"wwctl overlay import {name} {file}" for file in files]
    operations.server.shell(name="Create slurm overlay", commands=cmds)

class WWOverlays(FactBase):
    command = "wwctl overlay list -l"

    def process(self, output):
        lines = output[1:]
        files = defaultdict(list)
        for line in lines:
            perm, uid, gid, overlay, path = line.split()
            files[overlay].append(dict(perm=perm, uid=uid, gid=gid, path=path))

        return files

# Operations
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


# Create a slurm overlay for the nodes
overlays = host.get_fact(WWOverlays)
if ("slurm" not in overlays):
    create_ww_overlay("slurm", slurm_files)

munge_files =  Path(f).is_relative_to("/etc/munge") for f in slurm_files ]
# may chown if necessary here
