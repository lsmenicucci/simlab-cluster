from pyinfra.operations import dnf, git, files, server
from pyinfra.facts.server import Home
from pyinfra import host
from pathlib import Path

home = host.get_fact(Home)
assert type(home) == str, "Couldn get home directory"
ww_src_dir = Path().joinpath("warewulf").as_posix()

# Setup warewulf packages

dnf.packages(
    name="Install warewulf dependencies",
    packages=["golang", "dhcp-server", "tftp-server","nfs-utils"],
    present=True)

dnf.packages(
    name="Install dependencies required for the 'development' branch",
    packages=["gpgme-devel", "libassuan-devel"],
    present=True,
    extra_install_args="--enablerepo=powertools")

# Download and build source
files.directory(
    name="Create warewulf source dir",
    path=ww_src_dir,
    present=True
)

git.repo(
    name="Pull warewulf repo",
    branch="main",
    src="https://github.com/hpcng/warewulf",
    dest=ww_src_dir)

server.shell(
    name="Clear warewulf build",
    commands=[f"make -C {ww_src_dir} clean"])

server.shell(
    name="Compile warewulf source",
    commands=[f"make -C {ww_src_dir} all"])

server.shell(
    name="Install warewulf",
    commands=[f"make -C {ww_src_dir} install"],
    _sudo=True)