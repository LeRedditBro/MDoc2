<h1>create_tags_from_folder</h1>

<span><b>Declaration:</b></span>

```py
def create_tags_from_folder(folder_path, rel_path="")
```



<p>the function runs over all items in the given directory
if the item it finds is a directory, this function will run on it (recursive)
else if the item it finds is a file, it will run <code>create_tags_from_file</code> on it</p>

<span><b>Args:</b></span><table><tbody><tr><th>name</th><th>type</th><th>description</th></tr><tr><td>folder_path</td><td>str</td><td>path to the folder to run on</td></tr><tr><td>rel_path</td><td>str</td><td>relative path, used for recursive calls</td></tr></tbody></table>

