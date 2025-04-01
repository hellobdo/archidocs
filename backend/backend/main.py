import os
import sys
from typing import Dict, Tuple, Any

from backend.backend.docs_gen import (
    convert_html_to_docx,
    convert_html_to_pdf,
    convert_to_pdfa
)
from backend.backend.utils import (
    process_costs_and_dates,
    load_variables,
    render_html_template
)

def create_documents(template_name: str = "tr_coord") -> Tuple[bool, bool, bool]:
    """
    Create DOCX, PDF and PDF/A documents from a template.
    
    Args:
        template_name: Name of the template to use
        
    Returns:
        Tuple of (docx_success, pdf_success, pdfa_success)
    """
    # Create output directory if it doesn't exist
    os.makedirs('outputs', exist_ok=True)
    
    # Load and process variables
    variables = load_variables()
    processed_variables = process_costs_and_dates(variables)
    
    # Render HTML template
    html_content = render_html_template(template_name, processed_variables)
    
    # Save rendered HTML for inspection
    html_output_path = os.path.join('outputs', f"{template_name}_rendered.html")
    with open(html_output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Rendered HTML saved to: {html_output_path}")
    
    # Convert to DOCX
    docx_output_path = os.path.join('outputs', f"{template_name}_from_html.docx")
    docx_success = convert_html_to_docx(html_content, docx_output_path)
    
    # Convert to PDF (standard)
    pdf_output_path = os.path.join('outputs', f"{template_name}_from_html.pdf")
    pdf_success = convert_html_to_pdf(html_content, pdf_output_path)
    
    # Convert to PDF/A
    pdfa_output_path = os.path.join('outputs', f"{template_name}_from_html_pdfa.pdf")
    pdfa_success = False
    if pdf_success:
        pdfa_success = convert_to_pdfa(pdf_output_path, pdfa_output_path)
    
    return docx_success, pdf_success, pdfa_success


if __name__ == "__main__":
    # Get template name from command line if provided
    template_name = "tr_coord"
    if len(sys.argv) > 1:
        template_name = sys.argv[1]
    
    print(f"Testing HTML template: {template_name}")
    docx, pdf, pdfa = create_documents(template_name)
    
    print("\n--- RESULTS ---")
    print(f"DOCX conversion: {'SUCCESS' if docx else 'FAILED'}")
    print(f"PDF conversion:  {'SUCCESS' if pdf else 'FAILED'}")
    print(f"PDF/A conversion: {'SUCCESS' if pdfa else 'FAILED'}")
    
    if docx and pdf and pdfa:
        print("Test completed successfully!")
    else:
        print("Test completed with errors. Check the outputs directory for details.") 