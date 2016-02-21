Welcome to the MakoFW Demo Site!
================================

MakoFW is a minimalist static website generation framework, built on top of the [Mako](http://www.makotemplates.org/) templating engine.


Static is Beautiful
-------------------

Static webpages have some very nice features:

* Static is *Fast*.  Nothing is faster than serving a static page.  They can easily survive huge traffic spikes.

* Static is Immortal.  Once a static webpage is online, it almost never breaks.  No maintenence is required to keep them online.  They handle server upgrades, library updates, and host migrations with ease.

* Impossible to Hack.  A static page never introduces any extra security vulnerabilities.  Much, *much* safer than a dynamic site.

* Easy to Host.  Static websites are supported by *every* web host.


Mako is Awesome
---------------

I chose to build this framework on top of [Mako](http://www.makotemplates.org/) for the following reasons:

* Mako can produce any kind of output -- not just webpages.  Therefore, you can use MakoFW for any kind of static output generation.  (I like general solutions.)

* [Powerful Template Inheritence](http://docs.makotemplates.org/en/latest/inheritance.html).  Makes it easy to create consistent, scalable websites, no matter how large your site gets.

* Small Feature Set.  Helps you to learn it quickly.

* Widely Used.  Two famous users are [reddit.com](http://www.reddit.com/) and [Pylons/Pyramid](http://www.pylonsproject.org/).


MakoFW Makes it Easy
--------------------

MakoFW combines powerful tools like `rsync`, `make`, and `mako-render`, and adds a layer of convenience and integration on top.

* [MarkDown](https://en.wikipedia.org/wiki/Markdown) Integration.  Just type your content text into an `.md` file and it becomes a beautiful webpage.  Easy enough for my Mom.

* Faster Load Times.  Thanks to built-in support for aggressive client-side `Expires Header` caching, your pages will approach theoretical limits of speed and responsiveness.

* Improved Error Reporting.  When things go wrong, MakoFW produces very detailed and helpful error reports, allowing you to pin-point the cause of the problem with minimal effort.

* Here's the typical process of building a site with MakoFW:

    1. Create content (like MarkDown), mako templates, and static files (like images) in an `input` directory.
    1. Run `make`.  Content and templates are rendered, and the results are published to an `output` directory.
    1. View the output in a web browser.
    1. GOTO 1 until you're happy with the result.
    1. Upload the `output` directory to your webserver using `FTP` or `rsync`.

The best way to start learning MakoFW is to read through the included `input` files, which produce *this* website.  You can also read the documentation articles that are included in the [demo blog](${self.URL('/blog.html')}).  If you have questions, send them to [Christopher Sebastian](mailto:csebastian3@gmail.com).

[<i class="fa fa-photo"></i> View the Demo Photo Album](${self.URL('/photos.html', timestamp=None)})
----------------------------------------------------------------------

[<i class="fa fa-newspaper-o"></i> View the Demo Blog](${self.URL('/blog.html', timestamp=None)})
----------------------------------------------------------------------------

