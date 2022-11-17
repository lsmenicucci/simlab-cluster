from pyinfra import operations
from pyinfra import host, logger, facts 
from pathlib import Path

operations.dnf.packages(
    name="Install EPL repository",
    packages=["epel-release"],
    present=True)

operations.dnf.packages(
    name="Install container management packages",
    packages=["docker"],
    present=True)

# def_filename = "sample-rocky.def"

# homedir = host.get_fact(facts.server.Home)
# assert type(homedir) == str, "Could not fetch remote home dir"
# containers_dir = Path(homedir).joinpath("containers")

# def_dest = containers_dir.joinpath(def_filename)
# container_chroot = containers_dir.joinpath(Path(def_filename).stem)

# operations.files.directory(
#     name="Ensure containers directory",
#     path=containers_dir.as_posix(),
#     present=True)

# operations.files.put(
#     name="Copy container file",
#     src=def_filename,
#     dest=def_dest.as_posix())

# operations.server.shell(
#     name="Build the container",
#     commands=[f"apptainer build --sandbox {container_chroot.as_posix()} {def_dest.as_posix()}"])

# operations.server.shell(
#     name="Import into warewulf",
#     commands=[f"apptainer build --sandbox {container_chroot.as_posix()} {def_dest.as_posix()}"])

