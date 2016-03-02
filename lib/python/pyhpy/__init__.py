import os, json, codecs, sys, subprocess, re
import markdown as _markdown  # Use a different name for the module.

class DoubleSpaceMarkdownExtension(_markdown.extensions.Extension):
    def extendMarkdown(self, md, md_globals):
        DSPACE_RE = r'  '
        dspacePattern = DoubleSpaceMarkdownPattern(DSPACE_RE, markdown_instance=md)
        md.inlinePatterns.add('doublespace', dspacePattern, '_end')
class DoubleSpaceMarkdownPattern(_markdown.inlinepatterns.Pattern):
    def handleMatch(self, m): return '%s%s%snbsp; '%(_markdown.util.STX, ord('&'), _markdown.util.ETX)

class EqualSignHeaderMarkdownExtension(_markdown.extensions.Extension):
    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add('equalsignheader', EqualSignHeaderProcessor(md.parser), '>setextheader')
class EqualSignHeaderProcessor(_markdown.blockprocessors.HashHeaderProcessor):
    RE = re.compile(r'(^|\n)(?P<level>={1,6})(?P<header>.*?)=*(\n|$)')
    

# A MarkDown Mako Filter.  Use like this:
#     <%! import pyhpy %>
#     <%block filter="pyhpy.markdown">
#     Hello
#     -----
#     
#     This is **MarkDown**!
#     </%block>
def markdown(string, output_format='html5', cssClass='markdown-body'):
    md = _markdown.Markdown(output_format=output_format, extensions=['markdown.extensions.fenced_code', DoubleSpaceMarkdownExtension(), EqualSignHeaderMarkdownExtension()])

    # # I thought I needed to be able to escape angle brackets, but it turns out that I can already
    # # use <%! ... %> stuff directly -- i just need to add a blank line to separate it from inline content.
    # # But since I went thru the trouble to figure out the right way to solve this problem, I'm keeping this code for reference, since it's not intuitive:
    # if allow_anglebracket_escape:
    #     echars = md.ESCAPED_CHARS   # Usually, ESCAPED_CHARS is actually coming from the class level.  That's why we need to use this process to set it on the instance without affecting the class data.
    #     if '<' not in echars:
    #         md.ESCAPED_CHARS = ['<'] + echars
    #         assert '<' not in _markdown.Markdown.ESCAPED_CHARS  # Make sure we didn't actually modify the class data.

    out  = '<article class="%s">'%(cssClass,)    # We replicate the wrapper used on GitHub for compatibility with 3rd party CSS.
    out += md.convert(string)
    out += '</article>'
    return out

_fsRoot = None
def FS_ROOT():
    # Cache the result, since we don't expect the project root to change dynamically.
    global _fsRoot
    if _fsRoot == None:
        # Examine the call stack to derive the fsRoot from Mako module-level variables:
        # (I could have also examined the 'local.uri/local.filename' variables, but that would be a tiny bit more difficult.)
        import inspect
        level, frame = 0, inspect.currentframe()
        while frame:
            if '_template_uri' in frame.f_globals:
                assert frame.f_globals['_template_filename'].endswith(frame.f_globals['_template_uri']), '%r does not end with %r'%(frame.f_globals['_template_filename'], frame.f_globals['_template_uri'])
                fsRoot = frame.f_globals['_template_filename'][:-len(frame.f_globals['_template_uri'])]
                assert fsRoot[0] == '/'  and  fsRoot[-1] != '/', 'Non-absolute fsRoot: %r'%(fsRoot,)
                _fsRoot = fsRoot
                break
            level, frame = level+1, frame.f_back
        else: raise ValueError('Unable to auto-detect project root!')
    return _fsRoot
def url(path, urlRoot=None, fsRoot=None, mtime='auto'):
    # This function makes it easy to serve static files that are aggressively cached
    # on the client side, without making life difficult on the server side.  Whenever
    # an update to the file occurs, the timestamp will also update, resulting in a
    # new URL, which the client will fetch.

    if urlRoot == None: urlRoot = os.environ.get('URL_ROOT', '')

    assert path[0] == '/'
    assert not path.startswith('//'), 'Sloppy path: %r'%(path,)
    assert not urlRoot.endswith('/')
    U = urlRoot + path

    if mtime == 'auto':
        if fsRoot == None: fsRoot = FS_ROOT()
        fs_path = fsRoot + path
        if not os.path.exists(fs_path):
            # Could not find the referenced file.  Is it a markdown?
            fs_path = fsRoot + path + '.md'
        if not os.path.exists(fs_path):
            # Nope, not markdown.  How about a template?
            fs_path = fsRoot + path + '.mako'
        if not os.path.exists(fs_path): raise ValueError('Unable to find fs_path for url: %r'%(path,))
        mtime = getmtime(fs_path)
    if mtime != None:
        if '?' not in U: U += '?'
        else: U += '&'
        U += '_=%s'%(mtime,)

    return U


def meta(fsPath):
    metaVals = {}
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


def thumb(relImgPath, relThumbPath=None, fsRoot=None, width=None, height=None):
    ''' Uses ImageMagick CLI to create a thumbnail. '''
    crop = False
    if width==None and height==None: height = 128
    if width==None and height!=None: sizeStr = 'x%d'%(int(round(height)),)
    if width!=None and height==None: sizeStr = '%d'%(int(round(width)),)
    if width!=None and height!=None: crop, sizeStr = True, '%dx%d'%(int(round(width)), int(round(height)))
    if relThumbPath==None:
        base, ext = os.path.splitext(relImgPath)
        relThumbPath = '%s_THUMB_%s%s'%(base,sizeStr,ext)
    if fsRoot==None: fsRoot = FS_ROOT()
    assert relImgPath[0] == '/'  and  relImgPath[-1] != '/'
    assert relThumbPath[0] == '/'  and  relThumbPath[-1] != '/'
    absImgPath, absThumbPath = fsRoot+relImgPath, fsRoot+relThumbPath
    imgMtime, thumbMtime = getmtime(absImgPath, includeMeta=False), getmtime(absThumbPath, includeMeta=False, noExistTime=0)
    if thumbMtime < imgMtime:
        cmd = ['convert', absImgPath, '-thumbnail', '%s%s'%(sizeStr, '^' if crop else '')] + (['-gravity', 'center', '-extent', sizeStr] if crop else [])  + [absThumbPath]
        subprocess.check_call(cmd)
    return relThumbPath


