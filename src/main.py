import os
from copystatic import copy_from_source_to_destination
from gencontent import generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    copy_from_source_to_destination(dir_path_static, dir_path_public)

    generate_pages_recursive(
        dir_path_content,
        template_path,
        dir_path_public,
        dir_path_content,
    )


if __name__ == "__main__":
    main()
