from pathlib import Path
from collections import defaultdict
from pyinfra import host
from pyinfra.api import FactBase, facts, operation

WW_BIN = "wwctl"

class Overlays(FactBase):
    command = "wwctl overlay list -l"

    def process(self, output):
        lines = output[1:]
        files = defaultdict(list)
        for line in lines:
            perm, uid, gid, overlay, path = line.split()
            files[overlay].append(dict(perm=perm, uid=uid, gid=gid, path=path))

        return files

def is_parent(dr, file):
    try:
        Path(file).relative_to(Path(dr))        
        return True
    except ValueError:
        return False
    

def get_missing_directories(targets, existing):
    dirs = set()
    for target in targets:
        cur_level = Path(target)
        while cur_level.as_posix() != "/":
            try:
                cur_level = cur_level.parent
                dirs.add(cur_level.as_posix())
            except:
                break

    missing = []
    for dr in dirs:
        is_missing = True
        for f in existing:
            if (is_parent(dr, f)):
                is_missing = False 
                break 
        if (is_missing):
            missing.append(dr)

    return sorted(missing) 

@operation
def overlay(overlay_name, present=True, files=[], reimport=True, tidy=False):
    overlays = host.get_fact(Overlays)

    # Delete overlay in any case
    if (overlay_name in overlays):
        if (not present):
            yield f"{WW_BIN} overlay delete {overlay_name}"
            return
    else:
        if (present):
            yield f"{WW_BIN} overlay create {overlay_name}"

    # Create necessary dirs
    existing_files = []
    if (overlay_name in overlays):
        existing_files = [ p["path"] for p in overlays[overlay_name] ] 
    missing_dirs = get_missing_directories(files, existing_files)

    for dr in missing_dirs:
        yield f"{WW_BIN} overlay mkdir {overlay_name} {dr}"
    
    # Import/reimport files
    for target in files:
        if (target in existing_files):
            if (not reimport):
                continue 
            yield f"{WW_BIN} overlay delete {overlay_name} {target}"
            
        yield f"{WW_BIN} overlay import {overlay_name} {target}"
    
    # Tidy if necessary
    if (tidy):
        for file in existing_files:
            if (file not in files):
                yield f"{WW_BIN} overlay delete {overlay_name} {file}"
    
        
