"""
Utility functions for the document generation system.
"""

# Import and expose functions from loading module
from .utils import (
    load_variables,
    get_available_templates,
    render_html_template,
    create_zip_from_files
)

# Import only the main function from numbers_and_dates module
from .numbers_and_dates import process_costs_and_dates

__all__ = [
    # From numbers_and_dates
    'process_costs_and_dates',
    
    # From loading
    'load_variables',
    'get_available_templates',
    'render_html_template',
    'create_zip_from_files'
]
