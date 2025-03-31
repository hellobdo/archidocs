#!/usr/bin/env python3
"""
PDF/A Conversion Service - Converts standard PDFs to PDF/A format using Ghostscript.
"""
import os
import sys
import subprocess

def convert_to_pdfa(input_pdf, output_pdfa, pdfa_version="1"):
    """
    Convert a standard PDF to PDF/A using Ghostscript.
    
    Args:
        input_pdf: Path to the input PDF file
        output_pdfa: Path to the output PDF/A file
        pdfa_version: PDF/A version (1, 2, or 3)
        
    Returns:
        True if conversion was successful, False otherwise
    """
    print(f"Converting {input_pdf} to PDF/A-{pdfa_version}...")
    
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_pdfa)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Simplified Ghostscript command for PDF/A conversion
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
            return True
        else:
            print(f"Failed to create PDF/A-{pdfa_version} file.")
            print(f"Error: {process.stderr}")
            print(f"Command: {' '.join(cmd)}")
            
            # Try a different approach if the first one failed
            print("Trying alternative PDF/A conversion approach...")
            alt_cmd = [
                'gs',
                '-dPDFA',
                '-dBATCH',
                '-dNOPAUSE',
                '-dSAFER',
                '-sDEVICE=pdfwrite',
                '-sOutputFile=' + output_pdfa,
                input_pdf
            ]
            
            alt_process = subprocess.run(
                alt_cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            
            if alt_process.returncode == 0 and os.path.exists(output_pdfa):
                print(f"PDF/A file created using alternative approach at: {output_pdfa}")
                return True
            else:
                print(f"Alternative approach also failed. Error: {alt_process.stderr}")
                return False
            
    except Exception as e:
        print(f"Error during PDF/A conversion: {str(e)}")
        return False

def main():
    """Command line interface for PDF/A conversion."""
    if len(sys.argv) < 3:
        print("Usage: python pdfa_service.py <input_pdf> <output_pdfa> [pdfa_version]")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    output_pdfa = sys.argv[2]
    pdfa_version = sys.argv[3] if len(sys.argv) > 3 else "1"
    
    # Check if Ghostscript is installed and working
    try:
        version_output = subprocess.run(['gs', '--version'], capture_output=True, text=True, check=True)
        print(f"Ghostscript version: {version_output.stdout.strip()}")
    except Exception as e:
        print(f"Error checking Ghostscript: {str(e)}")
        sys.exit(1)
    
    # Convert the PDF to PDF/A
    success = convert_to_pdfa(input_pdf, output_pdfa, pdfa_version)
    
    if success:
        print("PDF/A conversion completed successfully!")
        sys.exit(0)
    else:
        print("PDF/A conversion failed.")
        sys.exit(1)

if __name__ == "__main__":
    main() 