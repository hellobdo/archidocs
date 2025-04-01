import os
import shutil
import unittest
from unittest.mock import patch, MagicMock

from backend.backend.main import generate_document
from tests._utils.test_utils import BaseTestCase, print_summary

class TestGenerateDocument(BaseTestCase):
    """Tests for the document generation functionality."""

    def setUp(self):
        super().setUp()
        # Create test output directory
        self.test_output_dir = os.path.join(os.getcwd(), 'test_outputs')
        os.makedirs(self.test_output_dir, exist_ok=True)
        
        # Template and variables
        self.template_name = "test_template"
        self.variables = {
            "title": "Test Document",
            "content": "This is a test document."
        }
        self.processed_variables = {
            "title": "Test Document",
            "content": "This is a test document.",
            "date": "abril de 2025"  # Added by process_costs_and_dates
        }
        
    def tearDown(self):
        # Clean up test directory
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
        super().tearDown()

    def test_docx_only_generation(self):
        """Test generating only DOCX document."""
        output_path = os.path.join(self.test_output_dir, 'test.docx')
        
        with patch('backend.backend.main.render_html_template') as mock_render, \
             patch('backend.backend.main.convert_html_to_docx') as mock_docx, \
             patch('backend.backend.main.process_costs_and_dates', return_value=self.processed_variables):
            
            # Mock successful DOCX conversion
            mock_render.return_value = "<html>Test content</html>"
            mock_docx.return_value = output_path
            
            # Generate document without PDF/A
            result = generate_document(
                self.template_name,
                self.variables,
                output_path,
                generate_pdfa=False
            )
            
            # Verify result
            self.assertEqual(result, {'docx': output_path})
            mock_docx.assert_called_once()
            mock_render.assert_called_once_with(self.template_name, self.processed_variables)
            self.log_case_result("DOCX generation successful", True)

    def test_docx_and_pdfa_generation(self):
        """Test generating both DOCX and PDF/A documents."""
        output_path = os.path.join(self.test_output_dir, 'test.docx')
        pdfa_path = output_path.replace('.docx', '.pdf')
        temp_pdf = output_path.replace('.docx', '_temp.pdf')
        
        with patch('backend.backend.main.render_html_template') as mock_render, \
             patch('backend.backend.main.convert_html_to_docx') as mock_docx, \
             patch('backend.backend.main.convert_html_to_pdf') as mock_pdf, \
             patch('backend.backend.main.convert_to_pdfa') as mock_pdfa, \
             patch('backend.backend.main.process_costs_and_dates', return_value=self.processed_variables):
            
            # Mock successful conversions
            mock_render.return_value = "<html>Test content</html>"
            mock_docx.return_value = output_path
            mock_pdf.return_value = temp_pdf
            mock_pdfa.return_value = pdfa_path
            
            # Generate both documents
            result = generate_document(
                self.template_name,
                self.variables,
                output_path,
                generate_pdfa=True
            )
            
            # Verify result
            self.assertEqual(result, {'docx': output_path, 'pdfa': pdfa_path})
            mock_docx.assert_called_once()
            mock_pdf.assert_called_once()
            mock_pdfa.assert_called_once()
            mock_render.assert_called_once_with(self.template_name, self.processed_variables)
            self.log_case_result("DOCX and PDF/A generation successful", True)

    def test_invalid_output_path(self):
        """Test handling of invalid output path (not ending in .docx)."""
        invalid_paths = [
            os.path.join(self.test_output_dir, 'test.pdf'),
            os.path.join(self.test_output_dir, 'test.pdfa'),
            os.path.join(self.test_output_dir, 'test.txt'),
            os.path.join(self.test_output_dir, 'test')
        ]
        
        with patch('backend.backend.main.render_html_template') as mock_render:
            mock_render.return_value = "<html>Test content</html>"
            
            for path in invalid_paths:
                with self.assertRaises(ValueError) as cm:
                    generate_document(self.template_name, self.variables, path)
                self.assertEqual(str(cm.exception), "Output path must end in .docx")
                self.log_case_result(f"Invalid path handled: {path}", True)

    def test_docx_conversion_failure(self):
        """Test handling of DOCX conversion failure."""
        output_path = os.path.join(self.test_output_dir, 'test.docx')
        
        with patch('backend.backend.main.render_html_template') as mock_render, \
             patch('backend.backend.main.convert_html_to_docx') as mock_docx, \
             patch('backend.backend.main.process_costs_and_dates', return_value=self.processed_variables):
            
            # Mock DOCX conversion failure
            mock_render.return_value = "<html>Test content</html>"
            mock_docx.return_value = None
            
            # Verify error is raised
            with self.assertRaises(RuntimeError) as cm:
                generate_document(self.template_name, self.variables, output_path)
            self.assertEqual(str(cm.exception), f"Failed to create DOCX: {output_path}")
            self.log_case_result("DOCX conversion failure handled", True)

    def test_pdf_conversion_failure(self):
        """Test handling of PDF conversion failure."""
        output_path = os.path.join(self.test_output_dir, 'test.docx')
        temp_pdf = output_path.replace('.docx', '_temp.pdf')
        
        with patch('backend.backend.main.render_html_template') as mock_render, \
             patch('backend.backend.main.convert_html_to_docx') as mock_docx, \
             patch('backend.backend.main.convert_html_to_pdf') as mock_pdf, \
             patch('backend.backend.main.process_costs_and_dates', return_value=self.processed_variables):
            
            # Mock DOCX success but PDF failure
            mock_render.return_value = "<html>Test content</html>"
            mock_docx.return_value = output_path
            mock_pdf.return_value = None
            
            # Verify error is raised
            with self.assertRaises(RuntimeError) as cm:
                generate_document(self.template_name, self.variables, output_path, generate_pdfa=True)
            self.assertEqual(str(cm.exception), f"Failed to create temporary PDF: {temp_pdf}")
            self.log_case_result("PDF conversion failure handled", True)

    def test_pdfa_conversion_failure(self):
        """Test handling of PDF/A conversion failure."""
        output_path = os.path.join(self.test_output_dir, 'test.docx')
        pdfa_path = output_path.replace('.docx', '.pdf')
        temp_pdf = output_path.replace('.docx', '_temp.pdf')
        
        with patch('backend.backend.main.render_html_template') as mock_render, \
             patch('backend.backend.main.convert_html_to_docx') as mock_docx, \
             patch('backend.backend.main.convert_html_to_pdf') as mock_pdf, \
             patch('backend.backend.main.convert_to_pdfa') as mock_pdfa, \
             patch('backend.backend.main.process_costs_and_dates', return_value=self.processed_variables):
            
            # Mock DOCX and PDF success but PDF/A failure
            mock_render.return_value = "<html>Test content</html>"
            mock_docx.return_value = output_path
            mock_pdf.return_value = temp_pdf
            mock_pdfa.return_value = None
            
            # Verify error is raised
            with self.assertRaises(RuntimeError) as cm:
                generate_document(self.template_name, self.variables, output_path, generate_pdfa=True)
            self.assertEqual(str(cm.exception), f"Failed to create PDF/A: {pdfa_path}")
            self.log_case_result("PDF/A conversion failure handled", True)

    def test_output_directory_creation(self):
        """Test that output directory is created if it doesn't exist."""
        nested_dir = os.path.join(self.test_output_dir, 'nested', 'dirs')
        output_path = os.path.join(nested_dir, 'test.docx')
        
        with patch('backend.backend.main.render_html_template') as mock_render, \
             patch('backend.backend.main.convert_html_to_docx') as mock_docx, \
             patch('backend.backend.main.process_costs_and_dates', return_value=self.processed_variables):
            
            # Mock successful DOCX conversion
            mock_render.return_value = "<html>Test content</html>"
            mock_docx.return_value = output_path
            
            # Generate document
            result = generate_document(
                self.template_name,
                self.variables,
                output_path,
                generate_pdfa=False
            )
            
            # Verify directory was created
            self.assertTrue(os.path.exists(nested_dir))
            self.assertEqual(result, {'docx': output_path})
            self.log_case_result("Output directory creation successful", True)

    def test_file_overwrite(self):
        """Test that existing files are overwritten."""
        output_path = os.path.join(self.test_output_dir, 'test.docx')
        pdfa_path = output_path.replace('.docx', '.pdf')
        
        # Create dummy files
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write("Original DOCX")
        with open(pdfa_path, 'w') as f:
            f.write("Original PDF/A")
        
        with patch('backend.backend.main.render_html_template') as mock_render, \
             patch('backend.backend.main.convert_html_to_docx') as mock_docx, \
             patch('backend.backend.main.convert_html_to_pdf') as mock_pdf, \
             patch('backend.backend.main.convert_to_pdfa') as mock_pdfa, \
             patch('backend.backend.main.process_costs_and_dates', return_value=self.processed_variables):
            
            # Mock successful conversions
            mock_render.return_value = "<html>Test content</html>"
            mock_docx.return_value = output_path
            mock_pdf.return_value = output_path.replace('.docx', '.pdf')
            mock_pdfa.return_value = pdfa_path
            
            # Generate both documents
            result = generate_document(
                self.template_name,
                self.variables,
                output_path,
                generate_pdfa=True
            )
            
            # Verify result
            self.assertEqual(result, {'docx': output_path, 'pdfa': pdfa_path})
            self.log_case_result("File overwrite successful", True)

if __name__ == '__main__':
    unittest.main(exit=False)
    print_summary()
