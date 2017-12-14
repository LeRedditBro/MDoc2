<h1>gen</h1><h3>NormalTag &gt; gen</h3>

<span><b>Declaration:</b></span>

```py
def gen(self)
```



<span><b>Returns:</b></span><table><tbody><tr><th>name</th><th>type</th><th>description</th></tr><tr><td>string</td><td>str</td><td>returns the complete text resulting from the combination of the specified parameters in the __init__</td></tr></tbody></table>

the tag `NormalTag("p", "hello world", None)` will `.gen()` into:
```<p>hello world</p>```

