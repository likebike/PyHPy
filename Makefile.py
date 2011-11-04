#!python

# Make Sucks.
#
# This script publishes the src directory to the www directory in an intelligent
# way.  Copies file data & permissions & ACLs, evaluates Mako templates, ignores
# hidden files, and notifies the user of files that are in the 'www' area that
# probably shouldn't be there.
#
# Written by Christopher Sebastian, 2011-11-04

import os, shutil, subprocess, sys

assert len(sys.argv) == 2
mode = sys.argv[1]  # dev or prod
assert mode in ['dev', 'prod']

SRC_DIR='/home/nomake/src'
WWW_DIR='/home/nomake/www/dev'
DOT_FILES_THAT_ARE_NOT_HIDDEN=['.htaccess']  # Dot files that we actually want
                                             # to copy.
EXTENSIONS_TO_IGNORE=['.swp', '.pyc']
if mode == 'prod':
    WWW_DIR='/home/nomake/www/prod'

print 'BUILD MODE:',mode
print 'SRC_DIR =',SRC_DIR
print 'WWW_DIR =',WWW_DIR
    

def getACL(path):
    curACLs = []
    popen = subprocess.Popen('getfacl --absolute-names %r'%(path,),
                             stdout=subprocess.PIPE,
                             shell=True)
    for line in popen.stdout:
        line = line.strip()
        if not line: continue
        if line.startswith('#'): continue
        curACLs.append(line)
    retcode = popen.wait()
    if retcode != 0: raise ValueError('Error getting ACL: %r'%(path,))
    return curACLs
def cpACL(srcPath, dstPath):
    retcode = subprocess.call('getfacl %r | setfacl --set-file=- %r'%(srcPath, dstPath), shell=True)
    if retcode != 0:
        raise ValueError('Error copying ACL: %r  -->  %r'%(srcPath, dstPath))
def getStats(path, includeSize=True):
    # Return the important, comparable filesystem stats that can
    # be used to compare file metadata.
    s = os.stat(path)
    acl = getACL(path)
    stats= {'mode':s.st_mode,
            'uid':s.st_uid,
            'gid':s.st_gid,
            'mtime':s.st_mtime,
            'acl':acl}
    if includeSize: stats['size'] = s.st_size
    return stats
def cpStats(srcPath, dstPath):
    cpACL(srcPath, dstPath)
    shutil.copystat(srcPath, dstPath)
def cpData(srcPath, dstPath):
    dstDir = os.path.dirname(dstPath)
    if not os.path.isdir(dstDir):
        raise ValueError('The destination directory does not exist!  Create it manually: %r'%(dstDir,))
    shutil.copy2(data['absPath'],dstPath) # Copy data, permissions, modtime.

    
def isHiddenFile(filename, fnameBase, fnameExt):
    for ext in EXTENSIONS_TO_IGNORE:
        if fnameExt.lower() == ext: return True
    for n in DOT_FILES_THAT_ARE_NOT_HIDDEN:
        if filename.startswith(n): return False
    if filename[0] in '_.': return True
    return False


okDstFiles = []
def hiddenFileHandler(data):
    #print 'Skipping hidden file:',data['srcPath']
    pass
def tmplFileHandler(data):
    dstPath = os.path.join(WWW_DIR, data['fnameBase'])
    dstModTime = 0
    if os.path.exists(dstPath): dstModTime = os.path.getmtime(dstPath)
    if data['srcModTime'] > dstModTime:
        print 'Evaluating Mako Template:'
        print '\t%s  -->  %s'%(data['absPath'],dstPath)
        retcode = subprocess.call(
                               'mako-render %r > %r'%(data['absPath'], dstPath),
                               shell=True)
        if retcode != 0:
            raise ValueError('Error with Mako Template: %r'%(data['absPath'],))
        cpStats(data['absPath'],dstPath)
    if getStats(data['absPath'], includeSize=False) != \
       getStats(dstPath, includeSize=False):
        print 'Copying Filesystem Metadata:'
        print '\t%s  -->  %s'%(data['absPath'],dstPath)
        cpStats(data['absPath'],dstPath)
    okDstFiles.append(dstPath)        
def normalFileHandler(data):
    dstPath = os.path.join(WWW_DIR, data['srcPath'])
    dstModTime = 0
    if os.path.exists(dstPath): dstModTime = os.path.getmtime(dstPath)
    if data['srcModTime'] > dstModTime:
        print 'Copying Normal File:'
        print '\t%s  -->  %s'%(data['absPath'],dstPath)
        cpData(data['absPath'], dstPath)
    if getStats(data['absPath']) != getStats(dstPath):
        print 'Copying Filesystem Metadata:'
        print '\t%s  -->  %s'%(data['absPath'],dstPath)
        cpStats(data['absPath'],dstPath)
    okDstFiles.append(dstPath)

allItems = []
for dirpath, dirnames, filenames in os.walk(SRC_DIR):
    for filename in filenames:

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

        if isHiddenFile(filename, fnameBase, fnameExt): data['handler'] = hiddenFileHandler
        elif fnameExt.lower() == '.tmpl': data['handler'] = tmplFileHandler
        else: data['handler'] = normalFileHandler

        allItems.append(data)

for data in allItems: data['handler'](data)

for dirpath, dirnames, filenames in os.walk(WWW_DIR):
    for filename in filenames:
        absPath = os.path.join(dirpath, filename)
        if absPath not in okDstFiles:
            print 'Unexpected WWW File:',absPath

print 'Done.  :)'
