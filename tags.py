import re
import os

# region Tag classes

re_match_file = re.compile("file=\"(.+?)\"")
re_find_element = re.compile("@(?P<tag>.+?)( (?P<flags>.+?))?\n(?:(?=\n|$)|(?P<body>[\s\S]+?)(?:(?=\n\n)\n\n|$))")

re_find_pair = re.compile("(.+?)=\"(.+?)\"")


def doc_to_tags(docstring):
    """
    @p
    the function breaks down a given docstring (plain text) into <code>Tag</code> objects
    each tag has its own unique way of expressing its attributes into string format
    see tags below

    @table
    Args:
        docstring (str): the plain text docstring to process

    @table
    Returns:
        tags (List<NormalTag>): a list of items implementing <code>NormalTag</code>

    @md
    file="tag_types.md"
    """

    tags = []

    for match in re_find_element.finditer(docstring):
        gd = match.groupdict()

        tag = gd["tag"]
        body = gd["body"]

        flags = {}
        if "flags" in gd and gd["flags"]:
            split = gd["flags"].split(" ")
            for s in split:
                k, v = re_find_pair.search(s).group(0)
                flags[k] = v

        if tag == "table":
            tags.append(TableTag(body, flags))
        elif tag == "md":
            tags.append(MDTag(body, flags))
        else:
            tags.append(NormalTag(tag, body, flags))

    return tags


class NormalTag:
    """
    @p
    The base tag class, used to inherit base class features and control base tag mechanics
    """

    def __init__(self, tag, text, flags):
        """
        @p
        constructs a <code>NormalTag</code> object
        the normal tag object is used to manage the passage of tag types, attributes and innerHTML from string format

        @table
        Args:
            tag (str): the html tag type, ie: p - paragraph, hr - horizontal rule ...
            text (str): this is the inner html of the tag, ie: what goes between two &lt;tag&gt;s
            flags (dict): the flags are the attributes the tag will get, the dict key is the key in the tag, and the dict value is the value in the tag

        @md
        >Notes:
        > + this is the base class for the tags
        > + `file="path_to_your_file.md"` found inside the text will be turned to the content of the file specified
        """
        self.tag = tag
        self.text = text
        self.flags = flags

        file_text = "404 - file not found!"

        if text:

            temp_body = text

            temp_body = re.sub("[ ]{2,}", "", temp_body)

            for match in re_match_file.findall(text):

                if os.path.isfile(match):
                    with open(match, "r") as f:
                        file_text = f.read()
                        f.close()

                temp_body = temp_body.replace("file=\"%s\"" % match, file_text, 1)

            self.text = temp_body

    def gen(self):
        """
        @table
        Returns:
            string (str): returns the complete text resulting from the combination of the specified parameters in the __init__

        @md
        the tag `NormalTag("p", "hello world", None)` will `.gen()` into:
        ```<p>hello world</p>```
        """

        str_attr = ""
        for k, v in self.flags.items():
            str_attr += " "+k+"=\"%s\"" % v

        return "<"+self.tag + str_attr + ">"+(self.text or "")+"</"+self.tag+">"


class MDTag(NormalTag):
    """
    @p
    this tag does not generate html format string, but returns plain text to be parsed by the markdown syntax
    """
    def __init__(self, text, flags):
        """
        @p

        @table
        Args:
            text (str): this is the inner html of the tag, ie: what goes between two &lt;tag&gt;s
            flags (dict): the flags are the attributes the tag will get, the dict key is the key in the tag, and the dict value is the value in the tag
        """
        super().__init__("md", text, flags)

    def gen(self):
        """
        @p

        @table
        Returns:
            text (str): just returns the <code>text</code> parameter passed to this tag, not as html format
        """
        return self.text


class TableTag(NormalTag):
    """
    @p
    accepts a special flag: <code>reg</code>
    the <code>reg</code> determines in which way the tag should break down its text content in-order to output it as a table in html format

    @md
    reg accepts:
    + the following format: `{column_name1} random text goes here {column_name_2} random text goes here {column_name_3}`, ie: `{name} ({type}): {description}` will match with `param_name (param_type): param_description`
    + aliases: the following are recognized: `google` = `{name} ({type}): {description}`
    + leaving `reg` blank will result to default alias `google`
    """

    __TABLE_ALIASES = {
        "google": "{name} ({type}): {description}"
    }

    def __init__(self, text, flags):
        """
        @p

        @table
        Args:
            text (str): this is the inner html of the tag, ie: what goes between two &lt;tag&gt;s
            flags (dict): the flags are the attributes the tag will get, the dict key is the key in the tag, and the dict value is the value in the tag
        """
        super().__init__("table", text, flags)
        if "regex" in flags:
            reg = flags["regex"]
        else:
            reg = "google"

        # check for aliases in the regex
        if reg in self.__TABLE_ALIASES:
            reg = self.__TABLE_ALIASES[reg]

        # create a list of headers, extracted from the template mustaches
        self.headers = re.findall(r"{(.+?)}", reg)

        # create the expected regex expression, that will extract coming lines into their template components
        reg = re.escape(reg)

        self.reg = re.compile("^"+re.sub(r"\\{.+?\\}", r"(.+?)", reg)+"$")

    def gen(self):
        """
        @table
        Returns:
            string (str): returns a table in html format with the text from __init__ broken down into it
        """
        split = self.text.split("\n")
        title = split[0]
        lines = split[1:]
        table = "<span><b>"+str(title)+"</b></span><table><tbody><tr><th>" + ("</th><th>".join(self.headers)) + "</th></tr>"
        for line in lines:
            tds = self.reg.findall(line)[0]

            table += "<tr><td>"+("</td><td>".join(tds))+"</td></tr>"
        table += "</tbody></table>"
        return table

# endregion
