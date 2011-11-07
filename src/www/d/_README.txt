=== The 'd' Directory ===

The 'd' directory's purpose is to allow us to create links to our big files
that will expire periodically.

Basically, our big files (like packages) are stored at ~/www/bigfiles/.  Every
day, cron will create a new randomly-named symlink located in this 'd'
directory, and the website will be re-made to use that new link.  Then, cron
will also delete 'd' symlinks that are older than a month.  This way, we can
have a static site that has links that expre after a month.

