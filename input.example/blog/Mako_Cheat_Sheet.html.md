[Mako](http://www.makotemplates.org/) is a powerful templating language, built on top of [Python](https://www.python.org/).  I recommend reading [Mako's excellent documentation](http://docs.makotemplates.org/en/latest/).

<http://abc.com/>

Here is a summary of the features I use most:

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


* inheritance
* global code
* local code
* $ {...}
* if else
* for
* %def
* %block
* self.body(), next.body()
* MakoFW features (provided in the __init__.tmpl file of the example project): self.URL(), self.FS_ROOT()
