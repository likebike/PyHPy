


Welcome to BetterThanCPP; a simple framework for producing static websites.



=== Overview ===

Do your work in ~/src.  "*.tmpl" files will be rendered as Mako templates.
All other types of files will just be copied normally.  ".*" and "_*" files
are considered to be hidden files and are not published...except for
".htaccess", which IS published.  Those are most of the rules, but to see all
the rules in detail, read ~/Makefile.py.

Publish your work to dev.nomake.org by running 'make' in ~/.

When you're happy with the result, publish your work to nomake.org by running
'make prod' in ~/.

Files that you put in ~/src/cache will be served with very aggressive Expires
Headers caching, which will cause the items to be *permanently* cached on the
browser side.  This results in super speeds for the website, but be aware that
if you need to push new data out, you need to use a new filename because
changes to existing files won't be seen by client browsers.

You can use some basic .htaccess directives, like the ones from mod_rewrite
and mod_headers, and Mime types.  CGI and PHP are *not* enabled.

All of this is actually served by the 'addon' user's "mianfeidawang" webserver
framework.  Communication works like this:

            HTTP             HTTP             Static & .htaccess
      Web   <-->  Webfaction <-->   Apache    <---------------->    ~/www
    Browser         Nginx          in 'addon'                     in 'nomake'
                                    account.                        account.

The httpd.conf file that controls everything is located at
/home/addon/apache/conf/httpd.conf.  This file is generated from
/home/addon/apache/conf/.src/httpd.conf.tmpl... so if you need to make a
change, edit the template and regenerate the httpd.conf file by running "make
publish" in /home/addon/apache/conf/.src.  (You shouldn't need to make any
changes, though...)

The 'addon' Apache writes its logs to serveral places:

    /home/nomake/logs/access_log   # These two are specific to the nomake.org
    /home/nomake/logs/error_log    # site.  You'll usually want to look here.

    /home/addon/apache/logs/access_log   # These two are useful for diagnosing
    /home/addon/apache/logs/error_log    # 'systematic' issues with the server,
                                         # rather than the site.



=== Why Static? ===

About 10 years ago, Christopher Sebastian made his first website: stockguy.net. 

Christopher was young and foolish back then, and he really didn't know what he
was doing.  Amazingly enough, Christopher somehow managed to use the C
Preprocessor (cpp), along with 'make' to produce that site.  He would define
various page elements as C (#define) macros, and then '#include' them in "C
template files" that he would write.  By using this approach, Christopher was
able to create a website that automatically shared common elements between
pages.  He would run the preprocessor on some input templates and produce a
bunch of .html outputs.  Finally, he would ftp those .html outputs to his
$2/month 100MB CGI-enabled (!) webhost, and that was that.

Sounds crazy, right?  Well, it was.  Needless to say, the C Preprocessor just
can't handle that sort of thing very well.  It wasn't very long before this
setup became more trouble than it was worth, and Christopher abandoned this
"static" approach for newfangled "agile" web technologies, such as CherryPy,
Turbogears, Ruby on Rails, Django, Wordpress, CodeIgniter, and Mongrel2.
These new dynamic technoliges made Christopher's life much easier, and he made
dozens and dozens of websites more quickly and easier than ever before.  Life
was good.

But as time went by, Christopher noticed something: all of the high-tech
websites that he was making required a steady amount of maintenance.  Things
would break, libraries needed updates, APIs would change, and servers would
get moved around and reconfigured.  Not to mention the security and bug fixes!
Christopher was always moving on to new things, so he didn't maintain the old
websites enough, and after a while all of his "agile" websites broke and went
offline.

Meanwhile, that old stupid stockguy.net site is still running... with zero
maintenance after a decade.  We can now see the real value of a static
website: once it's online, it will stay online... forever.

Now, Christopher is at it again.  But this time, he's doing things the "right
way".  Once again, he is making a pure-static framework, but this time he's
using tools that are made for the job: Mako and Python.  This new framework is
simple enough for anyone to use, even if they don't know anything about
programming.  Also, the resulting website is pure static and will be able to
stay online forever with zero maintenance.


