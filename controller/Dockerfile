FROM docker.io/warewulf/rocky

# Install some packages
RUN dnf install -y epel-release
RUN dnf config-manager --set-enabled powertools
RUN dnf install -y apptainer munge slurm slurm-slurmd

RUN dnf install -y gcc-gfortran openmpi-devel

# Fix munge logging mode
RUN sed -iE "s|^ExecStart(.*)$|\0 --syslog|"  /usr/lib/systemd/system/munge.service

# Enable munge and slurm
RUN systemctl enable munge slurmd

RUN systemctl disable NetworkManager
RUN echo "root:root" | chpasswd
