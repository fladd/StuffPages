Installation
------------

1. Make sure [Python 2][] is installed on your web server
2. Install the Python package [Markdown][markdown-python] on your web server (and optionally Pygments][] for code highlighting)
3. Download the source .zip from the [release page][] and extract it in a (non-served) directory on your web server


Usage
-----

1. Adapt the `config.py` file according to your settings:
    * `markdown_dir` is where your markdown pages (.md files) are located
    * `extras` is a dictionary with additional modules to be used by the [Markdown][markdown-python] Python package
    * `defaults` are the values to be used when nothing is set in the metadata of the Markdown file:
        * `output_dir` is where your web pages (.html files) will be written to
        * `url` is the URL from which the web page will be served from
        * `title` is the default title for web pages
        * `favicon` is a URL or file path for the favicon to be used
        * `style` is a URL or file path for the css style to be used
        * `settings` is a list of settings:
            * `noheader` for not creating a header
            * `nofooter` for not creating a footer
2. Create Markdown pages (.md files) in your `markdown_dir`
3. Run `python update.py` to create corresponding web pages (.html files) in the `output_dir`, that will be served at `url`


[StuffPages]: https://github.com/fladd/StuffPages/
[Markdown]: http://daringfireball.net/projects/markdown/
[Python 2]: http://www.python.org
[markdown-python]: https://pythonhosted.org/Markdown/
[release page]: https://github.com/fladd/StuffPages/releases/latest
[Pygments]: http://pygments.org
