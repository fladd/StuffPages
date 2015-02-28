#!/usr/bin/env python

_version_ = 0.2.0


import os
import subprocess
import shutil
from glob import glob
import sys; sys.dont_write_bytecode = True

from markdown2 import markdown_path

from config import markdown_dir, extras, defaults


for filename in glob(os.path.join(os.path.expanduser(markdown_dir), "*.md")):
    _default = defaults.copy()
    root, ext = os.path.splitext(filename)
    body = markdown_path(filename, extras=["metadata"] + extras)
    meta = ""
    if hasattr(body, "metadata"):
        for m in body.metadata.keys():
            if m.lower() in ["output_dir", "url", "title", "favicon", "style"]:
                _defaults[m.lower()] = body.metadata[m]
            else:
                meta += '<meta name="{0}" content="{1}">\n'.format(
                    m.lower(), body.metadata[m])

    htmldir = os.path.join(os.path.expanduser(_defaults["output_dir"]),
                           os.path.split(root)[-1])
    outfile = os.path.join(htmldir, "index.html")
    if not os.path.exists(outfile):
        os.makedirs(htmldir)
    title = "<title>{0}</title>".format(_defaults["title"])
    if os.path.exists(os.path.expanduser(_defaults["favicon"])):
        shutil.copy(os.path.expanduser(_defaults["favicon"]),
                    os.path.expanduser(htmldir))
        favicon_link = '<link rel="shortcut icon" href="{0}" type="image/vnd.microsoft.icon">'.format(os.path.split(defauts["favicon"])[-1])
    elif _defaults["favicon"].startswith("http"):
        favicon_link = '<link rel="shortcut icon" href="{0}" type="image/vnd.microsoft.icon">'.format(_defaults["favicon"])
    else:
        favicon_link = ""
    if os.path.exists(os.path.expanduser(_defaults["style"])):
        shutil.copy(os.path.expanduser(_defaults["style"]),
                    os.path.expanduser(htmldir))
        css_link = '<link href="{0}" rel="stylesheet"></link>'.format(os.path.split(_defaults["style"])[-1])
    elif defaults["style"].startswith("http"):
        css_link = '<link href="{0}" rel="stylesheet"></link>'.format(_defaults["style"])
    else:
        css_link = ""
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
{4}
</body>
</html>""".format(title, meta.rstrip("\n"), favicon_link, css_link, body)
    with open(outfile, 'w') as f:
        f.write(content)
