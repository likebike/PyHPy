#!/usr/bin/env python

# This script publishes the input directory to the output directory in an intelligent
# way.  Copies file data & permissions & ACLs, evaluates Mako templates, ignores
# hidden files.
#
# Written by Christopher Sebastian, 2011-11-04.  Redesigned 2016-03-01.

import os, sys, fnmatch, re, subprocess
import pyhpy.sync, pyhpy.fabricate

_processors = {}
def PROCESSORS(PROCS_DIR):
    global _processors
    if PROCS_DIR not in _processors: _processors[PROCS_DIR] = sorted(os.listdir(PROCS_DIR))
    return _processors[PROCS_DIR]
def classify(PROCS_DIR, ProjRelPath):
    projRelPath = ProjRelPath.lower()
    filename = os.path.split(projRelPath)[1]
    for processor in PROCESSORS(PROCS_DIR):
        match = re.match(r'^\d+-(.+?)=(.+)$', processor)   # match items like "30-filename=*.mako".
        if not match: continue
        valName, pattern = match.groups()
        assert valName in ['filename', 'path'], 'Invalid value name: %r'%(processor,)
        if fnmatch.fnmatchcase({'filename':filename, 'path':projRelPath}[valName], pattern): return os.path.realpath(os.path.join(PROCS_DIR,processor))
    raise ValueError('Unable to find processor for %r'%(projRelPath,))

def walkAndClassify(PROCS_DIR, rootDir):
    results = {}
    for dirpath, dirnames, filenames, symlinks in pyhpy.sync.walk(rootDir):
        def projRelPath(f):
            absPath = os.path.join(dirpath, f)
            assert absPath.startswith(rootDir)
            relPath = absPath[len(rootDir):]  # Path relative to rootDir.  /path/to/root/a/b/c becomes a/b/c
            assert relPath[0] == os.sep
            relPath = relPath[1:]
            assert relPath
            return relPath
        for dirname in list(dirnames):
            processor = classify(PROCS_DIR, projRelPath(dirname))
            if os.path.basename(processor) == 'SKIP':
                results[projRelPath(dirname)] = processor  # Even though we know we're going to skip this, call the SKIP processor anyway so that the user isn't confused when debugging.
                dirnames.remove(dirname)
        for filename in (filenames+symlinks): results[projRelPath(filename)] = classify(PROCS_DIR, projRelPath(filename))
    return results
    
def build(PROCS_DIR, IN_DIR, OUT_DIR):
    depsname = '.deps'
    builder = pyhpy.fabricate.Builder(ignore='^/(dev|proc|sys)/', dirs=['/'], depsname=os.path.join(IN_DIR, depsname), debug=False)
    processed = {}
    while True:    # Support auto-generation of files/templates.  (Loop until the filesystem is stable.)
        toProcess = walkAndClassify(PROCS_DIR, IN_DIR)
        if sorted(processed) == sorted(toProcess): break
        for projRelPath,processor in sorted(toProcess.items()):
            if projRelPath == depsname: continue    # Skip our dependency-tracking file.
            if projRelPath in processed: continue   # Only process items once.

            # Set some environment variables that might be useful for the processor:
            os.environ['PYHPY_IN_DIR'] = IN_DIR
            os.environ['PYHPY_OUT_DIR'] = OUT_DIR
            os.environ['PYHPY_REL_PATH'] = projRelPath
            os.environ['PYTHON'] = sys.executable
            # Also, make sure that the Python running this script is first on $PATH:
            # This way, scripts can use the same Python with "#!/usr/bin/env python".
            pyDir = os.path.dirname(sys.executable)
            pathPieces = os.environ['PATH'].split(':')
            if pathPieces[0] != pyDir: os.environ['PATH'] = pyDir+':'+os.environ['PATH']

            cmd = [processor, IN_DIR, OUT_DIR, projRelPath]
            try: builder.run(cmd, cwd=IN_DIR)
            except:
                print >> sys.stderr, '\nBuild Failed!'
                print >> sys.stderr, 'There was an error while running this command: %s\n'%(' '.join(map(repr,cmd)),)
                sys.exit(1)
                
        processed = toProcess
    return processed

if __name__ == '__main__':
    assert len(sys.argv) == 4
    _PROCS_DIR=os.path.abspath(sys.argv[1])
    _IN_DIR=os.path.abspath(sys.argv[2])
    _OUT_DIR=os.path.abspath(sys.argv[3])
    build(_PROCS_DIR, _IN_DIR, _OUT_DIR)

