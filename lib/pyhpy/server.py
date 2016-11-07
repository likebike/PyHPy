#!/usr/bin/env python
#
# Written 2016-02-25 by Christopher Sebastian
#
# Python's SimpleHTTPServer is pretty much what we want, except that it always serves relative to the current working directory.
# I need to be able to specify an alternate filesystem path for the docroot.  This way, the server can handle removal and movement
# of the underlying filesystem structure.  In other words, if I tell the server to use a docroot of /a/b/c/, and then I run
# "mv /a/b/c /a/b/x; mkdir /a/b/c" -- then I want the *new* (blank) /a/b/c directory to be served -- not the old one now located
# at /a/b/x .  Python's default SimpleHTTPServer remains attached to the original directory that it is started in, even after
# it gets moved.

import sys, SimpleHTTPServer, posixpath, os.path, urllib, subprocess


class PyHPyHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    # I have copy-pasted this method from SimpleHTTPServer.py, and I have modified it a tiny bit:
    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """ 
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        # Don't forget explicit trailing slash when normalizing. Issue17324
        trailing_slash = path.rstrip().endswith('/')
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = DOCROOT            ################# MODIFIED BY CHRISTOPHER SEBASTIAN -- changed "os.getcwd()" to "DOCROOT".
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path

    # I have added content auto-detection for files with no extension:
    def guess_type(self, path):
        """Guess the type of a file.

        Argument is a PATH (a filename).

        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.

        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.

        """

        base, ext = posixpath.splitext(path)
        if not ext: return subprocess.check_output(['/usr/bin/file', '-biL', path]).strip()   #####################  ADDED BY CHRISTOPHER SEBASTIAN
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']


DOCROOT=None   # This must be set.
def setDOCROOT(docroot):
    global DOCROOT
    assert docroot
    assert docroot[0] == '/', 'DOCROOT must be an absolute path.'
    assert docroot[-1] != '/', 'DOCROOT should not have a trailing slash.'
    DOCROOT = docroot
    print 'DOCROOT = %r'%(DOCROOT,)

def main():    
    if len(sys.argv) != 3: raise ValueError('usage: pyhpy.httpd PORT DOCROOT')
    setDOCROOT(os.path.abspath(sys.argv[2]))
    SimpleHTTPServer.test(HandlerClass=PyHPyHTTPRequestHandler)

if __name__ == '__main__': main()


