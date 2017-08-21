#!/usr/bin/env python

_version_ = "0.5.1"


import os
import re
import shutil
import codecs
import fnmatch
import time
import json
from datetime import datetime
from glob import glob
import sys; sys.dont_write_bytecode = True

from markdown import Markdown

from config import markdown_dir, extras, extras_configs, defaults

# Load update information
try:
    with open(".lastupdate") as f:
        lastupdate = json.load(f)
except:
    lastupdate = {"time": 0,
                  "pagelisting_files": []}

# Loop (recursively) over all markdown files in directory
outfiles = []
matches = []
for root, dirnames, filenames in os.walk(os.path.join(os.path.expanduser(markdown_dir))):
    for filename in fnmatch.filter(filenames, '*.md'):
        matches.append(os.path.join(root, filename))
                      
for filename in matches + list(set(lastupdate["pagelisting_files"]) - set(matches)):
    if not filename in lastupdate["pagelisting_files"]:
        if os.path.getmtime(filename) < lastupdate["time"]:
            continue

    # Read in content and convert to markdown
    _metas = defaults.copy()
    root, ext = os.path.splitext(filename)
    if "norecursion" in _metas["settings"]:
        if os.path.split(root)[0] != markdown_dir:
            continue
    with codecs.open(filename, encoding='utf-8') as f:
        text = f.read()
    md = Markdown(extensions=['markdown.extensions.meta'] + extras,
                  extension_configs=extras_configs, output_format="html5")
    html = md.convert(text)

    # Handle meta data
    meta = '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    if hasattr(md, "Meta"):
        for m in md.Meta.keys():
            _metas[m] = " ".join(md.Meta[m])
            if m.lower() not in ["output_dir", "title", "author_link", "favicon", "style", "settings"]:
                meta += '<meta name="{0}" content="{1}">\n'.format(
                    m.lower(), _metas[m])
    
    if "norecursion" in _metas["settings"]:
        htmldir = os.path.join(os.path.expanduser(_metas["output_dir"]),
                               os.path.split(root)[-1])
        if "index" in _metas["settings"]:
            htmldir = os.path.split(htmldir)[0]
    else:
        htmldir = os.path.join(os.path.expanduser(_metas["output_dir"]),
                               os.path.relpath(root, markdown_dir))
        if "index" in _metas["settings"]:
            htmldir = os.path.split(htmldir)[0]

    outfile = os.path.join(htmldir, "index.html")
    if not os.path.exists(htmldir):
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
    page_credits = "Created with [StuffPages](https://github.com/fladd/StuffPages) "
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
            if "author" in _metas.keys():
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

    # Write page
    with codecs.open(outfile, encoding='utf-8', mode='w') as f:
        f.write(content)
    print(filename)

    # Contains page listing?
    if "[pages]" in content.lower() or "[segap]" in content.lower():
        if not filename in lastupdate["pagelisting_files"]:
            lastupdate["pagelisting_files"].append(filename)
        outfiles.append(outfile)

# Substitute [PAGES/SEGAP]
for outfile in outfiles:
    with open(outfile) as f:
        content = f.read()
        pages = []
        htmldir = os.path.split(outfile)[0]
        for directory in os.listdir(htmldir):
            directory = os.path.abspath(os.path.join(htmldir, directory))
            if os.path.isdir(os.path.abspath(directory)):
                title = ""
                description = ""
                try:
                    with open(os.path.join(directory, "index.html")) as f:
                        for line in f:
                            if line.startswith("<title>") and line.endswith("</title>\n"):
                                title = line.replace("<title>", "").replace("</title>\n", "")
                            elif line.startswith('<meta name="description"'):
                                tmp = line.lstrip('<meta name="description" contents="')
                                description = tmp.rstrip('\n').rstrip('>').rstrip('"')
                    pages.append([title, description, os.path.split(directory)[-1]])
                except:
                    pass
        for substitute in ["[PAGES]", "[SEGAP]", "[pages]", "[segap]"]:
            if "<p>{0}</p>".format(substitute) in content:
                if substitute == "[PAGES]":
                    pages.sort(key=lambda x: x[0])
                elif substitute == "[SEGAP]":
                    pages.sort(key=lambda x: x[0])
                    pages.reverse()
                elif substitute == "[pages]":
                    pages.sort(key=lambda x: x[1])
                elif substitute == "[segap]":
                    pages.sort(key=lambda x: x[1])
                    pages.reverse()
                pages_list = '<ul class="pagelisting">\n'
                for page in pages:
                    pages_list += '<li><p><a href="{0}">{1}</a><br />{2}</p></li>\n'.format(page[2], page[0], page[1])
                pages_list += "</ul>\n"
                content = content.replace("<p>{0}</p>".format(substitute), pages_list)

    with open(outfile, 'w') as f:
        f.write(content)
        
# Save update information
lastupdate["time"] = time.time()
try:
    with open(".lastupdate", 'w') as f:
        json.dump(lastupdate, f)
except:
    pass
