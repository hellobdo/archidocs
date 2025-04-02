"""
Utility functions for loading and processing variables and templates.
"""

import json
import os
from jinja2 import Environment, FileSystemLoader
import zipfile
from typing import List, Optional

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
                
        # Sort templates alphabetically
        templates.sort()
    except Exception as e:
        print(f"Error listing templates: {e}")
    
    return templates

def render_html_template(template_name, variables_dict, template_dir=None):
    """Render an HTML template with the provided variables.
    
    Args:
        template_name (str): Name of the template file (without .html extension)
        variables_dict (dict): Dictionary of variables to render in the template
        template_dir (str, optional): Directory containing the template files. 
            If not provided, uses the default templates directory.
    """
    if template_dir is None:
        template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../templates/files")
    # Create environment with autoescaping enabled for security
    env = Environment(loader=FileSystemLoader(template_dir), autoescape=True)
    template = env.get_template(f"{template_name}.html")
    return template.render(**variables_dict)

def create_zip_from_files(files: List[str], output_zip_path: str) -> Optional[str]:
    """
    Create a ZIP file from a list of files.
    
    Args:
        files: List of file paths to include in the ZIP
        output_zip_path: Path where the ZIP file should be saved
    
    Returns:
        Path to the created ZIP file or None if creation failed
    """
    try:
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_zip_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Check that all files exist
        valid_files = []
        for file_path in files:
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                valid_files.append(file_path)
            else:
                print(f"Warning: File not found or empty: {file_path}")
        
        # If no valid files, return None
        if not valid_files:
            print("No valid files to add to ZIP")
            return None
        
        # Create the ZIP file
        with zipfile.ZipFile(output_zip_path, 'w') as zip_file:
            for file_path in valid_files:
                file_name = os.path.basename(file_path)
                print(f"Adding to ZIP: {file_path} as {file_name}")
                zip_file.write(file_path, arcname=file_name)
        
        # Verify the ZIP was created
        if os.path.exists(output_zip_path) and os.path.getsize(output_zip_path) > 0:
            print(f"ZIP created successfully at {output_zip_path} with size {os.path.getsize(output_zip_path)} bytes")
            return output_zip_path
        else:
            print(f"ZIP creation failed: {output_zip_path}")
            return None
            
    except Exception as e:
        print(f"Error creating ZIP: {str(e)}")
        import traceback
        traceback.print_exc()
        return None