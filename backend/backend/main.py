import os
import sys
from typing import Dict, Tuple, Any, Optional

from backend.backend.docs_gen import (
    convert_html_to_docx,
    convert_html_to_pdf,
    convert_to_pdfa
)
from backend.backend.utils import (
    process_costs_and_dates,
    render_html_template
)

def generate_document(template_name: str, variables: Dict[str, Any], output_path: str, generate_pdfa: bool = True) -> Dict[str, str]:
    """
    Generate document(s) from template. Can generate both DOCX and PDF/A if requested.
    
    Args:
        template_name: Template to use
        variables: Template variables
        output_path: Where to save the document
        generate_pdfa: If True and output is DOCX, also generates PDF/A
    Returns:
        Dict with paths to generated files: {'docx': path, 'pdfa': path}
    Raises:
        ValueError: If format is not supported
        RuntimeError: If document generation fails
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    html_content = render_html_template(template_name, process_costs_and_dates(variables))
    
    _, ext = os.path.splitext(output_path)
    if ext.lower() not in ['.docx', '.pdfa']:
        raise ValueError(f"Unsupported format: {ext}")
    
    result = {}
        
    if ext.lower() == '.docx':
        if not convert_html_to_docx(html_content, output_path):
            raise RuntimeError(f"Failed to create DOCX: {output_path}")
        result['docx'] = output_path
        
        if not generate_pdfa:
            return result
            
        # Generate PDF/A alongside DOCX
        pdfa_path = output_path.replace('.docx', '.pdfa')
        temp_pdf = output_path.replace('.docx', '.pdf')
        
    else:  # .pdfa
        pdfa_path = output_path
        temp_pdf = output_path.replace('.pdfa', '.pdf')
    
    # Generate PDF/A (either standalone or alongside DOCX)
    if not convert_html_to_pdf(html_content, temp_pdf):
        raise RuntimeError(f"Failed to create temporary PDF: {temp_pdf}")
        
    if not convert_to_pdfa(temp_pdf, pdfa_path):
        os.remove(temp_pdf)
        raise RuntimeError(f"Failed to create PDF/A: {pdfa_path}")
        
    os.remove(temp_pdf)
    result['pdfa'] = pdfa_path
    
    return result