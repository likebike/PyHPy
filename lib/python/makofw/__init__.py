import os, json, codecs, sys, subprocess
import markdown as _markdown  # Use a different name for the module.

# A MarkDown Mako Filter.  Use like this:
#     <%! import makofw %>
#     <%block filter="makofw.markdown">
#     Hello
#     -----
#     
#     This is **MarkDown**!
#     </%block>
def markdown(string, output_format='html5', allow_anglebracket_escape=False):
    # Angle Bracket Escapes are disabled by default because they are dangerous if you don't trust the source of the markdown.
    if allow_anglebracket_escape: string = string.replace('\\<', 'zzzESCAPEDLEFTANGLEBRACKETzzz').replace('\\>', 'zzzESCAPEDRIGHTANGLEBRACKETzzz')
    out = '<article class="markdown-body">\n'    # We replicate the wrapper used on GitHub for compatibility with 3rd party CSS.
    out += _markdown.markdown(string, output_format=output_format, extensions=['markdown.extensions.fenced_code'])
    out += '\n</article>\n'
    out = out.replace('  ', '&nbsp; ')  # Make double-spaces visible in the web browser.
    if allow_anglebracket_escape: out = out.replace('zzzESCAPEDLEFTANGLEBRACKETzzz', '<').replace('zzzESCAPEDRIGHTANGLEBRACKETzzz', '>')
    return out


def url(path, urlRoot, fsRoot=None, mtime='auto'):
    # This function makes it easy to serve static files that are aggressively cached
    # on the client side, without making life difficult on the server side.  Whenever
    # an update to the file occurs, the timestamp will also update, resulting in a
    # new URL, which the client will fetch.

    assert path[0] == '/'
    assert not urlRoot.endswith('/')
    assert not fsRoot.endswith('/')
    U = urlRoot + path

    if mtime == 'auto':
        fs_path = fsRoot + path
        if not os.path.exists(fs_path):
            # Could not find the referenced file.  Is it a markdown?
            fs_path = fsRoot + path + '.md'
        if not os.path.exists(fs_path):
            # Nope, not a markdown.  How about a template?
            fs_path = fsRoot + path + '.tmpl'
        if not os.path.exists(fs_path): raise ValueError('Unable to find fs_path for url: %r'%(path,))
        mtime = getmtime(fs_path)
    if mtime != None:
        if '?' not in U: U += '?'
        else: U += '&'
        U += '_=%s'%(mtime,)

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


def thumb(fsRoot, relImgPath, relThumbPath=None, width=None, height=None):
    ''' Uses ImageMagick CLI to create a thumbnail. '''
    if width==None and height==None: height = 100
    if width==None and height!=None: width = height*1.618
    if width!=None and height==None: height = width/1.618
    width, height = int(round(width)), int(round(height))
    if relThumbPath==None:
        base, ext = os.path.splitext(relImgPath)
        relThumbPath = base+'_THUMB_%dx%d'%(width,height)+ext
    assert fsRoot[0] == '/'  and  fsRoot[-1] != '/'
    assert relImgPath[0] == '/'  and  relImgPath[-1] != '/'
    assert relThumbPath[0] == '/'  and  relThumbPath[-1] != '/'
    absImgPath, absThumbPath = fsRoot+relImgPath, fsRoot+relThumbPath
    imgMtime, thumbMtime = getmtime(absImgPath, includeMeta=False), getmtime(absThumbPath, includeMeta=False, noExistTime=0)
    if thumbMtime < imgMtime:
        subprocess.check_call(['convert', absImgPath, '-thumbnail', '%dx%d^'%(width, height), '-gravity', 'center', '-extent', '%dx%d'%(width, height), absThumbPath])
    return relThumbPath


