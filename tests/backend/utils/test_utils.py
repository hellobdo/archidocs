from unittest.mock import patch, MagicMock
import tempfile
from jinja2 import TemplateNotFound, TemplateSyntaxError
import os
import sys
import unittest
import zipfile
import tempfile
from pathlib import Path

# Add project root to path to ensure imports work properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from tests._utils.test_utils import BaseTestCase, print_summary
from backend.backend.utils import get_available_templates, render_html_template, create_zip_from_files


class TestGetAvailableTemplates(BaseTestCase):
    """Test template discovery functionality."""
    
    def test_basic_template_discovery(self):
        """Test basic template discovery functionality."""
        try:
            with patch('os.path.dirname') as mock_dirname, \
                 patch('os.path.abspath') as mock_abspath, \
                 patch('os.listdir') as mock_listdir:
                
                # Mock the directory path
                mock_dirname.return_value = '/app/backend/utils'
                mock_abspath.return_value = '/app/backend/utils/utils.py'
                
                # Mock directory contents with some templates
                mock_listdir.return_value = [
                    'template1.html',
                    'template2.html',
                    'template3.html'
                ]
                
                # Get available templates
                templates = get_available_templates()
                
                # Check that it returns a list
                self.assertIsInstance(templates, list)
                
                # Check that all items are strings and match expected templates
                self.assertEqual(set(templates), {'template1', 'template2', 'template3'})
            
            self.log_case_result("Basic template discovery", True)
            
        except Exception as e:
            self.log_case_result("Basic template discovery", False)
            raise
    
    def test_file_extension_handling(self):
        """Test handling of different file extensions."""
        try:
            # Create a temporary directory with test files
            with patch('os.path.dirname') as mock_dirname, \
                 patch('os.path.abspath') as mock_abspath, \
                 patch('os.listdir') as mock_listdir:
                
                # Mock the directory path
                mock_dirname.return_value = '/app/backend/utils'
                mock_abspath.return_value = '/app/backend/utils/utils.py'
                
                # Mock directory contents with mixed file types
                mock_listdir.return_value = [
                    'template1.html',
                    'template2.HTML',
                    'template3.txt',
                    'template4.pdf',
                    'template5.html'
                ]
                
                # Get available templates
                templates = get_available_templates()
                
                # Check that only HTML files are included
                self.assertEqual(set(templates), {'template1', 'template2', 'template5'})
                
            self.log_case_result("File extension handling", True)
            
        except Exception as e:
            self.log_case_result("File extension handling", False)
            raise
    
    def test_empty_directory(self):
        """Test behavior with an empty templates directory."""
        try:
            with patch('os.path.dirname') as mock_dirname, \
                 patch('os.path.abspath') as mock_abspath, \
                 patch('os.listdir') as mock_listdir:
                
                # Mock the directory path
                mock_dirname.return_value = '/app/backend/utils'
                mock_abspath.return_value = '/app/backend/utils/utils.py'
                
                # Mock empty directory
                mock_listdir.return_value = []
                
                # Get available templates
                templates = get_available_templates()
                
                # Check that it returns an empty list
                self.assertEqual(templates, [])
                
            self.log_case_result("Empty directory handling", True)
            
        except Exception as e:
            self.log_case_result("Empty directory handling", False)
            raise
    
    def test_error_handling(self):
        """Test error handling when directory operations fail."""
        try:
            with patch('os.path.dirname') as mock_dirname, \
                 patch('os.path.abspath') as mock_abspath, \
                 patch('os.listdir') as mock_listdir:
                
                # Mock the directory path
                mock_dirname.return_value = '/app/backend/utils'
                mock_abspath.return_value = '/app/backend/utils/utils.py'
                
                # Mock directory error
                mock_listdir.side_effect = PermissionError("Permission denied")
                
                # Get available templates
                templates = get_available_templates()
                
                # Check that it returns an empty list on error
                self.assertEqual(templates, [])
                
            self.log_case_result("Error handling", True)
            
        except Exception as e:
            self.log_case_result("Error handling", False)
            raise
    
    def test_template_name_format(self):
        """Test handling of different template name formats."""
        try:
            with patch('os.path.dirname') as mock_dirname, \
                 patch('os.path.abspath') as mock_abspath, \
                 patch('os.listdir') as mock_listdir:
                
                # Mock the directory path
                mock_dirname.return_value = '/app/backend/utils'
                mock_abspath.return_value = '/app/backend/utils/utils.py'
                
                # Mock directory contents with various name formats
                mock_listdir.return_value = [
                    'template with spaces.html',
                    'template-with-hyphens.html',
                    'template_with_underscores.html',
                    'TemplateWithCamelCase.html',
                    'template_with_special_chars@#$%.html'
                ]
                
                # Get available templates
                templates = get_available_templates()
                
                # Check that all templates are included with correct names
                expected = {
                    'template with spaces',
                    'template-with-hyphens',
                    'template_with_underscores',
                    'TemplateWithCamelCase',
                    'template_with_special_chars@#$%'
                }
                self.assertEqual(set(templates), expected)
                
            self.log_case_result("Template name format handling", True)
            
        except Exception as e:
            self.log_case_result("Template name format handling", False)
            raise

