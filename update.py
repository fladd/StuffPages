#!/usr/bin/env python

_version_ = "0.3.6"


import os
import re
import shutil
from datetime import datetime
from glob import glob
import sys; sys.dont_write_bytecode = True

from markdown import Markdown

from config import markdown_dir, extras, defaults


# Loop over all files in markdown directory
for filename in glob(os.path.join(os.path.expanduser(markdown_dir), "*.md")):

    # Read in content and convert to markdown
    _defaults = defaults.copy()
    root, ext = os.path.splitext(filename)
    with open(filename) as f:
        text = f.read()
    md = Markdown(extensions=['markdown.extensions.meta'] + extras)
    html = md.convert(text)

    # Handle meta data
    meta = '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    _metas = {}
    if hasattr(md, "Meta"):
        for m in md.Meta.keys():
            if m in ["output_dir", "url", "title", "favicon", "style", "settings"]:
                _defaults[m] = " ".join(md.Meta[m])
            else:
                _metas[m] = " ".join(md.Meta[m])
                meta += '<meta name="{0}" content="{1}">\n'.format(
                    m.lower(), " ".join(md.Meta[m]))
    htmldir = os.path.join(os.path.expanduser(_defaults["output_dir"]),
                           os.path.split(root)[-1])
    outfile = os.path.join(htmldir, "index.html")
    if not os.path.exists(outfile):
        os.makedirs(htmldir)
    title = "<title>{0}</title>".format(_defaults["title"])
    if os.path.exists(os.path.expanduser(_defaults["favicon"])):
        shutil.copy(os.path.expanduser(_defaults["favicon"]),
                    os.path.expanduser(htmldir))
        favicon_link = '<link rel="shortcut icon" href="{0}" type="image/vnd.microsoft.icon">'.format(
            os.path.split(_defaults["favicon"])[-1])
    elif _defaults["favicon"].startswith("http"):
        favicon_link = '<link rel="shortcut icon" href="{0}" type="image/vnd.microsoft.icon">'.format(
            _defaults["favicon"])
    else:
        favicon_link = ""
    page_credits = "Created with [Stuff Pages](https://github.com/fladd/StuffPages). "
    if os.path.exists(os.path.expanduser(os.path.join("styles", _defaults["style"] + ".css"))):
        _defaults['style'] = os.path.join("styles", _defaults["style"] + ".css")
    if os.path.exists(os.path.expanduser(_defaults["style"])):
        with open(os.path.expanduser(_defaults["style"])) as f:
            first_line = f.readline()
            if first_line.startswith("/*"):
                first_line = first_line.lstrip("/*").rstrip("*/\n")
                page_credits += first_line
        shutil.copy(os.path.expanduser(_defaults["style"]),
                    os.path.expanduser(htmldir))
        css_link = '<link href="{0}" rel="stylesheet" media="screen">'.format(
            os.path.split(_defaults["style"])[-1])
    elif defaults["style"].startswith("http"):
        css_link = '<link href="{0}" rel="stylesheet" media="screen">'.format(
            _defaults["style"])
    else:
        css_link = ""

    # Handle header
    if "noheader" in _defaults["settings"]:
        header = ""
    else:
        header_pattern = re.compile(r".*?(<header>(.*?)</header>).*?", re.M | re.S)
        header_match = header_pattern.match(html)
        if header_match:
            header = "<header>" + header_match.group(2) + "</header>"
            html = html.replace(header_match.group(1), "")
        else:
            header = "<header>\n<h1>" + _defaults["title"] + "</h1>"
            if "description" in _metas.keys():
                header += "\n<p>" +_metas["description"] + "<p>"
            header += "\n</header>"

    # Handle footer
    if "nofooter" in _defaults["settings"]:
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
            if "author" in _metas.keys():
                footer += "\n<p><strong>&copy;" + repr(datetime.now().year) + \
                          " " + _metas["author"] + "</strong></p>"
            footer += "\n" + page_credits + "\n</footer>"

    # Put everything together
    content = \
"""<!DOCTYPE html>
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
<main>
{5}
</main>
{6}
</section>
</body>
</html>""".format(title, meta.rstrip("\n"), favicon_link, css_link, header, html, footer)
    with open(outfile, 'w') as f:
        f.write(content)
