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
    install_requires=[
        "lxml>=3.3.4",
        "cssselect>=0.9.1"
    ],
    name="existence",
    py_modules=["existence"],
    entry_points=entry_points,
    version="0.3.0",
    author="Eric Carmichael",
    author_email="eric@ckcollab.com",
    description="Checks static .html files for bad links",
    description_content_type="text/markdown",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="link checker",
    url="https://github.com/ckcollab/existence",
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
