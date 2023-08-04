from subprocess import run
from pathlib import Path

here = Path(__file__).parent

container_file = "container.sif"
container_path = here / container_file

def_file = "container.def"
def_path = here / def_file

# create apptainer container
if not container_path.exists():
    print(f"Creating container from {def_file}")
    cmd = ["apptainer", "build", container_path.as_posix(), def_path.as_posix()]
    run(cmd, check=True)
