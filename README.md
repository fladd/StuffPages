Introduction
============
 
I created _StuffPages_ as a quick way to publish simple web pages on my web server. Basically, it takes Markdown files from a specified directory, turns them into CSS-styeld HTML files, and saves the output in another specified directory. 

Have a look at some [examples](https://fladd.github.io/StuffPages/examples/)!

Installation 
============ 
 
1. Make sure [Python 3](http://www.python.org) (>=3.6) is installed 

2. Install pipx

    ```
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath
    ```

3. Install StuffPages
   
    ```
    pipx install stuffpages
    ```
 
Usage
=====
 
1. Initialize StuffPages within the directory that contains the Markdown files:
    
    ```
    cd /path/to/directory/
    stuffpages init
    ```

2. Adapt `/path/to/directory/_stuffpages/config.py` according to your settings: 
    * `output_dir` is the name of the directory that will contain the converted
      HTML files
    * `defaults` are the values to be used when nothing is set in the metadata of the Markdown file: 
        * `title` is the default title for generated pages 
        * `description` is the default description for generated pages
        * `author` is the default name of the author shown on generaged pages
        * `authorlink` is the default target the author name links to
        * `style` is a URL or file path for the css style to be used 
        * `settings` is an optional list of the following settings:
            * `nonav` for not creating a nav section
            * `noheader` for not creating a header section
            * `nofooter` for not creating a footer section
            * `norecursion` for not considering subdirectories
            * `selfcontained` for having a _resources directory for each page
    * `html_head` is a list of lines that are injected in the final HTML output between `<head>` and `</head>`
    * `html_nav` is a list of lines that are injected in the final HTML output between `<nav>` and `</nav>`
    * `html_header` is a list of lines that are injected in the final HTML output between `<header>` and `</header>`
    * `html_footer` is a list of lines that are injected in the final HTML output between `<footer>` and `</footer>`
    * `pagelisting_format` is a string describing the format for each item in pages listings ([PAGE])
    * `breadcrumb_format` is a string describing the format for each item in breadcrumb listings ([BREADCRUMB])
    * `extras` is a dictionary with additional modules to be used by the Markdown Python package 
    * `extras-configs` is a dictionary of configurations for the additional modules 

3. Build the HTML pages:
    
    ```
    stuffpages build
    ```

Listings
========

Each Markdown file, as well as the `html_(head|nav|header|footer)` in the config file can contain special listings markers:

* `[TOC]` will be replaced by the table of contents
* `[PAGES]` will be replaced by a list of pages sorted by title, prepending `!` (i.e. `[!PAGES]`) will reverse sort, and appending a defaults/meta data variable name (e.g. Description) will sort by that defaults/meta data (e.g. `[PAGES Description]`)
* `[BREADCRUMB]` will be replaced by a breadcrumb trail of links from the current page to the parent page


[Python 3]: http://www.python.org 
[Markdown]: https://pythonhosted.org/Markdown/ 
[PyMdownExtensions]: http://facelessuser.github.io/pymdown-extensions 
[BeautifulSoup]: https://www.crummy.com/software/BeautifulSoup/
[Pygments]: http://pygments.org 
[latest release]: https://github.com/fladd/StuffPages/releases/latest 
 

