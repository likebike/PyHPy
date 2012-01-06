#!/usr/bin/env python

import btcpp, os

def mtime(path):
    if not os.path.exists(path): return 0
    return os.path.getmtime(path)
def mkdir(path):
    if not os.path.exists(path):
        print 'Creating Directory:', path
        os.makedirs(path)

if __name__ == '__main__':
    DB_DIR=os.path.expanduser('~/src/db')
    SRC_WWW_DIR=os.path.expanduser('~/src/www')
    maxAppMTime = 0
    myMTime = mtime(__file__)
    allApps = []
    for app in btcpp.iterDbFiles(DB_DIR):
        allApps.append(app)
        maxAppMTime = max(maxAppMTime, app['dbFileMtime'])
        dstPath = os.path.join(SRC_WWW_DIR, 'apps', '%s.html.tmpl'%(app['dbFileBase'],))
        if max(myMTime, app['dbFileMtime'])>mtime(dstPath):
            print 'App Page', app['name'], dstPath
            mkdir(os.path.dirname(dstPath))
            open(dstPath, 'w').write('''
<%%inherit file="../_appPage.tmpl"/>
<%%def name='APP()'><%% return %(app)r %%></%%def>
            '''%dict(app=app))
        for ver in app['versions']:
            dstPath = os.path.join(SRC_WWW_DIR, 'apps', '%s-%s.html.tmpl'%(app['dbFileBase'],ver['version']))
            if max(myMTime, app['dbFileMtime'])>mtime(dstPath):
                print 'Version Page', app['name'], ver['version'], dstPath
                mkdir(os.path.dirname(dstPath))
                open(dstPath, 'w').write('''
<%%inherit file="../_appVersion.tmpl"/>
<%%def name='APP()'><%% return %(app)r %%></%%def>
<%%def name='VERSION()'><%% return %(ver)r %%></%%def>
                '''%dict(app=app, ver=ver))

    dstPath = os.path.join(SRC_WWW_DIR, 'apps', 'index.html.tmpl')
    if max(myMTime, maxAppMTime)>mtime(dstPath):
        print 'Apps List Page', dstPath
        mkdir(os.path.dirname(dstPath))
        open(dstPath, 'w').write('''
<%%inherit file="../_appsIndex.tmpl"/>
<%%def name='APPS()'><%% return %(apps)r %%></%%def>
        '''%dict(apps=allApps))



