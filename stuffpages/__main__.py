#!/usr/bin/env python3


import sys
import os

from stuffpages import StuffPages


def main():
    """Main function of CLI application."""

    if len(sys.argv) not in (2, 3) or \
       sys.argv[1] not in ("init", "build"):
        print("StuffPages - A quick way to create simple web pages using Markdown")
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
                print("ERROR: found _stuffpages/ in {0}! (Already initialized?)".format(directory))
        elif sys.argv[1] == "build":
            if sp.load_config():
                if not os.path.relpath(sp.input_dir,
                                       sp.output_dir).startswith(".."):
                    get = input("Output directory contains input directory! Continue? (y/[n]): ")
                    if get.lower() != "y":
                        return
                pages = sp.build()
                print("Built pages from {0}:".format(directory))
                for page in pages:
                    print(page)
            else:
                print("ERROR: could not parse _stuffpages/config.py from {0}! (StuffPages initialized?)".format(directory))


if __name__ == "__main__":
    main()
