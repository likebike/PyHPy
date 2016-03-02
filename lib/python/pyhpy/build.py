#!/usr/bin/env python

# This script publishes the input directory to the output directory in an intelligent
# way.  Copies file data & permissions & ACLs, evaluates Mako templates, ignores
# hidden files.
#
# Written by Christopher Sebastian, 2011-11-04.  Redesigned 2016-03-01.

import os, sys, fnmatch, re, subprocess, json, string, atexit
import pyhpy.sync, pyhpy.fabricate

def childEnv(IN_DIR, projRelPath, OUT_DIR):
    env = dict(os.environ)
    # Set some environment variables that might be useful:
    env['PYHPY_IN_DIR'] = IN_DIR
    env['PYHPY_REL_PATH'] = projRelPath
    env['PYHPY_OUT_DIR'] = OUT_DIR
    env['PYTHON'] = sys.executable
    # Also, make sure that the Python running this script is first on $PATH:
    # This way, scripts can use the same Python with "#!/usr/bin/env python".
    pyDir = os.path.dirname(sys.executable)
    env['PATH'] = pyDir+':'+os.environ['PATH']
    return env

routesname = '/.pyhpy_routes'
_routesCache = None
def write_routes(path):
    if _routesCache:
        with open(path, 'w') as f: json.dump(_routesCache, f, indent=4, sort_keys=True)
def classify(PROCS_DIR, IN_DIR, projRelPath, OUT_DIR):
    global _routesCache
    if _routesCache == None:
        _routesCache = {}
        try: _routesCache = json.load(open(IN_DIR+routesname))
        except: pass
        atexit.register(write_routes, path=IN_DIR+routesname)
    key = ' '.join((IN_DIR, projRelPath, OUT_DIR))
    if key not in _routesCache:
        router = os.path.join(PROCS_DIR, 'Router')
        result = subprocess.Popen([router, IN_DIR, projRelPath, OUT_DIR], env=childEnv(IN_DIR, projRelPath, OUT_DIR), stdout=subprocess.PIPE).stdout.read().strip()
        assert result, 'Router produced blank result!'
        # 'result' is either a path like 'SKIP', '/bin/rm', '../bin/render'
        # OR it's a JSON list of strings, like '["/bin/echo", "-n", "$PYHPY_REL_PATH"]'
        path = os.path.join(PROCS_DIR, result)
        if os.path.exists(path): _routesCache[key] = [path]
        else:
            print 'ASSUME A COMMAND:', result, path
            # Assume it's a command in a JSON list of strings.  Perform some template substitution.
            try:
                cmd = json.loads(result)
                if type(cmd) != list: raise ValueError('Expected a JSON list of strings')
                _routesCache[key] = map(str, cmd)
            except: raise ValueError('Error while processing %r -- Invalid Router output: %r'%(projRelPath, result))
    return _routesCache[key]

def walkAndClassify(PROCS_DIR, rootDir, OUT_DIR):
    results = {}
    for dirpath, dirnames, filenames, symlinks in pyhpy.sync.walk(rootDir):
        def projRelPath(f):
            absPath = os.path.join(dirpath, f)
            assert absPath.startswith(rootDir)
            relPath = absPath[len(rootDir):]  # Path relative to rootDir.  /path/to/root/a/b/c becomes /a/b/c
            assert relPath[0] == os.sep
            return relPath
        for dirname in list(dirnames):
            cmd = classify(PROCS_DIR, rootDir, projRelPath(dirname), OUT_DIR)
            if len(cmd)==1  and  os.path.basename(cmd[0])=='SKIP': dirnames.remove(dirname)
        for filename in (filenames+symlinks): results[projRelPath(filename)] = classify(PROCS_DIR, rootDir, projRelPath(filename), OUT_DIR)
    return results
    
def build(PROCS_DIR, IN_DIR, OUT_DIR):
    depsname = '/.pyhpy_deps'
    builder = pyhpy.fabricate.Builder(ignore='^/(dev|proc|sys)/', dirs=['/'], depsname=IN_DIR+depsname, debug=False)
    processed = {}
    while True:    # Support auto-generation of files/templates.  (Loop until the filesystem is stable.)
        toProcess = walkAndClassify(PROCS_DIR, IN_DIR, OUT_DIR)
        if sorted(processed) == sorted(toProcess): break
        for projRelPath,cmd in sorted(toProcess.items()):
            if projRelPath in [depsname, routesname]: continue    # Skip our build-tracking files.
            if projRelPath in processed: continue   # Only process items once.
            if len(cmd) == 1: cmd = cmd + [IN_DIR, projRelPath, OUT_DIR]  # Don't use += to avoid modification.
            try: builder.run(cmd, cwd=IN_DIR, env=childEnv(IN_DIR, projRelPath, OUT_DIR))
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

