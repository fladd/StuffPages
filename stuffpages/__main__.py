#!/usr/bin/env python3


import sys
import os

from stuffpages import StuffPages


def main():
    """Main function of CLI application."""

    if len(sys.argv) not in (2, 3) or \
       sys.argv[1] not in ("init", "build"):
        print("StuffPages - An quick way to create simple web pages using Markdown")
        print("")
        print("Usage: stuffpages <command> [<directory>]")
        print("")
        print("Commands:")
        print("  init     Inititialize StuffPages in <directory>")
        print("  build    Build all pages ('*.md') in <directory>")
        print("")
        print("If <directory> is unspecified, current directory will be used.")
    else:
        if len(sys.argv) == 3:
            directory = os.path.abspath(sys.argv[2])
        else:
            directory = os.path.abspath(os.getcwd())
        sp = StuffPages(directory)
        if sys.argv[1] == "init":
            if sp.init():
                print("Initialized StuffPages in {0}".format(directory))
            else:
                print("Error: found _stuffpages/ in {0}! (Already initialized?)".format(directory))
        elif sys.argv[1] == "build":
            pages = sp.build()
            if pages is None:
                print("Error: could not parse _stuffpages/config.py from {0}! (StuffPages initialized?)".format(directory))
            else:
                print("Built pages from {0}:".format(directory))
                for page in pages:
                    print(page)


if __name__ == "__main__":
    main()
