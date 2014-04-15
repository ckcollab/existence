existence
=========

Checks static html files for bad or empty links. See [here](http://www.ericcarmichael.com/writing-my-first-python-package.html) why I wrote this, I hate missing details!

# Example bad or empty links

```
<a href=""></a>            Empty
<a href></a>               Empty
<a href="python.org"></a>  Any bad link, this one is missing http://
```

# Usage

Command line

    > python existence.py /path/to/dir

Python

    from existence import check_directory
    check_directory("/path/to/dir")

Existence will recursively check each subdir as well!
