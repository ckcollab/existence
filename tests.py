import unittest

from .existence import


# <a href></a> should trigger problem
# <a href=""></a> should trigger problem
# <a href="#"></a> shouldn't trigger problem

