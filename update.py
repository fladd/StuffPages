#!/usr/bin/env python

_version_ = "0.4.1"


import os
import re
import shutil
import codecs
from datetime import datetime
from glob import glob
import sys; sys.dont_write_bytecode = True

from markdown import Markdown

from config import markdown_dir, extras, extras_configs, defaults


# Loop over all files in markdown directory
for filename in glob(os.path.join(os.path.expanduser(markdown_dir), "*.md")):

    # Read in content and convert to markdown
    _metas = defaults.copy()
    root, ext = os.path.splitext(filename)
    with codecs.open(filename, encoding='utf-8') as f:
        text = f.read()
    md = Markdown(extensions=['markdown.extensions.meta'] + extras,
                  extension_configs=extras_configs, output_format="html5")
    html = md.convert(text)

    # Handle meta data
    if hasattr(md, "Meta"):
        for m in md.Meta.keys():
            _metas[m] = " ".join(md.Meta[m])
    meta = '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    for m in _metas:
        if _metas[m] and m.lower() not in ["output_dir", "title", "author_link", "favicon", "style", "settings"]:
            meta += '<meta name="{0}" content="{1}">\n'.format(
                m.lower(), _metas[m])
    htmldir = os.path.join(os.path.expanduser(_metas["output_dir"]),
                           os.path.split(root)[-1])
    outfile = os.path.join(htmldir, "index.html")
    if not os.path.exists(outfile):
        os.makedirs(htmldir)
    title = "<title>{0}</title>".format(_metas["title"])
    if os.path.exists(os.path.expanduser(_metas["favicon"])):
        shutil.copy(os.path.expanduser(_metas["favicon"]),
                    os.path.expanduser(htmldir))
        favicon_link = '<link rel="shortcut icon" href="{0}" type="image/vnd.microsoft.icon">'.format(
            os.path.split(_metas["favicon"])[-1])
    elif _metas["favicon"].startswith("http"):
        favicon_link = '<link rel="shortcut icon" href="{0}" type="image/vnd.microsoft.icon">'.format(
            _metas["favicon"])
    else:
        favicon_link = ""
    page_credits = "Created with [StuffPages](https://github.com/fladd/StuffPages)"
    if os.path.exists(os.path.expanduser(os.path.join("styles", _metas["style"] + ".css"))):
        _metas['style'] = os.path.join("styles", _metas["style"] + ".css")
    if os.path.exists(os.path.expanduser(_metas["style"])):
        with open(os.path.expanduser(_metas["style"])) as f:
            first_line = f.readline()
            if first_line.startswith("/*"):
                first_line = first_line.lstrip("/*").rstrip("*/\n")
                page_credits += first_line
        shutil.copy(os.path.expanduser(_metas["style"]),
                    os.path.expanduser(htmldir))
        css_link = '<link href="{0}" rel="stylesheet" media="screen">'.format(
            os.path.split(_metas["style"])[-1])
    elif _metas["style"].startswith("http"):
        css_link = '<link href="{0}" rel="stylesheet" media="screen">'.format(
            _metas["style"])
    else:
        css_link = ""

    # Handle header
    if "noheader" in _metas["settings"]:
        header = ""
    else:
        header_pattern = re.compile(r".*?(<header>(.*?)</header>).*?", re.M | re.S)
        header_match = header_pattern.match(html)
        if header_match:
            header = "<header>" + header_match.group(2) + "</header>"
            html = html.replace(header_match.group(1), "")
        else:
            header = "<header>\n<h1>" + _metas["title"] + "</h1>"
            if "description" in _metas.keys():
                header += "\n<p>" +_metas["description"] + "</p>"
            header += "\n</header>"

    # Handle footer
    if "nofooter" in _metas["settings"]:
        footer = ""
    else:
        page_credits = Markdown().convert(page_credits).replace("<p>", "<p class='page-credits'>")
        footer_pattern = re.compile(r".*?(<footer>(.*?)</footer>).*?", re.M | re.S)
        footer_match = footer_pattern.match(html)
        if footer_match:
            footer = "<footer>" + footer_match.group(2) + "\n" + page_credits + "\n</footer>"
            html = html.replace(footer_match.group(1), "")
        else:
            footer = "<footer>"
            if "author" in _metas.keys() anf _metas["author"]:
                author = _metas["author"]
                if "author_link" in _metas.keys() and _metas["author_link"]:
                    author = '<a href="{0}">{1}</a>'.format(_metas["author_link"], author)
                footer += "\n<p><strong>&copy;" + repr(datetime.now().year) + \
                          " " + author + "</strong></p>"
            footer += "\n" + page_credits + "\n</footer>"

    # Put everything together
    content = \
u"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
{0}
{1}
{2}
{3}
</head>
<body>
{4}
<section>
{5}
</section>
{6}
</body>
</html>""".format(title, meta.rstrip("\n"), favicon_link, css_link, header, html, footer)
    with codecs.open(outfile, encoding='utf-8', mode='w') as f:
        f.write(content)
