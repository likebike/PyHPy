#!/usr/bin/env python

# This script publishes the src directory to the www directory in an intelligent
# way.  Copies file data & permissions & ACLs, evaluates Mako templates, ignores
# hidden files, and notifies the user of files that are in the 'www' area that
# probably shouldn't be there.
#
# Written by Christopher Sebastian, 2011-11-04

import os, sys
import makofw.sync

DOT_FILES_THAT_ARE_NOT_HIDDEN=['.htaccess']  # Dot files that we actually want
                                             # to copy.
EXTENSIONS_TO_IGNORE=['.swp', '.pyc']

def isHiddenFile(filename, fnameBase, fnameExt):
    for ext in EXTENSIONS_TO_IGNORE:
        if fnameExt.lower() == ext: return True
    for n in DOT_FILES_THAT_ARE_NOT_HIDDEN:
        if filename.startswith(n): return False
    if filename[0] in '_.': return True
    if filename[-1] in '~': return True
    return False


def normalFileHandler(data, DST_DIR, okDstFiles):
    dstPath = os.path.join(DST_DIR, data['srcPath'])
    makofw.sync.syncNormalFile(data['absPath'], dstPath)
    okDstFiles.append(dstPath)
def hiddenFileHandler(data, DST_DIR, okDstFiles):
    #print 'Skipping hidden file:',data['srcPath']
    pass
def symlinkHandler(data, DST_DIR, okDstFiles):
    dstPath = os.path.join(DST_DIR, data['srcPath'])
    makofw.sync.syncSymlink(data['absPath'], dstPath)
    okDstFiles.append(dstPath)
def makoFileHandler(data, DST_DIR, okDstFiles):
    dstPath = os.path.join(DST_DIR, data['fnameBase'])
    makofw.sync.syncMakoTemplate(data['absPath'], dstPath)
    okDstFiles.append(dstPath)        

def walkAndClassify(rootDir):
    results = {}
    for dirpath, dirnames, filenames, symlinks in makofw.sync.walk(rootDir):
        for dirname in list(dirnames):
            if isHiddenFile(dirname, dirname, ''):
                dirnames.remove(dirname)
        for filename in (filenames+symlinks):
            absPath = os.path.join(dirpath, filename)
            assert absPath.startswith(rootDir)
            srcPath = absPath[len(rootDir):]
            assert srcPath[0] == os.sep
            srcPath = srcPath[1:]
            assert srcPath
            srcModTime = os.path.getmtime(os.path.join(rootDir, srcPath))
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
            results[srcPath] = data
    return results
    
def publish(SRC_DIR, DST_DIR):
    okDstFiles = []
    processed, toProcess = {}, walkAndClassify(SRC_DIR)    # A simple way to support auto-generation of files/templates.  (Loop until the filesystem is stable.)
    while sorted(processed) != sorted(toProcess):
        okDstFiles = []
        for srcPath,data in sorted(toProcess.items()): data['handler'](data, DST_DIR, okDstFiles)
        processed, toProcess = toProcess, walkAndClassify(SRC_DIR)
    unexpectedDstFiles = []
    for dirpath, dirnames, filenames, symlinks in makofw.sync.walk(DST_DIR):
        for filename in (filenames+symlinks):
            absPath = os.path.join(dirpath, filename)
            if absPath not in okDstFiles:
                unexpectedDstFiles.append(absPath)
    return processed, unexpectedDstFiles

def main(SRC_DIR, DST_DIR):
    processed, unexpectedDstFiles = publish(SRC_DIR, DST_DIR)
    for f in unexpectedDstFiles:
        if int(os.environ.get('AUTO_RM', '0')) == 1:
            print 'Auto-Removing:',f
            os.unlink(f)
        else: print 'Unexpected WWW File:',f


if __name__ == '__main__':
    assert len(sys.argv) == 3
    _SRC_DIR=sys.argv[1]
    _DST_DIR=sys.argv[2]

    print 'SRC_DIR =',_SRC_DIR
    print 'DST_DIR =',_DST_DIR
    print 'ACL_CHECK =',os.environ.get('ACL_CHECK', 1)
        
    main(_SRC_DIR, _DST_DIR)

    print 'Done.  :)'

