#!/usr/bin/env python3
"""
Documents Generation Engine - A script to generate documents from HTML templates.
"""
import os
from jinja2 import Environment, FileSystemLoader
from htmldocx import HtmlToDocx
import weasyprint
import sys

def convert_html_to_docx(html_content, output_path):
    """Convert HTML content to DOCX."""
    # Create the output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Convert HTML to DOCX using HTMLToDocx
    parser = HtmlToDocx()
    docx = parser.parse_html_string(html_content)
    docx.save(output_path)
    
    if os.path.exists(output_path):
        print(f"DOCX file created at: {output_path}")
        return True
    else:
        print(f"Failed to create DOCX file at: {output_path}")
        return False

def convert_html_to_pdf(html_content, output_path):
    """Convert HTML content to PDF."""
    # Create the output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Convert HTML to PDF using WeasyPrint
    html = weasyprint.HTML(string=html_content)
    pdf = html.write_pdf()
    
    # Write the PDF to file
    with open(output_path, 'wb') as f:
        f.write(pdf)
    
    if os.path.exists(output_path):
        print(f"PDF file created at: {output_path}")
        return True
    else:
        print(f"Failed to create PDF file at: {output_path}")
        return False