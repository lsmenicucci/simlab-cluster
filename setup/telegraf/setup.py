from pathlib import Path
from pyinfra import host, operations

conf_file = Path(__file__).parent.joinpath("telegraf.conf").as_posix()
operations.files.put(conf_file, "/etc/telegraf/telegraf.conf", force=True, create_remote_dir=True)

operations.systemd.service("telegraf", restarted=True, enabled=True)
