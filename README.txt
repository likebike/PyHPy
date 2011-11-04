=== Overview ===

Do your work in ~/src.

Publish your work to dev.nomake.org by running 'make' in ~/.

When you're happy with the result, publish your work to nomake.org by running 'make prod' in ~/.

Files that you put in ~/src/cache will be served with very aggressive Expires Headers caching, which will cause the items to be *permanently* cached on the browser side.  This results in super speeds for the website, but be aware that if you need to push new data out, you need to use a new filename because changes to existing files won't be seen by client browsers.


