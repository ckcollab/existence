existence
=========

Checks static html files for bad or empty links. See [here](http://www.ericcarmichael.com/writing-my-first-python-package.html) why I wrote this, I hate missing details!

# Example bad or empty links

```html
<a href=""></a>            Empty
<a href></a>               Empty
<a href="python.org"></a>  Any bad link will fail, this one is missing http://
```

# Usage

Command line

    > existence /path/to/dir

Python

```python
from existence import check_directory
check_directory("/path/to/dir")
```

Existence will recursively check each subdir as well!


# Running tests

    > python -m unittest discover
