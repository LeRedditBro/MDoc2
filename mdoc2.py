from tags import *
import os
import pathlib
import argparse

# define preset hardcoded extract methods for each supported language
DOC_PRESETS = {
    "py": {
        # def|class     function_name       (function parameters)       :       """(with no @ignore)        doc content         """
        "find_all": re.compile("(?P<type_raw>def|class) (?P<function_name>.+?)(?P<function_params>\(.+?\))?:\n *[\"\']{3} *(?!=@ignore)\n(?P<doc_body>[\s\S]+?)\n *[\"\']{3}"),
        "raw_types": {"def": "method", "class": "class"}
    }
}

out_dir = None
cwg = os.getcwd()

class_list = []
# a list of lists, where each list is a list of methods
method_list = []


def create_tags_from_folder(folder_path, rel_path=""):
    """
    @p
    the function runs over all items in the given directory
    if the item it finds is a directory, this function will run on it (recursive)
    else if the item it finds is a file, it will run <code>create_tags_from_file</code> on it

    @table
    Args:
        folder_path (str): path to the folder to run on
        rel_path (str): relative path, used for recursive calls
    """

    # files_in_folder = os.listdir(folder_path)
    # for folder_file in files_in_folder:
    #     file_path = folder_path + "/" + folder_file
    #     if os.path.isfile(file_path):
    #         create_tags_from_file(file_path)
    #     elif os.path.isdir(file_path):
    #         create_tags_from_folder(file_path)
    files_in_folder = os.listdir(folder_path + "/" + rel_path)
    for folder_file in files_in_folder:
        file_path = folder_path + "/" + folder_file
        if os.path.isfile(file_path):
            create_tags_from_file(rel_path + folder_file)
        elif os.path.isdir(file_path):
            create_tags_from_folder(folder_path, rel_path + "/" + folder_file + "/")


def create_tags_from_file(file_path):
    """
    @p
    the function checks if the file is supported for documentation
    supported types: .py
    if the file is supported the function opens the file and extracts key components from its raw text, matching a selection specifically picked for its file type format
    for each component it finds, it handles it based on whether its a <code>class</code> or a <code>method</code>

    @table
    Args:
        file_path (str): path to the file to check and/or extract
    """

    global class_list, method_list

    class_list = []
    method_list = []

    lang = re.findall(r"\.([^.]+?)$", file_path)[0]

    # only run if the language is accepted

    if lang in DOC_PRESETS:

        with open(file_path) as f:
            string_file = f.read()
            f.close()

        preset = DOC_PRESETS[lang]

        for m in preset["find_all"].findall(string_file):
            type_raw, function_name, function_params, doc_body = m

            if preset["raw_types"][type_raw] == "method":
                # create method for class

                if not class_list:
                    method_list.append(create_function_page(file_path, class_list[-1][0] if class_list else None, function_name, function_params, doc_body))
                else:
                    class_list[-1][1].append(create_function_page(file_path, class_list[-1][0] if class_list else None, function_name, function_params, doc_body))

                pass
            elif preset["raw_types"][type_raw] == "class":
                class_list.append((function_name, [], file_path, function_params, doc_body))

        file_index_text = ""

        class_list_desc = []

        for cls in class_list:
            class_list_desc.append(create_class_page(cls[2], cls[0], cls[3], cls[4], cls[1]))

        # classes into the index list
        if class_list:
            table_str = "<table><tbody><tr><th>Class</th><th>Description</th></tr>"

            for classes in class_list_desc:
                table_str += "<tr>%s</tr>" % ("<td><a href=\"%s/%s.md\">%s</a></td><td>%s</td>" % (classes[0], classes[0], classes[0], classes[1]))

            table_str += "</tbody></table>"

            file_index_text += "<span><b>Classes:</b></span>" + table_str + "\n\n"

        # methods into the index list
        if method_list:
            table_str = "<table><tbody><tr><th>Method</th><th>Description</th></tr>"

            for methods in method_list:
                table_str += "<tr>%s</tr>" % ("<td><a href=\"%s.md\">%s</a></td><td>%s</td>" % (methods[0], methods[0], methods[1]))

            table_str += "</tbody></table>"

            file_index_text += "<span><b>Methods:</b></span>" + table_str + "\n\n"

        # generate index file (only if text is present tho)
        if file_index_text:
            file_index_dir = out_dir + "/" + os.path.splitext(file_path)[0]
            file_index_name = (file_index_dir.split("/")[-1])
            file_index_dir = file_index_dir + "/" + file_index_name

            file_index_text = ("<h1>%s</h1>" % (file_index_name + "." + lang)) + file_index_text

            with open(file_index_dir+".md", "w") as f:
                f.write(file_index_text)
                f.close()


