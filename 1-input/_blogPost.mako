<%inherit file="/blog.html.mako" />
<% 
  assert self.uri.endswith('.html.mako'), 'Unexpected Extension: %r'%(self.uri,)
  date,mdFilename,meta,title,image = self.attr.postInfo(self.uri[:-5]+'.md')
%>
<h1 class=postTitle>${title}</h1>
<div class=postMeta>Published <span class=postDate>${date}</span>,&nbsp; by <span class=postAuthor>${meta['author']}</span></div>
<img class="postMainImg roundBorder" src="${image}" />
${next.body()}
