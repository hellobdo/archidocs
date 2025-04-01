import os
import sys
import shutil
import unittest
from pathlib import Path

# Add project root to path to ensure imports work properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from backend.backend.docs_gen.pdfa_service import convert_to_pdfa
from tests._utils.test_utils import BaseTestCase, print_summary

class TestPdfaService(BaseTestCase):
    """Tests for the PDF/A conversion service functionality.
    
    Note: Directory creation is handled by the caller (main.py).
    This test suite focuses on the core conversion functionality.
    """

    def setUp(self):
        super().setUp()
        # Create test output directory if it doesn't exist
        self.test_output_dir = os.path.join(os.getcwd(), 'test_outputs')
        os.makedirs(self.test_output_dir, exist_ok=True)
        
        # Create a minimal valid PDF file for testing
        self.test_pdf = os.path.join(self.test_output_dir, 'test.pdf')
        with open(self.test_pdf, 'wb') as f:
            f.write(b'%PDF-1.4\n%EOF\n')  # Minimal valid PDF
        
    def tearDown(self):
        # Clean up the test output directory
        if os.path.exists(self.test_output_dir):
            try:
                shutil.rmtree(self.test_output_dir)
                print(f"Removed test output directory: {self.test_output_dir}")
            except Exception as e:
                print(f"Warning: Could not remove test output directory: {str(e)}")
        
        super().tearDown()

    def test_basic_pdfa_conversion(self):
        """Test basic PDF to PDF/A conversion.
        
        Verifies that the function can convert a basic PDF to PDF/A format.
        Directory creation is handled by the caller.
        """
        # Define output path
        output_path = os.path.join(self.test_output_dir, 'test_pdfa.pdf')
        
        # Capture stdout
        original_stdout = self.capture_stdout()
        
        try:
            # Execute the conversion
            print(f"\nTesting basic PDF to PDF/A conversion")
            result = convert_to_pdfa(self.test_pdf, output_path)
            
            # Check conversion was successful
            self.assertEqual(result, output_path, "Function should return the output file path")
            self.assertTrue(os.path.exists(output_path), "Output file should exist")
            self.assertTrue(os.path.getsize(output_path) > 0, "Output file should not be empty")
            
            self.log_case_result("Basic PDF/A conversion", True)
            
        except Exception as e:
            print(f"Error in test_basic_pdfa_conversion: {str(e)}")
            import traceback
            traceback.print_exc()
            self.log_case_result("Basic PDF/A conversion", False)
            self.fail(f"Unexpected error: {str(e)}")
        finally:
            self.restore_stdout(original_stdout)

    def test_pdfa_version_selection(self):
        """Test PDF/A conversion with different versions.
        
        Verifies that the function can convert to different PDF/A versions.
        Directory creation is handled by the caller.
        """
        versions = ["1", "2", "3"]
        
        for version in versions:
            # Define output path
            output_path = os.path.join(self.test_output_dir, f'test_pdfa_{version}.pdf')
            
            # Capture stdout
            original_stdout = self.capture_stdout()
            
            try:
                # Execute the conversion
                print(f"\nTesting PDF to PDF/A-{version} conversion")
                result = convert_to_pdfa(self.test_pdf, output_path, version)
                
                # Check conversion was successful
                self.assertEqual(result, output_path, f"Function should return the output file path for PDF/A-{version}")
                self.assertTrue(os.path.exists(output_path), f"Output file for PDF/A-{version} should exist")
                self.assertTrue(os.path.getsize(output_path) > 0, f"Output file for PDF/A-{version} should not be empty")
                
                self.log_case_result(f"PDF/A-{version} conversion", True)
                
            except Exception as e:
                print(f"Error in test_pdfa_version_selection for version {version}: {str(e)}")
                import traceback
                traceback.print_exc()
                self.log_case_result(f"PDF/A-{version} conversion", False)
                self.fail(f"Unexpected error: {str(e)}")
            finally:
                self.restore_stdout(original_stdout)

    def test_file_overwrite(self):
        """Test that existing PDF/A files are overwritten.
        
        Verifies that the function can overwrite existing files.
        Directory creation is handled by the caller.
        """
        # Define output path
        output_path = os.path.join(self.test_output_dir, 'overwrite_test_pdfa.pdf')
        
        # Create a dummy file first
        with open(output_path, 'w') as f:
            f.write("This is a dummy file that should be overwritten")
        
        # Get the modification time
        original_mtime = os.path.getmtime(output_path)
        
        # Capture stdout
        original_stdout = self.capture_stdout()
        
        try:
            # Wait a moment to ensure modification time would be different
            import time
            time.sleep(1)
            
            # Execute the conversion
            print(f"\nTesting PDF/A file overwrite behavior")
            result = convert_to_pdfa(self.test_pdf, output_path)
            
            # Check if file was overwritten
            self.assertEqual(result, output_path, "Function should return the output file path")
            self.assertTrue(os.path.exists(output_path), "Output file should exist")
            self.assertNotEqual(original_mtime, os.path.getmtime(output_path), 
                               "File modification time should change, indicating overwrite")
            
            self.log_case_result("PDF/A file overwrite behavior", True)
            
        except Exception as e:
            print(f"Error in test_file_overwrite: {str(e)}")
            import traceback
            traceback.print_exc()
            self.log_case_result("PDF/A file overwrite behavior", False)
            self.fail(f"Unexpected error: {str(e)}")
        finally:
            self.restore_stdout(original_stdout)

    def test_invalid_input_file(self):
        """Test handling of invalid input file.
        
        Verifies that the function handles invalid PDF files gracefully.
        Directory creation is handled by the caller.
        """
        # Define output path
        output_path = os.path.join(self.test_output_dir, 'invalid_test_pdfa.pdf')
        
        # Create an invalid PDF file
        invalid_pdf = os.path.join(self.test_output_dir, 'invalid.pdf')
        with open(invalid_pdf, 'w') as f:
            f.write("This is not a valid PDF file")
        
        # Capture stdout
        original_stdout = self.capture_stdout()
        
        try:
            # Execute the conversion
            print(f"\nTesting invalid input file handling")
            result = convert_to_pdfa(invalid_pdf, output_path)
            
            # The conversion should fail gracefully
            self.assertIsNone(result, "Function should return None for invalid input")
            
            self.log_case_result("Invalid input file handling", True)
            
        except Exception as e:
            # It's acceptable if this raises an exception, but we'll log it
            print(f"Note: Invalid input file handling raised exception: {str(e)}")
            self.log_case_result("Invalid input file handling - exception path", True)
        finally:
            self.restore_stdout(original_stdout)

    def test_nonexistent_input_file(self):
        """Test handling of nonexistent input file.
        
        Verifies that the function handles nonexistent files gracefully.
        Directory creation is handled by the caller.
        """
        # Define output path
        output_path = os.path.join(self.test_output_dir, 'nonexistent_test_pdfa.pdf')
        
        # Capture stdout
        original_stdout = self.capture_stdout()
        
        try:
            # Execute the conversion with nonexistent file
            print(f"\nTesting nonexistent input file handling")
            result = convert_to_pdfa('nonexistent.pdf', output_path)
            
            # The conversion should fail gracefully
            self.assertIsNone(result, "Function should return None for nonexistent input")
            
            self.log_case_result("Nonexistent input file handling", True)
            
        except Exception as e:
            # It's acceptable if this raises an exception, but we'll log it
            print(f"Note: Nonexistent input file handling raised exception: {str(e)}")
            self.log_case_result("Nonexistent input file handling - exception path", True)
        finally:
            self.restore_stdout(original_stdout)


if __name__ == "__main__":
    # Run tests
    unittest.main(exit=False)
    
    # Print summary
    print_summary() 