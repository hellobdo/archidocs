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
    Generate document(s) from template. Always generates DOCX, and optionally generates PDF/A alongside it.
    
    Args:
        template_name: Template to use
        variables: Template variables
        output_path: Where to save the DOCX document
        generate_pdfa: If True, also generates PDF/A alongside DOCX
    Returns:
        Dict with paths to generated files: {'docx': path} or {'docx': path, 'pdfa': path}
    Raises:
        ValueError: If output_path doesn't end in .docx
        RuntimeError: If document generation fails
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    html_content = render_html_template(template_name, process_costs_and_dates(variables))
    
    _, ext = os.path.splitext(output_path)
    if ext.lower() != '.docx':
        raise ValueError("Output path must end in .docx")
    
    # Always generate DOCX
    docx_path = convert_html_to_docx(html_content, output_path)
    if not docx_path:
        raise RuntimeError(f"Failed to create DOCX: {output_path}")
    
    result = {'docx': docx_path}
    
    if not generate_pdfa:
        return result
        
    # Generate PDF/A alongside DOCX if requested
    pdfa_path = output_path.replace('.docx', '.pdfa')
    temp_pdf = output_path.replace('.docx', '.pdf')
    
    # Generate PDF/A through intermediate PDF
    pdf_path = convert_html_to_pdf(html_content, temp_pdf)
    if not pdf_path:
        raise RuntimeError(f"Failed to create temporary PDF: {temp_pdf}")
        
    pdfa_result = convert_to_pdfa(pdf_path, pdfa_path)
    if os.path.exists(pdf_path):  # Only try to remove if it exists
        os.remove(pdf_path)  # Clean up temporary PDF
    
    if not pdfa_result:
        raise RuntimeError(f"Failed to create PDF/A: {pdfa_path}")
        
    result['pdfa'] = pdfa_result
    
    return result