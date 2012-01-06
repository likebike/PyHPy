# I need to work with the "apps tree" from multiple places.
# This module allows me to keep the logic in one place.

import os, json

def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()


def iterDbFiles(dbDir, ext='.json'):
    dbDir = os.path.abspath(dbDir)
    for item in os.listdir(dbDir):
        path = os.path.join(dbDir,item)
        if not os.path.isfile(path):
            print 'Unexpected non-file: %s'%(path,)
            continue
        if not item.endswith(ext):
            print 'Skipping file with wrong extension: %s'%(path,)
            continue
        base = item[:-len(ext)]
        props = {'dbDir':dbDir,
                 'dbFilePath':path,
                 'dbFileName':item,
                 'dbFileBase':base,
                 'dbFileMtime':os.path.getmtime(path)}
        props.update(json.load(open(path)))
        yield props

