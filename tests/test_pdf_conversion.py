import os
import sys
import shutil
import unittest
import subprocess
from pathlib import Path

# Add project root to path to ensure imports work properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.document_service import convert_docx_to_pdf
from tests._utils.test_utils import BaseTestCase, print_summary

class TestPDFConversion(BaseTestCase):
    """Tests for the PDF conversion functionality."""

    def setUp(self):
        super().setUp()
        # Create test output directory if it doesn't exist
        self.test_output_dir = os.path.join(os.getcwd(), 'test_outputs')
        os.makedirs(self.test_output_dir, exist_ok=True)
        
        # Find a suitable test DOCX file
        self.test_docx = self._find_test_docx()
        
        # If a suitable test file is found, copy it to our test directory
        if self.test_docx:
            self.test_docx_copy = os.path.join(self.test_output_dir, 'test_document.docx')
            shutil.copy2(self.test_docx, self.test_docx_copy)
        
    def tearDown(self):
        # Clean up any created PDF files after tests
        test_pdf = None
        if hasattr(self, 'test_docx_copy'):
            test_pdf = self.test_docx_copy.replace('.docx', '.pdf')
            
        if test_pdf and os.path.exists(test_pdf):
            try:
                os.remove(test_pdf)
                print(f"Removed test PDF: {test_pdf}")
            except Exception as e:
                print(f"Warning: Could not remove test PDF: {str(e)}")
        
        # Clean up the test DOCX copy
        if hasattr(self, 'test_docx_copy') and os.path.exists(self.test_docx_copy):
            try:
                os.remove(self.test_docx_copy)
                print(f"Removed test DOCX copy: {self.test_docx_copy}")
            except Exception as e:
                print(f"Warning: Could not remove test DOCX copy: {str(e)}")
                
        # Remove test output directory if it's empty
        try:
            if os.path.exists(self.test_output_dir) and not os.listdir(self.test_output_dir):
                os.rmdir(self.test_output_dir)
                print(f"Removed test output directory: {self.test_output_dir}")
        except Exception as e:
            print(f"Warning: Could not remove test output directory: {str(e)}")
            
        super().tearDown()
        
    def _find_test_docx(self):
        """Find a suitable DOCX file for testing."""
        # First check the outputs directory
        outputs_dir = os.path.join(os.getcwd(), 'outputs')
        if os.path.exists(outputs_dir):
            for file in os.listdir(outputs_dir):
                if file.endswith('.docx'):
                    return os.path.join(outputs_dir, file)
                    
        # If no file found in outputs, check templates directory
        templates_dir = os.path.join(os.getcwd(), 'backend', 'templates', 'files')
        if os.path.exists(templates_dir):
            for file in os.listdir(templates_dir):
                if file.endswith('.docx'):
                    return os.path.join(templates_dir, file)
        
        # If still no file found, create a simple test document
        if not os.path.exists(outputs_dir):
            os.makedirs(outputs_dir)
        
        test_docx = os.path.join(outputs_dir, 'test_document.docx')
        if not os.path.exists(test_docx):
            try:
                # Create a simple test file
                with open('/tmp/test.txt', 'w') as f:
                    f.write('Test content for PDF conversion')
                
                # Try to convert it to DOCX using LibreOffice
                cmd = [
                    'libreoffice',
                    '--headless',
                    '--convert-to', 'docx',
                    '--outdir', outputs_dir,
                    '/tmp/test.txt'
                ]
                subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Rename the file if needed
                if os.path.exists(os.path.join(outputs_dir, 'test.docx')):
                    os.rename(os.path.join(outputs_dir, 'test.docx'), test_docx)
                
                if os.path.exists(test_docx):
                    return test_docx
            except Exception as e:
                print(f"Error creating test document: {str(e)}")
                
        # Return None if no suitable file is found
        return None
        
    def test_conversion_valid_file(self):
        """Test conversion with a valid DOCX file."""
        # Skip if no valid test file was found
        if not hasattr(self, 'test_docx_copy') or not os.path.exists(self.test_docx_copy):
            self.skipTest("No valid DOCX test file found")
            
        # Capture stdout to see debug messages
        original_stdout = self.capture_stdout()
        
        try:
            # Execute the conversion
            print(f"\nTesting conversion of valid file: {self.test_docx_copy}")
            pdf_path = convert_docx_to_pdf(self.test_docx_copy)
            
            # Check that PDF was created
            self.assertIsNotNone(pdf_path, "PDF path should not be None")
            self.assertTrue(os.path.exists(pdf_path), "PDF file should exist")
            self.assertTrue(os.path.getsize(pdf_path) > 0, "PDF file should not be empty")
            
            self.log_case_result("Valid file conversion", True)
            
        except Exception as e:
            print(f"Error in test_conversion_valid_file: {str(e)}")
            import traceback
            traceback.print_exc()
            self.log_case_result("Valid file conversion", False)
            self.fail(f"Unexpected error: {str(e)}")
        finally:
            self.restore_stdout(original_stdout)
            
    def test_conversion_nonexistent_file(self):
        """Test conversion with a file that doesn't exist."""
        # Use a non-existent file path
        non_existent_path = os.path.join(self.test_output_dir, 'does_not_exist.docx')
        
        # Capture stdout to see debug messages
        original_stdout = self.capture_stdout()
        
        try:
            # Execute the conversion
            print(f"\nTesting conversion of non-existent file: {non_existent_path}")
            pdf_path = convert_docx_to_pdf(non_existent_path)
            
            # Conversion should fail gracefully
            self.assertIsNone(pdf_path, "PDF path should be None for non-existent file")
            
            self.log_case_result("Non-existent file handling", True)
            
        except Exception as e:
            print(f"Error in test_conversion_nonexistent_file: {str(e)}")
            import traceback
            traceback.print_exc()
            self.log_case_result("Non-existent file handling", False)
            self.fail(f"Unexpected error: {str(e)}")
        finally:
            self.restore_stdout(original_stdout)
    
    def test_libreoffice_installed(self):
        """Test that LibreOffice is properly installed."""
        original_stdout = self.capture_stdout()
        
        try:
            # Try to run LibreOffice to check its version
            process = subprocess.run(
                ['libreoffice', '--version'], 
                check=False,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            
            print(f"LibreOffice version check output: {process.stdout}")
            if process.stderr:
                print(f"LibreOffice version check errors: {process.stderr}")
            
            # Check if we got some output indicating LibreOffice is installed
            self.assertTrue(process.returncode == 0 or 'LibreOffice' in process.stdout, 
                           "LibreOffice should be installed and return a version string")
            
            self.log_case_result("LibreOffice installation", True)
            
        except Exception as e:
            print(f"Error checking LibreOffice: {str(e)}")
            import traceback
            traceback.print_exc()
            self.log_case_result("LibreOffice installation", False)
            self.fail(f"Error checking LibreOffice: {str(e)}")
        finally:
            self.restore_stdout(original_stdout)

if __name__ == "__main__":
    # Run tests
    unittest.main(exit=False)
    
    # Print summary
    print_summary()
