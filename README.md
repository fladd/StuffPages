StuffPages
==========

A quick way to create simple web pages with [Markdown][]


Installation
------------

1. Make sure [Python][] is installed on your web server [^Python2]
2. Install the Python package [Markdown2][] on your web server
3. Download the [.zip][] and extract it in a (non-served) directory on your web server


Usage
-----

1. Adapt the `config.py` file according to your settings:

  * `markdown_dir` is where your markdown (.md) files are located
  * `extras` is a dictionary with additional modules to be used by the [Markdown2][] Python package
  * `defaults` are the values to be used when nothing is set in the metadata of the Markdown file

2. Create a Markdown pages (.md files) in your `markdown_dir`
3. Run `python update.py` to create corresponding web pages (.html files) in the `output_dir`, that will be served at `url`


[^python2]: Only tested with Python 2!

[Markdown]: http://daringfireball.net/projects/markdown/
[Python]: http://www.python.org
[Markdown2]: https://github.com/trentm/python-markdown2
[.zip]: https://github.com/fladd/StuffPages/archive/master.zip
