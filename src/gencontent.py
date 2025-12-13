import os

from block_markdown import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("no h1 header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as from_file:
        markdown = from_file.read()

    with open(template_path, "r") as template_file:
        template = template_file.read()

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    with open(dest_path, "w") as dest_file:
        dest_file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, root_content_dir):
    relative_dir = os.path.relpath(dir_path_content, root_content_dir)
    dest_subdir = os.path.join(dest_dir_path, relative_dir)
    os.makedirs(dest_subdir, exist_ok=True)

    for entry in os.listdir(dir_path_content):
        current_path = os.path.join(dir_path_content, entry)

        if os.path.isfile(current_path) and current_path.endswith(".md"):
            dest_path = os.path.join(dest_subdir, "index.html")
            generate_page(current_path, template_path, dest_path)
        elif os.path.isdir(current_path):
            generate_pages_recursive(current_path, template_path, dest_dir_path, root_content_dir)
    