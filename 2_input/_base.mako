## You should always use this file as the top of your inheritance chain.  It provides some convenient infrastructure and it doesn't affect output.
## (Note that I am always using a '\' character at the end of each line to avoid outputting extra whitespace.)
<%! import os, pyhpy %>\
${next.body()}\
## Here, we provide some convenience infrastructure.  We can't provide this in the 'pyhpy' module because we are not aware of our project when running that code.
## We know that this _base.mako file is always going to be at the top level of our project, so therefore we can know our project root.
<%def name="FS_ROOT()"><%
    return os.path.dirname(local.attr._template_filename)
%></%def>\
<%def name="URL_ROOT()"><%
    # Customize the return value of this function to match your webapp mount point.
    # For example, if your website URL is http://xyz.com/blog/... ,
    # then this function should probably return '/blog' or 'http://xyz.com/blog'.
    # A value of '' implies that your website appears at the domain root (http://xyz.com/...).
    return ''
%></%def>\
<%def name="URL(path=None, mtime='auto')"><%
    buildDir = self.FS_ROOT()
    if path==None:
        # Make it easy to figure out which page is being rendered.
        # Just produce the URL to the template that is being rendered, WITHOUT THE URL-ROOT.
        # If you really need a web-usable URL, you can URL(URL()).
        assert self.attr._template_filename.startswith(buildDir)
        return self.attr._template_filename[len(buildDir):]
    return pyhpy.url(path, urlRoot=self.URL_ROOT(), fsRoot=buildDir, mtime=mtime)
%></%def>\
