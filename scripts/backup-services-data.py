from pathlib import Path
from subprocess import run
from tempfile import NamedTemporaryFile

RESTIC_REPO = Path("/backup/services")
RESTIC_BIN = "restic"

assert RESTIC_REPO.exists(), f"Restic repo {RESTIC_REPO} does not exist"

here = Path(__file__).parent.resolve()
repo_root = here.parent

services_folder = repo_root / "services"
services = [x for x in services_folder.iterdir() if x.is_dir()]

files_to_backup = []
for service in services:
    data_folder = service / "data" 
    if not data_folder.exists():
        continue 

    files_to_backup.append(data_folder.as_posix())


def create_include_file(filename, files_to_backup):
    with open(filename, "w") as f:
        for file in files_to_backup:
            f.write(f"{file}\n")

print("Will backup the following files:")
for file in files_to_backup:
    print(f"  - {file}")

if input("Continue? [y/N] ").lower() != "y":
    exit(1)

with NamedTemporaryFile() as f:
    create_include_file(f.name, files_to_backup)
    print("Created temporary include file:", f.name)

    cmd = [RESTIC_BIN, "-r", RESTIC_REPO.as_posix(), "backup", "--files-from", f.name]
    
    print("Running command:", " ".join(cmd))
    run(cmd)
