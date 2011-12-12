#!/bin/bash

MYDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

PATH="$MYDIR/usr/local/bin:$MYDIR/usr/local/sbin:$MYDIR/usr/bin:$MYDIR/usr/sbin:$MYDIR/bin:$MYDIR/sbin:$PATH"
LD_LIBRARY_PATH="$MYDIR/usr/local/lib:$MYDIR/usr/lib:$MYDIR/lib:$LD_LIBRARY_PATH"
MANPATH="$MYDIR/usr/local/share/man:$MYDIR/usr/local/man:$MYDIR/usr/share/man:$MANPATH"

exec "$@"
