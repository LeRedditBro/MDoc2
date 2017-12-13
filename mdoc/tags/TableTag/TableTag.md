<h1>TableTag</h1>

<span><b>Declaration:</b></span>

```py
class TableTag(NormalTag)
```



<span><b>Methods:</b></span><table><tbody><tr><th>Method</th><th>Description</th></tr><tr><td><a href="__init__.md">__init__</a></td><td></td></tr><tr><td><a href="gen.md">gen</a></td><td>No information is given... first element was not of type paragraph!</td></tr></tbody></table>

<p>accepts a special flag: <code>reg</code>
the <code>reg</code> determines in which way the tag should break down its text content in-order to output it as a table in html format</p>

reg accepts:
+ the following format: `{column_name1} random text goes here {column_name_2} random text goes here {column_name_3}`, ie: `{name} ({type}): {description}` will match with `param_name (param_type): param_description`
+ aliases: the following are recognized: `google` = `{name} ({type}): {description}`
+ leaving `reg` blank will result to default alias `google`

