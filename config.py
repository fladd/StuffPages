# The directory in which the source markdown (.md) files are located
markdown_dir = "examples" 
 
# Additional 'extras' to be used by the Python 'markdown' package
extras = ['markdown.extensions.extra',
          'markdown.extensions.headerid',
          'markdown.extensions.codehilite',
          ]
 
# Default settings (can be overwritten by meta data) 
defaults = {"output_dir" : "~/Desktop/",
                 "title" : "A StuffPages page", 
               "favicon" : "",
                 "style" : "styles/simple.css",
               "settings": ""
           }
