import os
import re
import uuid
import shutil
import codecs
import fnmatch
import importlib.util
from string import Template
import sys; sys.dont_write_bytecode = True

from markdown import Markdown
from markdown.extensions.meta import MetaPreprocessor
from bs4 import BeautifulSoup, NavigableString


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

    def __init__(self, input_dir):
        """Initialise a StuffPages object.

        Parameters
        ----------
        input_dir : str
            the directory with the .md files

        """

        self.input_dir = os.path.abspath(input_dir)
        self.stuffpages_dir = os.path.join(self.input_dir, "_stuffpages")

    def _load_config(self):
        """Load local config."""

        try:
            cwd = os.getcwd()
            os.chdir(self.stuffpages_dir)
            spec = importlib.util.spec_from_file_location(
                "module.name", os.path.join(self.stuffpages_dir, "config.py"))
            local_config = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(local_config)
            self.output_dir = local_config.output_dir
            self.defaults = local_config.defaults
            self.html_head = local_config.html_head
            self.html_nav = local_config.html_nav
            self.html_header = local_config.html_header
            self.html_footer = local_config.html_footer
            self.pagelisting_format = local_config.pagelisting_format
            self.breadcrumb_format = local_config.breadcrumb_format
            self.extras = local_config.extras
            self.extras_configs = local_config.extras_configs
            os.chdir(cwd)
            return True

        except:
            return False

    def init(self):
        """Create a default 'config.py'.

        Returns True if successful, False otherwise.

        """

        config_path = os.path.abspath(os.path.split(__file__)[0])
        if os.path.exists(self.stuffpages_dir):
            return False
        shutil.copytree(os.path.join(config_path, "_stuffpages"),
                        self.stuffpages_dir)

        return True

    def build(self):
        """Build pages ('*.md').

        Returns written pages dictionary, or None if config not loaded.

        """

        output_files = {}

        if not self._load_config():
            return None

        if not os.path.isabs(self.output_dir):
            self.output_dir = os.path.abspath(os.path.join(self.stuffpages_dir,
                                                           self.output_dir))

        # Find (recursively) all markdown files in directory
        matches = []
        for root, dirnames, filenames in os.walk(self.input_dir):
            for filename in fnmatch.filter(filenames, '*.md'):
                if os.path.relpath(root, self.output_dir).startswith(".."):
                    matches.append(os.path.join(root, filename))

        # Process each markdown file
        for filename in matches:

            # Read in main content and meta data
            _metas = self.defaults.copy()
            root, ext = os.path.splitext(filename)
            rel_mddir = os.path.relpath(os.path.split(root)[0], self.input_dir)
            meta_data, meta_text, main_text = split_meta(filename)

            # Handle meta data
            for m in meta_data.keys():
                _metas[m] = " ".join(meta_data[m])

            if "settings" in _metas and \
                    "norecursion" in _metas["settings"]:
                if os.path.split(root)[0] != self.input_dir:
                    continue

            htmldir = os.path.join(self.output_dir,
                                   os.path.relpath(root, self.input_dir))
            if os.path.split(filename)[-1] == "index.md":
                htmldir = os.path.split(htmldir)[0]

            if "title" in _metas and _metas["title"] is None:
                _metas["title"] = os.path.split(htmldir)[-1]

            outfile = os.path.join(htmldir, "index.html")
            if not os.path.exists(htmldir):
                os.makedirs(htmldir)

            # Handle head, nav, header and footer
            def create_section(section, name):
                rtn = '<!--<{0}>-->\n\n'.format(name)
                for line in section:
                    rtn += line + "\n"
                rtn += '\n<!--</{0}>-->'.format(name)
                rtn = Template(rtn).safe_substitute(_metas)
                return rtn.rstrip("\n")

            head = create_section(self.html_head, "head")

            nav = ''
            if "settings" in _metas and not "nonav" in _metas["settings"]:
                nav = create_section(self.html_nav, "nav")

            header = ''
            if "settings" in _metas and not "noheader" in _metas["settings"]:
                header = create_section(self.html_header, "header")

            footer = ''
            if "settings" in _metas and not "nofooter" in _metas["settings"]:
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

<!--<main>-->

{4}

<!--</main>-->

{5}

