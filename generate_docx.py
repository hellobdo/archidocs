#!/usr/bin/env python3
import os
import json
import argparse
from datetime import datetime
import sys
import glob
from docxtpl import DocxTemplate

def load_variables(variables_path="templates/variables.json"):
    """Load variables from a JSON file."""
    with open(variables_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_portuguese_month(month_number):
    """Convert month number to Portuguese month name."""
    pt_months = {
        1: "janeiro",
        2: "fevereiro",
        3: "março",
        4: "abril",
        5: "maio",
        6: "junho",
        7: "julho",
        8: "agosto",
        9: "setembro",
        10: "outubro",
        11: "novembro",
        12: "dezembro"
    }
    return pt_months.get(month_number, "")

def get_available_templates():
    """Get a list of available templates."""
    templates = []
    for path in glob.glob('templates/files/*.docx'):
        template_name = os.path.splitext(os.path.basename(path))[0]
        templates.append(template_name)
    return templates

def generate_document(template_name, variables, output_path):
    """Generate a document from a template and variables."""
    # Determine template path
    template_path = os.path.join('templates', f"files/{template_name}.docx")
    
    # Check if template exists
    if not os.path.exists(template_path):
        print(f"Error: Template '{template_name}' not found")
        return False
    
    try:
        # Load the docx template
        doc = DocxTemplate(template_path)
        
        # Render the template with the variables
        doc.render(variables)
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save the generated document
        doc.save(output_path)
        print(f"Document successfully generated at: {output_path}")
        return True
    except Exception as e:
        print(f"Error generating document: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Generate documents from Word templates')
    parser.add_argument('--templates', '-t', nargs='*', help='Templates to generate (default: all)')
    parser.add_argument('--variables', '-v', default='templates/variables.json', 
                        help='JSON file with variables (default: templates/variables.json)')
    parser.add_argument('--output-dir', '-d', default='outputs', help='Output directory (default: outputs/)')
    parser.add_argument('--list', '-l', action='store_true', help='List available templates')
    
    args = parser.parse_args()
    
    # Get available templates
    available_templates = get_available_templates()
    
    # List templates if requested
    if args.list:
        print("Available templates:")
        for template in available_templates:
            print(f"  - {template}")
        return
    
    # Determine which templates to generate
    templates_to_generate = args.templates if args.templates else available_templates
    
    # Load variables
    try:
        variables = load_variables(args.variables)
    except FileNotFoundError:
        print(f"Error: Variables file '{args.variables}' not found")
        sys.exit(1)
    
    # Process date variable if it exists with special format
    if 'date' in variables and variables['date'].lower() == 'today':
        now = datetime.now()
        month_name = get_portuguese_month(now.month)
        variables['date'] = f"{month_name} de {now.year}"
    
    # Generate each document
    for template_name in templates_to_generate:
        output_path = os.path.join(args.output_dir, f"{template_name}.docx")
        generate_document(template_name, variables, output_path)

if __name__ == '__main__':
    main() 