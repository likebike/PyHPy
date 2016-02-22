<i class="fa fa-download fa-lg"></i> The Project Setup Process
==============================================================

Unlike most software tools, MakoFW is not supposed to be installed on your system;  Instead, you should download a copy of MakoFW into each new project that you create.  This ensures that your projects remain independent, and self-contained.  Here are the instructions to create a new MakoFW project:

Step 1:  If Necessary, Install Dependencies
-------------------------------------------

If your system doesn't already have them, you'll need to install Python2.7, GNU Make, and ImageMagick first:

```bash
sudo apt-get install python2.7 make imagemagick
```

(If there is sufficient demand, I can update MakoFW with Python3 support.)


Step 2:  Set Up the Project Directory and Download MakoFW
---------------------------------------------------------

Let's pretend that we want the new project to be stored at `~/mysite`.  In that case, you'd run:

```bash
mkdir -p ~/mysite                # Create the project directory.
cd ~/mysite                      # Enter the directory.
# Download the latest MakoFW to ~/mysite/makofw/ :
curl http://makofw.likebike.com/makofw-latest.tar.gz | tar x
```

At this point, our project directory has been created and MakoFW has been downloaded into the `makofw` subdirectory.  Next, let's copy the example `Makefile` and `input`:

```bash
cd ~/mysite
cp makofw/Makefile.example Makefile
cp -r makofw/input.example input
```

That's it.  We now have a functional MakoFW project.  In the next step, we will test it out.


Step 3:  Test the New Project
-----------------------------

Use the `make` command to build the project:

```bash
cd ~/mysite
make
```

The above command will produce an `output` directory, where the results are placed.  For your convenience, a simple web server is included to help you view the results:

```bash
cd ~/mysite
make devserver   # This will run a local HTTP server on port 8000.
```

Once the development web server is running, you can view your site at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) .

After you have confirmed that everything is working, you might want to take the opportunity to check your project into an SCM, like [Git](https://git-scm.com/).


<i class="fa fa-gift fa-lg"></i> Out-of-the-Box Functionality
=============================================================

If you just want a blog...
--------------------------

How to use FontAwesome
----------------------

Apache Expires Headers
----------------------
* .htaccess included

