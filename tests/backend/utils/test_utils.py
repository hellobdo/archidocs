import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add project root to path to ensure imports work properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from backend.backend.utils.utils import get_available_templates
from tests._utils.test_utils import BaseTestCase, print_summary

class TestGetAvailableTemplates(BaseTestCase):
    """Test template discovery functionality."""
    
    def test_basic_template_discovery(self):
        """Test basic template discovery functionality."""
        try:
            # Get available templates
            templates = get_available_templates()
            
            # Check that it returns a list
            self.assertIsInstance(templates, list)
            
            # Check that all items are strings
            for template in templates:
                self.assertIsInstance(template, str)
            
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

if __name__ == "__main__":
    # Run tests
    unittest.main(exit=False)
    
    # Print summary
    print_summary() 