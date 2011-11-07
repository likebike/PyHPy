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

SRC_DIR='/home/nomake/src/www'
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
def getStats(path, includeSize=True, includeMTime=True):
    # Return the important, comparable filesystem stats that can
    # be used to compare file metadata.
    s = os.stat(path)
    acl = None
    if int(os.environ.get('ACL_CHECK', 1)): acl = getACL(path)
    stats= {'mode':s.st_mode,
            'uid':s.st_uid,
            'gid':s.st_gid,
            'acl':acl}
    if includeMTime: stats['mtime'] = s.st_mtime
    if includeSize: stats['size'] = s.st_size
    return stats
def cpStats(srcPath, dstPath, touch=True):
    if int(os.environ.get('ACL_CHECK', 1)): cpACL(srcPath, dstPath)
    shutil.copystat(srcPath, dstPath)
    if touch: os.utime(dstPath, None) # set the modtime to now.
def cpData(srcPath, dstPath, touch=True):
    dstDir = os.path.dirname(dstPath)
    if not os.path.isdir(dstDir):
        print 'Creating Directory:'
        print '\t%s'%(dstDir,)
        os.makedirs(dstDir)
    shutil.copy2(data['absPath'],dstPath) # Copy data, permissions, modtime.
    if touch: os.utime(dstPath, None) # set the modtime to now.

    
def isHiddenFile(filename, fnameBase, fnameExt):
    for ext in EXTENSIONS_TO_IGNORE:
        if fnameExt.lower() == ext: return True
    for n in DOT_FILES_THAT_ARE_NOT_HIDDEN:
        if filename.startswith(n): return False
    if filename[0] in '_.': return True
    return False


def getMakoTemplateDeps(tmplPath, allDeps=None, recursive=True):
    ''' Pretend that you have a template named "index.html.tmpl", and it
        inherits from "_master.tmpl".  When you give this function the path to
        the index template, this will return the path to _master so you can
        check the modification times of the deps.  This way, you can regenerate
        index.html if the master changes.
    
        Several methods are used to determine dependencies:
        
        First, standard Mako "inherit" lines are detected (using a very
        primitive algorithm... so be nice with your line formatting, please.):

            <%inherit file="_master.tmpl"/>

        Secondly, dependencies are extracted from 'namespace' lines:

            <%namespace name="task_common" file="task/common.tmpl"/>
        
        Finally, the user can add lines like this:

            ## DEP: /path/to/dep/file1.py
            ## DEP: ../_file2.tmpl

        Dependencies are recursively searched for dependencies too.
    '''
    assert os.path.isabs(tmplPath)
    if allDeps==None: allDeps = []
    deps = []
    for line in open(tmplPath):
        line = line.strip()
        if not line: continue
        pieces = line.split()
        if len(pieces)>2  and  pieces[0]=='##'  and  pieces[1]=='DEP:':
            path = line[line.index(pieces[2]):]
            if not os.path.isabs(path):
                path = os.path.join(os.path.dirname(tmplPath), path)
            deps.append(path)
        elif line.startswith('<%inherit')  or  line.startswith('<%namespace'):
            fileI = line.index('file=')
            quoteChar = line[fileI+5]
            path = line[fileI+6:line.index(quoteChar, fileI+6)]
            if not os.path.isabs(path):
                path = os.path.join(os.path.dirname(tmplPath), path)
            deps.append(path)
    newDeps = []
    for d in deps:
        if d not in allDeps:
            newDeps.append(d)
            allDeps.append(d)
    if not recursive: return newDeps
    for d in newDeps:
        if os.path.exists(d): getMakoTemplateDeps(d, allDeps)
    return allDeps

def walk(path):
    for dirpath, dirnames, filenames in os.walk(path):
        symlinks = []
        for i,filename in reversed(list(enumerate(filenames))):
            absPath = os.path.join(dirpath, filename)
            if os.path.islink(absPath):
                symlinks.append(filename)
                filenames.pop(i)
        for i,dirname in reversed(list(enumerate(dirnames))):
            absPath = os.path.join(dirpath, dirname)
            if os.path.islink(absPath):
                symlinks.append(dirname)
                dirnames.pop(i)
        yield dirpath, dirnames, filenames, symlinks



okDstFiles = []
def hiddenFileHandler(data):
    #print 'Skipping hidden file:',data['srcPath']
    pass
def tmplFileHandler(data):
    lastModTime = data['srcModTime']
    for dep in getMakoTemplateDeps(data['absPath']):
        assert os.path.isabs(dep)
        if not os.path.exists(dep):
            print 'Dependency does not exist: %r'%(dep,)
            continue
        lastModTime = max(lastModTime, os.path.getmtime(dep))
    dstPath = os.path.join(WWW_DIR, data['fnameBase'])
    dstModTime = 0
    if os.path.exists(dstPath): dstModTime = os.path.getmtime(dstPath)
    if lastModTime > dstModTime:
        print 'Evaluating Mako Template:'
        print '\t%s  -->  %s'%(data['absPath'],dstPath)
        retcode = subprocess.call(
                               'cd %r; mako-render %r > %r'%(data['dirpath'], data['absPath'], dstPath),
                               shell=True)
        if retcode != 0:
            raise ValueError('Error with Mako Template: %r'%(data['absPath'],))
        cpStats(data['absPath'],dstPath)
    if getStats(data['absPath'], includeSize=False, includeMTime=False) != \
       getStats(dstPath, includeSize=False, includeMTime=False):
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
        cpStats(data['absPath'], dstPath, touch=False)
    okDstFiles.append(dstPath)
def symlinkHandler(data):
    dstPath = os.path.join(WWW_DIR, data['srcPath'])
    linkto = os.readlink(data['absPath'])
    needToCreate = True
    if os.path.islink(dstPath):
        if os.readlink(dstPath) == linkto: needToCreate = False
    if needToCreate:
        dstDir = os.path.dirname(dstPath)
        if not os.path.isdir(dstDir):
            print 'Creating Directory:'
            print '\t%s'%(dstDir,)
            os.makedirs(dstDir)
        print 'Creating Symlink:'
        print '\t%s  -->  %s'%(dstPath,linkto)
        if os.path.exists(dstPath): os.remove(dstPath)
        os.symlink(linkto, dstPath)
    okDstFiles.append(dstPath)
        

allItems = []
for dirpath, dirnames, filenames, symlinks in walk(SRC_DIR):
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

        if isHiddenFile(filename, fnameBase, fnameExt): data['handler'] = hiddenFileHandler
        elif fnameExt.lower() == '.tmpl': data['handler'] = tmplFileHandler
        elif os.path.islink(absPath): data['handler'] = symlinkHandler
        else: data['handler'] = normalFileHandler

        allItems.append(data)

for data in allItems: data['handler'](data)

for dirpath, dirnames, filenames, symlinks in walk(WWW_DIR):
    for filename in (filenames+symlinks):
        absPath = os.path.join(dirpath, filename)
        if absPath not in okDstFiles:
            print 'Unexpected WWW File:',absPath

print 'Done.  :)'
