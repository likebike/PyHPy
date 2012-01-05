#!/usr/bin/env python

# This script publishes the src directory to the www directory in an intelligent
# way.  Copies file data & permissions & ACLs, evaluates Mako templates, ignores
# hidden files, and notifies the user of files that are in the 'www' area that
# probably shouldn't be there.
#
# Written by Christopher Sebastian, 2011-11-04

import os, sys
import seb_sync

assert len(sys.argv) == 2
mode = sys.argv[1]  # dev or prod
assert mode in ['dev', 'prod']

SRC_DIR=os.path.expanduser('~/src/www')
WWW_DIR=os.path.expanduser('~/www/dev')
DOT_FILES_THAT_ARE_NOT_HIDDEN=['.htaccess']  # Dot files that we actually want
                                             # to copy.
EXTENSIONS_TO_IGNORE=['.swp', '.pyc']
if mode == 'prod': WWW_DIR=os.path.expanduser('~/www/prod')

print 'BUILD MODE:',mode
print 'SRC_DIR =',SRC_DIR
print 'WWW_DIR =',WWW_DIR
    

def isHiddenFile(filename, fnameBase, fnameExt):
    for ext in EXTENSIONS_TO_IGNORE:
        if fnameExt.lower() == ext: return True
    for n in DOT_FILES_THAT_ARE_NOT_HIDDEN:
        if filename.startswith(n): return False
    if filename[0] in '_.': return True
    return False


okDstFiles = []
def normalFileHandler(data):
    dstPath = os.path.join(WWW_DIR, data['srcPath'])
    seb_sync.syncNormalFile(data['absPath'], dstPath)
    okDstFiles.append(dstPath)
def hiddenFileHandler(data):
    #print 'Skipping hidden file:',data['srcPath']
    pass
def symlinkHandler(data):
    dstPath = os.path.join(WWW_DIR, data['srcPath'])
    seb_sync.syncSymlink(data['absPath'], dstPath)
    okDstFiles.append(dstPath)
def makoFileHandler(data):
    dstPath = os.path.join(WWW_DIR, data['fnameBase'])
    seb_sync.syncMakoTemplate(data['absPath'], dstPath)
    okDstFiles.append(dstPath)        


allItems = []
for dirpath, dirnames, filenames, symlinks in seb_sync.walk(SRC_DIR):
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

for dirpath, dirnames, filenames, symlinks in seb_sync.walk(WWW_DIR):
    for filename in (filenames+symlinks):
        absPath = os.path.join(dirpath, filename)
        if absPath not in okDstFiles:
            print 'Unexpected WWW File:',absPath

print 'Done.  :)'
