<i class="fa fa-download fa-lg"></i> The Project Setup Process
==============================================================

Unlike most software tools, MakoFW is not supposed to be installed globally on your system;  Instead, you should download a local copy of MakoFW into each new project that you create.  This ensures that your projects remain independent, and self-contained.  Here are the instructions to create a new MakoFW project:

Step 1:  If Necessary, Install Dependencies
-------------------------------------------

If your system doesn't already have them, you'll need to install Python2.7, GNU Make, and ImageMagick:

```bash
sudo apt-get install python2.7 make imagemagick
```

(If there is sufficient demand, I can update MakoFW with Python3 support.)


Step 2:  Initialize the Project Directory
-----------------------------------------

Let's pretend that we want the new project to be stored at `~/mysite/`.  In that case, you'd run:

```bash
mkdir -p ~/mysite                # Create the project directory.
cd ~/mysite/                     # Enter the directory.
# Download the latest MakoFW to ~/mysite/makofw/ :
curl http://makofw.likebike.com/makofw-latest.tar.gz | tar x
```

At this point, our project directory has been created and MakoFW has been downloaded into the `makofw` subdirectory.  Next, let's copy the example `Makefile` and `input`:

```bash
cd ~/mysite/
cp makofw/Makefile.example Makefile
cp -r makofw/input.example input
```

That's it.  We now have a functional MakoFW project.  In the next step, we will test it out.


Step 3:  Test the New Project
-----------------------------

Use the `make` command to build the project:

```bash
cd ~/mysite/
make
```

The above command will produce an `output` directory, where the results are placed.  For your convenience, a simple web server is included to help you view the results:

```bash
cd ~/mysite/
make devserver   # This will run a local HTTP server on port 8000.
```

Once the development web server is running, you can view your site at <http://127.0.0.1:8000/> .

After you have confirmed that everything is working, you might want to take the opportunity to check your project into an SCM, like [Git](https://git-scm.com/).


<i class="fa fa-gift fa-lg"></i> Out-of-the-Box Functionality
=============================================================

MakoFW comes with an example website (the site you're reading right now), which you might want to use as a starting point for your project.


MarkDown-Powered Demo Blog
--------------------------

The demo blog is generated from a directory of `.md` posts (written in the MarkDown text format), with matching `.meta` files for metadata (like Author, Summary, Post Image, and Publication Date).

The demo blog generates a separate HTML page for each post, and shows a list of all the posts, sorted by reverse Publication Date.

If you just want to get some articles online quickly, the included demo blog might be a good starting point -- just create your own `.md` and `.meta` files in the `/input/blog/` directory, and then run `make`.


FontAwesome
-----------

The example site uses [FontAwesome](http://fontawesome.io/), which provides more than 600 vector graphic icons.  [View the complete set of icons here](http://fontawesome.io/icons/).  Here are a few examples:

<i class="fa fa-3x fa-bicycle"></i> &nbsp;
<i class="fa fa-3x fa-fort-awesome"></i> &nbsp;
<i class="fa fa-3x fa-birthday-cake"></i> &nbsp;
<i class="fa fa-3x fa-cubes"></i> &nbsp;
<i class="fa fa-3x fa-envelope-o"></i> &nbsp;
<i class="fa fa-3x fa-heartbeat"></i> &nbsp;
<i class="fa fa-3x fa-line-chart"></i> &nbsp;
<i class="fa fa-3x fa-signal"></i> &nbsp;
<i class="fa fa-3x fa-wrench"></i> &nbsp;
<i class="fa fa-3x fa-thumbs-o-down"></i> &nbsp;
<i class="fa fa-3x fa-cog fa-spin"></i> &nbsp;

It's easy to use a FontAwesome icon on your site;  Just include the `fa-*` CSS classes on your elements.  The `<i>` tag is often used for this purpose.  For example:

```html
I like to ride my <i class="fa fa-bicycle"></i>!
```

...would produce this output:  I like to ride my <i class="fa fa-bicycle"></i>!


Thumbnail Creation
------------------

The `makofw.thumb()` function makes it easy to produce thumbnail images.  The demo blog and photo album both make frequent use of this feature.  Here are some examples of how to use it:

```html
<img src="${'$'}{makofw.thumb(self.FS_ROOT(), '/static/blogImg/default.jpg', width=150)}" />
<img src="${'$'}{makofw.thumb(self.FS_ROOT(), '/static/blogImg/default.jpg', height=150)}" />
<img src="${'$'}{makofw.thumb(self.FS_ROOT(), '/static/blogImg/default.jpg', width=150, height=150)}" />
```

...and here's the output:

<%! import makofw %>
<img src="${self.URL(makofw.thumb(self.FS_ROOT(), '/static/blogImg/default.jpg', width=150))}" />
<img src="${self.URL(makofw.thumb(self.FS_ROOT(), '/static/blogImg/default.jpg', height=150))}" />
<img src="${self.URL(makofw.thumb(self.FS_ROOT(), '/static/blogImg/default.jpg', width=150, height=150))}" />

Notice that the image is cropped-to-fit if `width` and `height` are both specified.


Apache Expires Headers
----------------------

`Expires` headers instruct web browsers to employ their most aggressive form of client-side caching.  This caching will reduce the number of requests that are issued to the server, and will dramatically improve your site's load time and responsiveness.  However, when using aggressive caching, you need a way to notify clients when new data is available... otherwise they will continue to use their cached versions and won't notice the new stuff.

The example site comes with .htaccess files that enable `Expires` headers for all requests to `/static/...` URLs.  It also provides a way to make it easy to make updates to these files: the `input/__init__.tmpl` file defines the `self.URL(path, mtime)` function.  This function is useful for generation of URLs that incorporate a website mount point and a timestamp.  For the following examples, assume that your site will be hosted at `http://xyz.com/store/...` (mount point = `"http://xyz.com/store"`):

<table style="font-size: 85%">
  <tr><th>Mako Template Code</th><th>Output</th></tr>
  <tr><td><code>&lt;a href="${'$'}{self.URL('/static/css/home.css')}"&gt;...&lt;/a&gt;</code></td><td><code>&lt;a href="http://xyz.com/store/static/css/home.css?_=12345678"&gt;...&lt;/a&gt;</code><br>(The '_' value is the filesystem modification time of 'home.css'.)</td></tr>
  <tr><td><code>&lt;a href="${'$'}{self.URL('/home.html', mtime=None)}"&gt;...&lt;/a&gt;</code></td><td><code>&lt;a href="http://xyz.com/store/home.html"&gt;...&lt;/a&gt;</code><br>Since this URL is not underneath <code>/static/</code>, Expires headers will not be used.  We can use <code>mtime=None</code> to disable the addition of a timestamp because it's a bit ugly.</td></tr>
  <tr><td><code>self.URL()</code></td><td>This is a special case.  It returns the path of the template that is currently being rendered, without the mount point.  For example, <code>"/home.html.tmpl"</code>.</td></tr>
</table>

The first example in the above table shows how how easy it is to generate URLs that include the filesystem modification time.  This timestamp helps clients to know when new data is available.  Therefore, you can achieve the best of both worlds: aggressive client-side caching, with convenient ability to publish data updates.


