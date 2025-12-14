import os
import sys
from copystatic import copy_from_source_to_destination
from gencontent import generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
base_path = sys.argv[1] if len(sys.argv) > 1 else "/"

def main():
    copy_from_source_to_destination(dir_path_static, dir_path_docs)

    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_docs,
        dir_path_content,
        base_path,
    )


if __name__ == "__main__":
    main()
