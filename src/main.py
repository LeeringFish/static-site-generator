import os
import shutil

from textnode import TextNode
from textnode import TextType
from copystatic import copy_from_source_to_destination

def main():
    copy_from_source_to_destination("static", "public")


if __name__ == "__main__":
    main()
