Introduction 
============ 
 
I created _StuffPages_ as a quick way to publish simple web pages on my web server. Basically, it takes Markdown files from a specified directory, turns them into CSS-styeld HTML files, and saves the output in another specified directory. 

Here are some demos: http://stuff.fladd.de/pages

 
Installation 
============ 
 
1. Make sure [Python 2][] is installed 
 
2. Install the Python packages [Markdown][], [PyMdownExtensions][] and [Pygments][] (optional, for code highlighting): 
   ``` 
   pip install markdown pymdown-extensions pygments 
   ``` 
 
3. Download the [latest realse][] and extract it 
 
[Python 2]: http://www.python.org 
[Markdown]: https://pythonhosted.org/Markdown/ 
[PyMdownExtensions]: http://facelessuser.github.io/pymdown-extensions 
[Pygments]: http://pygments.org 
[latest release]: https://github.com/fladd/StuffPages/releases/latest 
 
 
Usage 
===== 
 
1. Adapt the `config.py` file according to your settings: 
    * `markdown_dir` is where your markdown pages (.md files) are located 
    * `extras` is a dictionary with additional modules to be used by the Markdown Python package 
    * `extras-configs` is a dictionary of configurations for the additional modules 
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