def create_function_page(file_path, class_name, method_name, method_params, method_doc_body):
    """
    @p
    the function comes from a standpoint that the specified parameters are for a <code>method</code> and builds a method page by:
    combining tags found in the file with <code>tags.doc_to_tags</code> and inserting html between tactical points in-order to make the page more appealing to the user

    @table
    Args:
        file_path (str): the path to the file we read from, required for positioning the save file
        class_name (str): if the method is not tied to a class, specify <code>None</code>
        method_name (str): the method name, without any syntax
        method_params (str): the parameters the function is expecting, wrapped in parenthesis
        method_doc_body (str): the text content of the method's docstring

    @table
    Returns:
        method_name (str): the method name
        desc (str): the description for the method (if found)
    """

    folder_dir = out_dir + "/" + os.path.splitext(file_path)[0] + ("/"+class_name if class_name else "")

    if not os.path.isdir(folder_dir):
        pathlib.Path(folder_dir).mkdir(parents=True, exist_ok=True)

        # write meta.txt to folder to determine its type in the future
        with open(folder_dir + "/meta.txt", "w") as f:
            f.write("class" if class_name else "file")
            f.close()

    tags = doc_to_tags(method_doc_body)

    if tags[0].tag == "p":
        desc = tags[0].text
    else:
        desc = "No information is given... first element was not of type paragraph!"

    fs_class_name = (class_name if class_name else "")

    tags.insert(0, "<h1>%s</h1>%s" % (method_name, "<h3>" + fs_class_name + " &gt; " + method_name + "</h3>" if class_name else ""))

    tags.insert(1, "<span><b>Declaration:</b></span>\n\n```py\ndef %s\n```\n\n" % (method_name + method_params))

    file_text = ""

    for tag in tags:
        file_text += (tag if type(tag) == str else tag.gen()) + "\n\n"

    with open(folder_dir+"/"+method_name+".md", "w") as f:
        f.write(file_text)
        f.close()

    return method_name, (desc or "")


def create_class_page(file_path, class_name, class_impl, class_doc_body, class_methods):
    """
    @p
    the function comes from a standpoint that the specified parameters are for a <code>class</code> and builds a class page by:
    combining tags found in the file with <code>tags.doc_to_tags</code> and inserting html between tactical points in-order to make the page more appealing to the user

    @table
    Args:
        file_path (str): the path to the file we read from, required for positioning the save file
        class_name (str): the class name, without any syntax
        class_impl (str): the parameters the function is expecting, wrapped in parenthesis
        class_doc_body (str): the text content of the method's docstring
        class_methods (List<Tuple<str, str>>): the methods to list under the class page

    @table
    Returns:
        class_name (str): the class name
        desc (str): the description for the class (if found)
    """

    folder_dir = out_dir + "/" + os.path.splitext(file_path)[0] + ("/" + class_name)
    # if class_name else "")

    if not os.path.isdir(folder_dir):
        pathlib.Path(folder_dir).mkdir(parents=True, exist_ok=True)

        # write meta.txt to folder to determine its type in the future
        with open(folder_dir + "/meta.txt", "w") as f:
            f.write("class")
            f.close()

    tags = doc_to_tags(class_doc_body)

    desc = tags[0].text if tags and tags[0].text == "p" else ""

    tags.insert(0, "<h1>%s</h1>" % class_name)

    table_str = "<table><tbody><tr><th>Method</th><th>Description</th></tr>"

    for class_method in class_methods:

        table_str += "<tr>%s</tr>" % ("<td><a href=\"%s.md\">%s</a></td><td>%s</td>" % (class_method[0], class_method[0], class_method[1]))

    table_str += "</tbody></table>"

    tags.insert(1, "<span><b>Methods:</b></span>" + table_str)

    tags.insert(1, "<span><b>Declaration:</b></span>\n\n```py\nclass %s\n```\n\n" % (class_name + class_impl))

    file_text = ""

    for tag in tags:
        file_text += (tag if type(tag) == str else tag.gen()) + "\n\n"

    with open(folder_dir+"/"+class_name+".md", "w") as f:
        f.write(file_text)
        f.close()

    return class_name, desc


