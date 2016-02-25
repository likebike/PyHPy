[Mako](http://www.makotemplates.org/) is a powerful (and fast) templating language, built on top of [Python](https://www.python.org/).  I recommend reading [Mako's excellent documentation](http://docs.makotemplates.org/en/latest/).

Here is what I consider to be the bare minimum you need to know to use Mako well:

<table>
<tr><th>Mako Template Code</th><th>Output</th></tr>
<tr>
  <td><pre>line 0
line 1
line 2</pre></td>
  <td><pre>
line 0
line 1
line 2
</pre></td>
  </td>
</tr>
</table>


* Simple text and unicode
* Comments, <${'%text'}>
* Newline escaping
* $ {...}
* if else
* for, while
* %block  (REQUIRES TOO MUCH UNDERSTANDING, otherwise you can't see the difference between %def)
* %def
* local code
* module-level code
    * accessible/overridable via self.attr  (DO NOT MENTION.  Encourages behavior that requres deep knowledge.)
* escaping -- for html/url/markdown escaping/filtering, using the '|' pipe method and filter= method.  Introduced here becasue module-level code is a good place for filters or imports of filters.
* inheritance
    * self.body(), next.body()
    * overriding defs and blocks
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


