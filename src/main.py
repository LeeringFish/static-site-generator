import os
from copystatic import copy_from_source_to_destination
from gencontent import generate_page

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    copy_from_source_to_destination(dir_path_static, dir_path_public)

    generate_page(
        os.path.join(dir_path_content, "index.md"),
        template_path,
        os.path.join(dir_path_public, "index.html"),
    )


if __name__ == "__main__":
    main()
