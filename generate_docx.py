#!/usr/bin/env python3
import os
import json
import argparse
from datetime import datetime
import sys
import glob
from docxtpl import DocxTemplate
from num2words import num2words

def load_variables(variables_path="templates/variables.json"):
    """Load variables from a JSON file."""
    with open(variables_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def format_number_pt(number, show_decimals=True, currency_symbol="€"):
    """Format number in Portuguese style.
    
    Args:
        number: The number to format
        show_decimals: If True, show 2 decimal places; if False, show only integer part
        currency_symbol: Currency symbol to append (empty string for no symbol)
        
    Returns:
        Formatted string (e.g., "1.234,56 €" or "1.234")
    """
    if show_decimals:
        # Format with 2 decimal places
        formatted = f"{number:.2f}"
        
        # Split by decimal point
        int_part, dec_part = formatted.split('.')
    else:
        # Format without decimal places (round to integer)
        int_part = str(int(number))
        dec_part = None
    
    # Add thousands separator to integer part
    int_part_with_sep = ''
    for i, digit in enumerate(reversed(int_part)):
        if i > 0 and i % 3 == 0:
            int_part_with_sep = '.' + int_part_with_sep
        int_part_with_sep = digit + int_part_with_sep
    
    # Combine with decimal part if needed
    if show_decimals and dec_part:
        result = f"{int_part_with_sep},{dec_part}"
    else:
        result = int_part_with_sep
    
    # Add currency symbol if provided
    if currency_symbol:
        result += f" {currency_symbol}"
    
    return result

def num_to_words_pt(number, currency=None, lang='pt_pt'):
    """Convert a number to words in Portuguese.
    
    Args:
        number: The number to convert
        currency: Optional currency name (e.g., 'euro', 'euros')
        
    Returns:
        String representation of the number in Portuguese words
    """
    try:
        # Get integer and decimal parts
        int_part = int(number)
        decimal_part = int(round((number - int_part) * 100))
        
        # Convert to words
        int_words = num2words(int_part, lang=lang)
        
        # Handle currency if provided
        if currency:
            # Determine singular or plural form
            if int_part == 1:
                # Singular
                result = f"{int_words} {currency}"
            else:
                # Plural
                result = f"{int_words} {currency}s"
                
            # Add cents if there are any
            if decimal_part > 0:
                cent_words = num2words(decimal_part, lang=lang)
                
                if decimal_part == 1:
                    result += f" e {cent_words} centavo"
                else:
                    result += f" e {cent_words} centavos"
        else:
            # Without currency
            result = int_words
            
            # Add decimal part if there is any
            if decimal_part > 0:
                dec_words = num2words(decimal_part, lang=lang)
                result += f" vírgula {dec_words}"
        
        return result
    
    except Exception as e:
        print(f"Error converting number to words: {e}")
        return str(number)

def process_total_cost(qty, cost_per_unit):
    """Process and add calculated variables."""
    # Calculate total_cost if qty and cost_per_unit exist
    total_cost = qty * cost_per_unit
    return total_cost

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

def to_number(variable):
    """Convert variables to numbers."""
    variable_float = round(float(variable), 2)
    return variable_float

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

    # Convert variables to numbers
    if 'qty' in variables and 'cost_per_unit' in variables:
        qty = to_number(variables['qty'])
        cost_per_unit = to_number(variables['cost_per_unit'])
    
    # Process calculated variables
        total_cost = process_total_cost(qty, cost_per_unit)
        total_cost_formatted = format_number_pt(total_cost, True, "€")
        total_cost_words = num_to_words_pt(total_cost, "euro")

    variables['total_cost'] = total_cost_formatted
    variables['total_cost_words'] = total_cost_words
    variables['qty'] = format_number_pt(qty, True, "")
    variables['cost_per_unit'] = format_number_pt(cost_per_unit, True, "€")
    
    # Generate each document
    for template_name in templates_to_generate:
        output_path = os.path.join(args.output_dir, f"{template_name}.docx")
        generate_document(template_name, variables, output_path)

if __name__ == '__main__':
    main()