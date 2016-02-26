#!/usr/bin/env python

import sys, os, codecs, mako.template, mako.lookup, json
import makofw


def getMakoTemplateDeps(tmplPath, allDeps=None, recursive=True):
    ''' Pretend that you have a template named "index.html.tmpl", and it
        inherits from "_master.tmpl".  When you give this function the path to
        the index template, this will return the path to _master so you can
        check the modification times of the deps.  This way, you can regenerate
        index.html if the master changes.
    
        Several methods are used to determine dependencies:
        
        First, standard Mako "inherit" lines are detected (using a very
        primitive algorithm... so be nice with your line formatting, please.):

            <%inherit file="_master.tmpl"/>

        Secondly, dependencies are extracted from 'namespace' lines:

            <%namespace name="task_common" file="task/common.tmpl"/>
        
        Finally, the user can add lines like this:

            ## DEP: /path/to/dep/file1.py
            ## DEP: ../_file2.tmpl

        2016-02-18: Added ability to use '.meta' JSON 'extra_deps' entry:

            page.html.tmpl         ...checks:
            page.html.tmpl.meta -- { "extra_deps" : ["/a/b/c.xyz", "../e/f.ghi"] }

        Dependencies are recursively searched for dependencies too.
    '''
    assert os.path.isabs(tmplPath)
    if allDeps==None: allDeps = []
    deps = []
    lineGen = None
    try:
        for line in codecs.open(tmplPath, encoding='utf-8'):
            line = line.strip()
            if not line: continue
            pieces = line.split()
            if len(pieces)>2  and  pieces[0]=='##'  and  pieces[1]=='DEP:':
                path = line[line.index(pieces[2]):]
                if not os.path.isabs(path):
                    path = os.path.join(os.path.dirname(tmplPath), path)
                deps.append(path)
            elif line.startswith('<%inherit')  or  line.startswith('<%namespace'):
                fileI = line.index('file=')
                quoteChar = line[fileI+5]
                path = line[fileI+6:line.index(quoteChar, fileI+6)]
                if not os.path.isabs(path):
                    path = os.path.join(os.path.dirname(tmplPath), path)
                deps.append(path)
    except UnicodeDecodeError:
        # This often happens when trying to open a binary file, such as a JPEG (which gets included as a dependency as some other template).
        pass
    metaDeps = makofw.meta(tmplPath).get('extra_deps', [])
    if isinstance(metaDeps, basestring): raise ValueError("META 'extra_deps' needs to be a list, not a string!")
    deps.extend(metaDeps)
    newDeps = []
    for d in deps:
        if d not in allDeps:
            newDeps.append(d)
            allDeps.append(d)
    if not recursive: return newDeps
    for d in newDeps:
        if os.path.exists(d): getMakoTemplateDeps(d, allDeps)
    return allDeps



class ChrisTemplateLookup(object):
    ''' I used the "French Cafe" method {1} to build a better Mako
        TemplateLookup.  The default TemplateLookup handles relative paths of
        includes in a very strange way that is non-intuitive and doesn't scale.
        This one implements a much simpler one.

        {1} http://samba.org/ftp/tridge/misc/french_cafe.txt
    '''
    def __init__(self, defaultPath):
        assert os.path.isabs(defaultPath)
        self.uriCache = {}
        self.defaultPath = defaultPath
    def adjust_uri(self, uri, relativeto):
        result = os.path.normpath(os.path.join(os.path.dirname(
                         self.uriCache.get(relativeto, self.defaultPath)), uri))
        #print 'adjust_uri', uri, relativeto, result
        return result
    def get_template(self, uri):
        path = os.path.normpath(os.path.join(os.path.dirname(self.defaultPath),
                                                                           uri))
        template = getMakoTemplate(path, lookup=self)
        self.uriCache[template.uri] = path
        #print 'got_tempalte: %r %r'%(template.uri,path)
        return template
#   def __getattr__(self, name):
#       raise ValueError('ChrisTemplateLookup: Tried to getattr: %r'%name)
#   def __setattr__(self, name, value):
#       print 'ChrisTemplateLookup: Setting attr: %r %r'%(name,value)
#       object.__setattr__(self, name, value)



def getTemplateCode(template, outputEncoding='ascii'): return ('\n'.join(['%03d: %s'%(i+1,l) for i,l in enumerate(template._code.splitlines())])).encode(outputEncoding, 'backslashreplace')

__ALL_TEMPLATES = []
def getMakoTemplate(path, lookup=None):
    if not lookup: lookup = ChrisTemplateLookup(path)
    template = None
    try: template = mako.template.Template(codecs.open(path, encoding='utf-8').read(), lookup=lookup, input_encoding='utf-8', filename=path)
    except:
        class FakeTmpl: _code = '!!! Mako Parse Error !!!'
        __ALL_TEMPLATES.append((path, FakeTmpl()))
        raise
    __ALL_TEMPLATES.append((path,template))
    return template


def makoRender(path, kwargs):
    try:
        template = getMakoTemplate(path)
        return template.render_unicode(**kwargs)
    except:
        print >> sys.stderr, '\nThere was an error in one of the following templates:'
        for p,t in reversed(__ALL_TEMPLATES):
            print >> sys.stderr, '\n\n=== Template Code for %s: ==='%(p,)
            print >> sys.stderr, getTemplateCode(t)
        print >> sys.stderr
        print >> sys.stderr, sys.exc_info()[1].message
        print >> sys.stderr
        raise


def varsplit(var):
    if "=" not in var: return (var, "")
    return var.split("=", 1)


if __name__=='__main__':
    tmplPath = sys.argv[1]
    kwargs = dict([varsplit(var) for var in sys.argv[2:]])
    tmplPath = os.path.abspath(tmplPath)
    sys.stdout.write(makoRender(tmplPath, kwargs))


