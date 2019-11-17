# TODO: No underscores in defaults names?
# TODO: Pygments style
# TODO: Rethink default copyright date mechanism
# Only write HTML if old HTML changed
# Then use current date in config as default date
import os
import re
import shutil
import codecs
import fnmatch
import importlib.util
from glob import glob
import sys; sys.dont_write_bytecode = True

from markdown import Markdown
from markdown.extensions.meta import MetaPreprocessor
from bs4 import BeautifulSoup


def split_meta(filename):
        """Split markdown file into meta data, meta text and main text."""

        with codecs.open(filename, encoding='utf-8') as f:
            text = f.read().split("\n")
            class FakeMeta:
                def __init__(self):
                    self.Meta = None
            class MetaPreprocessor2(MetaPreprocessor):
                def __init__(self):
                    self.md = FakeMeta()
            m = MetaPreprocessor2()
            main_text = m.run(text[:])
            meta_text = [x for x in set(text).difference(set(main_text)) \
                         if x.strip() not in ["---", "...", ""]]
        return (m.md.Meta, "\n".join(meta_text).strip(),
                "\n".join(main_text).strip())


class StuffPages:
    """A class representing a StuffPages directory."""

    def __init__(self, markdown_dir):
        """Initialise a StuffPages object.

        Parameters
        ----------
        markdown_dir : str
            the directory with the .md files

        """

        self.markdown_dir = os.path.abspath(markdown_dir)

    def _load_config(self):
        """Load local config."""

        try:
            spec = importlib.util.spec_from_file_location(
                "module.name", os.path.join(self.markdown_dir, "_stuffpages",
                                            "config.py"))
            local_config = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(local_config)
            self.extras = local_config.extras
            self.extras_configs = local_config.extras_configs
            self.defaults = local_config.defaults
            self.html_head = local_config.html_head
            self.html_nav = local_config.html_nav
            self.html_header = local_config.html_header
            self.html_footer = local_config.html_footer
            self.pagelisting_format = local_config.pagelisting_format
            self.breadcrumb_format = local_config.breadcrumb_format
            return True

        except:
            return False

    def init(self):
        """Create a default 'config.py'.

        Returns True if successful, False otherwise.

        """

        config_path = os.path.abspath(os.path.split(__file__)[0])
        if os.path.exists(os.path.join(self.markdown_dir, "_stuffpages")):
            return False
        shutil.copytree(os.path.join(config_path, "_stuffpages"),
                        os.path.join(self.markdown_dir, "_stuffpages"))

        return True

    def build(self):
        """Build pages ('*.md').

        Returns written pages dictionary, or None if config not loaded.

        """

        if not self._load_config():
            return None

        # Loop (recursively) over all markdown files in directory
        matches = []
        written_files = {}

        for root, dirnames, filenames in os.walk(self.markdown_dir):
            for filename in fnmatch.filter(filenames, '*.md'):
                if os.path.relpath(root,
                                   self.defaults["output_dir"]).startswith(".."):
                    matches.append(os.path.join(root, filename))

        for filename in matches:

            # Read in main content and meta data
            _metas = self.defaults.copy()
            root, ext = os.path.splitext(filename)
            if "norecursion" in _metas["settings"]:
                if os.path.split(root)[0] != self.markdown_dir:
                    continue
            meta_data, meta_text, main_text = split_meta(filename)

            # Handle meta data
            for m in meta_data.keys():
                _metas[m] = " ".join(meta_data[m])
            if os.path.isabs(_metas["output_dir"]):
                output_dir = _metas["output_dir"]
            else:
                output_dir = os.path.abspath(
                    os.path.join(self.markdown_dir, _metas["output_dir"]))
            htmldir = os.path.join(output_dir, os.path.relpath(
                root, self.markdown_dir))
            if os.path.split(filename)[-1] == "index.md":
                htmldir = os.path.split(htmldir)[0]

            outfile = os.path.join(htmldir, "index.html")
            if not os.path.exists(htmldir):
                os.makedirs(htmldir)

            written_files[outfile] = {'md': os.path.abspath(filename),
                                      'metas': _metas,
                                      'pagelisting': False,
                                      'breadcrumb': False,
                                      'html': ""}

            # Handle head, nav, header and footer
            def create_section(section, name):
                rtn = '<!--<{0}>-->\n\n'.format(name)
                for line in section:
                    rtn += line + "\n"
                rtn += '\n<!--</{0}>-->'.format(name)
                pattern = re.compile(r"{{(.*?)}}")
                for match in pattern.findall(rtn):
                    if match.lower() in _metas:
                        rtn = rtn.replace("{{" + match + "}}",
                                          _metas[match.lower()])
                return rtn.rstrip("\n")

            head = create_section(self.html_head, "head")

            nav = ''
            if not "nonav" in _metas["settings"]:
                nav = create_section(self.html_nav, "nav")

            header = ''
            if not "noheader" in _metas["settings"]:
                header = create_section(self.html_header, "header")

            footer = ''
            if not "nofooter" in _metas["settings"]:
                footer = create_section(self.html_footer, "footer")

            # Put everything together
            content = \
    u"""{0}

<!--<!DOCTYPE html>-->

<!--<html>-->

{1}

<!--<body>-->

{2}

{3}

{4}

{5}

<!--</body>-->
<!--</html>-->""".format(meta_text, head, nav, header, main_text, footer)

            # Convert to HTML
            md = Markdown(extensions=['markdown.extensions.meta'] + self.extras,
                          extension_configs=self.extras_configs,
                          output_format="html5")
            html = md.convert(content)

            # Fix HTML output
            fixed_html = []
            for line in html.split("\n"):
                if line.startswith("<p>") and \
                        line != "<p>" and \
                        not line.endswith("</p>"):
                    fixed_html.append(line[3:])
                elif line.endswith("</p>") and \
                        line != "</p>" and \
                        not line.startswith("<p>"):
                    fixed_html.append(line[:-4])
                else:
                    fixed_html.append(line)

            # Fix footnotes position (if present)
            pos1 = fixed_html.index("<!--</html>-->")
            if pos1 != len(fixed_html):
                try:
                    pos2 = fixed_html.index("<!--<footer>-->")
                except:
                    pos2 = fixed_html.index("<!--</body>-->")
                tmp = fixed_html[pos1 + 1:]
                tmp.reverse()
                for x in tmp:
                    fixed_html.insert(pos2, x)
                    fixed_html.pop()

            # Insert HTML tags
            for pos,line in enumerate(fixed_html):
                if line in ["<!--<!DOCTYPE html>-->",
                            "<!--<html>-->",
                            "<!--</html>-->",
                            "<!--<body>-->",
                            "<!--</body>-->",
                            "<!--<head>-->",
                            "<!--</head>-->",
                            "<!--<nav>-->",
                            "<!--</nav>-->",
                            "<!--<header>-->",
                            "<!--</header>-->",
                            "<!--<section>-->",
                            "<!--</section>-->",
                            "<!--<footer>-->",
                            "<!--</footer>-->"]:
                    fixed_html[pos] = line[4:-3]

            html = "\n".join(fixed_html)

            # Handle linked files
            soup = BeautifulSoup(html, "html.parser")
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

                # links to generated pages
                if True in [os.path.relpath(
                    os.path.split(m)[0],
                    self.markdown_dir) == link for m in matches]:
                    l[tag] = os.path.join(os.path.relpath(
                        output_dir,
                        os.path.split(outfile)[0]), link)

                # other absolute links
                elif os.path.isabs(link):
                    if "selfcontained" in _metas["settings"]:
                        to_ = os.path.join(htmldir, "_resources",
                                           os.path.split(link)[-1])
                        l[tag] = os.path.join("_resources",
                                              os.path.split(link)[-1])
                    else:
                        to_ = os.path.join(output_dir, "_resources",
                                           os.path.split(link)[-1])
                        l[tag] = os.path.join(
                            os.path.relpath(
                                output_dir,
                                os.path.split(outfile)[0]),
                            "_resources", os.path.split(link)[-1])
                    if os.path.exists(link):
                        if os.path.isfile(link):
                            if not os.path.exists(os.path.split(to_)[0]):
                                os.makedirs(os.path.split(to_)[0])
                            if not os.path.exists(to_):
                                shutil.copy(link, to_)
                        else:
                            if not os.path.exists(to_):
                                shutil.copytree(link, to_)

                # other relative links
                elif not (link.startswith("#") or ":" in link):
                    if "selfcontained" in _metas["settings"]:
                        to_ = os.path.join(htmldir, "_resources", link)
                        l[tag] = os.path.join("_resources", link)
                    else:
                        to_ = os.path.join(output_dir, "_resources", link)
                        l[tag] = os.path.join(
                            os.path.relpath(
                                output_dir,
                                os.path.split(outfile)[0]),
                            "_resources", link)
                    if os.path.exists(link):
                        if os.path.isfile(link):
                            if not os.path.exists(os.path.split(to_)[0]):
                                os.makedirs(os.path.split(to_)[0])
                            if not os.path.exists(to_):
                                shutil.copy(link, to_)
                        else:
                            if not os.path.exists(to_):
                                shutil.copytree(link, to_)

           written_files["html"] = str(soup)

            # Write page
            with codecs.open(outfile, encoding='utf-8', mode='w') as f:
                f.write(html)

            # TODO: Move these checks down?
            # Contains page listing?
            if re.search("(^<p>\[(!?)PAGES\s?(.*)\]</p>$)", html,
                         re.MULTILINE) is not None:
                written_files[outfile]['pagelisting'] = True

            # Contains breadcrumb listing?
            if re.search("(^<p>\[(BREADCRUMB)\]</p>$)", html,
                         re.MULTILINE) is not None:
                written_files[outfile]['breadcrumb'] = True

        # Substitute listings
        for outfile in [k for k,v in written_files.items() \
                        if v['pagelisting'] or v['breadcrumb']]:

                # TODO: Work directly on outfile["html"] instead of content!

                # Substitute [PAGES]
                if written_files[outfile]['pagelisting']:
                    pages = []  # [filename, metas]
                    htmldir = os.path.split(outfile)[0]
                    for directory in os.listdir(htmldir):
                        if directory == "_resources":
                            continue
                        if os.path.isdir(os.path.join(htmldir, directory)):
                            page = os.path.join(htmldir, directory,
                                                "index.html")
                            try:
                                pages.append([directory,
                                              written_files[page]['metas']])
                            except:
                                pages.append([directory, {}])
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
                                item = '<li>' + self.pagelisting_format + '</li>'
                                p = re.compile(r"{{(.*?)}}")
                                for m in p.findall(self.pagelisting_format):
                                    item = item.replace(
                                        "{{" + m + "}}",
                                        page[1][m.lower()])
                                pages_list += item.format(page[0]) + '\n'
                            except:
                                item = '<li><a href="{0}">{1}</a></li>'
                                pages_list += item.format(
                                    page[0], os.path.split(page[0])[-1]) + '\n'

                        pages_list += "</ul>\n"
                        content = content.replace("{0}\n".format(
                            match[0]), pages_list, 1)

                # Substitute [BREADCRUMB]
                if written_files[outfile]['breadcrumb']:
                    if os.path.isabs(_metas["output_dir"]):
                        output_dir = _metas["output_dir"]
                    else:
                        output_dir = os.path.abspath(
                            os.path.join(self.markdown_dir,
                                         _metas["output_dir"]))
                    path = os.path.split(outfile)[0]
                    trail = []
                    while path != output_dir:
                        path = os.path.split(path)[0]
                        trail.append(os.path.join(path, 'index.html'))
                    trail.reverse()
                    for match in re.findall("(^<p>\[(BREADCRUMB)\]</p>$)",
                                            content, re.MULTILINE):
                        bc = '<span class="breadcrumb">~<span>/</span>'
                        for c,t in enumerate(trail):
                            try:
                                crumb = self.breadcrumb_format + "<span>/</span>"
                                p = re.compile(r"{{(.*?)}}")
                                for m in p.findall(self.breadcrumb_format):
                                    crumb = crumb.replace(
                                        "{{" + m + "}}",
                                        written_files[t]["metas"][m.lower()])
                                bc += crumb.format((len(trail) - c) * '../')
                            except:
                                crumb = '<a href="{0}">{1}</a><span>/</span>'
                                bc += crumb.format((len(trail) - c) * '../',
                                                   (len(trail) - c + 1) * '.')
                        bc += '</span>'

                        content = content.replace("{0}\n".format(match[0]),
                                                  bc, 1)

                    # TODO: Remove unchanged pages!

            # Write page
            with open(outfile, 'w') as f:
                f.write(content)

        return written_files
