Welcome to the MakoFW Demo Site!
================================

MakoFW is a minimalist static website generation framework, built on top of the [Mako](http://www.makotemplates.org/) template engine.


Static is Beautiful
-------------------

Static webpages have some very nice features:

* They are *fast*.  Nothing is faster than serving a static page.  You can easily survive huge traffic spikes.

* They are immortal.  Once a static webpage is online, it almost never breaks.  No maintenence is required to keep them online.  They handle server upgrades, library updates, and host migrations with ease.

* Impossible to hack.  A static page never introduces any extra security vulnerabilities.  Much, *much* safer than a dynamic site.


Mako is Awesome
---------------

I chose to build this framework on top of [Mako](http://www.makotemplates.org/) for the following reasons:

* Mako can produce any kind of output -- not just webpages.  Therefore, you can use MakoFW for any kind of static output generation.  (I like general solutions.)

* [Powerful Template Inheritence](http://docs.makotemplates.org/en/latest/inheritance.html).  Makes it easy to create consistent, scalable websites with huge numbers of pages.

* Small Feature Set.  Helps you to learn it quickly.

* Widely Used.  Used by [reddit.com](http://www.reddit.com/), and [Pylons/Pyramid](http://www.pylonsproject.org/).


MakoFW Makes it Easy
--------------------

MakoFW combines powerful tools like `rsync`, `make`, and `mako-render`, and adds a layer of convenience and integration on top.

* [MarkDown](https://en.wikipedia.org/wiki/Markdown) Integration.  Just type your content text into an `.md` file and it becomes a beautiful webpage.  Easy enough for my Mom.

* Here's the typical process of building a site with MakoFW:

    1. Place content (like MarkDown), mako templates, and static files (like images) into an `input` directory.
    1. `make`
    1. Content and templates are rendered, and the results are published to an `output` directory.
    1. View the output in a web browser.
    1. GOTO 1




[<i class="fa fa-photo"></i> View the Example Photo Album](${self.URL('/photos.html', timestamp=None)})
----------------------------------------------------------------------

[<i class="fa fa-newspaper-o"></i> Read the Example Blog](${self.URL('/blog.html', timestamp=None)})
----------------------------------------------------------------------------

