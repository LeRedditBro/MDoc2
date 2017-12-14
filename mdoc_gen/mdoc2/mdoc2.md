<h1>mdoc2.py</h1><span><b>Methods:</b></span><table><tbody><tr><th>Method</th><th>Description</th></tr><tr><td><a href="create_tags_from_folder.md">create_tags_from_folder</a></td><td>the function runs over all items in the given directory
if the item it finds is a directory, this function will run on it (recursive)
else if the item it finds is a file, it will run <code>create_tags_from_file</code> on it</td></tr><tr><td><a href="create_tags_from_file.md">create_tags_from_file</a></td><td>the function checks if the file is supported for documentation
supported types: .py
if the file is supported the function opens the file and extracts key components from its raw text, matching a selection specifically picked for its file type format
for each component it finds, it handles it based on whether its a <code>class</code> or a <code>method</code></td></tr><tr><td><a href="create_function_page.md">create_function_page</a></td><td>the function comes from a standpoint that the specified parameters are for a <code>method</code> and builds a method page by:
combining tags found in the file with <code>tags.doc_to_tags</code> and inserting html between tactical points in-order to make the page more appealing to the user</td></tr><tr><td><a href="create_class_page.md">create_class_page</a></td><td>the function comes from a standpoint that the specified parameters are for a <code>class</code> and builds a class page by:
combining tags found in the file with <code>tags.doc_to_tags</code> and inserting html between tactical points in-order to make the page more appealing to the user</td></tr><tr><td><a href="create_file_map.md">create_file_map</a></td><td>used to print a file map, can be used with mapping of file name to either:
- print to terminal with color
- save to md file for navigation</td></tr></tbody></table>

