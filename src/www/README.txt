=== The nomake.org chroot Environment ===

INSTALLATION:

    Just un-tar the package.  If you're reading this, you've already done this.

USAGE:

    ===========  BASICS  ========================

    You must be root to use the chroot.


    To start a bash shell in the chroot:

        ./run.sh


    To run a single command in the chroot:

        ./run.sh command args...



    ===========  ADVANCED  ========================

    If you want to use a different chroot directory:

        CHROOT_DIR=/path/to/root ./run.sh [command args...]


    If you want to enter the chroot without mounting the host into the chroot:

        MOUNT_HOST=0 ./run.sh [command args...]


    If you want to manually unmount the host from the chroot:

        ./umount_host.py

