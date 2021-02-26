import os

import pymdownx.emoji


# HTML output directory
output_dir = "html"

# Default settings (can be overwritten by meta data)
defaults = {
    "title":        None,  # None will set title to file/directory name
    "description":  "",
    "author":       "Unknown",
    "authorlink":   "https://en.wikipedia.org/wiki/Anonymous_work",
    "date":         "",
    "style":        os.path.abspath("styles/default.css"),
    "settings":     "",
    #"favicon":     ""
}

# HTML Head
# Can make use of defaults/meta data (lowercase, prefixed with $) and listings
html_head = [
    '<meta charset="UTF-8">',
    '<meta name="viewport" content="width=device-width, initial-scale=1">',
    '<title>$title</title>',
    '<meta name="author" content="$author">',
    '<meta name="description" content="$description">',
    '<link href="$style" rel="stylesheet" media="screen" />',
    #'<link rel="icon" href="$favicon" type="image/x-icon" />'
]

# HTML navigation
# Can make use of defaults/meta data (lowercase, prefixed with $) and listings
html_nav = [
    '[BREADCRUMB]',
]

# HTML Header
# Can make use of defaults/meta data (lowercase, prefixed with $) and listings
html_header = [
    '<h1>$title</h1>',
    '<p>$description</p>',
]

# HTML Footer
# Can make use of defaults/meta data (lowercase, prefixed with $) and listings
html_footer = [
    '<p>',
    '<strong>&copy; <a href="$authorlink">$author</a></strong>',
    '<br>',
    '<em>$date</em>',
    '</p>',
    '<p>',
    'Created with <a href="https://fladd.github.io/StuffPages/">StuffPages</a>',
    '</p>',
]

# Format for each item in pages listings ([PAGES])
# Can make use of defaults/meta data (lowercase, prefixed with $)
# $LINK will be replaced by a (relative) link to page
pagelisting_format = '<p><a href="$LINK">$title</a><br />$description</p>'

# Format for each item in breadcrumb listings ([BREADCRUMB])
# Can make use of defaults/meta data (lowercase, prefixed with $)
# $LINK will be replaced by (relative) link to page
breadcrumb_format = '<a href="$LINK">$title</a>'

# Additional 'extras' to be used by the Python 'markdown' package
extras = [
    'markdown.extensions.def_list',    # Definition Lists
    'markdown.extensions.footnotes',   # Footnotes
    'markdown.extensions.md_in_html',  # Markdown within HTML
    'markdown.extensions.tables',      # Tables
    'markdown.extensions.toc',         # Table of Contents
    'pymdownx.betterem',               # Improved emphasis handling
    'pymdownx.emoji',                  # Emoji
    'pymdownx.highlight',              # Syntax highlighting
    'pymdownx.magiclink',              # Generate links from raw URLs
    'pymdownx.superfences',            # Fenced Code Blocks
    'pymdownx.tasklist',               # Task Lists
    'pymdownx.tilde',                  # Underline and subscript
    # Add more 'extras' here
]

# Configuration for additional 'extras'
extras_configs = {
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
