// Here is Javascript that will run on the photos page.


if(jQuery.browser.msie  &&  jQuery.browser.version<7) {
  // I'm not going to put the effort into making the Javascript work for IE 6.
  // Just use the non-Javascript version.
} else {
    jQuery(function() {
        jQuery('img#bigPhoto').load(function () {
            // Gets executed when the image 'src' finishes loading.
            jQuery('div#bigPhotoArea').slideDown('slow');
        });
        jQuery('li.thumbnail a').click(function() {
            jQuery('img#bigPhoto').attr('src', jQuery(this).attr('href'));
            return false;
        });
        jQuery('a#next').click(function() {
            var curSrc = jQuery('img#bigPhoto').attr('src');
            var curI = jQuery.inArray(curSrc, photos);   // IE has no indexOf method.
            var newI = curI + 1;
            if(newI >= photos.length) newI = 0;
            jQuery('img#bigPhoto').attr('src', photos[newI]);
            return false;
        });
        jQuery('a#prev').click(function() {
            var curSrc = jQuery('img#bigPhoto').attr('src');
            var curI = jQuery.inArray(curSrc, photos);   // IE has no indexOf method.
            var newI = curI - 1;
            if(newI < 0) newI = photos.length - 1;
            jQuery('img#bigPhoto').attr('src', photos[newI]);
            return false;
        });
    });
}
