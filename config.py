import pymdownx.emoji


# The directory in which the source markdown (.md) files are located
markdown_dir = "examples" 

# Default settings (can be overwritten by meta data) 
defaults = {
    "output_dir" : "~/Desktop/",     # The output directory
    "title" : "A StuffPages page",   # The default page title
    "favicon" : "",                  # Link to Favicon file
    "style" : "styles/default.css",  # The default style
    "settings": ""                   # Additional settings (noheader/nofooter)
}

# Additional 'extras' to be used by the Python 'markdown' package
extras = ['markdown.extensions.codehilite',  # Syntax highlighting for code blocks
          'markdown.extensions.def_list',    # Definition Lists
          'markdown.extensions.footnotes',   # Footnotes
          'markdown.extensions.tables',      # Tables
          'markdown.extensions.toc',         # Table of Contents
          'pymdownx.betterem',               # Improved emphasis handling
          'pymdownx.emoji',                  # Emoji
          'pymdownx.magiclink',              # Generate links from raw URLs
          'pymdownx.superfences',            # Fenced Code Blocks
          'pymdownx.tasklist',               # Task Lists
          'pymdownx.tilde',                  # Underline (no subscript, see settings below)
          # Add more 'extras' here
          ]

# Configuration for additional 'extras'
extras_configs = {
    'markdown.extensions.codehilite': {
        'guess_lang': False
    },
    'markdown.extensions.footnotes': {
        'BACKLINK_TEXT': "&#8617;&#65038;"
    },
    'markdown.extensions.toc': {
        'permalink': "#"
    },
    "pymdownx.emoji": {
        "emoji_index": pymdownx.emoji.gemoji,
        "emoji_generator": pymdownx.emoji.to_png,
        "alt": "short",
        "options": {
            "attributes": {
                "align": "absmiddle",
                "height": "20px",
                "width": "20px"
            },
            "image_path": "https://assets-cdn.github.com/images/icons/emoji/unicode/",
            "non_standard_image_path": "https://assets-cdn.github.com/images/icons/emoji/"
        }
    },
    'pymdownx.tilde': {
         'subscript': False
    },
    # Add more 'extras' settings here
}
