#!/usr/bin/env python

# This script publishes the src directory to the www directory in an intelligent
# way.  Copies file data & permissions & ACLs, evaluates Mako templates, ignores
# hidden files, and notifies the user of files that are in the 'www' area that
# probably shouldn't be there.
#
# Written by Christopher Sebastian, 2011-11-04

import os, sys
import makofw.sync

assert len(sys.argv) == 3

SRC_DIR=sys.argv[1]
DST_DIR=sys.argv[2]
DOT_FILES_THAT_ARE_NOT_HIDDEN=['.htaccess']  # Dot files that we actually want
                                             # to copy.
EXTENSIONS_TO_IGNORE=['.swp', '.pyc']

print 'SRC_DIR =',SRC_DIR
print 'DST_DIR =',DST_DIR
print 'ACL_CHECK =',os.environ.get('ACL_CHECK', 1)
    

def isHiddenFile(filename, fnameBase, fnameExt):
    for ext in EXTENSIONS_TO_IGNORE:
        if fnameExt.lower() == ext: return True
    for n in DOT_FILES_THAT_ARE_NOT_HIDDEN:
        if filename.startswith(n): return False
    if filename[0] in '_.': return True
    return False


okDstFiles = []
def normalFileHandler(data):
    dstPath = os.path.join(DST_DIR, data['srcPath'])
    makofw.sync.syncNormalFile(data['absPath'], dstPath)
    okDstFiles.append(dstPath)
def hiddenFileHandler(data):
    #print 'Skipping hidden file:',data['srcPath']
    pass
def symlinkHandler(data):
    dstPath = os.path.join(DST_DIR, data['srcPath'])
    makofw.sync.syncSymlink(data['absPath'], dstPath)
    okDstFiles.append(dstPath)
def makoFileHandler(data):
    dstPath = os.path.join(DST_DIR, data['fnameBase'])
    makofw.sync.syncMakoTemplate(data['absPath'], dstPath)
    okDstFiles.append(dstPath)        


allItems = []
for dirpath, dirnames, filenames, symlinks in makofw.sync.walk(SRC_DIR):
    for filename in (filenames+symlinks):
        absPath = os.path.join(dirpath, filename)
        assert absPath.startswith(SRC_DIR)
        srcPath = absPath[len(SRC_DIR):]
        assert srcPath[0] == '/'
        srcPath = srcPath[1:]
        assert srcPath
        srcModTime = os.path.getmtime(os.path.join(SRC_DIR, srcPath))
        fnameBase, fnameExt = os.path.splitext(srcPath)
        data = {'dirpath':dirpath,
                'filename':filename,
                'absPath':absPath,
                'srcPath':srcPath,
                'srcModTime':srcModTime,
                'fnameBase':fnameBase,
                'fnameExt':fnameExt,
               }

        if isHiddenFile(filename, fnameBase, fnameExt):
            data['handler'] = hiddenFileHandler
        elif fnameExt.lower() == '.tmpl': data['handler'] = makoFileHandler
        elif os.path.islink(absPath): data['handler'] = symlinkHandler
        else: data['handler'] = normalFileHandler
        allItems.append(data)

for data in allItems: data['handler'](data)

for dirpath, dirnames, filenames, symlinks in makofw.sync.walk(DST_DIR):
    for filename in (filenames+symlinks):
        absPath = os.path.join(dirpath, filename)
        if absPath not in okDstFiles:
            print 'Unexpected WWW File:',absPath

print 'Done.  :)'
