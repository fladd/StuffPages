StuffPages
==========

A quick way to create simple web pages with [Markdown][]


Installation
------------

1. Make sure [Python 2][] is installed on your web server
2. Install the Python package [Markdown2][] on your web server
3. Download the source .zip from the [release page][] and extract it in a (non-served) directory on your web server


Usage
-----

1. Adapt the `config.py` file according to your settings:

  * `markdown_dir` is where your markdown pages (.md files) are located
  * `extras` is a dictionary with additional modules to be used by the [Markdown2][] Python package
  * `defaults` are the values to be used when nothing is set in the metadata of the Markdown file:
    * `output_dir` is where your web pages (.html files) will be written to
    * `url` is the URL from which the web page will be served from
    * `title` is the default title for web pages
    * `favicon` is a URL or file path for the favicon to be used
    * `style` is a URL or file path for the css style to be used

2. Create Markdown pages (.md files) in your `markdown_dir`
3. Run `python update.py` to create corresponding web pages (.html files) in the `output_dir`, that will be served at `url`



[Markdown]: http://daringfireball.net/projects/markdown/
[Python 2]: http://www.python.org
[Markdown2]: https://github.com/trentm/python-markdown2
[release page]: https://github.com/fladd/StuffPages/releases/latest