#!/bin/bash

# usage: ./run.sh
# usage: MOUNT_HOST=0 ./run.sh
#
# Written by Christopher Sebastian, 2011-12-13

set -o errexit   # Abort script if there is an error.
set -o nounset
# set -x  # Trace


if [ "$(id -u)" != "0" ]; then
    echo 'You should be root to run this.' 1>&2
    exit 1
fi


MYDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ "${CHROOT_DIR:-notset}" = "notset" ]; then
    CHROOT_DIR=$MYDIR/ROOT
fi


# Create some mounts to the host system:
if [ "$(ls /dev | wc -l)" != "$(ls $CHROOT_DIR/dev | wc -l)" ]; then mount -o bind /dev $CHROOT_DIR/dev; fi
if [ "$(ls /sys | wc -l)" != "$(ls $CHROOT_DIR/sys | wc -l)" ]; then mount -o bind /sys $CHROOT_DIR/sys; fi
if [ "$(ls /proc | wc -l)" != "$(ls $CHROOT_DIR/proc | wc -l)" ]; then mount -o bind /proc $CHROOT_DIR/proc; fi

# And a way to access the root filesystem:
if [ "${MOUNT_HOST:-1}" == "1" ]; then
    if [ ! -f "$MYDIR/umount_host.py" ]; then
        wget -q -O "$MYDIR/umount_host.py" http://nomake.org/umount_host.py
        chmod a+x "$MYDIR/umount_host.py"
    fi
    CHROOT_DIR="$CHROOT_DIR" MOUNT=1 "$MYDIR/umount_host.py"
fi


# Also need to copy some files over:
cp /etc/resolv.conf $CHROOT_DIR/etc/resolv.conf


export PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin
export LANG=C

set +o errexit  # Don't abort if an error occurs after this point.

if [ -z "$*" ]; then               # If there are no args...
    chroot $CHROOT_DIR /bin/bash   # Just run a shell.
    result=$?
else
    chroot $CHROOT_DIR "$@"        # Otherwise, run the specified command.
    result=$?
fi

echo
read -p 'Unmount the chroot host entries? (y/N) ' answer
if [ "${answer:-N}" = "y" ]; then
    CHROOT_DIR="$CHROOT_DIR" MOUNT=0 "$MYDIR/umount_host.py"
fi
echo

exit $result