<!--</body>-->
<!--</html>-->""".format(meta_text, head, nav, header, main_text, footer)

            # Convert to HTML
            md = Markdown(extensions=['markdown.extensions.meta'] + self.extras,
                          extension_configs=self.extras_configs,
                          output_format="html5")
            html = md.reset().convert(content)

            # Fix HTML output
            fixed_html = []
            lines =html.split("\n")
            for c, line in enumerate(lines):
                try:
                    if lines[c-2]  == "<!--<head>-->":
                        line = line.replace("<p>", "")
                    if lines[c+1] == "<!--</head>-->":
                        line = line.replace("</p>", "")
                except:
                    pass

                #line = line.replace("<p><figcaption>", "<figcaption>")
                #line = line.replace("</figcaption></p>", "</figcaption>")
                #if line.startswith("<p><figcaption>") and \
                #        line.endswith("</figcaption></p>"):
                #    fixed_html.append(line[3:-4])
                #elif line.startswith("<p>") and \
                #        line != "<p>" and \
                #        not line.endswith("</p>"):
                #    fixed_html.append(line[3:])
                #elif line.endswith("</p>") and \
                #        line != "</p>" and \
                #        not line.startswith("<p>"):
                #    fixed_html.append(line[:-4])
                #else:
                #    fixed_html.append(line)
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
                            "<!--<main>-->",
                            "<!--</main>-->",
                            "<!--<footer>-->",
                            "<!--</footer>-->"]:
                    fixed_html[pos] = line[4:-3]

            html = "\n".join(fixed_html)

            soup = BeautifulSoup(html, "html.parser")

            # Append whitespace between headings and potential permalink symbol
            headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
            for c,h in enumerate(headings):
                try:
                    if repr(h.contents[1]).startswith('<a class="headerlink"'):
                        headings[c].contents[0] = \
                            NavigableString(headings[c].contents[0] + " ")
                except:
                    pass

            # Handle linked files
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
                internal_link = False

                # Skip web links
                if link.startswith(("#", "mailto:", "tel:")) or "://" in link:
                    continue

                # Make absolute links relative if possible
                if os.path.isabs(link):
                    if "settings" in _metas and \
                            "selfcontained" in _metas["settings"]:
                        # If within directory of current file
                        linkpath = os.path.normpath(os.path.join(
                            os.path.split(filename)[0], link))
                        if not os.path.relpath(
                                linkpath,
                                os.path.split(filename)[0]).startswith(".."):
                            link = os.path.relpath(link,
                                                   os.path.split(filename)[0])
                    else:
                        # If within input directory
                        if not os.path.relpath(
                                link, self.input_dir).startswith(".."):
                            link = os.path.relpath(link,
                                                   os.path.split(filename)[0])

                # Make relative links absolute if necessary
                if not os.path.isabs(link):
                    abs_link = os.path.abspath(
                        os.path.join(os.path.split(filename)[0], link))
                    if "settings" in _metas and \
                            "selfcontained" in _metas["settings"]:
                        # If outside of directory of current file
                        linkpath = os.path.normpath(os.path.join(
                            os.path.split(filename)[0], link))
                        if os.path.relpath(
                                linkpath,
                                os.path.split(filename)[0]).startswith(".."):
                            link = abs_link
                        else:
                            internal_link = True
                    else:
                        # If outside of input directory
                        if os.path.relpath(abs_link,
                                           self.input_dir).startswith(".."):
                            link = abs_link
                        else:
                            internal_link = True

                # Links to other pages
                if internal_link and link.endswith(".md"):
                    root_, file_ = os.path.split(link)
                    name_, ext_ = os.path.splitext(file_)
                    if os.path.split(filename)[-1] == "index.md":
                        up = "."
                    else:
                        up = ".."
                    if link.endswith("index.md"):
                        l[tag] = os.path.join(up, root_).replace('\\', '/')
                    else:
                        l[tag] = os.path.join(
                            up, root_, name_).replace('\\', '/')
                    continue

                # Other absolute links
                if os.path.isabs(link):
                    target_dir = uuid.uuid3(uuid.NAMESPACE_URL, link).hex
                    if "settings" in _metas and \
                            "selfcontained" in _metas["settings"]:
                        to_ = os.path.join(htmldir, "_resources",
                                           target_dir,
                                           os.path.split(link)[-1])
                        l[tag] = os.path.join(
                            "_resources", target_dir,
                            os.path.split(link)[-1]).replace('\\', '/')
                    else:
                        to_ = os.path.join(self.output_dir, "_resources",
                                           target_dir,
                                           os.path.split(link)[-1])
                        l[tag] = os.path.join(
                            os.path.relpath(self.output_dir,
                                            os.path.split(outfile)[0]),
                            "_resources", target_dir,
                            os.path.split(link)[-1]).replace('\\', '/')

                    if os.path.exists(link):
                        if os.path.isfile(link):
                            if not os.path.exists(os.path.split(to_)[0]):
                                os.makedirs(os.path.split(to_)[0])
                            shutil.copyfile(link, to_)
                        else:
                            shutil.copytree(link, to_)

                # Other relative links
                else:
                    from_ = os.path.normpath(os.path.join(self.input_dir,
                                                          rel_mddir, link))
                    if "settings" in _metas and \
                            "selfcontained" in _metas["settings"]:
                        to_ = os.path.join(htmldir, "_resources", link)
                        l[tag] = os.path.join(
                            "_resources", link).replace('\\', '/')
                    else:
                        to_ = os.path.normpath(os.path.join(self.output_dir,
                                                            "_resources",
                                                            rel_mddir,
                                                            link))

                        l[tag] = os.path.normpath(os.path.join(
                            os.path.relpath(self.output_dir,
                                            os.path.split(outfile)[0]),
                            "_resources", rel_mddir, link)).replace('\\', '/')
                    if os.path.exists(from_):
                        if os.path.isfile(from_):
                            if not os.path.exists(os.path.split(to_)[0]):
                                os.makedirs(os.path.split(to_)[0])
                            shutil.copyfile(from_, to_)
                        else:
                            shutil.copytree(from_, to_)

            # Add to output files
            output_files[outfile] = {'md': os.path.abspath(filename),
                                     'metas': _metas,
                                     'html': str(soup),
                                     'update': True}

        # Once all output files are known, postprocess each one
        for outfile in output_files:

            # Substitute [PAGES]
            if re.search("(^<p>\[(!?)PAGES\s?(.*)\]</p>$)",
                         output_files[outfile]["html"],
                         re.MULTILINE) is not None:
                output_files[outfile]['pagelisting'] = True
                pages = []  # [filename, metas]
                htmldir = os.path.split(outfile)[0]
                for directory in os.listdir(htmldir):
                    if directory == "_resources":
                        continue
                    if os.path.isdir(os.path.join(htmldir, directory)):
                        page = os.path.join(htmldir, directory, "index.html")
                        try:
                            pages.append([directory,
                                          output_files[page]['metas']])
                        except:
                            pages.append([directory, {}])
                for match in re.findall("(^<p>\[(!?)PAGES\s?(.*)\]</p>$)",
                                        output_files[outfile]["html"],
                                        re.MULTILINE):
                    pages.sort(key=lambda x: x[0])  # sort by filename
                    try:  # sort by meta
                        pages.sort(key=lambda x: x[1][match[2].lower()])
                    except:
                        pass
                    if match[1] == '!':  # reverse sort
                        pages.reverse()
                    pages_list = '<ul class="pagelisting">\n'
                    for page in pages:
                        item = '<li>' + self.pagelisting_format + '</li>'
                        pages_list += Template(item).safe_substitute(
                            page[1], LINK=page[0]).replace('\\', '/')
                    pages_list += "</ul>\n"

                    output_files[outfile]["html"] = \
                        output_files[outfile]["html"].replace("{0}\n".format(
                            match[0]), pages_list, 1)

            # Substitute [BREADCRUMB]
            if re.search("(^<p>\[(BREADCRUMB)\]</p>$)",
                         output_files[outfile]["html"],
                         re.MULTILINE) is not None:
                output_files[outfile]['breadcrumb'] = True
                path = os.path.split(outfile)[0]
                trail = []
                while path != self.output_dir:
                    path = os.path.split(path)[0]
                    trail.append(os.path.join(path, 'index.html'))
                trail.reverse()
                for match in re.findall("(^<p>\[(BREADCRUMB)\]</p>$)",
                                        output_files[outfile]["html"],
                                        re.MULTILINE):
                    bc = '<span class="breadcrumb">~<span>/</span>'
                    for c,t in enumerate(trail):
                        crumb = self.breadcrumb_format + "<span>/</span>"
                        bc += Template(crumb).safe_substitute(
                            output_files[t]["metas"],
                            LINK=(len(trail) - c) * '../')
                    bc += '</span>'

                    output_files[outfile]["html"] = \
                        output_files[outfile]["html"].replace(
                            "{0}\n".format(match[0]), bc, 1)

            # Don't update page if there are no changes
            if os.path.exists(outfile):
                with open(outfile, encoding='utf-8', mode='r') as f:
                    old_html = f.read()
                if old_html == output_files[outfile]["html"]:
                    output_files[outfile]["update"] = False

        # Write output files
        for outfile in output_files:
            if output_files[outfile]["update"]:
                with codecs.open(outfile, encoding='utf-8', mode='w') as f:
                    f.write(output_files[outfile]["html"])

        return [x for x in output_files if output_files[x]["update"]]
