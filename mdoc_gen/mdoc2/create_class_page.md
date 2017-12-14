<h1>create_class_page</h1>

<span><b>Declaration:</b></span>

```py
def create_class_page(file_path, class_name, class_impl, class_doc_body, class_methods)
```



<p>the function comes from a standpoint that the specified parameters are for a <code>class</code> and builds a class page by:
combining tags found in the file with <code>tags.doc_to_tags</code> and inserting html between tactical points in-order to make the page more appealing to the user</p>

<span><b>Args:</b></span><table><tbody><tr><th>name</th><th>type</th><th>description</th></tr><tr><td>file_path</td><td>str</td><td>the path to the file we read from, required for positioning the save file</td></tr><tr><td>class_name</td><td>str</td><td>the class name, without any syntax</td></tr><tr><td>class_impl</td><td>str</td><td>the parameters the function is expecting, wrapped in parenthesis</td></tr><tr><td>class_doc_body</td><td>str</td><td>the text content of the method's docstring</td></tr><tr><td>class_methods</td><td>List<Tuple<str, str>></td><td>the methods to list under the class page</td></tr></tbody></table>

<span><b>Returns:</b></span><table><tbody><tr><th>name</th><th>type</th><th>description</th></tr><tr><td>class_name</td><td>str</td><td>the class name</td></tr><tr><td>desc</td><td>str</td><td>the description for the class (if found)</td></tr></tbody></table>

