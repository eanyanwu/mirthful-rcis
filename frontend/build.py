#################################
# Build script for the frontend #
#################################

# Without html templating, there would be a lot of repeated html code.
# With html templating, this problem goes a way, but now we need an
# intermediate step to convert our templates into plain html.
# This build script takes care of that.
# Html templating is given to us for free by Jinja2. This is not an addeded
# dependency because Flask already uses it 

import os
import os.path
import shutil
from jinja2 import Environment, FileSystemLoader

def filter_func(template_name):
    is_html = template_name.endswith('.html')
    is_child_template = not template_name.startswith('templates/')

    return is_html and is_child_template 

def apply_templates():
    # The location from which templates will be discovered
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # This is where we will output the files to be served
    output_dir = os.path.join(current_dir, "www")

    # We will copy the css and js folders as-is
    css_dir = os.path.join(current_dir, 'css')
    js_dir = os.path.join(current_dir, 'js')

    # Clear the output_dir if it already exists
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    os.mkdir(output_dir)

    # Copy css files
    shutil.copytree(css_dir, os.path.join(output_dir, 'css'))

    # Copy js files
    shutil.copytree(js_dir, os.path.join(output_dir, 'js'))


    # Create the jinja2 environment 
    # All templates are loaded into this, and it looks like that is what
    # allows template inheritance
    env = Environment (
        loader=FileSystemLoader(current_dir)
    )

    # We only want to render child templates
    # Meaning, we only want to render *.html files that inherit from something
    # else
    child_templates = env.list_templates(filter_func=filter_func)

    for template_name in child_templates:
        template = env.get_template(template_name)
        rendered = template.render()

        # Create the full path for the output file
        filename = template.filename
        leaf_part = filename[filename.find('html'):].replace('html/', '')
        new_path = os.path.join(output_dir, leaf_part)

        # Create any intermediate directories
        new_path_dir = os.path.dirname(new_path)
        os.makedirs(new_path_dir, exist_ok=True)

        # Write the file
        with open(new_path, mode='w') as f:
            f.write(rendered)


if __name__ == '__main__':
    apply_templates()

