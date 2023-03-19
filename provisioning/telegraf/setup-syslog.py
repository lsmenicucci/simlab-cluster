from pyinfra import operations


conf_file = Path(__file__).parent.joinpath("rsyslog.conf").as_posix()

operations.dnf.packages(packages=["rsyslog"], present=True)

operations.files.put(conf_file, "/etc/rsyslog.conf", force=True, create_remote_dir=True)
operations.systemd.service("rsyslog", enabled=True, running=True)
