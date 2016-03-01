<%inherit file="/_base_pretty.mako" />
<%! import os, pyhpy %>

%if self.uri==local.uri:

%else:
${next.body()}
<hr class=afterPost />
<h1>Related Blog Posts:</h1>
%endif

<ul class=posts>
%for i,(date,mdRelPath,meta,title,image) in enumerate(self.getPosts()):
    <li class="post ${'post-useSep' if i>0 else ''}">
        <a href="${pyhpy.url('%s'%(mdRelPath[:-3],), mtime=None)}">
            <img class="postImg roundBorder" src="${pyhpy.url(pyhpy.thumb(image, width=243, height=150))}" />
            <div class=postTitle>${title}</div>
            <div class=postSummary>${meta['summary']}</div>
            <div class=postMeta><span class=date>${meta['date']}</span> - by <span class=author>${meta['author']}</span></div>
        </a>
        <div class=clearFloats></div>
    </li>
%endfor
</ul>

<%block name='PAGE_CSS'>
  <link rel="stylesheet" type="text/css" href="${pyhpy.url('/static/css/blog.css')}">
</%block>
<%def name="getPosts()"><% return reversed(sorted([self.postInfo('/blog/'+x) for x in os.listdir(os.path.join(pyhpy.FS_ROOT(), 'blog')) if x.endswith('.html.md')])) %></%def>
<%def name="postInfo(mdRelPath)"><%
    assert mdRelPath.startswith('/')  and  mdRelPath.endswith('.html.md'), 'Unexpected blog post filename: %r'%(mdRelPath,)
    meta = pyhpy.meta(pyhpy.FS_ROOT()+mdRelPath)
    title = os.path.split(mdRelPath)[1][:-8].replace('_', ' ')
    return meta['date'], mdRelPath, meta, title, meta['image']
%></%def>
