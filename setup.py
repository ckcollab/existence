import os
from setuptools import setup

readme = open(os.path.join(os.path.dirname(__file__), "README.md")).read()

setup(
    name="existence",
    py_modules=["existence"],
    version="0.0.1",
    author="Eric Carmichael",
    author_email="eric@ckcollab.com",
    description="Checks static .html files for bad links",
    long_description=readme,
    license="MIT",
    keywords="link checker",
    url="https://github.com/ckcollab/existence",
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
