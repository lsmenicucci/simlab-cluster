# syntax=docker/dockerfile:1
FROM docker.io/warewulf/rocky

# Install some packages
RUN dnf install -y epel-release
RUN dnf config-manager --set-enabled powertools
RUN dnf install -y apptainer munge slurm slurm-slurmd

RUN dnf install -y gcc-gfortran openmpi-devel

# Install telegraf
RUN cat <<EOF | tee /etc/yum.repos.d/influxdb.repo
[influxdb]
name = InfluxDB Repository - RHEL \$releasever
baseurl = https://repos.influxdata.com/rhel/\$releasever/\$basearch/stable
enabled = 1
gpgcheck = 1
gpgkey = https://repos.influxdata.com/influxdata-archive_compat.key
EOF

RUN dnf install -y telegraf
COPY telegraf.service /etc/systemd/system/
RUN systemctl enable telegraf

# Fix munge logging mode
RUN sed -iE "s|^ExecStart(.*)$|\0 --syslog|"  /usr/lib/systemd/system/munge.service

# Enable munge and slurm
RUN systemctl enable munge slurmd

# Disable network manager
RUN systemctl disable NetworkManager

# Set root password
RUN echo "root:root" | chpasswd