class TestRenderHtmlTemplate(BaseTestCase):
    def setUp(self):
        """Set up test environment with temporary template directory."""
        # Call parent's setUp to initialize class_name and test_name
        super().setUp()
        
        self.temp_dir = tempfile.mkdtemp()
        self.template_dir = os.path.join(self.temp_dir, "templates")
        os.makedirs(self.template_dir, exist_ok=True)
        
        # Create test templates
        self.create_test_template("test_template.html", "Hello {{ name }}!")
        self.create_test_template("complex_template.html", """
            <div>
                <h1>{{ title }}</h1>
                <p>{{ content }}</p>
                {% if show_extra %}
                <div class="extra">{{ extra_content }}</div>
                {% endif %}
            </div>
        """)
        self.create_test_template("invalid_template.html", "{% invalid syntax %}")

    def tearDown(self):
        """Clean up test environment."""
        import shutil
        shutil.rmtree(self.temp_dir)
        # Call parent's tearDown to clean up patches
        super().tearDown()

    def create_test_template(self, filename, content):
        """Helper method to create test template files."""
        with open(os.path.join(self.template_dir, filename), 'w') as f:
            f.write(content)

    def test_basic_template_rendering(self):
        """Test basic template rendering with simple variables."""
        try:
            variables = {"name": "World"}
            result = render_html_template("test_template", variables, template_dir=self.template_dir)
            self.assertEqual(result, "Hello World!")
            self.log_case_result("Basic template rendering", True)
        except Exception as e:
            self.log_case_result("Basic template rendering", False)
            raise

    def test_complex_template_rendering(self):
        """Test rendering of complex template with conditional logic."""
        try:
            variables = {
                "title": "Test Title",
                "content": "Test Content",
                "show_extra": True,
                "extra_content": "Extra Info"
            }
            result = render_html_template("complex_template", variables, template_dir=self.template_dir)
            self.assertIn("Test Title", result)
            self.assertIn("Test Content", result)
            self.assertIn("Extra Info", result)
            self.log_case_result("Complex template rendering", True)
        except Exception as e:
            self.log_case_result("Complex template rendering", False)
            raise

    def test_template_not_found(self):
        """Test handling of non-existent template."""
        try:
            with self.assertRaises(TemplateNotFound):
                render_html_template("nonexistent_template", {}, template_dir=self.template_dir)
            self.log_case_result("Template not found handling", True)
        except Exception as e:
            self.log_case_result("Template not found handling", False)
            raise

    def test_invalid_template_syntax(self):
        """Test handling of template with invalid syntax."""
        try:
            with self.assertRaises(TemplateSyntaxError):
                render_html_template("invalid_template", {}, template_dir=self.template_dir)
            self.log_case_result("Invalid template syntax handling", True)
        except Exception as e:
            self.log_case_result("Invalid template syntax handling", False)
            raise

    def test_missing_variables(self):
        """Test handling of missing variables in template."""
        try:
            variables = {
                "name": "World",
                "show_extra": True,  # Add this to see extra content
                "extra_content": "Extra Info"
            }
            result = render_html_template("complex_template", variables, template_dir=self.template_dir)
            # Check that missing variables are rendered as empty strings
            self.assertIn("<h1></h1>", result)  # title is empty
            self.assertIn("<p></p>", result)    # content is empty
            self.assertIn("Extra Info", result)  # extra_content is present
            self.log_case_result("Missing variables handling", True)
        except Exception as e:
            self.log_case_result("Missing variables handling", False)
            raise

    def test_empty_variables(self):
        """Test rendering with empty variables dictionary."""
        try:
            result = render_html_template("test_template", {}, template_dir=self.template_dir)
            self.assertEqual(result, "Hello !")
            self.log_case_result("Empty variables handling", True)
        except Exception as e:
            self.log_case_result("Empty variables handling", False)
            raise

    def test_special_characters(self):
        """Test handling of special characters in variables."""
        try:
            variables = {
                "title": "Special Title!@#$%^&*()!",
                "content": "Content with special chars!@#$%^&*()!"
            }
            result = render_html_template("complex_template", variables, template_dir=self.template_dir)
            # Check that special characters are properly escaped
            self.assertIn("Special Title!@#$%^&amp;*()!", result)
            self.assertIn("Content with special chars!@#$%^&amp;*()!", result)
            self.log_case_result("Special characters handling", True)
        except Exception as e:
            self.log_case_result("Special characters handling", False)
            raise

    def test_html_escaping(self):
        """Test that HTML in variables is properly escaped."""
        try:
            self.create_test_template("escape_test.html", "{{ content }}")
            variables = {"content": "<script>alert('xss')</script>"}
            result = render_html_template("escape_test", variables, template_dir=self.template_dir)
            self.assertIn("&lt;script&gt;", result)
            self.assertIn("&lt;/script&gt;", result)
            self.log_case_result("HTML escaping", True)
        except Exception as e:
            self.log_case_result("HTML escaping", False)
            raise

    def test_template_directory_error(self):
        """Test handling of template directory access errors."""
        try:
            with self.assertRaises(Exception):
                render_html_template("test_template", {}, template_dir="/nonexistent/dir")
            self.log_case_result("Template directory error handling", True)
        except Exception as e:
            self.log_case_result("Template directory error handling", False)
            raise

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