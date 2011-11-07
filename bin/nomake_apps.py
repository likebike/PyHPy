# I need to work with the "apps tree" from multiple places.
# This module allows me to keep the logic in one place.

import os, json, time, hashlib

APPS_DIR = '/home/nomake/src/apps'
SRC_WWW_DIR = '/home/nomake/src/www'
SCREENSHOT_DIR = '/home/nomake/www/bigfiles/screenshots'
PACKAGE_DIR = '/home/nomake/www/bigfiles/packages'


def hashfile(afile, hasher, blocksize=65536):
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()

def iterAppDirs():
    for item in os.listdir(APPS_DIR):
        fullPath = os.path.join(APPS_DIR, item)
        if not os.path.isdir(fullPath):
            print 'Unexpected item in Apps Dir: %r'%(item,)
            continue
        yield fullPath

def iterAppVersions(appDir):
    versionsDir = os.path.join(appDir, 'versions')
    for item in os.listdir(versionsDir):
        fullPath = os.path.join(versionsDir, item)
        if not item.endswith('.json'):
            print 'Unexpected item in App Versions: %r'%(fullPath,)
            continue
        version = item[:-len('.json')]
        props = json.load(open(fullPath))
        packageFilename = props['filename']
        packagePath = os.path.join(PACKAGE_DIR, packageFilename)
        assert os.path.exists(packagePath), 'Package file does not exist: %r'%(packagePath,)
        props['version'] = version
        props['mtime'] = os.path.getmtime(packagePath)
        if 'date' not in props:
            props['date'] = time.strftime('%Y-%M-%d', time.localtime(props['mtime']))
        if 'hash_md5' not in props:
            print 'Calculating md5 of %s...'%(packagePath),
            hex = hashfile(open(packagePath, 'rb'), hashlib.md5())
            print '"hash_md5":"%s"'%(hex,)
            props['hash_md5'] = hex
        if 'hash_sha1' not in props:    
            print 'Calculating sha1 of %s...'%(packagePath),
            hex = hashfile(open(packagePath, 'rb'), hashlib.sha1())
            print '"hash_sha1":"%s"'%(hex,)
            props['hash_sha1'] = hex
        yield props

def readScreenshots(appDir):
    fullPath = os.path.join(appDir, 'screenshots.json')
    props = {'screenshots':json.load(open(fullPath))}
    props['mtime:screenshots.json'] = os.path.getmtime(fullPath)
    return props

def readAppMetadata(appDir):
    fullPath = os.path.join(appDir, 'app.json')
    props = json.load(open(fullPath))
    props['mtime:app.json'] = os.path.getmtime(fullPath)
    return props

def iterApps():
    for appDir in iterAppDirs():
        props = {'appDirPath':appDir,
                 'appDir':os.path.basename(appDir)}
        props.update(readAppMetadata(appDir))
        props.update(readScreenshots(appDir))
        props['versions'] = [v for v in iterAppVersions(appDir)]
        props['mtime'] = max(props['mtime:app.json'], props['mtime:screenshots.json'], *[v['mtime'] for v in props['versions']])
        yield props



