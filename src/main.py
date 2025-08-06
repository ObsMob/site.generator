import os
import shutil
import re
import sys

from markdown_blocks import markdown_to_html_node


def main():
    
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "/"
    
    template_path = "./template.html"
    src_path = "./content"
    dst_path = "./docs"
    
    static_to_public(dst_path)
    generate_pages_recursive(src_path, dst_path, base_path, template_path)

def static_to_public(dst, src="./static"):
    
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
    
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            os.mkdir(dst_path)
            static_to_public(dst_path, src_path)

def extract_title(markdown):
    heading_exist = re.match(r"^#\s+(.*)", markdown)

    if not heading_exist:
        raise Exception('file is missing a "# heading"')

    return heading_exist.group(1).strip()

def generate_page(src_path, dst_path, base_path, template_path):
    print(f'Generating page from {src_path} to {dst_path} using {template_path}')
    
    with open(src_path, "r") as f:
        markdown = f.read()
    
    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html)
    page = page.replace('href="/', f'href="{base_path}')
    page = page.replace('src="/', f'src="{base_path}')

    with open(dst_path, "w") as f:
        f.write(page)

def generate_pages_recursive(src_path_content, dst_path_content, base_path, template_path):
    for item in os.listdir(src_path_content):
        src_path = os.path.join(src_path_content, item)
        
        if os.path.isfile(src_path):
            if item.endswith(".md"):
                root, ext = os.path.splitext(item)
                dst_path = os.path.join(dst_path_content, f'{root}.html')
                generate_page(src_path, dst_path, base_path, template_path)

        elif os.path.isdir(src_path):
            dst_path = os.path.join(dst_path_content, item)

            if not os.path.exists(dst_path):
                os.mkdir(dst_path)
                
            generate_pages_recursive(src_path, dst_path, base_path, template_path)


if __name__ == "__main__":
    main()