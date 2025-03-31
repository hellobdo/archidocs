"""
Document generation module for creating DOCX and PDF documents from HTML templates.
"""

from .html_converter import (
    convert_html_to_docx,
    convert_html_to_pdf
)
from .pdfa_service import convert_to_pdfa

__all__ = [
    # HTML to DOCX conversion
    'convert_html_to_docx',
    
    # HTML to PDF conversion
    'convert_html_to_pdf',
    
    # PDF/A conversion
    'convert_to_pdfa',
]
