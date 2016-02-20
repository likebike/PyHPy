import os, json, codecs, sys
import markdown as _markdown  # Use a different name for the module.

# A MarkDown Mako Filter.  Use like this:
#     <%! import makofw %>
#     <%block filter="makofw.markdown">
#     Hello
#     -----
#     
#     This is **MarkDown**!
#     </%block>
def markdown(string, output_format='html5'):
    out = '<div class=markdownWrapper>\n'
    out += _markdown.markdown(string, output_format=output_format)
    out += '\n</div>\n'
    return out


def url(path, urlRoot, fsRoot=None, timestamp='auto'):
    # This function makes it easy to serve static files that are aggressively cached
    # on the client side, without making life difficult on the server side.  Whenever
    # an update to the file occurs, the timestamp will also update, resulting in a
    # new URL, which the client will fetch.

    assert path[0] == '/'
    assert not urlRoot.endswith('/')
    assert not fsRoot.endswith('/')
    U = urlRoot + path

    if timestamp == 'auto':
        fs_path = fsRoot + path
        if not os.path.exists(fs_path):
            # Could not find the referenced file.  Is it a markdown?
            fs_path = fsRoot + path + '.md'
        if not os.path.exists(fs_path):
            # Nope, not a markdown.  How about a template?
            fs_path = fsRoot + path + '.tmpl'
        if not os.path.exists(fs_path): raise ValueError('Unable to find fs_path for url: %r'%(path,))
        timestamp = getmtime(fs_path)
    if timestamp != None:
        if '?' not in U: U += '?'
        else: U += '&'
        U += 'timestamp=%s'%(timestamp,)

    return U


def meta(fsPath):
    metaVals = {
        'extra_deps':[],
        'inherit':None,    # Used by MarkDown files.
    }
    dfltMetaPath = os.path.join(os.path.dirname(fsPath), '__default__.meta')
    if os.path.exists(dfltMetaPath): metaVals.update(json.load(codecs.open(dfltMetaPath, encoding='utf-8')))
    metaPath = fsPath+'.meta'
    if os.path.exists(metaPath): metaVals.update(json.load(codecs.open(metaPath, encoding='utf-8')))
    return metaVals


def getmtime(path, includeMeta=True, noExistTime=None):
    # Get a truncated file modification time to compensate for OS weirdness.
    if noExistTime!=None and not os.path.exists(path): return noExistTime
    mtime = os.path.getmtime(path)
    factor = 1000.0
    if sys.platform.startswith('win'): factor = 10.0
    mtime = float(int(mtime*factor))/factor
    if includeMeta:
        mtime = max(mtime, getmtime(os.path.join(os.path.dirname(path), '__default__.meta'), includeMeta=False, noExistTime=mtime))
        mtime = max(mtime, getmtime(path+'.meta', includeMeta=False, noExistTime=mtime))
    return mtime


