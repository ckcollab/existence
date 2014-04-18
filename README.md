existence
=========

Recursively scans directories for static html files for bad or empty links. See
[here](http://www.ericcarmichael.com/writing-my-first-python-package.html) why I wrote this, I hate missing details!

# Example bad or empty links

```html
<a href=""></a>            Empty
<a href></a>               Empty
<a href="python.org"></a>  Any bad link will fail, this one is missing http://
```

## Command line

    > existence /path/to/dir
    Checking links...
    57 of 57
    All of your links exist!

    > existence /path/to/bad/links
    Broken link found in file /path/to/bad/links/index.html on line 121 linking to None
    Broken link found in file /path/to/bad/links/other.html on line 22 linking to non-existant.html

## Python

```python
>>> from existence import scan
>>> scan("/path/to/dir")
[]
>>> scan("/path/to/bad/links")
[
    ('None', '/path/to/bad/links/index.html', 121),
    ('non-existant.html', '/path/to/bad/links/other.html', 22)
]
# Returns a list of bad url tuples: [(url, file_name, line_number)]
```

# Progress bar

To enable the progress bar `pip install progressbar==2.3`


# Running tests

    > python -m unittest discover
