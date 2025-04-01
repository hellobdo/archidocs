import os
import sys
import shutil
import unittest
import subprocess
import zipfile
import tempfile
from pathlib import Path

# Add project root to path to ensure imports work properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.connector.wrapper import create_zip_from_files
from tests._utils.test_utils import BaseTestCase, print_summary

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
