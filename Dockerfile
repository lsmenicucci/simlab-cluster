FROM docker.io/library/rockylinux:8

RUN dnf update -y ;\
    dnf install -y --allowerasing coreutils \
    cpio \
    dhclient \
    e2fsprogs \
    ethtool \
    findutils \
    initscripts \
    ipmitool \
    iproute \
    kernel-core \
    net-tools \
    network-scripts \
    nfs-utils \
    openssh-clients \
    openssh-server \
    pciutils \
    psmisc \
    rsync \
    rsyslog \
    strace \
    wget \
    which \
    words ;\
    dnf clean all

RUN sed -i -e '/^account.*pam_unix\.so\s*$/s/\s*$/\ broken_shadow/' /etc/pam.d/system-auth ;\
    sed -i -e '/^account.*pam_unix\.so\s*$/s/\s*$/\ broken_shadow/' /etc/pam.d/password-auth ;\
    rm -f /etc/sysconfig/network-scripts/ifcfg-e* ;\
    systemctl unmask console-getty.service dev-hugepages.mount getty.target sys-fs-fuse-connections.mount systemd-logind.service systemd-remount-fs.service ;\
    systemctl enable network ;\
    touch /etc/sysconfig/disable-deprecation-warnings ;\
    mkdir -p /etc/warewulf ;\
    touch /etc/warewulf/excludes ;\
    touch /etc/warewulf/container_exit.sh ;\
    chmod +x /etc/warewulf/container_exit.sh ;\
    echo "#!/bin/sh" > /etc/warewulf/container_exit.sh ;\
    echo "set -x" >> /etc/warewulf/container_exit.sh ;\
    echo "LANG=C" >> /etc/warewulf/container_exit.sh ;\
    echo "LC_CTYPE=C" >> /etc/warewulf/container_exit.sh ;\
    echo "export LANG LC_CTYPE" >> /etc/warewulf/container_exit.sh ;\
    echo "dnf clean all" >> /etc/warewulf/container_exit.sh ;\
    echo "/boot/" > /etc/warewulf/excludes ;\
    echo "/usr/share/GeoIP" >> /etc/warewulf/excludes