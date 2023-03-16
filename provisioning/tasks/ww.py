from pyinfra.api import FactBase, facts, operation

class WWOverlays(FactBase):
    command = "wwctl overlay list -l"

    def process(self, output):
        lines = output[1:]
        files = defaultdict(list)
        for line in lines:
            perm, uid, gid, overlay, path = line.split()
            files[overlay].append(dict(perm=perm, uid=uid, gid=gid, path=path))

        return files

