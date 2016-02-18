import os, json, codecs
import markdown as mdMod  # Use a different name for the module.

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
    out += mdMod.markdown(string, output_format=output_format)
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
        timestamp = os.path.getmtime(fs_path)
    if timestamp != None:
        if '?' not in U: U += '?'
        else: U += '&'
        U += 'timestamp=%s'%(timestamp,)

    return U


def meta(fsPath):
    metaVals = {
        'extra_deps':[],
        'inherit':None,   # Used by MarkDown files.
        'mtime':0,
        'creation_time':'20??-01-01 @ 00:00',
        'author':'Anonymous',
        'description':'Describe Me.',
    }
    if os.path.exists(fsPath): metaVals['mtime'] = os.path.getmtime(fsPath)
    metaPath = fsPath+'.meta'
    if os.path.exists(metaPath): metaVals.update(json.load(codecs.open(metaPath, encoding='utf-8')))
    return metaVals


