<%inherit file="_base_pretty.mako" />
<%! import os, pyhpy %>

%if self.URL()=='/blog.html.mako':

%else:
${next.body()}
<hr class=afterPost />
<h1>Related Blog Posts:</h1>
%endif

<ul class=posts>
%for i,(date,mdFilename,meta,title,image) in enumerate(self.getPosts()):
    <li class="post ${'post-useSep' if i>0 else ''}">
        <a href="${self.URL('/blog/%s'%(mdFilename[:-3],), mtime=None)}">
            <img class="postImg roundBorder" src="${self.URL(pyhpy.thumb(self.FS_ROOT(), image, width=243, height=150))}" />
            <div class=postTitle>${title}</div>
            <div class=postSummary>${meta['summary']}</div>
            <div class=postMeta><span class=date>${meta['date']}</span> - by <span class=author>${meta['author']}</span></div>
        </a>
        <div class=clearFloats></div>
    </li>
%endfor
</ul>

<%block name='PAGE_CSS'>
  <link rel="stylesheet" type="text/css" href="${self.URL('/static/css/blog.css')}">
</%block>
<%def name="getPosts()"><% return reversed(sorted([self.postInfo(x) for x in os.listdir(os.path.join(self.FS_ROOT(), 'blog')) if x.endswith('.html.md')])) %></%def>
<%def name="postInfo(mdFilename)"><%
     assert mdFilename.endswith('.html.md')
     meta = pyhpy.meta(os.path.join(self.FS_ROOT(), 'blog', mdFilename))
     title = mdFilename[:-8].replace('_', ' ')
     return meta['date'], mdFilename, meta, title, meta['image']
%></%def>
