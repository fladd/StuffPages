# The directory in which the source markdown (.md) files are located
markdown_dir = "examples" 
 
# Additional 'extras' to be used by the Python 'markdown' package
extras = ['markdown.extensions.toc',
          'markdown.extensions.codehilite',
          'pymdownx.extra',
          'pymdownx.github'
          ]

extras_configs = {'markdown.extensions.toc': {
                     'permalink': "#"
                     },
                 'markdown.extensions.codehilite': {
                     'guess_lang': False
                     }
                  }

# Default settings (can be overwritten by meta data) 
defaults = {"output_dir" : "~/Desktop/",
                 "title" : "A StuffPages page",
               "favicon" : "",
                 "style" : "styles/default.css",
               "settings": ""
           }
