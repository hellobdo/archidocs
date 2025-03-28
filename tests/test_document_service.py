import os
import sys
import shutil
import unittest
import subprocess
import zipfile
import tempfile
from pathlib import Path

# Add project root to path to ensure imports work properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.document_service import convert_docx_to_pdf, create_zip_from_files
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

class TestZipCreation(BaseTestCase):
    """Tests for the ZIP file creation functionality."""

    def setUp(self):
        super().setUp()
        # Create test output directory if it doesn't exist
        self.test_output_dir = os.path.join(os.getcwd(), 'test_outputs')
        os.makedirs(self.test_output_dir, exist_ok=True)
        
        # Create some test files
        self.test_files = []
        for i in range(3):
            test_file = os.path.join(self.test_output_dir, f'test_file_{i}.txt')
            with open(test_file, 'w') as f:
                f.write(f'Test content for file {i}')
            self.test_files.append(test_file)
        
    def tearDown(self):
        # Clean up test files
        for file_path in self.test_files:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Warning: Could not remove test file: {str(e)}")
        
        # Clean up zip file if created
        zip_path = os.path.join(self.test_output_dir, 'test_archive.zip')
        if os.path.exists(zip_path):
            try:
                os.remove(zip_path)
                print(f"Removed test ZIP: {zip_path}")
            except Exception as e:
                print(f"Warning: Could not remove test ZIP: {str(e)}")
        
        # Remove test output directory if it's empty
        try:
            if os.path.exists(self.test_output_dir) and not os.listdir(self.test_output_dir):
                os.rmdir(self.test_output_dir)
                print(f"Removed test output directory: {self.test_output_dir}")
        except Exception as e:
            print(f"Warning: Could not remove test output directory: {str(e)}")
            
        super().tearDown()
    
    def test_create_zip_from_valid_files(self):
        """Test creating a ZIP from valid files."""
        # Define output path for the ZIP
        zip_path = os.path.join(self.test_output_dir, 'test_archive.zip')
        
        # Capture stdout to see debug messages
        original_stdout = self.capture_stdout()
        
        try:
            # Execute the ZIP creation
            print(f"\nTesting ZIP creation with valid files")
            result_path = create_zip_from_files(self.test_files, zip_path)
            
            # Check that ZIP was created
            self.assertIsNotNone(result_path, "ZIP path should not be None")
            self.assertTrue(os.path.exists(zip_path), "ZIP file should exist")
            self.assertTrue(os.path.getsize(zip_path) > 0, "ZIP file should not be empty")
            
            # Verify ZIP contents
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                
                # Check if all test files are in the ZIP
                for test_file in self.test_files:
                    filename = os.path.basename(test_file)
                    self.assertIn(filename, file_list, f"File {filename} should be in the ZIP")
            
            self.log_case_result("Valid files ZIP creation", True)
            
        except Exception as e:
            print(f"Error in test_create_zip_from_valid_files: {str(e)}")
            import traceback
            traceback.print_exc()
            self.log_case_result("Valid files ZIP creation", False)
            self.fail(f"Unexpected error: {str(e)}")
        finally:
            self.restore_stdout(original_stdout)
    
    def test_create_zip_with_nonexistent_files(self):
        """Test creating a ZIP with some non-existent files."""
        # Define output path for the ZIP
        zip_path = os.path.join(self.test_output_dir, 'test_archive.zip')
        
        # Create a list with valid and non-existent files
        mixed_files = self.test_files.copy()
        mixed_files.append(os.path.join(self.test_output_dir, 'nonexistent_file.txt'))
        
        # Capture stdout to see debug messages
        original_stdout = self.capture_stdout()
        
        try:
            # Execute the ZIP creation
            print(f"\nTesting ZIP creation with mixed files (valid and non-existent)")
            result_path = create_zip_from_files(mixed_files, zip_path)
            
            # Check that ZIP was created despite some missing files
            self.assertIsNotNone(result_path, "ZIP path should not be None")
            self.assertTrue(os.path.exists(zip_path), "ZIP file should exist")
            self.assertTrue(os.path.getsize(zip_path) > 0, "ZIP file should not be empty")
            
            # Verify ZIP contents - should only include valid files
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                
                # Check if only valid test files are in the ZIP
                for test_file in self.test_files:
                    filename = os.path.basename(test_file)
                    self.assertIn(filename, file_list, f"File {filename} should be in the ZIP")
                
                # Non-existent file should not be in the ZIP
                self.assertNotIn('nonexistent_file.txt', file_list, "Non-existent file should not be in the ZIP")
            
            self.log_case_result("Mixed files ZIP creation", True)
            
        except Exception as e:
            print(f"Error in test_create_zip_with_nonexistent_files: {str(e)}")
            import traceback
            traceback.print_exc()
            self.log_case_result("Mixed files ZIP creation", False)
            self.fail(f"Unexpected error: {str(e)}")
        finally:
            self.restore_stdout(original_stdout)
    
    def test_create_zip_with_all_nonexistent_files(self):
        """Test creating a ZIP with only non-existent files."""
        # Define output path for the ZIP
        zip_path = os.path.join(self.test_output_dir, 'test_archive.zip')
        
        # List of non-existent files
        nonexistent_files = [
            os.path.join(self.test_output_dir, 'nonexistent_file1.txt'),
            os.path.join(self.test_output_dir, 'nonexistent_file2.txt')
        ]
        
        # Capture stdout to see debug messages
        original_stdout = self.capture_stdout()
        
        try:
            # Execute the ZIP creation
            print(f"\nTesting ZIP creation with only non-existent files")
            result_path = create_zip_from_files(nonexistent_files, zip_path)
            
            # ZIP should not be created if all files are invalid
            self.assertIsNone(result_path, "ZIP path should be None when all files are invalid")
            self.assertFalse(os.path.exists(zip_path), "ZIP file should not exist when all files are invalid")
            
            self.log_case_result("All non-existent files ZIP handling", True)
            
        except Exception as e:
            print(f"Error in test_create_zip_with_all_nonexistent_files: {str(e)}")
            import traceback
            traceback.print_exc()
            self.log_case_result("All non-existent files ZIP handling", False)
            self.fail(f"Unexpected error: {str(e)}")
        finally:
            self.restore_stdout(original_stdout)
    
    def test_create_zip_with_empty_file_list(self):
        """Test creating a ZIP with an empty list of files."""
        # Define output path for the ZIP
        zip_path = os.path.join(self.test_output_dir, 'test_archive.zip')
        
        # Capture stdout to see debug messages
        original_stdout = self.capture_stdout()
        
        try:
            # Execute the ZIP creation with empty list
            print(f"\nTesting ZIP creation with empty file list")
            result_path = create_zip_from_files([], zip_path)
            
            # ZIP should not be created if no files are provided
            self.assertIsNone(result_path, "ZIP path should be None when no files are provided")
            self.assertFalse(os.path.exists(zip_path), "ZIP file should not exist when no files are provided")
            
            self.log_case_result("Empty file list ZIP handling", True)
            
        except Exception as e:
            print(f"Error in test_create_zip_with_empty_file_list: {str(e)}")
            import traceback
            traceback.print_exc()
            self.log_case_result("Empty file list ZIP handling", False)
            self.fail(f"Unexpected error: {str(e)}")
        finally:
            self.restore_stdout(original_stdout)
    
    def test_create_zip_in_outputs_directory(self):
        """Test creating a ZIP file directly in the outputs directory."""
        # Define output path for the ZIP in outputs directory
        outputs_dir = os.path.join(os.getcwd(), 'outputs')
        os.makedirs(outputs_dir, exist_ok=True)
        zip_path = os.path.join(outputs_dir, 'test_outputs_directory.zip')
        
        # Ensure the zip file doesn't exist before the test
        if os.path.exists(zip_path):
            os.remove(zip_path)
        
        # Capture stdout to see debug messages
        original_stdout = self.capture_stdout()
        
        try:
            # Execute the ZIP creation
            print(f"\nTesting ZIP creation directly in outputs directory")
            result_path = create_zip_from_files(self.test_files, zip_path)
            
            # Check that ZIP was created in the outputs directory
            self.assertIsNotNone(result_path, "ZIP path should not be None")
            self.assertTrue(os.path.exists(zip_path), "ZIP file should exist in outputs directory")
            self.assertTrue(os.path.getsize(zip_path) > 0, "ZIP file should not be empty")
            
            # Verify ZIP contents
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                
                # Check if all test files are in the ZIP
                for test_file in self.test_files:
                    filename = os.path.basename(test_file)
                    self.assertIn(filename, file_list, f"File {filename} should be in the ZIP")
            
            self.log_case_result("ZIP creation in outputs directory", True)
            
        except Exception as e:
            print(f"Error in test_create_zip_in_outputs_directory: {str(e)}")
            import traceback
            traceback.print_exc()
            self.log_case_result("ZIP creation in outputs directory", False)
            self.fail(f"Unexpected error: {str(e)}")
        finally:
            self.restore_stdout(original_stdout)
            
            # Clean up the ZIP file in outputs
            if os.path.exists(zip_path):
                try:
                    os.remove(zip_path)
                    print(f"Removed test ZIP from outputs: {zip_path}")
                except Exception as e:
                    print(f"Warning: Could not remove test ZIP from outputs: {str(e)}")

if __name__ == "__main__":
    # Run tests
    unittest.main(exit=False)
    
    # Print summary
    print_summary()
