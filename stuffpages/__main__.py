#!/usr/bin/env python


import sys
import os

from stuffpages import StuffPages


def main():
    """Main function of CLI application."""

    if len(sys.argv) not in (2, 3) or \
       sys.argv[1] not in ("init", "build", "update"):
        print("")
        print("StuffPages - An quick way to create simple web pages using Markdown")
        print("")
        print("Usage: stuffpages <command> [<directory>]")
        print("")
        print("Commands:")
        print("  init     Init default 'config.py' in <directory>")
        print("  build    Build all pages ('*.md') in <directory>")
        print("  update   Update new/changed pages in <directory>")
        print("")
        print("If <directory> is unspecified, current directory will be used.")
        print("")
    else:
        if len(sys.argv) == 3:
            directory = os.path.abspath(sys.argv[2])
        else:
            directory = os.path.abspath(os.getcwd())
        sp = StuffPages(directory)
        if sys.argv[1] == "init":
            sp.init()
        elif sys.argv[1] == "build":
            sp.build()
        elif sys.argv[1] == "update":
            sp.update()


if __name__ == "__main__":
    main()
