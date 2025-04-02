import os
import subprocess
import shutil

def convert_docx_to_pdf(docx_path: str) -> str:
    """
    Convert a DOCX document to PDF format using LibreOffice in headless mode.
    
    Args:
        docx_path: Path to the DOCX document
        
    Returns:
        Path to the generated PDF file or None if conversion failed
    """
    
    try:
        # Check if the source file exists
        if not os.path.exists(docx_path):
            print(f"Error: Source DOCX file not found: {docx_path}")
            return None
            
        # Generate the output PDF path by replacing .docx with .pdf
        pdf_path = docx_path.replace(".docx", ".pdf")
        
        # Ensure output directory exists
        pdf_dir = os.path.dirname(pdf_path)
        if pdf_dir and not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)
        
        print(f"Converting {docx_path} to {pdf_path}")
        print(f"Source file size: {os.path.getsize(docx_path)} bytes")
        
        # Check if LibreOffice is available
        try:
            # Try to find LibreOffice executable
            libreoffice_paths = [
                "libreoffice",  # Linux/Mac standard path
                "/usr/bin/libreoffice",  # Linux common location
                "/Applications/LibreOffice.app/Contents/MacOS/soffice",  # macOS
                "soffice"  # Alternative command name
            ]
            
            libreoffice_cmd = None
            for path in libreoffice_paths:
                try:
                    # Check if command exists
                    subprocess.run([path, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                    libreoffice_cmd = path
                    print(f"Found LibreOffice at: {path}")
                    break
                except (subprocess.SubprocessError, FileNotFoundError):
                    continue
            
            if not libreoffice_cmd:
                print("LibreOffice not found in expected locations")
                # In Docker container the path might be different, try anyway with default
                libreoffice_cmd = "libreoffice"
            
            # Get absolute paths for conversion
            docx_abs_path = os.path.abspath(docx_path)
            output_dir = os.path.dirname(os.path.abspath(pdf_path))
            
            # Run LibreOffice in headless mode for standard PDF conversion
            cmd = [
                libreoffice_cmd,
                "--headless",
                "--convert-to", "pdf",
                "--outdir", output_dir,
                docx_abs_path
            ]
            
            print(f"Running LibreOffice PDF conversion command: {' '.join(cmd)}")
            process = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            
            print(f"Command output: {process.stdout}")
            if process.stderr:
                print(f"Command errors: {process.stderr}")
            
            # Check if the PDF was created
            if os.path.exists(pdf_path):
                file_size = os.path.getsize(pdf_path)
                print(f"PDF created at: {pdf_path} with size: {file_size} bytes")
                
                if file_size > 0:
                    print(f"PDF successfully created at: {pdf_path}")
                    return pdf_path
                else:
                    print(f"Error: PDF file was created but is empty (0 bytes): {pdf_path}")
                    return None
            else:
                print(f"Error: PDF file was not created at expected location: {pdf_path}")
                
                # There may be a case where LibreOffice created the PDF with a different name
                # Try to find it in the output directory
                base_name = os.path.splitext(os.path.basename(docx_path))[0]
                for file in os.listdir(output_dir):
                    if file.startswith(base_name) and file.endswith(".pdf"):
                        found_pdf = os.path.join(output_dir, file)
                        print(f"Found PDF with different name: {found_pdf}")
                        # Copy to expected location
                        shutil.copy2(found_pdf, pdf_path)
                        return pdf_path
                        
                return None
                
        except Exception as lo_e:
            print(f"Error running LibreOffice: {str(lo_e)}")
            import traceback
            traceback.print_exc()
            return None
            
    except Exception as e:
        print(f"Error converting DOCX to PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

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
    
def pdfa_service(docx_path: str) -> str:
    """
    Main function to handle DOCX to PDF/A conversion.
    
    Args:
        docx_path: Path to the input DOCX file
        
    Returns:
        str: Path to the generated PDF/A file if successful, None otherwise
    """
    print("Starting DOCX to PDF/A conversion service...")
    
    # Step 1: Convert DOCX to standard PDF
    pdf_path = convert_docx_to_pdf(docx_path)
    if not pdf_path:
        print("Failed to convert DOCX to PDF. Aborting PDF/A conversion.")
        return None
    
    # Step 2: Convert standard PDF to PDF/A
    pdfa_path = pdf_path.replace(".pdf", "_pdfa.pdf")
    pdfa_result = convert_to_pdfa(pdf_path, pdfa_path)
    
    if pdfa_result:
        print(f"Successfully converted {docx_path} to PDF/A: {pdfa_result}")
        return pdfa_result
    else:
        print(f"PDF/A conversion failed. Standard PDF is available at: {pdf_path}")
        return pdf_path