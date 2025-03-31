"""
Utility functions for loading and processing variables and templates.
"""

import json
import os
from jinja2 import Environment, FileSystemLoader

def load_variables(variables_path="/app/templates/variables.json"):
    """Load variables from a JSON file."""
    with open(variables_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_available_templates():
    """Get a list of available templates."""
    templates = []
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../templates/files")
    
    try:
        # List all files in the directory
        files = os.listdir(template_dir)
        
        # Filter for HTML files
        for file in files:
            if file.lower().endswith('.html'):
                # Extract template name (filename without extension)
                template_name = os.path.splitext(file)[0]
                templates.append(template_name)
    except Exception as e:
        print(f"Error listing templates: {e}")
    
    return templates

def render_html_template(template_name, variables_dict):
    """Render an HTML template with the provided variables."""
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../templates/files")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(f"{template_name}.html")
    return template.render(**variables_dict)