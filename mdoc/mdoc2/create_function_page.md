<h1>create_function_page</h1>

<span><b>Declaration:</b></span>

```py
def create_function_page(file_path, class_name, method_name, method_params, method_doc_body)
```



<p>the function comes from a standpoint that the specified parameters are for a <code>method</code> and builds a method page by:
combining tags found in the file with <code>tags.doc_to_tags</code> and inserting html between tactical points in-order to make the page more appealing to the user</p>

<span><b>Args:</b></span><table><tbody><tr><th>name</th><th>type</th><th>description</th></tr><tr><td>file_path</td><td>str</td><td>the path to the file we read from, required for positioning the save file</td></tr><tr><td>class_name</td><td>str</td><td>if the method is not tied to a class, specify <code>None</code></td></tr><tr><td>method_name</td><td>str</td><td>the method name, without any syntax</td></tr><tr><td>method_params</td><td>str</td><td>the parameters the function is expecting, wrapped in parenthesis</td></tr><tr><td>method_doc_body</td><td>str</td><td>the text content of the method's docstring</td></tr></tbody></table>

<span><b>Returns:</b></span><table><tbody><tr><th>name</th><th>type</th><th>description</th></tr><tr><td>method_name</td><td>str</td><td>the method name</td></tr><tr><td>desc</td><td>str</td><td>the description for the method (if found)</td></tr></tbody></table>

