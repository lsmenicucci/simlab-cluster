import sys, pathlib 
sys.path.append( pathlib.Path(__file__).parent.as_posix() )
import api as ww

ww.overlay(overlay_name = "slurm", files = [
    "/etc/munge/munge.key",
    "/etc/slurm/slurm.conf",
    "/etc/slurm/slurmdbd.conf",
    ], reimport = True)

ww.overlay(overlay_name = "telegraf", files = [
    "/etc/default/telegraf",
    "/etc/telegraf/telegraf.conf",
    ], reimport = True)
