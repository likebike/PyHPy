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
#     <%! import makofw %>
#     <%block filter="makofw.markdown">
#     Hello
#     -----
#     
#     This is **MarkDown**!
#     </%block>
def markdown(string, output_format='html5'):
    md = _markdown.Markdown(output_format=output_format, extensions=['markdown.extensions.fenced_code', DoubleSpaceMarkdownExtension(), EqualSignHeaderMarkdownExtension()])

    # # I thought I needed to be able to escape angle brackets, but it turns out that I can already
    # # use <%! ... %> stuff directly -- i just need to add a blank line to separate it from inline content.
    # # But since I went thru the trouble to figure out the right way to solve this problem, I'm keeping this code for reference, since it's not intuitive:
    # if allow_anglebracket_escape:
    #     echars = md.ESCAPED_CHARS   # Usually, ESCAPED_CHARS is actually coming from the class level.  That's why we need to use this process to set it on the instance without affecting the class data.
    #     if '<' not in echars:
    #         md.ESCAPED_CHARS = ['<'] + echars
    #         assert '<' not in _markdown.Markdown.ESCAPED_CHARS  # Make sure we didn't actually modify the class data.

    out  = '<article class="markdown-body">'    # We replicate the wrapper used on GitHub for compatibility with 3rd party CSS.
    out += md.convert(string)
    out += '</article>'
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
            fs_path = fsRoot + path + '.markdown'
        if not os.path.exists(fs_path):
            # Another markdown extension?
            fs_path = fsRoot + path + '.md'
        if not os.path.exists(fs_path):
            # Nope, not markdown.  How about a template?
            fs_path = fsRoot + path + '.mako'
        if not os.path.exists(fs_path):
            # Alternative mako template extension:
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
    crop = False
    if width==None and height==None: height = 128
    if width==None and height!=None: sizeStr = 'x%d'%(int(round(height)),)
    if width!=None and height==None: sizeStr = '%d'%(int(round(width)),)
    if width!=None and height!=None: crop, sizeStr = True, '%dx%d'%(int(round(width)), int(round(height)))
    if relThumbPath==None:
        base, ext = os.path.splitext(relImgPath)
        relThumbPath = '%s_THUMB_%s%s'%(base,sizeStr,ext)
    assert fsRoot[0] == '/'  and  fsRoot[-1] != '/'
    assert relImgPath[0] == '/'  and  relImgPath[-1] != '/'
    assert relThumbPath[0] == '/'  and  relThumbPath[-1] != '/'
    absImgPath, absThumbPath = fsRoot+relImgPath, fsRoot+relThumbPath
    imgMtime, thumbMtime = getmtime(absImgPath, includeMeta=False), getmtime(absThumbPath, includeMeta=False, noExistTime=0)
    if thumbMtime < imgMtime:
        cmd = ['convert', absImgPath, '-thumbnail', '%s%s'%(sizeStr, '^' if crop else '')] + (['-gravity', 'center', '-extent', sizeStr] if crop else [])  + [absThumbPath]
        print cmd
        subprocess.check_call(cmd)
    return relThumbPath


