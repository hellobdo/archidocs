#!/usr/bin/env python3
"""
PDF/A Conversion Service - Converts standard PDFs to PDF/A format using Ghostscript.
"""
import os
import subprocess

def convert_to_pdfa(input_pdf, output_pdfa, pdfa_version="1"):
    """
    Convert a standard PDF to PDF/A using Ghostscript.
    
    Args:
        input_pdf: Path to the input PDF file
        output_pdfa: Path to the output PDF/A file (directory must exist)
        pdfa_version: PDF/A version (1, 2, or 3)
        
    Returns:
        str: Path to the generated PDF/A file if successful, None otherwise
    """
    print(f"Converting {input_pdf} to PDF/A-{pdfa_version}...")
    
    # Ghostscript command for PDF/A conversion
    cmd = [
        'gs',
        f'-dPDFA={pdfa_version}',
        '-dBATCH',
        '-dNOPAUSE',
        '-dPDFACompatibilityPolicy=1',
        '-dPDFSETTINGS=/prepress',
        '-dAutoRotatePages=/None',
        '-sDEVICE=pdfwrite',
        '-sOutputFile=' + output_pdfa,
        input_pdf
    ]
    
    try:
        # Run Ghostscript
        process = subprocess.run(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        
        # Check if the conversion was successful
        if process.returncode == 0 and os.path.exists(output_pdfa):
            print(f"PDF/A-{pdfa_version} file created at: {output_pdfa}")
            print(f"Ghostscript command output: {process.stdout}")
            return output_pdfa
        else:
            print(f"Failed to create PDF/A-{pdfa_version} file.")
            print(f"Error: {process.stderr}")
            print(f"Command: {' '.join(cmd)}")
            return None
            
    except Exception as e:
        print(f"Error during PDF/A conversion: {str(e)}")
        return None 