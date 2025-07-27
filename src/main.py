import os
import shutil
import re

from markdown_blocks import markdown_to_html_node

def main():
    src_path_content = "./content"
    template_path = "./template.html"
    dst_path_content = "./public"
    
    static_to_public()
    generate_pages_recursive(src_path_content, template_path, dst_path_content)

def static_to_public(src="./static", dst="./public"):
    
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
            static_to_public(src_path, dst_path)

def extract_title(markdown):
    heading_exist = re.match(r"^#\s+(.*)", markdown)

    if not heading_exist:
        raise Exception('file is missing a "# heading"')

    return heading_exist.group(1).strip()

def generate_page(src, template_path, dst):
    print(f'Generating page from {src} to {dst} using {template_path}')
    
    with open(src, "r") as f:
        markdown = f.read()
    
    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html)
    
    # file_name = src.split("/")[-1].rstrip("md")
    # dst_path = os.path.join(dst, f'{file_name}.html')

    with open(dst, "w") as f:
        f.write(page)

def generate_pages_recursive(src_path_content, template_path, dst_path_content):
    for item in os.listdir(src_path_content):
        src_path = os.path.join(src_path_content, item)
        
        if os.path.isfile(src_path):
            if item.endswith(".md"):
                root, ext = os.path.splitext(item)
                dst_path = os.path.join(dst_path_content, f'{root}.html')
                generate_page(src_path, template_path, dst_path)
        else:
            if os.path.isdir(src_path):
                dst_path = os.path.join(dst_path_content, item)

                if not os.path.exists(dst_path):
                    os.mkdir(dst_path)
                
                generate_pages_recursive(src_path, template_path, dst_path)


if __name__ == "__main__":
    main()