Introduction 
============ 
 
I created _StuffPages_ as a quick way to publish simple web pages on my web server. Basically, it takes Markdown files from a specified directory, turns them into CSS-styeld HTML files, and saves the output in another specified directory. 

Here are some demos: http://stuff.fladd.de/pages

 
Installation 
============ 
 
1. Make sure [Python 2][] is installed 
 
2. Download the [latest release][]

3. Install it:
    ```
    pip install stuffpages
    ```

[latest release]: https://github.com/fladd/StuffPages/releases/latest 
 
 
Usage 
===== 
 
1. Create a `config.py` file in your Markdown directory:
    ```
    stuffpages init <markdown_dir>
    ```

2. Adapt the `config.py` file according to your settings: 
    * `extras` is a dictionary with additional modules to be used by the Markdown Python package 
    * `extras-configs` is a dictionary of configurations for the additional modules 
    * `defaults` are the values to be used when nothing is set in the metadata of a Markdown file: 
        * `output_dir` is where your web pages (.html files) will be written to 
        * `style` is a URL or file path for the css style to be used 
        * `author` is the name of the author
        * `author_link` is a link to the author's website or email address
        * `title` is the default title for web pages 
        * `description` is the default description for web pages
        * `favicon` is a URL or file path for the favicon to be used 
        * `settings` is a list of settings:
            * `index` for creating an index page
            * `noheader` for not creating a header 
            * `nofooter` for not creating a footer
            * `norecursion` for not considering subdirectories
            * `nolinkedfilescopy` for not copying linked files

3. Create Markdown pages (.md files) in your Markdown directory:
   * `[TOC]` will be replaced by the table of contents
   * `[PAGES]` will be replaced by a sorted list of pages (use `[SEGAP]` for reversed sorting)

4. Create corresponding web pages (.html files) in the `output_dir`:
    ```
    stuffpages update <markdown_dir>
    ```
