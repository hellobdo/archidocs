#!/usr/bin/env python3
"""
Documents Generation Engine - A script to generate documents from HTML templates.
"""
import os
from jinja2 import Environment, FileSystemLoader
from htmldocx import HtmlToDocx
import weasyprint
import sys
from weasyprint import HTML

def convert_html_to_docx(html_content, output_path):
    """
    Convert HTML content to DOCX format.
    
    Args:
        html_content: HTML content as string
        output_path: Path to save the DOCX file (directory must exist)
        
    Returns:
        str: Path to the generated DOCX file if successful, None otherwise
    """
    try:
        # Convert HTML to DOCX using HtmlToDocx
        parser = HtmlToDocx()
        docx = parser.parse_html_string(html_content)
        docx.save(output_path)
            
        print(f"DOCX file created at: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error converting HTML to DOCX: {str(e)}")
        return None

def convert_html_to_pdf(html_content, output_path):
    """
    Convert HTML content to PDF format.
    
    Args:
        html_content: HTML content as string
        output_path: Path to save the PDF file (directory must exist)
        
    Returns:
        str: Path to the generated PDF file if successful, None otherwise
    """
    try:
        # Convert HTML to PDF using WeasyPrint
        pdf_content = HTML(string=html_content).write_pdf()
        
        # Write the PDF content to file
        with open(output_path, 'wb') as f:
            f.write(pdf_content)
            
        print(f"PDF file created at: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error converting HTML to PDF: {str(e)}")
        return None