"""
Numbers and Dates Utility - Converts numbers to words and formats dates in Portuguese style.
"""

from num2words import num2words
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime

def split_number_parts(number):
    """Split a number into its integer and decimal parts.
    
    Args:
        number: The number to split
        
    Returns:
        tuple: (integer_part, decimal_part)
    """
    # Get integer part
    int_part = int(number)
    
    # Get decimal part with 2 decimal places
    formatted = f"{number:.2f}"
    _, dec_str = formatted.split('.')
    decimal_part = int(dec_str)
    
    return int_part, decimal_part

def format_number_pt(number, show_decimals=True, currency_symbol="€"):
    """Format number in Portuguese style.
    
    Args:
        number: The number to format
        show_decimals: If True, show 2 decimal places; if False, show only integer part
        currency_symbol: Currency symbol to append (empty string for no symbol)
        
    Returns:
        Formatted string (e.g., "1.234,56 €" or "1.234")
    """
    
    int_part, dec_part = split_number_parts(number)
    
    # Add thousands separator to integer part
    int_part_with_sep = ''
    for i, digit in enumerate(reversed(str(int_part))):
        if i > 0 and i % 3 == 0:
            int_part_with_sep = '.' + int_part_with_sep
        int_part_with_sep = digit + int_part_with_sep
    
    # Combine with decimal part if needed
    if show_decimals:
        result = f"{int_part_with_sep},{dec_part:02d}"
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
        # Get integer and decimal parts using utility function
        int_part, decimal_part = split_number_parts(number)
        
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


def process_total_cost(qty, cost_per_unit):
    """Calculate the total cost from quantity and cost per unit.
    
    Args:
        qty: The quantity (must be numeric)
        cost_per_unit: The cost per unit (must be numeric)
        
    Returns:
        The total cost precisely rounded to 2 decimal places
        
    Raises:
        TypeError: If either qty or cost_per_unit is not numeric
    """
    # Validate inputs
    if not isinstance(qty, (int, float)) or not isinstance(cost_per_unit, (int, float)):
        raise TypeError("Both quantity and cost_per_unit must be numeric values")
    
    # Calculate total cost
    total_cost = qty * cost_per_unit
    
    # Use to_number for consistent rounding
    return to_number(total_cost)

def to_number(variable):
    """Convert variables to numbers with precise decimal handling.
    
    Uses Decimal for precise arithmetic to avoid floating point precision issues.
    
    Args:
        variable: The value to convert to a number
        
    Returns:
        The value as a float, precisely rounded to 2 decimal places
        
    Raises:
        ValueError: If the input is infinity (positive or negative)
    """
    # Check for infinity values
    if isinstance(variable, float) and (variable == float('inf') or variable == float('-inf')):
        raise ValueError("Cannot convert infinity values to numbers")
    
    # Convert to Decimal for precise arithmetic
    decimal_value = Decimal(str(variable))
    
    # Round to 2 decimal places using ROUND_HALF_UP
    rounded_value = decimal_value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    # Convert back to float for compatibility
    return float(rounded_value)

def process_date(variables):
    """Process the date variable, formatting it in Portuguese style."""
    now = datetime.now()
    month_name = get_portuguese_month(now.month)
    variables['date'] = f"{month_name} de {now.year}"
    return variables

def process_costs_and_dates(variables):
    """
    Process cost-related variables, calculating total cost and formatting
    monetary values appropriately.
    
    Args:
        variables: Dictionary containing variable values, including 'qty' and 'cost_per_unit'
        
    Returns:
        Updated variables dictionary with calculated total cost and formatted values
    """
    # Make a copy of the variables to avoid modifying the original
    variables = variables.copy()
    
    # Get date in Portuguese style
    variables = process_date(variables)
    
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
    
    return variables