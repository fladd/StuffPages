import os
from datetime import datetime

import pymdownx.emoji


# Default settings (can be overwritten by meta data)
defaults = {
    "output_dir" : "html",
    "style" : "default",  # Name of built in style or path/url of .css file
    "author": "",
    "author_link": "",
    "title" : "A StuffPages page",
    "description": "",
    "settings": "",
    #"favicon": ""
}

# HTML head (can make use of default settings and meta data)
html_head = [
    '<meta charset="UTF-8">',
    '<meta name="viewport" content="width=device-width, initial-scale=1">',
    '<title>{{title}}</title>',
    '<meta name="author" content="{{author}}">',
    '<meta name="description" content="{{description}}">',
    '<link href="{{style}}" rel="stylesheet" media="screen">'
    #'<link rel="icon" href="{{favicon}}" type="image/x-icon" />'
]

# HTML Header (can make use of default settings and meta data)
html_header = [
    '<header>',
    '<h1>{{title}}</h1>',
    '<p>{{description}}</p>',
    '</header>'
]

# HTML Footer (can make use of default settings and meta data)
html_footer = [
    '<footer>',
    '<p><strong>&copy; {0} <a href="{{author_link}}">{{author}}</a></strong></p>'.format(datetime.now().year),
    '<p class="page-credits">Created with <a href="https://github.com/fladd/StuffPages">StuffPages</a></p>',
    '</footer>'
]

# Additional 'extras' to be used by the Python 'markdown' package
extras = [
    'markdown.extensions.codehilite',  # Syntax highlighting for code blocks
    'markdown.extensions.def_list',    # Definition Lists
    'markdown.extensions.footnotes',   # Footnotes
    'markdown.extensions.tables',      # Tables
    'markdown.extensions.toc',         # Table of Contents
    'pymdownx.extrarawhtml',
    'pymdownx.betterem',               # Improved emphasis handling
    'pymdownx.emoji',                  # Emoji
    'pymdownx.magiclink',              # Generate links from raw URLs
    'pymdownx.superfences',            # Fenced Code Blocks
    'pymdownx.tasklist',               # Task Lists
    'pymdownx.tilde',                  # Underline and subscript
    # Add more 'extras' here
]

# Configuration for additional 'extras'
extras_configs = {
    'markdown.extensions.codehilite': {
        'guess_lang': False
    },
    'markdown.extensions.footnotes': {
        'BACKLINK_TEXT': u"&#8617;&#65038;"
    },
    'markdown.extensions.toc': {
        'anchorlink': False,
        'permalink': "#"
    },
    "pymdownx.emoji": {
        "emoji_generator": pymdownx.emoji.to_alt,
        "alt": "unicode",
    },
    'pymdownx.tilde': {
         'subscript': False
    }
}
