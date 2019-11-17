import os
from datetime import datetime

import pymdownx.emoji


# Default settings (can be overwritten by meta data)
defaults = {
    "output_dir": "_stuffpages/html",
    "style": "_stuffpages/styles/default.css",
    #"favicon": ""
    "title": "A StuffPages page",  # Needed!
    "description": "",
    "author": "",
    "author_link": "",
    "date" : str(datetime.now().date())
    "settings": "",
}

# HTML Head (can make use of defaults/meta data and listings)
html_head = [
    '<meta charset="UTF-8">',
    '<meta name="viewport" content="width=device-width, initial-scale=1">',
    '<title>{{title}}</title>',
    '<meta name="author" content="{{author}}">',
    '<meta name="description" content="{{description}}">',
    '<link href="{{style}}" rel="stylesheet" media="screen">',
    #'<link rel="icon" href="{{favicon}}" type="image/x-icon" />'
]

# HTML navigation (can make use of defaults/meta data and listings)
html_nav = [
    '[BREADCRUMB]',
]

# HTML Header (can make use of defaults/meta data and listings)
html_header = [
    '<h1>{{title}}</h1>',
    '<p>{{description}}</p>',
]

# HTML Footer (can make use of default settings and meta data)
html_footer = [
    '<p>',
    '<strong>&copy; <a href="{{author_link}}">{{author}}</a>' +\
        ' | {{date}}</strong>',
    '<br />',
    'Created with <a href="https://github.com/fladd/StuffPages">StuffPages</a>',
    '</p>',
]

# Format for each item in pages listings ([PAGES])
# (can make use of defaults/meta data)
# {0} will be replaced by link to page
pagelisting_format = '<p><a href="{0}">{{title}}</a><br />{{description}}</p>'

# Format for each item in breadcrumb listings ([BREADCRUMB])
# (can make use of defaults/meta data)
# {0} will be replaced by link to page
breadcrumb_format = '<a href="{0}">{{title}}</a>'

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
        'BACKLINK_TEXT': u"&#8617;&#65038;",
    },
    'markdown.extensions.toc': {
        #'anchorlink': True,
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
