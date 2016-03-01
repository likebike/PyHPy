<%inherit file="/photos.html.mako" />
<%!
    import os, pyhpy
    ## These get overridden by inheriting templates:
    THIS_PHOTO, PREV_PHOTO, NEXT_PHOTO = None, None, None
%>
<div id=bigPhotoArea>
  <a id=prev class=navLink href="${pyhpy.url('/photos/%s.html'%(self.attr.PREV_PHOTO,), mtime=None)}"><i class="fa fa-arrow-left"></i>&nbsp;Previous</a>
  <a id=next class=navLink href="${pyhpy.url('/photos/%s.html'%(self.attr.NEXT_PHOTO,), mtime=None)}">Next&nbsp;<i class="fa fa-arrow-right"></i></a>
  <%
    photoPath = os.path.join(self.photosDir(), self.attr.THIS_PHOTO) + '.jpeg'
    meta = pyhpy.meta(photoPath)
  %>
  <div id=textStuff>
    <p class=description>${meta['description']}</p>
    <p class=location>${meta['location']}</p>
  </div>
  <img id=bigPhoto src="${pyhpy.url('/static/photoalbum/%s.jpeg'%(self.attr.THIS_PHOTO,))}">
</div>

