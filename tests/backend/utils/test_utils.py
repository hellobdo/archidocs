import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import tempfile
from jinja2 import TemplateNotFound, TemplateSyntaxError

# Add project root to path to ensure imports work properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from backend.backend.utils.utils import get_available_templates, render_html_template
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

if __name__ == "__main__":
    # Run tests
    unittest.main(exit=False)
    
    # Print summary
    print_summary() 