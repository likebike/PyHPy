<%!
    def stripBlankLines(string):
        out = string.splitlines()
        while out and not out[0].strip(): out = out[1:]
        while out and not out[-1].strip(): out = out[:-1]
        return '\n'.join(out)
%>
<%def name="EXAMPLE_CODE(files, output)">
<ul class=exampleCode>
  %for fname,data in files:
    <li class=exampleCode><div class=title>${fname}</div><div class=text>${data | stripBlankLines,h}</div></li>
  %endfor
    <li class=exampleOutput><div class=title>Output</div><div class=text>${output | stripBlankLines,h}</div></li>
</ul>
</%def>

<i class="fa fa-graduation-cap fa-lg"></i> Learning Mako by Example
=============================================================

[Mako](http://www.makotemplates.org/) is a powerful (and fast) templating language, built on top of [Python](https://www.python.org/).

This page teaches Mako's most essential features through a series of examples.  If you have questions about anything, or if you want to learn about other cool Mako features that are not covered here, refer to the [official Mako docs](http://docs.makotemplates.org/en/latest/).


Text and Unicode
----------------

${self.EXAMPLE_CODE([
('text_example.tmpl', ur'''
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

output=ur'''
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
${self.EXAMPLE_CODE([('comment_example.tmpl', ur'''
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

output=ur'''
Mako has two types of comments:



But you can't put comments at the end of lines.  ## See?

Here is a multi-line comment:





## The <'''+ur'''%text> tag tells Mako to just pass data directly to the output.
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

${self.EXAMPLE_CODE([('escape_example.tmpl', ur'''
Mako only has two character escapes:

  * backslash+newline  -->  ""  (empty string)
    (Enables you to prevent newlines from going to the output.)

  * '%%' at the beginning of a line  -->  '%'
    (A single '%' at the beginning of a line is interpreted as a flow control.)

Examples:

A back-slash at the end \
of a line will prevent \
the newline character \
from appearing in the \
output.

%if True:      # Flow Control lines start with a single '%'.
%endif

%% %% %%       The first '%%' becomes '%'.

    %% %% %%   Escape does not happen if the line is indented.


The following escapes do NOT work:

\\ $$ \$ \< \> \{ \}  \( \) \! \@ \# \% \^ \& \* \( \) \= \+ \~ \' \" \?
\<% foo='BAR' %>    Code still runs.
\${foo}             Eval still occurs.


## If you want to escape anything other than a newline, you need to
## perform a string operation instead.  You'll learn about the
## <% ... %> and ${...} operators later, but for now, pretend that
## you want to output a literal "${foo}", and you don't want Mako
## to interpret it.  You *could* use the <%text> operator that we
## already learned about, or you could do something like this:

    ${'$'}{foo}
    ${'${foo}'}
    ${'%if True:'}
''')],
output=ur'''
Mako only has two character escapes:

  * backslash+newline  -->  ""  (empty string)
    (Enables you to prevent newlines from going to the output.)

  * '%%' at the beginning of a line  -->  '%'
    (A single '%' at the beginning of a line is interpreted as a flow control.)

Examples:

A back-slash at the end of a line will prevent the newline character from appearing in the output.


% %% %%       The first '%%' becomes '%'.

   %% %% %%   Escape does not happen if the line is indented.


The following escapes do NOT work:

\\ $$ \$ \< \> \{ \}  \( \) \! \@ \# \% \^ \& \* \( \) \= \+ \~ \' \" \?
\    Code still runs.
\BAR             Eval still occurs.



    ${foo}
    ${foo}
    %if True:
''')}


${'${...}'}
-----------

${self.EXAMPLE_CODE([('eval_example.tmpl',ur'''
## ${...} performs an evaluation and puts the result in its place.
## The "..." can be any Python expression.

<% foo='BAR' %>
${}
${'foo'}
${foo}
${2+3}
The biggest number in the list is: ${max(1,2,3,4,5,4,3,2,1)}.
${'foo'.upper()}${ foo.lower() }
${ [1,2,3,4,5] }
${ {1:2, 3:4} }
${__import__('os').listdir('/')}

<%
class A(object):
    def __str__(self): return 'It uses __str__.'
    def __repr__(self): return 'It uses __repr__.'
%>

Does ${'${...}'} use __str__ or __repr__?  ${A()}
''')],
output=ur'''



foo
BAR
5
The biggest number in the list is: 5.
FOObar
[1, 2, 3, 4, 5]
{1: 2, 3: 4}
['mnt', 'vmlinuz.old', 'sys', 'dev', 'home', 'initrd.img', 'usr', 'var', 'srv', 'tmp', 'lib', 'lost+found', 'root', 'run', 'initrd.img.old', 'vmlinuz', 'boot', 'sbin', 'media', 'bin', 'opt', 'lib64', 'cdrom', 'proc', 'etc']



Does ${...} use __str__ or __repr__?  It uses __str__.
''')}


Flow Controls
-------------

${self.EXAMPLE_CODE([('flow_example.tmpl', ur'''
## All Python flow controls are supported:
##     if/elif/else, for, while, try/except, etc.
## You always need to use "%end..." to mark the end of blocks.

<% n, foo = 5, 'BAR' %>

## Indentation doesn't matter at all.  I just do it out of habit:
<ul>
%for i in range(n):
    <li>
    %if i == 3:
        Item Number Three: ${foo}
        <% break %>
    %else:
        Item #${i}: foo
    %endif
    </li>
%endfor
</ul>
## Look at the output that was produced by the loop.
## Notice that the 'break' command prevents the
## output of the final </li> tag, and also causes
## the </ul> to appear in a place that you
## probably didn't expect.


## Here's an example where I don't use indentation:
<p>\
%try:
${open('/proc/version').read().strip()}\
%except:
ERROR READING KERNEL VERSION\
%endtry
</p>
''')],
output=ur'''


<ul>
    <li>
        Item #0: foo
    </li>
    <li>
        Item #1: foo
    </li>
    <li>
        Item #2: foo
    </li>
    <li>
        Item Number Three: BAR
        </ul>


<p>Linux version 3.19.0-16-generic (buildd@komainu) (gcc version 4.9.2 (Ubuntu 4.9.2-10ubuntu13) ) #16-Ubuntu SMP Thu Apr 30 16:09:58 UTC 2015</p>
''')}


${'&lt;% ... %&gt;'}
--------------

${self.EXAMPLE_CODE([('inline_exec_example.tmpl', ur'''
## The <% ... %> block performs "inline execution" of Python code.
<%
    # This is normal Python code.
    def factorial(n):
        if n<=0: return 0
        if n==1: return 1
        return n*factorial(n-1)
    def times1000(n): return n*1000
        
    items = [(n,factorial(n)) for n in range(10)]
    total = 0
%>

%for (n,fact) in items:
    ## This code executes during each loop iteration:
    <% total += n %>
    factorial(${n})=${fact}, times1000(${n})=${times1000(n)}
%endfor

TOTAL = ${total}
''')], output=ur'''


    factorial(0)=0, times1000(0)=0

    factorial(1)=1, times1000(1)=1000

    factorial(2)=2, times1000(2)=2000

    factorial(3)=6, times1000(3)=3000

    factorial(4)=24, times1000(4)=4000

    factorial(5)=120, times1000(5)=5000

    factorial(6)=720, times1000(6)=6000

    factorial(7)=5040, times1000(7)=7000

    factorial(8)=40320, times1000(8)=8000

    factorial(9)=362880, times1000(9)=9000

TOTAL = 45
''')}


${'&lt;%! ... %&gt;'}
---------------

${self.EXAMPLE_CODE([('module_exec_example.tmpl', ur'''
## The <%! ... %> block performs "module execution" of Python code.
## It executes ONLY ONCE, near the top of the generated Python module.
## <%! ... %> is typically used for two things:
##     * import of modules
##     * definition of variables/functions/classes

<%!
    import os, pyhpy
    inline, module = [], []
%>

start
<%  inline.append('start') %>
<%! module.append('start') %>

%if True:
    if-True
    <%  inline.append('if-True') %>
    <%! module.append('if-True') %>
%endif

%if False:
    if-False
    <%  inline.append('if-False') %>
    <%! module.append('if-False') %>
%elif False:
    elif-False
    <%  inline.append('elif-False') %>
    <%! module.append('elif-False') %>
%else:
    else
    <%  inline.append('else') %>
    <%! module.append('else') %>
%endif

%for i in range(3):
    for
    <%  inline.append('for') %>
    <%! module.append('for') %>
%else:
    for-else
    <%  inline.append('for-else') %>
    <%! module.append('for-else') %>
%endfor

## Note that Mako does not support 'else' attached to 'while'.
%while True:
    while
    <%  inline.append('while') %>
    <%! module.append('while') %>
    <% break %>
%endwhile

## Note that Mako only supports try-except and try-finally,
## NOT try-except-finally.
%try:
    try-except
    <%  inline.append('try-except') %>
    <%! module.append('try-except') %>
%except:
    except
    <%  inline.append('except') %>
    <%! module.append('except') %>
%endtry

%try:
    try-finally
    <%  inline.append('try-finally') %>
    <%! module.append('try-finally') %>
%finally:
    finally
    <%  inline.append('finally') %>
    <%! module.append('finally') %>
%endtry

end
<%  inline.append('end') %>
<%! module.append('end') %>

inline execution = ${inline}
module execution = ${module}
 ''')], output=ur'''


start



    if-True



    else



    for


    for


    for


    for-else



    while



    try-except



    try-finally


    finally



end



inline execution = ['start', 'if-True', 'else', 'for', 'for', 'for', 'for-else', 'while', 'try-except', 'try-finally', 'finally', 'end']
module execution = ['start', 'if-True', 'if-False', 'elif-False', 'else', 'for', 'for-else', 'while', 'try-except', 'except', 'try-finally', 'finally', 'end']
''')}


&lt;%def&gt;
------------


<div class=tester>
</div>




${self.EXAMPLE_CODE([('', ur''' ''')], output=ur''' ''')}
${self.EXAMPLE_CODE([('', ur''' ''')], output=ur''' ''')}


* Simple text and unicode
* Comments, %text
* Newline escaping
* $ {...}
* if else
* for, while
* inline code
* module-level code
    * accessible/overridable via self.attr  (DO NOT MENTION.  Encourages behavior that requres deep knowledge.)
* %block  (REQUIRES TOO MUCH UNDERSTANDING, otherwise you can't see the difference between %def)
* %def
* escaping -- for html/url/markdown escaping/filtering, using the '|' pipe method and filter= method.  Introduced here becasue module-level code is a good place for filters or imports of filters.
* inheritance
    * self.body(), next.body()
    * overriding defs and blocks
    * capture()
    * pyhpy fragile syntax!
* %include
* Better understanding of 'self', 'local', 'next', 'parent', 'UNDEFINED', and 'context'
* How to debug when things go wrong
* PyHPy features
    * (provided in the __init__.tmpl file of the example project): self.URL(), self.FS_ROOT()
    * dependencies   (## DEP)  (MIGHT WANT TO CHANGE SYNTAX?)
    * meta
    * NOT SURE IF THIS IS THE RIGHT PAGE FOR THIS: Sane search paths.
    * NOT SURE IF THIS IS THE RIGHT PAGE FOR THIS: error reporting
    * IN MARKDOWN CHEAT SHEET:  Mention double-space and equalSignHeader extensions

