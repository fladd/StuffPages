# The directory in which the source markdown (.md) files are located
markdown_dir = "examples" 
 
# Additional 'extras' to be used by the Python 'markdown2' package 
extras = ['markdown.extensions.extra',
          'markdown.extensions.headerid',
          'markdown.extensions.codehilite',
          ]
 
# Default settings (can be overwritten by meta data) 
defaults = {"output_dir" : "~/Desktop/",
                   "url" : "http://www.example.com",
                 "title" : "A StuffPages page", 
               "favicon" : "http://www.example.com/favicon", 
                 "style" : "styles/cayman.css",
                 "font" : "http://fonts.googleapis.com/css?family=Open+Sans:400,700"
           }
