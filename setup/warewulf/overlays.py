import sys, pathlib 
sys.path.append( pathlib.Path(__file__).parent.as_posix() )
import api as ww

from pyinfra import operations

ww.overlay(overlay_name = "slurm", files = [
    "/etc/munge/munge.key",
    "/etc/slurm/slurm.conf",
    "/etc/slurm/slurmdbd.conf",
    ], reimport = True)

ww.overlay(overlay_name = "telegraf", files = [
    "/etc/default/telegraf",
    "/etc/telegraf/telegraf.conf",
    "/etc/rsyslog.conf",
    ], reimport = True)

operations.server.shell(commands=["wwctl overlay build"])
