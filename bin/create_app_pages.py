#!python

import nomake_apps, os

def mtime(path):
    if not os.path.exists(path): return 0
    return os.path.getmtime(path)
def mkdir(path):
    if not os.path.exists(path):
        print 'Creating Directory:', path
        os.makedirs(path)

if __name__ == '__main__':
    maxAppMTime = 0
    for app in nomake_apps.iterApps():
        maxAppMTime = max(maxAppMTime, app['mtime'])
        dstPath = os.path.join(nomake_apps.SRC_WWW_DIR, 'apps', '%s.html.tmpl'%(app['appDir'],))
        if app['mtime'] > mtime(dstPath):
            print app['name'], 'App Page', dstPath
            mkdir(os.path.dirname(dstPath))
            open(dstPath, 'w').write('test')
        for ver in app['versions']:
            dstMTime = 0 # TODO
            dstPath = os.path.join(nomake_apps.SRC_WWW_DIR, 'apps', '%s-%s.html.tmpl'%(app['appDir'],ver['version']))
            if ver['mtime'] > mtime(dstPath):
                print app['name'], ver['version'], 'Version Page', dstPath
                mkdir(os.path.dirname(dstPath))
                open(dstPath, 'w').write('test')

    dstPath = os.path.join(nomake_apps.SRC_WWW_DIR, 'list.html.tmpl')
    if maxAppMTime > mtime(dstPath):
        print 'List Page', dstPath
        mkdir(os.path.dirname(dstPath))
        open(dstPath, 'w').write('test')



