from subprocess import run
from pathlib import Path
from rich import print


class NetworkConfigurator():
    def __init__(self) -> None:
        self.devices = []

    def add_device(self, device_name):
        self.devices.append(device_name)
        return {
            "nic": "tap"
        }


class VirtualMachine:
    def __init__(self, run_cmd: str, disk_file: str, memory: str):
        self.run_cmd = run_cmd
        self.disk_file = Path(disk_file)
        self.memory = memory

    def _run(self, *extra_options):
        cmd = [self.run_cmd]

        run_options = {
            "drive": f"file={self.disk_file},format=qcow2",
            "m": self.memory,
            "enable-kvm": True,
        }

        for options in extra_options:
            run_options = {**run_options, **options}

        for key, value in run_options.items():
            if (type(value) == bool):
                if (value):
                    cmd += [f"-{key}"]
            else:
                cmd += [f"-{key}", value]

        print("$ ", " ".join(cmd))
        result = run(cmd, capture_output=True)
        stdout, stderr = result.stdout.decode(), result.stderr.decode()

        if result.returncode != 0:
            print("[!] Process ended with nonzero returncode")

        if (len(stdout)):
            print(stdout)

        if (len(stderr)): 
            print(stderr)

    def start(self, *options):
        base_options = {
            "boot": "c"
        }

        return self._run(base_options, *options)

    def start_instalation(self, iso_img):
        iso_img_path = Path(iso_img)

        assert iso_img_path.exists(), "ISO image not found"

        options = {
            "cdrom": iso_img_path.as_posix(),
            "boot": "d",
        }

        return self._run(options)


net = NetworkConfigurator()
v = VirtualMachine("qemu-system-x86_64", "./disks/test", "1G")

#v.start_instalation("./Rocky-8.5-x86_64-minimal.iso")
v.start(net.add_device("head"))