CHAR_X_LEN = 2
CHAR_Y_LEN = 1
CHAR_X_PADDING = 2

CHAR_UR = "┗" + ("━" * CHAR_X_LEN)
# CHAR_UR = "┗" + ("═" * CHAR_X_LEN)
CHAR_UD = "┃" + (" " * CHAR_X_LEN)
CHAR_CLEAR = " " + (" " * CHAR_X_LEN)
CHAR_UDR = "┣" + ("━" * CHAR_X_LEN)
# CHAR_UDR = "┣" + ("═" * CHAR_X_LEN)


def create_file_map(directory, full_dir="", trans_func=None, add_index_files=False, rel=""):
    """
    @p
    used to print a file map, can be used with mapping of file name to either:
    - print to terminal with color
    - save to md file for navigation

    @table
    Returns:
        string (str): the string file map
    """

    flag = False

    if not full_dir:
        flag = True
        full_dir = directory

    items = [f for f in os.listdir(full_dir) if f != "meta.txt" and (not add_index_files and f != directory+".md") and not (flag and f == "index.md")]

    meta_path = full_dir + "/meta.txt"

    item_type = "dir"

    if os.path.isfile(meta_path):
        with open(meta_path, "r") as f:
            item_type = f.read()
            f.close()

    dir_name = "" if flag else directory

    if trans_func:
        directory = trans_func(directory, item_type, rel)

    rel = rel + dir_name + "/"

    text = [directory]

    n = len(items)

    for i in range(0, n):
        item = items[i]

        if i == 0 and CHAR_Y_LEN > 0:
            text.append(CHAR_UD)

        if i == n-1:
            mark_type = CHAR_UR
            mark_ud = CHAR_CLEAR
        else:
            mark_type = CHAR_UDR
            mark_ud = CHAR_UD

        item_dir = full_dir + "/" + item

        if os.path.isfile(item_dir):
            item_text = trans_func(item, "method", rel)

            if item_text:
                text.append(mark_type+item_text)
        else:
            lines = create_file_map(item, item_dir, trans_func, add_index_files, rel)

            m = len(lines)

            for j in range(0, m):

                line = lines[j]

                if j == 0:
                    mark_type_j = mark_type
                else:
                    mark_type_j = mark_ud

                text.append(mark_type_j + line)

        if CHAR_Y_LEN > 0:
            text.append(mark_ud)

    return "\n".join([(" " * CHAR_X_PADDING) + f for f in text]) if flag else text


ap = argparse.ArgumentParser()

ap.add_argument("out", metavar="OUT", type=str)


def tree_item_to_badge(item, item_type, rel):

    print(rel + item)

    switcher = {
        "dir": item,
        "class": "<img src=\"https://img.shields.io/badge/Class-%s-cyan.svg?style=flat-square\" height=\"20px\" style=\"vertical-align: bottom\">" % item.replace("_", "__").replace("-", "--"),
        "method": "<img src=\"https://img.shields.io/badge/Method-%s-orange.svg?style=flat-square\" height=\"20px\" style=\"vertical-align: bottom\">" % item.replace("_", "__").replace("-", "--"),
        "file": "<a href=\"%s\"><img src=\"https://img.shields.io/badge/File-%s-blue.svg?style=flat-square\" height=\"20px\" style=\"vertical-align: bottom\"></a>" % (rel, item.replace("_", "__").replace("-", "--"))
    }
    return switcher.get(item_type, "No item type found ?")


if __name__ == "__main__":

    out_arg = ap.parse_args().out
    out_dir = out_arg + "/mdoc_gen"
    #
    # out_dir = cwg + "/mdoc_gen"
    create_tags_from_folder(cwg)

    print(create_file_map(out_dir, trans_func=lambda name, item_type, rel: ("\033[100;97m" if item_type == "dir" else
                          "\033[43;97m" if item_type == "method" else
                          "\033[47;97m" if item_type == "class" else "\033[46;97m") + name + "\033[0m" + (" - class" if item_type == "class" else " - method" if item_type == "method" else " - file" if item_type == "file" else "")))

    with open(out_dir+"/index.md", "w") as fl:
        fl.write("<h1>Welcome to the automatically generated documentation!</h1><br><p>Have a look at what we have to offer:</p><br><pre>\"")
        fl.write(create_file_map(out_dir, trans_func=tree_item_to_badge))
        fl.write("\"</pre>")
        fl.close()

    print("Created markdown for project! at:")
    print("\033[44;97m%s\033[0m\n" % out_dir)


