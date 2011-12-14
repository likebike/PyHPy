#!/usr/bin/python

# usage: CHROOT_DIR=/path/to/root ./umount_host.py
# usage: CHROOT_DIR=/path/to/root MOUNT=1 ./umount_host.py
#
# Written by Christopher Sebastian, 2011-12-13

import subprocess, sys, re, os, shutil

if os.getuid() != 0:
    print >> sys.stderr, 'You should be root to run this.'
    sys.exit(1)

def stripEndingSlash(s):
    while s.endswith('/'): s = s[:-1]
    return s

CHROOT_DIR = stripEndingSlash(os.path.abspath(os.environ.get('CHROOT_DIR','ROOT')))
assert CHROOT_DIR
assert CHROOT_DIR not in ['/','/dev','/proc','/sys']
HOST_MOUNT_POINT = stripEndingSlash(os.environ.get('HOST_MOUNT_POINT','/mnt/host'))
assert HOST_MOUNT_POINT
assert HOST_MOUNT_POINT[0] == '/'
assert HOST_MOUNT_POINT not in ['/','/dev','/proc','/sys']


def sortByPathLength(paths):
    # You need to mount shorter paths first to support nested mounts.
    return [y for l,y in sorted([(len(x),x) for x in paths])]
hostMountPoints = []
chrootMountPoints = []

if os.path.exists('/proc/self/mountstats'):
    for line in open('/proc/self/mountstats'):
        # Look for lines like this:  device auto.direct mounted on /data/mmc/tas with fstype autofs
        if not line.startswith('device '): continue
        mountPoint = os.path.abspath(re.search('device .+ mounted on (.+) with .+', line).group(1))
        if mountPoint.startswith(CHROOT_DIR+'/'):
            if mountPoint in chrootMountPoints: continue
            chrootMountPoints.append(mountPoint)
        else:
            if mountPoint in hostMountPoints: continue
            hostMountPoints.append(mountPoint)
else:
    # The 'mount' command does not list the automount entries in some cases.
    # That's why we attempt to use /proc/mounts directly.
    popen = subprocess.Popen('mount', stdout=subprocess.PIPE, shell=True)
    stdout = popen.stdout.read()
    retcode = popen.wait()
    if retcode: sys.exit(retcode)
    for line in stdout.splitlines():
        mountPoint = os.path.abspath(re.search('.+ on (.+) type .+', line).group(1))
        if mountPoint.startswith(CHROOT_DIR+'/'):
            if mountPoint in chrootMountPoints: continue
            chrootMountPoints.append(mountPoint)
        else:
            if mountPoint in hostMountPoints: continue
            hostMountPoints.append(mountPoint)


hostMountPoints = sortByPathLength(hostMountPoints)
chrootMountPoints = sortByPathLength(chrootMountPoints)


if int(os.environ.get('MOUNT', '0')):
    # Operate in MOUNT mode.
    def getChrootMountPoint(hostMountPoint):
        assert hostMountPoint[0] == '/'
        assert CHROOT_DIR[-1] != '/'
        return stripEndingSlash( CHROOT_DIR + HOST_MOUNT_POINT + hostMountPoint )

    todoMountPoints = []
    for hostMountPoint in hostMountPoints:
        assert os.path.exists(hostMountPoint)
        chrootMountPoint = getChrootMountPoint(hostMountPoint)
        if chrootMountPoint not in chrootMountPoints:
            todoMountPoints.append(hostMountPoint)

    retcode = 0
    for hostMountPoint in todoMountPoints:
        chrootMountPoint = getChrootMountPoint(hostMountPoint)
        if not os.path.exists(chrootMountPoint):
            print >> sys.stderr, 'Creating: %s'%(chrootMountPoint)
            os.makedirs(chrootMountPoint)
            shutil.copymode(hostMountPoint, chrootMountPoint)  # Copy permissions
        print >> sys.stderr, 'Mounting: %s'%(chrootMountPoint)
        retcode = subprocess.call('mount --bind %r %r'%(hostMountPoint, chrootMountPoint), shell=True) or retcode
    sys.exit(retcode)


# UMOUNT Logic:
retcode = 0
for chrootMountPoint in reversed(chrootMountPoints):  # Reversed because we need to unmount the long ones first.
    print >> sys.stderr, 'Unmounting: %s'%(chrootMountPoint,)
    retcode = subprocess.call('umount %r'%(chrootMountPoint,), shell=True) or retcode
sys.exit(retcode)

