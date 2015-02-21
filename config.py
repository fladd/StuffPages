# The directory in wich the source markdown (.md) files are located 
markdown_dir = "examples" 
 
# Additional 'extras' to be used by the Python 'markdown2' package 
extras = ['headers-id', 
          'footnotes',
          'fenced-code-blocks',
          ]
 
# Default settings (can be overwritten by meta data) 
defaults = {"output_dir" : "~/public_html/stuff/",
                   "url" : "http://www.example.com",
                 "title" : "A StuffPages page", 
               "favicon" : "http://www.example.com/favicon", 
                 "style" : "styles/solarized_dark.css", 
           }
