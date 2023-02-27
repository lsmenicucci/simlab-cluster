from pyinfra.operations import dnf, git, files, server
from pyinfra.facts.server import Home
from pyinfra import host, logger
from pathlib import Path

home = host.get_fact(Home)
assert type(home) == str, "Couldn get home directory"

# Setup warewulf packages

dnf.packages(
    name="Install warewulf dependencies",
    packages=["golang", "dhcp-server", "tftp-server","nfs-utils", "make"],
    present=True)

dnf.packages(
    name="Install dependencies required for the 'development' branch",
    packages=["gpgme-devel", "libassuan-devel"],
    present=True,
    extra_install_args="--enablerepo=powertools")

# Download and build source
dnf.packages(
    name="Install tools for downloading release",
    packages=["curl"],
    present=True)

ww_release_url = "https://github.com/hpcng/warewulf/releases/download/v4.3.0/warewulf-4.3.0.tar.gz"
ww_release_filename = ww_release_url.split("/")[-1]
ww_release_path = Path(home).joinpath(ww_release_filename).as_posix()
ww_source_dir = Path(home).joinpath(ww_release_filename.replace(".tar.gz", "")).as_posix()

logger.info(ww_source_dir)

server.shell(
    name="Fetch warewulf release",
    commands=[f"curl -L {ww_release_url} --output {ww_release_path}"])

files.directory(
    name="Create source directory",
    path=ww_source_dir,
    present=True)

server.shell(
    name="Extract archive",
    commands=[f"tar xf {ww_release_path}"])


server.shell(
    name="Clear warewulf build",
    commands=[f"make -C {ww_source_dir} clean"])

server.shell(
    name="Compile warewulf source",
    commands=[f"make -C {ww_source_dir} all"])

server.shell(
    name="Install warewulf",
    commands=[f"make -C {ww_source_dir} install"],
    _sudo=True)