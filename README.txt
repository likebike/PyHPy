


Welcome to PyHPy; a simple framework for producing static websites.


=== Installation ===

You need to have Python 2.6 or 2.7 installed.
Also, you need 'make'.  I use GNU Make 3.81.

To install, just extract the files from the archive you downloaded.  Then,
copy the Makefile.example to your project root and rename it to 'Makefile'.
Then, edit the Makefile and make sure that the variables at the top of the
file make sense for your project.  In particular, you should probably edit
these:

    PYHPY_DIR   --  The directory where the PyHPY package is.
    SRC_DIR     --  The directory where your source files and templates are.
    WWW_DEV     --  The directory that your Development site is served from.
    WWW_PROD    --  The directory that your Production site is served from.
    PYTHON      --  The path to your Python executable.
    PYTHONPATH  --  On Windows, you need to change the ':' to ';'.
                    Also, you may want to change '/' chars to '\\'.


=== Overview ===

Quick Summary:

    make       --  Build the development site.
    make fast  --  Build the development site by only publishing the files that
                   have changed, and skip ACL checks.
    make prod  --  Build the production site.


Do your work in the SRC_DIR that you defined in the Makefile.  '*.tmpl' files
will be rendered as Mako templates.  All other types of files will just be
copied normally.  '.*' and '_*' files are considered to be hidden files and are
not published... except for '.htaccess', which IS published.  Those are most of
the rules, but to see all the rules in detail, read $PYHPY_DIR/bin/publish.py.

Publish your work to the Development site by running 'make' in your project
root.  Or, if you're in a hurry, you can use 'make fast', which will skip ACL
synchronization.

When you're happy with the result, publish your work to your Production site by
running 'make prod' in your project root.

Files that you put in $SRC_DIR/static will be served with very aggressive
Expires Headers caching, which will cause the items to be *permanently* cached
on the browser side.  This results in super speeds for the website, but be aware
that if you need to push new data out, you need to use a new filename because
changes to existing files won't be seen by client browsers.  A convenience
function is defined to help manage this for you.  In the '_master.html.tmpl'
template, a "URL(paty, timestamp='auto')" function is defined that helps you
to generate URLs that automatically have the modification time of the file
included in the URL.  Use it like this:

    <a href="${self.URL('/static/img/photo.jpeg')}">Click Me</a>

After the template gets renered, the result will be something like this:

    <a href="/static/img/photo.jpeg?timestamp=12345678.0">Click Me</a>

You can use some basic .htaccess directives, like the ones from mod_rewrite
and mod_headers, and Mime types.  CGI and PHP are *not* enabled.


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
'static' approach for newfangled 'agile' web technologies, such as CherryPy,
Turbogears, Ruby on Rails, Django, Wordpress, CodeIgniter, and Mongrel2.
These new dynamic technoliges made Christopher's life much easier, and he made
dozens and dozens of websites more quickly and more easily than ever before.
Life was good.

But as time went by, Christopher noticed something: all of the high-tech
websites that he was making required a steady amount of maintenance.  Things
would break, libraries needed updates, APIs would change, and servers would
get moved around and reconfigured.  Not to mention the security and bug fixes!
Christopher was always moving on to new things, so he didn't maintain the old
websites enough, and after a while all of his 'agile' websites broke and went
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
















































=================================================================
=================================================================
=================================================================
=================================================================
=================================================================
=================================================================
=================================================================
=================================================================
=================================================================
=================================================================
=========                   =====================================
========= O L D   S T U F F =====================================
=========                   =====================================
========= O L D   S T U F F =====================================
=========                   =====================================
========= O L D   S T U F F =====================================
=========                   =====================================
========= O L D   S T U F F =====================================
=========                   =====================================
========= O L D   S T U F F =====================================
=========                   =====================================
========= O L D   S T U F F =====================================
=========                   =====================================
========= O L D   S T U F F =====================================
=========                   =====================================
========= O L D   S T U F F =====================================
=========                   =====================================
=================================================================
=================================================================
=================================================================
=================================================================
=================================================================
=================================================================
=================================================================
==========               ========================================
==========  I G N O R E  ========================================
==========               ========================================
=================================================================
=================================================================
=================================================================
=================================================================
=================================================================
=================================================================
=================================================================
=================================================================
=================================================================
=================================================================








=== Nomake.org File Structure ===

Life starts in ~/src/apps.  This is a directory structure of JSON files that
serves as a database for the build scripts.  Here is an example section of the
directory:

    apps/
    apps/aria2c
    apps/aria2c/app.json
    apps/aria2c/screenshots.json
    apps/aria2c/versions
    apps/aria2c/versions/1.13.0.json

The above listing shows one app entry: aria2c.  There is one apps/APPNAME
directory for each app.  Under that, there are several items:

    app.json --  Some data about the app, including its name, description,
                 homepage, etc.

    screenshots.json  --  A list of screenshots and their descriptions.

    versions  --  A directory containing version files.  The version files
                  contain information such as the package filename, its creation
                  date, and its checksums.

When you run a 'make' command, the FIRST thing that happens is the
~/bin/create_app_pages.py script runs and turns all this JSON data into TMPL
files in the ~/src/www/apps directory.

So, that's where the ~/src/www/apps pages come from.

In additon to that, you manually create TMPL, HTML, CSS, and JS (and whatever
else) under the ~/src/www/ directory.  (Just don't put any manual data
under ~/src/apps because that is an auto-generated area.)

The SECOND thing that a 'make' command does is copy (almost) everything from
~/src/www to ~/www/dev or ~/www/prod.  The file data and metadata (owner,
permissions, ACL, and sometimes the modification time (depending on file type))

So that's how stuff gets from the ~/src/www area to the ~/www area.

There's one more area that needs some explanation: ~/src/www/d.  This contains
a bunch of synlinks that all point to ~/www/bigfiles.  A new randomly-named
symlink is created daily (and the site is regenerated using this new symlink
in the download URLs), and any symlinks older than a month are deleted.  This
allows us to have auto-expiring download links so people don't leech off us
too much.



=== Server Architecture (of Christopher's WebFaction account) ===

All of this is actually served by the 'addon' user's 'mianfeidawang' webserver
framework.  Communication works like this:

            HTTP             HTTP             Static & .htaccess
      Web   <-->  Webfaction <-->   Apache    <---------------->    ~/www
    Browser         Nginx          in 'addon'                     in 'nomake'
                                    account.                        account.


The 'addon' Apache writes its logs to serveral places:

    /home/nomake/logs/access_log_addon   # These two are specific to the
    /home/nomake/logs/error_log_addon    # nomake.org site.  You'll usually
                                         # want to look here.


    /home/addon/apache/logs/access_log   # These two are useful for diagnosing
    /home/addon/apache/logs/error_log    # 'systematic' issues with the server,
                                         # rather than the site.


The httpd.conf file that controls everything is located at
/home/addon/apache/conf/httpd.conf.  Talk to Christopher if you need a change to
be made because this file is an important part of the 'mianfeidawang' framework,
which serves a dozen sites besides nomake.org.


