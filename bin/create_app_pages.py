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
    myMTime = mtime(__file__)
    allApps = []
    for app in nomake_apps.iterApps():
        allApps.append(app)
        maxAppMTime = max(maxAppMTime, app['mtime'])
        dstPath = os.path.join(nomake_apps.SRC_WWW_DIR, 'apps', '%s.html.tmpl'%(app['appDir'],))
        if max(myMTime, app['mtime'])>mtime(dstPath):
            print 'App Page', app['name'], dstPath
            mkdir(os.path.dirname(dstPath))
            open(dstPath, 'w').write('''
<%%inherit file="../_appPage.tmpl"/>
            '''%dict())
        for ver in app['versions']:
            dstPath = os.path.join(nomake_apps.SRC_WWW_DIR, 'apps', '%s-%s.html.tmpl'%(app['appDir'],ver['version']))
            if max(myMTime, ver['mtime'])>mtime(dstPath):
                print 'Version Page', app['name'], ver['version'], dstPath
                mkdir(os.path.dirname(dstPath))
                open(dstPath, 'w').write('''
<%%inherit file="../_appVersion.tmpl"/>
                '''%dict())

    dstPath = os.path.join(nomake_apps.SRC_WWW_DIR, 'apps', 'index.html.tmpl')
    if max(myMTime, maxAppMTime)>mtime(dstPath):
        print 'Apps List Page', dstPath
        mkdir(os.path.dirname(dstPath))
        open(dstPath, 'w').write('''
<%%inherit file="../_appsIndex.tmpl"/>
<%%def name='listApps()'><%% return %(allApps)r %%></%%def>
        '''%dict(allApps=allApps))



