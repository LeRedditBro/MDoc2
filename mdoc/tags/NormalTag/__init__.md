<h1>__init__</h1><h3>NormalTag &gt; __init__</h3>

<span><b>Declaration:</b></span>

```py
def __init__(self, tag, text, flags)
```



<p>constructs a <code>NormalTag</code> object
the normal tag object is used to manage the passage of tag types, attributes and innerHTML from string format</p>

<span><b>Args:</b></span><table><tbody><tr><th>name</th><th>type</th><th>description</th></tr><tr><td>tag</td><td>str</td><td>the html tag type, ie: p - paragraph, hr - horizontal rule ...</td></tr><tr><td>text</td><td>str</td><td>this is the inner html of the tag, ie: what goes between two &lt;tag&gt;s</td></tr><tr><td>flags</td><td>dict</td><td>the flags are the attributes the tag will get, the dict key is the key in the tag, and the dict value is the value in the tag</td></tr></tbody></table>

>Notes:
> + this is the base class for the tags
> + `404 - file not found!` found inside the text will be turned to the content of the file specified

