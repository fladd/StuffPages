#!/usr/bin/env python


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
from bs4 import BeautifulSoup


class StuffPages:
    """A class representing a StuffPages directory."""

    def __init__(self, markdown_dir):
        """Initialise a StuffPages object.

        Parameters
        ----------
        markdown_dir : str
            the directory with the .md files

        """

        self.markdown_dir = markdown_dir

    def init(self):
        """Create a default 'config.py'."""

        #TODO: ask if config found
        config_path = os.path.abspath(os.path.split(__file__)[0])
        config_file = os.path.join(config_path, "config.py")
        try:
            shutil.copy(config_file, os.path.join(self.markdown_dir,
                                                  "config.py"))
        except:
            pass

    def build(self):
        """Build all pages ('*.md')."""

        #TODO: ask if lastupdate is found
        try:
            os.remove(os.path.join(self.markdown_dir, ".lastupdate"))
        except:
            pass
        self.update()

    def update(self):
        """Update new/changed pages."""

        # Load global config
        from config import extras, extras_configs, defaults

        # Load local config
        try:  # TODO: adapt for Py3
            imp.load_module(imp.find_module("config", [self.markdown_dir]))
            extras = config.extras
            extras_configs = config.extras
            defaults = config.defaults
        except:
            pass

        # Load update information
        if os.path.exists(os.path.join(self.markdown_dir, ".lastupdate")):
            with open(os.path.join(self.markdown_dir, ".lastupdate")) as f:
                lastupdate = json.load(f)
        else:
            lastupdate = {"time": 0,
                        "pagelisting_files": []}

        # Loop (recursively) over all markdown files in directory
        outfiles = []
        matches = []
        written_pages = []
        for root, dirnames, filenames in os.walk(self.markdown_dir):
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
                if os.path.split(root)[0] != self.markdown_dir:
                    continue
            with codecs.open(filename, encoding='utf-8') as f:
                text = f.read()
            md = Markdown(extensions=['markdown.extensions.meta'] + extras,
                          extension_configs=extras_configs,
                          output_format="html5")
            html = md.convert(text)

            # Handle meta data
            meta = '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            if hasattr(md, "Meta"):
                for m in md.Meta.keys():
                    _metas[m] = " ".join(md.Meta[m])
            for m in _metas:
                if _metas[m] and m.lower()and m.lower() not in ["output_dir",
                                                                "title",
                                                                "author_link",
                                                                "favicon",
                                                                "style",
                                                                "settings"]:
                    meta += '<meta name="{0}" content="{1}">\n'.format(m.lower(), _metas[m])

            if os.path.isabs(_metas["output_dir"]):
                output_dir = _metas["output_dir"]
            else:
                output_dir = os.path.abspath(
                    os.path.join(self.markdown_dir, _metas["output_dir"]))
            if "norecursion" in _metas["settings"]:
                htmldir = os.path.join(output_dir, os.path.split(root)[-1])
                if "index" in _metas["settings"]:
                    htmldir = os.path.split(htmldir)[0]
            else:
                htmldir = os.path.join(output_dir,
                                       os.path.relpath(root, self.markdown_dir))
                if "index" in _metas["settings"]:
                    htmldir = os.path.split(htmldir)[0]

            outfile = os.path.join(htmldir, "index.html")
            if not os.path.exists(htmldir):
                os.makedirs(htmldir)
            title = "<title>{0}</title>".format(_metas["title"])
            if os.path.exists(_metas["favicon"]):
                shutil.copy(_metas["favicon"],
                            htmldir)
                favicon_link = '<link rel="shortcut icon" href="{0}" type="image/vnd.microsoft.icon">'.format(
                    os.path.split(_metas["favicon"])[-1])
            elif _metas["favicon"].startswith("http"):
                favicon_link = '<link rel="shortcut icon" href="{0}" type="image/vnd.microsoft.icon">'.format(
                    _metas["favicon"])
            else:
                favicon_link = ""
            page_credits = "Created with [StuffPages](https://github.com/fladd/StuffPages) "
            if _metas["style"].startswith("http"):
                css_link = '<link href="{0}" rel="stylesheet" media="screen">'.format(_metas["style"])
            else:
                if _metas["style"].endswith(".css"):
                    if os.path.isabs(_metas["style"]):
                        style_file = _metas["style"]
                    else:
                        style_file = os.path.abspath(
                            os.path.join(self.markdown_dir, _metas["style"]))
                else:
                    style_file = os.path.abspath(os.path.join(
                        os.path.split(__file__)[0], "styles",
                        _metas["style"])) + ".css"
                if os.path.exists(style_file):
                    with open(style_file) as f:
                        first_line = f.readline()
                        if first_line.startswith("/*"):
                            first_line = first_line.lstrip("/*").rstrip("*/\n")
                            page_credits += first_line

                    try:
                        shutil.copy(style_file, htmldir)
                    except:
                        pass
                    css_link = '<link href="{0}" rel="stylesheet" media="screen">'.format(
                        os.path.split(style_file)[-1])
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

            # Copy linked files
            if not "nolinkedfilescopy" in _metas["settings"]:
                soup = BeautifulSoup(content, "html.parser")
                links = [x['href'] for x in soup.find_all('a')] + \
                        [x['src'] for x in soup.find_all('img')] + \
                        [x['src'] for x in soup.find_all('source')]
                for link in links:
                    #from_ = link
                    #to_ = os.path.join(htmldir, os.path.split(link)[-1])
                    if not os.path.isabs(link):
                        from_ = os.path.abspath(os.path.join(self.markdown_dir,
                                                             link))
                        if from_.startswith(self.markdown_dir):
                            to_ = os.path.join(htmldir, os.path.relpath(
                                from_, self.markdown_dir))
                            if os.path.exists(from_):
                                if os.path.isfile(from_):
                                    try:
                                        os.makedirs(os.path.split(to_)[0])
                                    except:
                                        pass
                                    try:
                                        shutil.copy(from_, to_)
                                    except:
                                        pass
                                else:
                                    try:
                                        shutil.copytree(from_, to_)
                                    except:
                                        pass

            # Write page
            with codecs.open(outfile, encoding='utf-8', mode='w') as f:
                f.write(content)
                written_pages.append(filename)

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
                                soup = BeautifulSoup(f.read(), "html.parser")
                                title = soup.title.string
                                description = soup.find_all(
                                    attrs={"name":"description"})[0]['content']
                            pages.append([title, description, os.path.split(directory)[-1]])
                        except:
                            pass
                for substitute in ["[PAGES]", "[SEGAP]", "[pages]", "[segap]"]:
                    if "<p>{0}</p>\n".format(substitute) in content:
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
                            pages_list += '<li><p><a href="{0}">{1}</a><br />{2}</p></li>\n'.format(page[2],
                                                                                                    page[0],
                                                                                                    page[1])
                        pages_list += "</ul>\n"
                        content = content.replace("<p>{0}</p>\n".format(substitute), pages_list)

            with open(outfile, 'w') as f:
                f.write(content)

        # Save update information
        lastupdate["time"] = time.time()
        try:
            with open(os.path.join(self.markdown_dir, ".lastupdate"), 'w') as f:
                json.dump(lastupdate, f)
        except:
            pass

        if written_pages != []:
            print("")
            for page in written_pages:
                print(page)
            print("")
