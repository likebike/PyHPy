==================  The nomake.org chroot Environment  ========================

INSTALLATION:

    Just un-tar the package.  If you're reading this, you're already done.

USAGE:

    You can think of this chroot environment sort of like an Apache web server:

    1)  You need to 'start' it.

    2)  Then you can 'run' stuff on it.

    3)  After you're all done, you need to 'stop' it.


    ==============  START  ==============

    The 'start' script does a few important things that are required for full
    functionality of the chroot.  It's a lot like your computer's startup
    scripts that get run when the computer starts:

    1)  It copies some files from your host system, like /etc/resolv.conf.

    2)  It mounts some important core things, like /dev /proc /sys and /tmp.

    3)  If the MOUNT_HOST=1 environment variable is set, it mounts a bunch of
        other things in /mnt/host that allow you to have access to your host
        system from the chroot.  WARNING:  If you do this, it is especially
        important to remember to 'stop' the chroot before you delete the chroot
        directory!  Otherwise, you will end up deleting everyting on your host
        computer as well!

    4)  Runs the '/nomake/boot.sh' script in the CHROOT.  This script executes
        *inside* the chroot environment.  The behavior of this script is
        specific to the chroot image.  It might start a web server, mount a
        samba share, or even start a graphical XFCE session.

    5)  It creates a '*000_RUNNING' file next to the nomake environment
        directory (not in the chroot -- in the directory one level above this
        README.txt file).  The purpose of this file is to remind you that the
        chroot environment is currently running.  This helps to avoid deleting
        chroots that have active mounts inside of them (and thereby accidentally
        deleting stuff on your host system).

    It is fine to run the 'start' script multiple times.  It does not do
    anything if the work is already done.

    Note that it is sometimes possible to 'run' stuff without running 'start'
    first, but this only works for very simple things because important pieces
    of the system will be missing or turned off.


    ==============   RUN   ==============

    After you have started the chroot environment, you can 'run' stuff!

    The 'run' script makes it easy to run things inside the chroot environment.
    Here are some (contrived) examples:
    
    # Start an interactive shell as 'root':
    ./run

    # Start an interactive shell as 'user':
    CHROOT_USER=user ./run

    # Just run a single command (aptitude) as 'user':
    CHROOT_USER=user ./run ls /
    CHROOT_USER=user ./run aptitude
    CHROOT_USER=user ./run apachectl restart

    # Command chaining.  All three commands are executed inside the chroot.
    CHROOT_USER=user ./run 'find / | wc -l ; du -hs /' 2>/dev/null  # Fully quoted
    CHROOT_USER=user ./run find / \| wc -l \; du -hs / 2>/dev/null  # Slash escapes

    # Standard I/O redirection and piping works between the host and chroot:
    find /usr | CHROOT_USER=user ./run wc -l > really_contrived_output.txt

    # GUI apps work fine:
    CHROOT_USER=user ./run 'DISPLAY=:1 xaralx'
    DISPLAY=:1 CHROOT_USER=user ./run xaralx
    

    ==============  STOP  ===============

    The 'stop' script is opposite to the 'start' script.  It turns off all the
    things that 'start' turned on, in the reverse order.

    1)  It removes the '*000_RUNNING' file.

    2)  It runs the '/nomake/halt.sh' script in the CHROOT.

    3)  Everything is un-mounted.  This includes any host mounts, /dev /proc
        /sys /tmp and any other mounts that were created inside the chroot.

    WARNING:  It is *critical* that you run the 'stop' script before you move,
    AA        delete, or modify the chroot directory from the outside.  It is
    R R       common for the chroot to have mounts of the host environment.  If
    N  N      you delete the chroot directory while those mounts are still
    I   I     active, you will end up deleting all the files on your computer!
    N    N    This is why 'run' shells always ask you whether you want to 'stop'
    G     G   the environment when you exit.




-------------------------------------------------------------------------------
Written by Christopher Sebastian (csebastian3@gmail.com), 2011-12-14
