<h1>doc_to_tags</h1>

<span><b>Declaration:</b></span>

```py
def doc_to_tags(docstring)
```



<p>the function breaks down a given docstring (plain text) into <code>Tag</code> objects
each tag has its own unique way of expressing its attributes into string format
see tags below</p>

<span><b>Args:</b></span><table><tbody><tr><th>name</th><th>type</th><th>description</th></tr><tr><td>docstring</td><td>str</td><td>the plain text docstring to process</td></tr></tbody></table>

<span><b>Returns:</b></span><table><tbody><tr><th>name</th><th>type</th><th>description</th></tr><tr><td>tags</td><td>List<NormalTag></td><td>a list of items implementing <code>NormalTag</code></td></tr></tbody></table>

## @table - the table tag
syntax:
```md
@table reg="{name} ({type}): {description}"
Table title here:
    name1 (type1): description1
    name1 (type2): description2
    name1 (type3): description3
```

## @md - the markdown tag
syntax:
```md
@md
the text here will appear as pure markdown
## this is mardown <h2> !
```

## @lang - the codeblock tag
syntax:
```md
@lang type="py"
text written in here will appear through a ```py``` block
```

## @<tag name> - the normal html tag
syntax:
```md
@p
this is paragraph

@img src="http://image_url.png"

@hr

@br

@span
some text here

@code
some more highlighted text here

and so on...
```

