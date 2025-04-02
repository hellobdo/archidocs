#!/usr/bin/env python3
import os
import json
import argparse
from datetime import datetime
import sys
import glob
from docxtpl import DocxTemplate
from num2words import num2words
from decimal import Decimal, ROUND_HALF_UP

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
        int_part = str(round(number))
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
        # Use string formatting to get exact decimal part (avoids floating point errors)
        formatted = f"{number:.2f}"
        _, dec_str = formatted.split('.')
        decimal_part = int(dec_str)
        
        print(f"Debug - Number: {number}, Int part: {int_part}, Decimal part: {decimal_part}")
        
        # Convert to words
        int_words = num2words(int_part, lang=lang)
        
        # Add comma after "mil" if it's followed by additional numbers
        # Improved logic to handle different positions of "mil" in the string
        if "mil" in int_words and int_part > 1000 and int_part % 1000 != 0:
            # Check for different patterns: ' mil ', 'mil ' (at start), or ' mil' (at end)
            if ' mil ' in int_words:
                int_words = int_words.replace(' mil ', ' mil, ')
            elif int_words.startswith('mil '):
                int_words = int_words.replace('mil ', 'mil, ')
            elif int_words.endswith(' mil'):
                # This should rarely happen, but included for completeness
                pass
        
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
                result += f", {dec_words}"
        
        return result
    
    except Exception as e:
        print(f"Error converting number to words: {e}")
        return str(number)

def to_number(variable):
    """Convert variables to numbers with precise decimal handling.
    
    Uses Decimal for precise arithmetic to avoid floating point precision issues.
    
    Args:
        variable: The value to convert to a number
        
    Returns:
        The value as a float, precisely rounded to 2 decimal places
    """
    # Convert to Decimal for precise arithmetic
    decimal_value = Decimal(str(variable))
    
    # Round to 2 decimal places using ROUND_HALF_UP
    rounded_value = decimal_value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    # Convert back to float for compatibility
    return float(rounded_value)

def process_total_cost(qty, cost_per_unit):
    """Calculate the total cost from quantity and cost per unit.
    
    Args:
        qty: The quantity
        cost_per_unit: The cost per unit
        
    Returns:
        The total cost precisely rounded to 2 decimal places
    """
    # Calculate total cost
    total_cost = qty * cost_per_unit
    
    # Use to_number for consistent rounding
    return to_number(total_cost)

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
    template_dir = 'backend/templates/files'
    
    try:
        # List all files in the directory
        files = os.listdir(template_dir)
        
        # Filter for .docx files
        for file in files:
            if file.lower().endswith('.docx'):
                # Extract template name (filename without extension)
                template_name = os.path.splitext(file)[0]
                templates.append(template_name)
    except Exception as e:
        print(f"Error listing templates: {e}")
    
    return templates

def generate_document(template_name, variables, output_path):
    """Generate a document from a template and variables."""
    # Make a copy of variables to avoid modifying the original
    variables = variables.copy()
    
    # Process date variable with special format
    now = datetime.now()
    month_name = get_portuguese_month(now.month)
    variables['date'] = f"{month_name} de {now.year}"

    # Process cost calculations if required variables exist
    if 'qty' in variables and 'cost_per_unit' in variables:
        # Convert variables to numbers with precise decimal handling
        qty = to_number(variables['qty'])
        cost_per_unit = to_number(variables['cost_per_unit'])
        
        # Calculate total cost
        total_cost = process_total_cost(qty, cost_per_unit)
        
        # Generate formatted versions
        total_cost_words = num_to_words_pt(total_cost, "euro")
        total_cost_formatted = format_number_pt(total_cost, True, "€")
        
        # Update variables
        variables['total_cost'] = total_cost_formatted
        variables['total_cost_words'] = total_cost_words
        variables['qty'] = format_number_pt(qty, True, "")
        variables['cost_per_unit'] = format_number_pt(cost_per_unit, True, "€")

    # Process accessibility calculations if required variables exist
    if 'accessibility_width' in variables and 'accessibility_height' in variables:
        variables['accessibility_width'] = to_number(variables['accessibility_width'])
        variables['accessibility_height'] = to_number(variables['accessibility_height'])
    
    # Determine template path
    template_path = os.path.join('backend/templates/files', f"{template_name}.docx")
    
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