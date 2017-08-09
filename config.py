import pymdownx.emoji


# The directory in which the source markdown (.md) files are located
markdown_dir = "pages" 

# Default settings (can be overwritten by meta data) 
defaults = {
    "output_dir" : "~/public_html/stuff/pages",
    "style" : "styles/default.css",
    "author": "Florian Krause",
    "author_link": "http://www.fladd.de",
    "title" : "A StuffPages page",
    "description": "",
    "favicon" : "",
    "settings": ""
}

# Additional 'extras' to be used by the Python 'markdown' package
extras = ['markdown.extensions.codehilite',  # Syntax highlighting for code blocks
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
