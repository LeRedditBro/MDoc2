<h1>create_tags_from_file</h1>

<span><b>Declaration:</b></span>

```py
def create_tags_from_file(file_path)
```



<p>the function checks if the file is supported for documentation
supported types: .py
if the file is supported the function opens the file and extracts key components from its raw text, matching a selection specifically picked for its file type format
for each component it finds, it handles it based on whether its a <code>class</code> or a <code>method</code></p>

<span><b>Args:</b></span><table><tbody><tr><th>name</th><th>type</th><th>description</th></tr><tr><td>file_path</td><td>str</td><td>path to the file to check and/or extract</td></tr></tbody></table>

