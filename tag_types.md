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