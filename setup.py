import os
from setuptools import setup


try:
    with open('README.md') as readme:
        long_description = readme.read()
except (IOError, ImportError):
    long_description = ''

entry_points = {
    'console_scripts': [
        'existence = existence:main',
    ]
}

setup(
    install_requires = [
        "lxml>=3.3.4",
        "cssselect>=0.9.1"
    ],
    name="existence",
    py_modules=["existence"],
    entry_points=entry_points,
    version="0.2.2",
    author="Eric Carmichael",
    author_email="eric@ckcollab.com",
    description="Checks static .html files for bad links",
    long_description=long_description,
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
