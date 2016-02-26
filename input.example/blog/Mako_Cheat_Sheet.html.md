<%def name="EXAMPLE_CODE(files, output)">
<ul class=exampleCode>
  %for fname,data in files:
    <li class=exampleCode><div class=title>${fname}</div><div class=text>${data.strip() | h}</div></li>
  %endfor
    <li class=exampleOutput><div class=title>Output</div><div class=text>${output.strip() | h}</div></li>
</ul>
</%def>

<i class="fa fa-graduation-cap fa-lg"></i> Learning Mako by Example
=============================================================

[Mako](http://www.makotemplates.org/) is a powerful (and fast) templating language, built on top of [Python](https://www.python.org/).

This page teaches the essential Mako features through a series of examples.  If you have questions about anything, or if you want to learn about the cool advanced Mako features that are not covered here, refer to the [official Mako docs](http://docs.makotemplates.org/en/latest/).


Text and Unicode
----------------

${self.EXAMPLE_CODE([
('text_example.tmpl', u'''
Everything in this example is just text, so it goes directly to the output.

Unicode is fully supported:  我喜欢看喜羊羊与灰太狼。

<p>HTML is just <b>text</b>.</p>

*MarkDown* is also _just_ [text](http://itsjusttext.com/).

def whatAboutCode(a,b,c):
    return 'Guess what -- code is text too!'

(function() {
    console.log("It doesn't matter what programming language.");
    alert("It's all just text.");
})();
''')],

output=u'''
Everything in this example is just text, so it goes directly to the output.

Unicode is fully supported:  我喜欢看喜羊羊与灰太狼。

<p>HTML is just <b>text</b>.</p>

*MarkDown* is also _just_ [text](http://itsjusttext.com/).

def whatAboutCode(a,b,c):
    return 'Guess what -- code is text too!'

(function() {
    console.log("It doesn't matter what programming language.");
    alert("It's all just text.");
})();
''')}


Comments and <${'%'}text>
--------------------
${self.EXAMPLE_CODE([('comment_example.tmpl', u'''
Mako has two types of comments:

## A line comment starts with two '#' characters.

        ## Line comments can be intented.

But you can't put comments at the end of lines.  ## See?

Here is a multi-line comment:
<%doc>
All these lines
    will not go
to the output.
</%doc>

<%doc>You can also use <%doc> on a single line.</%doc>

<%text>
## The <%text> tag tells Mako to just pass data directly to the output.
## This is sometimes useful when the data you want to produce
## conflicts with Mako syntax.

## Comments have no effect.  All Mako syntax is disabled.
<%doc>Same with multi-line comments.</%doc>
${"""You'll learn what these other features are supposed to do later.
     Right now, they do nothing because <%text> disables them."""}
<%def name="F()">foo</%def>
<% n=5 %>
%if n>3:
    ${self.F()}
%endif
</%text>

## Finally, after the </%text> tag, Mako starts processing again.
''')],

output=u'''
Mako has two types of comments:



But you can't put comments at the end of lines.  ## See?

Here is a multi-line comment:





## The <'''+'''%text> tag tells Mako to just pass data directly to the output.
## This is sometimes useful when the data you want to produce
## conflicts with Mako syntax.

## Comments have no effect.  All Mako syntax is disabled.
<%doc>Same with multi-line comments.</%doc>
${"""You'll learn what these other features are supposed to do later.
     Right now, they do nothing because <%text> disables them."""}
<%def name="F()">foo</%def>
<% n=5 %>
%if n>3:
    ${self.F()}
%endif


''')}



Escapes
-------

${self.EXAMPLE_CODE([('escape_example.tmpl', r'''
The only thing that can be backslash-escaped is a newline.

A back-slash at the end \
of a line will prevent \
the newline character \
from appearing in the \
output.

For example, you can NOT escape these other things:

\\ \$ \< \> \{ \}  \( \) \! \@ \# \% \^ \& \* \( \) \= \+ \~ \' \" \?

\<% foo='BAR' %>
\${foo}

## If you want to escape anything other than a newline, you need to
## perform a string operation instead.  You'll learn about the
## <% ... %> and ${...} operators later, but for now, pretend that
## you want to output a literal "${foo}", and you don't want Mako
## to interpret it.  You *could* use the <%text> operator that we
## learned about, or you could do something like this:

    ${'$'}{foo}
    ${'${foo}'}

In other words, use escapes for newlines, \
and string operations for everything else.
''')],
output=r'''
The only thing that can be backslash-escaped is a newline.

A back-slash at the end of a line will prevent the newline character from appearing in the output.

For example, you can NOT escape these other things:

\\ \$ \< \> \{ \}  \( \) \! \@ \# \% \^ \& \* \( \) \= \+ \~ \' \" \?

\
\BAR


    ${foo}
    ${foo}

In other words, use escapes for newlines, and string operations for everything else.
''')}


${'${...}'}
-----------

${self.EXAMPLE_CODE([('eval_example.tmpl','''
## The ${...} operator performs an evaluation and puts the result in its place.
## The "..." can be any Python expression.

<% foo='BAR' %>
${}
${'foo'}
${foo}
${2+3}
${max(1,2,3,4,5,4,3,2,1)}
${'foo'.upper()}
${foo.lower()}
${[1,2,3,4,5]}
${{1:2, 3:4}}
${__import__('os').listdir('/')}
''')],
output='''

foo
BAR
5
5
FOO
bar
[1, 2, 3, 4, 5]
{1: 2, 3: 4}
['mnt', 'sys', 'dev', 'home', 'usr', 'var', 'srv', 'tmp', 'lib', 'lost+found', 'root', 'run', 'boot', 'sbin', 'media', 'bin', 'opt', 'lib64', 'cdrom', 'proc', 'etc']
''')}


${'&lt;% ... %&gt;'}
--------------


<div>
</div>



${'&lt;%! ... %&gt;'}
---------------







* Simple text and unicode
* Comments, %text
* Newline escaping
* $ {...}
* local code
* module-level code
    * accessible/overridable via self.attr  (DO NOT MENTION.  Encourages behavior that requres deep knowledge.)
* if else
* for, while
* %block  (REQUIRES TOO MUCH UNDERSTANDING, otherwise you can't see the difference between %def)
* %def
* escaping -- for html/url/markdown escaping/filtering, using the '|' pipe method and filter= method.  Introduced here becasue module-level code is a good place for filters or imports of filters.
* inheritance
    * self.body(), next.body()
    * overriding defs and blocks
    * capture()
    * makofw fragile syntax!
* %include
* Better understanding of 'self', 'local', 'next', 'parent', 'UNDEFINED', and 'context'
* How to debug when things go wrong
* MakoFW features
    * (provided in the __init__.tmpl file of the example project): self.URL(), self.FS_ROOT()
    * dependencies   (## DEP)  (MIGHT WANT TO CHANGE SYNTAX?)
    * meta
    * NOT SURE IF THIS IS THE RIGHT PAGE FOR THIS: Sane search paths.
    * NOT SURE IF THIS IS THE RIGHT PAGE FOR THIS: error reporting
    * IN MARKDOWN CHEAT SHEET:  Mention double-space and equalSignHeader extensions

