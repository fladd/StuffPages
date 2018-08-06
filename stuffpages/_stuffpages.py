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
        from config import html_head, html_nav, html_header, html_footer
        from config import pagelisting_format

        # Load local config
        try:  # TODO: adapt for Py3
            imp.load_module(imp.find_module("config", [self.markdown_dir]))
            extras = config.extras
            extras_configs = config.extras
            defaults = config.defaults
            html_head = config.html_head
            html_nav = config.html_nav
            html_header = config.html_header
            html_footer = config.html_footer
            pagelisting_format = config.pagelisting_format

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
        for filename in matches + list(set(lastupdate["pagelisting_files"]) \
                - set(matches)):
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
            if hasattr(md, "Meta"):
                for m in md.Meta.keys():
                    _metas[m] = " ".join(md.Meta[m])

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
                htmldir = os.path.join(output_dir, os.path.relpath(
                    root, self.markdown_dir))
                if "index" in _metas["settings"]:
                    htmldir = os.path.split(htmldir)[0]

            outfile = os.path.join(htmldir, "index.html")
            if not os.path.exists(htmldir):
                os.makedirs(htmldir)

            written_files[outfile] = {'md': os.path.abspath(filename),
                                      'metas': _metas,
                                      'pagelisting': False,
                                      'breadcrumb': False}

            # Handle head, header and footer
            def create_section(section):
                rtn = ''
                for line in section:
                    rtn += line + "\n"
                pattern = re.compile(r"{{.*?}}")
                for match in pattern.matchall(rtn):
                    if match.lower() in _metas:
                        rtn = rtn.replace("{{" + match + "}}",
                                          _metas[match.lower()])
                return rtn

            head = create_section(html_head)

            nav = ''
            if not "nonav" in _metas["settings"]:
                header = create_section(html_nav)

            header = ''
            if not "noheader" in _metas["settings"]:
                header = create_section(html_header)

            footer = ''
            if not "nofooter" in _metas["settings"]:
                footer = create_section(html_footer)

            # Put everything together
            content = \
    u"""<!DOCTYPE html>
<html>
{0}
<body>
{1}
<section>
{2}
</section>
{3}
</body>
</html>""".format(head, header, html, footer)

            # Handle linked files
            soup = BeautifulSoup(content, "html.parser")
            links = soup.find_all('link') + \
                    soup.find_all('a') + \
                    soup.find_all('img') + \
                    soup.find_all('source')
            for l in links:
                if l.name in ("link", "a"):
                    tag = "href"
                elif l.name in ("img", "source"):
                    tag = "src"
                link = l[tag]
                if os.path.isabs(link):
                    to_ = os.path.join(htmldir, os.path.split(link)[-1])
                    if os.path.exists(link):
                        if os.path.isfile(link):
                            try:
                                if not os.path.exists(os.path.split(to_)[0]):
                                    os.makedirs(os.path.split(to_)[0])
                                shutil.copy(link, to_)
                                l[tag] = os.path.split(link)[-1]
                            except:
                                pass
                        else:
                            try:
                                shutil.copytree(link, to_)
                                l[tag] = os.path.split(link)[-1]
                            except:
                                pass
                elif not (link.startswith("#") or ":" in link):
                    l[tag] = os.path.relpath(os.path.abspath(link),
                                             os.path.abspath(htmldir))

            # Write page
            with codecs.open(outfile, encoding='utf-8', mode='w') as f:
                f.write(content)
                written_pages.append(filename)

            # Contains page listing?
            if re.search("^\[(!?)PAGES\s?(.*)\]$", content,
                         re.MULTILINE) is not None:
                if not filename in lastupdate["pagelisting_files"]:
                    lastupdate["pagelisting_files"].append(filename)
                outfiles.append(outfile)
                written_files[outfile]['pagelisting'] = True

            # Contains breadcrumb menu?
            if re.search("^\[(BREADCRUMB)\]$", content,
                         re.MULTILINE) is not None:
                written_files[outfile]['breadrumb'] = True

        # Substitute [PAGES]
        for outfile in [k for k,v in written_files.items() if y['pagelisting']:
            with open(outfile) as f:
                content = f.read()
                pages = []  # [filename, metas]
                htmldir = os.path.split(outfile)[0]
                for directory in os.listdir(htmldir):
                    directory = os.path.abspath(os.path.join(htmldir,
                                                             directory))
                    if os.path.isdir(os.path.abspath(directory)):
                        page = os.path.join(directory, "index.html")
                        try:
                            pages.append(directory, written_files[page]['metas'])
                        except:
                            pages.append(directory, {})
                for match in re.findall("(^<p>\[(!?)PAGES\s?(.*)\]</p>$)",
                                        content, re.MULTILINE):
                    pages.sort(key=lambda x: x[0])  # sort by filename
                    try:  # sort by meta
                        pages.sort(key=lambda x: x[1][match[2]])
                    except:
                        pass
                    if match[1] == '!':  # reverse sort
                        pages.reverse()
                    pages_list = '<ul class="pagelisting">\n'
                    for page in pages:
                        try:
                            item = '<li>' + pagelisting_format + '</li>'
                            p = re.compile(r"{{.*?}}")
                                for m in p.matchall(pagelisting_format):
                                    if m.lower() in page[1]:
                                    item = item.replace("{{" + m + "}}",
                                                        page[1][m.lower()])
                        except:
                            item = '<li><a href="{0}">{0}</a></li>'

                        pages_list += item.format(page[0]) + '\n'

                    pages_list += "</ul>\n"
                    content = content.replace("{0}\n".format(match[0]),
                                                             pages_list, 1)

            with open(outfile, 'w') as f:
                f.write(content)

        # Substitute [BREADCRUMB]
        for outfile in [k for k,v in written_files.items() if y['breadcrumb']:
            with open(outfile) as f:
                content = f.read()
                if os.path.isabs(_metas["output_dir"]):
                    output_dir = _metas["output_dir"]
                else:
                    output_dir = os.path.abspath(
                        os.path.join(self.markdown_dir, _metas["output_dir"]))
                path = os.path.abspath(os.path.relpath(
                    os.path.split(outfile)[-1], output_dir))
                trail = []
                while path != output_dir:
                    path = os.path.split(path)[-1] 
                    with open(os.path.join(path, 'index.html') as f:
                        soup = BeautifulSoup(f.read(), "html.parser")
                        trail.append(soup.title.string)
                trail.reverse() 
                for match in re.findall("(^<p>\[(BREADCRUMB)\]</p>$)",
                                        content, re.MULTILINE):
                    bc = '<span class="breadcrumb">~<span>/</span>'
                    for c,t in enumerate(trail):
                        bc += '<a href="{0}">{1}</a><span>/</span>'.format(
                            (c + 1) * '../', t) 
                    bc += '</span>'
                    content = content.replace("{0}\n".format(match[0]), bc, 1)

            with open(outfile, 'w') as f:
                f.write(content)

        # Save update information
        lastupdate["time"] = time.time()
        try:
            with open(os.path.join(self.markdown_dir,
                                   ".lastupdate"), 'w') as f:
                json.dump(lastupdate, f)
        except:
            pass

        if written_files != {}:
            print("")
            for page in written_files:
                print(page)
            print("")
