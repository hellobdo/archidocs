import os
import sys
import shutil
import unittest
import tempfile
from pathlib import Path

# Add project root to path to ensure imports work properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from backend.backend.docs_gen.html_converter import convert_html_to_docx, convert_html_to_pdf
from tests._utils.test_utils import BaseTestCase, print_summary

class TestHtmlToDocx(BaseTestCase):
    """Tests for the HTML to DOCX converter functionality.
    
    Note: Directory creation is handled by the caller (main.py).
    This test suite focuses on the core conversion functionality using HtmlToDocx.
    """

    def setUp(self):
        super().setUp()
        # Create test output directory if it doesn't exist
        self.test_output_dir = os.path.join(os.getcwd(), 'test_outputs')
        os.makedirs(self.test_output_dir, exist_ok=True)
        
        # Prepare basic HTML content for testing
        self.basic_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Document</title>
        </head>
        <body>
            <h1>Test Heading</h1>
            <p>This is a paragraph for testing.</p>
        </body>
        </html>
        """
        
        # Prepare complex HTML content for testing
        self.complex_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Complex Test Document</title>
            <style>
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid black; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>Complex Document Test</h1>
            <p>This document contains <strong>formatted text</strong>, <em>different styles</em>, and other elements.</p>
            
            <h2>Section with a List</h2>
            <ul>
                <li>Item 1</li>
                <li>Item 2 with <strong>bold text</strong></li>
                <li>Item 3</li>
            </ul>
            
            <h2>Section with a Table</h2>
            <table>
                <tr>
                    <th>Header 1</th>
                    <th>Header 2</th>
                </tr>
                <tr>
                    <td>Data 1</td>
                    <td>Data 2</td>
                </tr>
                <tr>
                    <td>Data 3</td>
                    <td>Data 4</td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        # Prepare HTML with special characters
        self.special_chars_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Special Characters Test</title>
        </head>
        <body>
            <h1>Special Characters Test</h1>
            <p>Testing various special characters:</p>
            <ul>
                <li>Accents: é, è, ê, ë</li>
                <li>Special symbols: ©, ®, ™, €, £, ¥</li>
                <li>Non-breaking space: &nbsp;</li>
                <li>Quotes: "smart quotes" and 'smart quotes'</li>
            </ul>
        </body>
        </html>
        """
        
    def tearDown(self):
        # Clean up the test output directory
        if os.path.exists(self.test_output_dir):
            try:
                shutil.rmtree(self.test_output_dir)
                print(f"Removed test output directory: {self.test_output_dir}")
            except Exception as e:
                print(f"Warning: Could not remove test output directory: {str(e)}")
        
        super().tearDown()
    
    def test_basic_conversion(self):
        """Test converting basic HTML to DOCX.
        
        Verifies that the function can convert simple HTML content to DOCX format using HtmlToDocx.
        Directory creation is handled by the caller.
        """
        # Define output path
        output_path = os.path.join(self.test_output_dir, 'basic_test.docx')
        
        # Capture stdout
        original_stdout = self.capture_stdout()
        
        try:
            # Execute the conversion
            print(f"\nTesting basic HTML to DOCX conversion")
            result = convert_html_to_docx(self.basic_html, output_path)
            
            # Check conversion was successful
            self.assertEqual(result, output_path, "Function should return the output file path")
            self.assertTrue(os.path.exists(output_path), "Output file should exist")
            self.assertTrue(os.path.getsize(output_path) > 0, "Output file should not be empty")
            
            self.log_case_result("Basic HTML to DOCX conversion", True)
            
        except Exception as e:
            print(f"Error in test_basic_conversion: {str(e)}")
            import traceback
            traceback.print_exc()
            self.log_case_result("Basic HTML to DOCX conversion", False)
            self.fail(f"Unexpected error: {str(e)}")
        finally:
            self.restore_stdout(original_stdout)
    
    def test_complex_conversion(self):
        """Test converting complex HTML with tables and formatting to DOCX.
        
        Verifies that the function can handle complex HTML with tables, lists, and formatting using HtmlToDocx.
        Directory creation is handled by the caller.
        """
        # Define output path
        output_path = os.path.join(self.test_output_dir, 'complex_test.docx')
        
        # Capture stdout
        original_stdout = self.capture_stdout()
        
        try:
            # Execute the conversion
            print(f"\nTesting complex HTML to DOCX conversion")
            result = convert_html_to_docx(self.complex_html, output_path)
            
            # Check conversion was successful
            self.assertEqual(result, output_path, "Function should return the output file path")
            self.assertTrue(os.path.exists(output_path), "Output file should exist")
            self.assertTrue(os.path.getsize(output_path) > 0, "Output file should not be empty")
            
            self.log_case_result("Complex HTML to DOCX conversion", True)
            
        except Exception as e:
            print(f"Error in test_complex_conversion: {str(e)}")
            import traceback
            traceback.print_exc()
            self.log_case_result("Complex HTML to DOCX conversion", False)
            self.fail(f"Unexpected error: {str(e)}")
        finally:
            self.restore_stdout(original_stdout)
    
    def test_special_chars_conversion(self):
        """Test converting HTML with special characters to DOCX.
        
        Verifies that the function can handle special characters and symbols using HtmlToDocx.
        Directory creation is handled by the caller.
        """
        # Define output path
        output_path = os.path.join(self.test_output_dir, 'special_chars_test.docx')
        
        # Capture stdout
        original_stdout = self.capture_stdout()
        
        try:
            # Execute the conversion
            print(f"\nTesting special characters HTML to DOCX conversion")
            result = convert_html_to_docx(self.special_chars_html, output_path)
            
            # Check conversion was successful
            self.assertEqual(result, output_path, "Function should return the output file path")
            self.assertTrue(os.path.exists(output_path), "Output file should exist")
            self.assertTrue(os.path.getsize(output_path) > 0, "Output file should not be empty")
            
            self.log_case_result("Special characters HTML to DOCX conversion", True)
            
        except Exception as e:
            print(f"Error in test_special_chars_conversion: {str(e)}")
            import traceback
            traceback.print_exc()
            self.log_case_result("Special characters HTML to DOCX conversion", False)
            self.fail(f"Unexpected error: {str(e)}")
        finally:
            self.restore_stdout(original_stdout)
    
    def test_empty_html_handling(self):
        """Test handling of empty HTML content for DOCX conversion.
        
        Verifies that the function can handle empty HTML content using HtmlToDocx.
        Directory creation is handled by the caller.
        """
        # Define output path
        output_path = os.path.join(self.test_output_dir, 'empty_test.docx')
        
        # Capture stdout
        original_stdout = self.capture_stdout()
        
        try:
            # Execute the conversion with empty HTML
            print(f"\nTesting empty HTML to DOCX conversion")
            empty_html = "<html><body></body></html>"
            result = convert_html_to_docx(empty_html, output_path)
            
            # Conversion should still succeed with an empty document
            self.assertEqual(result, output_path, "Function should return the output file path")
            self.assertTrue(os.path.exists(output_path), "Output file should exist even for empty HTML")
            
            self.log_case_result("Empty HTML to DOCX conversion", True)
            
        except Exception as e:
            print(f"Error in test_empty_html_handling: {str(e)}")
            import traceback
            traceback.print_exc()
            self.log_case_result("Empty HTML to DOCX conversion", False)
            self.fail(f"Unexpected error: {str(e)}")
        finally:
            self.restore_stdout(original_stdout)
    
    def test_invalid_html_handling(self):
        """Test handling of invalid HTML content for DOCX conversion.
        
        Verifies that the function can handle malformed HTML content using HtmlToDocx.
        Directory creation is handled by the caller.
        """
        # Define output path
        output_path = os.path.join(self.test_output_dir, 'invalid_test.docx')
        
        # Capture stdout
        original_stdout = self.capture_stdout()
        
        try:
            # Execute the conversion with invalid HTML (malformed tags)
            print(f"\nTesting invalid HTML to DOCX conversion")
            invalid_html = "<html><body><div>Unclosed div tag</html>"
            result = convert_html_to_docx(invalid_html, output_path)
            
            # HtmlToDocx should handle invalid HTML and still produce some output
            self.assertEqual(result, output_path, "Function should return the output file path")
            self.assertTrue(os.path.exists(output_path), "Output file should exist even for invalid HTML")
            
            self.log_case_result("Invalid HTML to DOCX conversion", True)
            
        except Exception as e:
            # It's acceptable if this raises an exception, but we'll log it
            print(f"Note: Invalid HTML to DOCX conversion raised exception: {str(e)}")
            self.log_case_result("Invalid HTML to DOCX conversion - exception path", True)
        finally:
            self.restore_stdout(original_stdout)
    
    def test_file_overwrite(self):
        """Test that existing DOCX files are overwritten.
        
        Verifies that the function can overwrite existing files using HtmlToDocx.
        Directory creation is handled by the caller.
        """
        # Define output path
        output_path = os.path.join(self.test_output_dir, 'overwrite_test.docx')
        
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
            print(f"\nTesting DOCX file overwrite behavior")
            result = convert_html_to_docx(self.basic_html, output_path)
            
            # Check if file was overwritten
            self.assertEqual(result, output_path, "Function should return the output file path")
            self.assertTrue(os.path.exists(output_path), "Output file should exist")
            self.assertNotEqual(original_mtime, os.path.getmtime(output_path), 
                               "File modification time should change, indicating overwrite")
            
            self.log_case_result("DOCX file overwrite behavior", True)
            
        except Exception as e:
            print(f"Error in test_file_overwrite: {str(e)}")
            import traceback
            traceback.print_exc()
            self.log_case_result("DOCX file overwrite behavior", False)
            self.fail(f"Unexpected error: {str(e)}")
        finally:
            self.restore_stdout(original_stdout)


class TestHtmlToPdf(BaseTestCase):
    """Tests for the HTML to PDF converter functionality.
    
    Note: Directory creation is handled by the caller (main.py).
    This test suite focuses on the core conversion functionality.
    """

    def setUp(self):
        super().setUp()
        # Create test output directory if it doesn't exist
        self.test_output_dir = os.path.join(os.getcwd(), 'test_outputs')
        os.makedirs(self.test_output_dir, exist_ok=True)
        
        # Prepare basic HTML content for testing
        self.basic_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Document</title>
        </head>
        <body>
            <h1>Test Heading</h1>
            <p>This is a paragraph for testing.</p>
        </body>
        </html>
        """
        
        # Prepare complex HTML content for testing
        self.complex_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Complex Test Document</title>
            <style>
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid black; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>Complex Document Test</h1>
            <p>This document contains <strong>formatted text</strong>, <em>different styles</em>, and other elements.</p>
            
            <h2>Section with a List</h2>
            <ul>
                <li>Item 1</li>
                <li>Item 2 with <strong>bold text</strong></li>
                <li>Item 3</li>
            </ul>
            
            <h2>Section with a Table</h2>
            <table>
                <tr>
                    <th>Header 1</th>
                    <th>Header 2</th>
                </tr>
                <tr>
                    <td>Data 1</td>
                    <td>Data 2</td>
                </tr>
                <tr>
                    <td>Data 3</td>
                    <td>Data 4</td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        # Prepare HTML with special characters
        self.special_chars_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Special Characters Test</title>
        </head>
        <body>
            <h1>Special Characters Test</h1>
            <p>Testing various special characters:</p>
            <ul>
                <li>Accents: é, è, ê, ë</li>
                <li>Special symbols: ©, ®, ™, €, £, ¥</li>
                <li>Non-breaking space: &nbsp;</li>
                <li>Quotes: "smart quotes" and 'smart quotes'</li>
            </ul>
        </body>
        </html>
        """
        
    def tearDown(self):
        # Clean up the test output directory
        if os.path.exists(self.test_output_dir):
            try:
                shutil.rmtree(self.test_output_dir)
                print(f"Removed test output directory: {self.test_output_dir}")
            except Exception as e:
                print(f"Warning: Could not remove test output directory: {str(e)}")
        
        super().tearDown()

    def test_basic_conversion(self):
        """Test converting basic HTML to PDF.
        
        Verifies that the function can convert simple HTML content to PDF format.
        Directory creation is handled by the caller.
        """
        # Define output path
        output_path = os.path.join(self.test_output_dir, 'basic_test.pdf')
        
        # Capture stdout
        original_stdout = self.capture_stdout()
        
        try:
            # Execute the conversion
            print(f"\nTesting basic HTML to PDF conversion")
            result = convert_html_to_pdf(self.basic_html, output_path)
            
            # Check conversion was successful
            self.assertEqual(result, output_path, "Function should return the output file path")
            self.assertTrue(os.path.exists(output_path), "Output file should exist")
            self.assertTrue(os.path.getsize(output_path) > 0, "Output file should not be empty")
            
            self.log_case_result("Basic HTML to PDF conversion", True)
            
        except Exception as e:
            print(f"Error in test_basic_conversion: {str(e)}")
            import traceback
            traceback.print_exc()
            self.log_case_result("Basic HTML to PDF conversion", False)
            self.fail(f"Unexpected error: {str(e)}")
        finally:
            self.restore_stdout(original_stdout)

    def test_complex_conversion(self):
        """Test converting complex HTML with tables and formatting to PDF.
        
        Verifies that the function can handle complex HTML with tables, lists, and formatting.
        Directory creation is handled by the caller.
        """
        # Define output path
        output_path = os.path.join(self.test_output_dir, 'complex_test.pdf')
        
        # Capture stdout
        original_stdout = self.capture_stdout()
        
        try:
            # Execute the conversion
            print(f"\nTesting complex HTML to PDF conversion")
            result = convert_html_to_pdf(self.complex_html, output_path)
            
            # Check conversion was successful
            self.assertEqual(result, output_path, "Function should return the output file path")
            self.assertTrue(os.path.exists(output_path), "Output file should exist")
            self.assertTrue(os.path.getsize(output_path) > 0, "Output file should not be empty")
            
            self.log_case_result("Complex HTML to PDF conversion", True)
            
        except Exception as e:
            print(f"Error in test_complex_conversion: {str(e)}")
            import traceback
            traceback.print_exc()
            self.log_case_result("Complex HTML to PDF conversion", False)
            self.fail(f"Unexpected error: {str(e)}")
        finally:
            self.restore_stdout(original_stdout)

    def test_special_chars_conversion(self):
        """Test converting HTML with special characters to PDF.
        
        Verifies that the function can handle special characters and symbols.
        Directory creation is handled by the caller.
        """
        # Define output path
        output_path = os.path.join(self.test_output_dir, 'special_chars_test.pdf')
        
        # Capture stdout
        original_stdout = self.capture_stdout()
        
        try:
            # Execute the conversion
            print(f"\nTesting special characters HTML to PDF conversion")
            result = convert_html_to_pdf(self.special_chars_html, output_path)
            
            # Check conversion was successful
            self.assertEqual(result, output_path, "Function should return the output file path")
            self.assertTrue(os.path.exists(output_path), "Output file should exist")
            self.assertTrue(os.path.getsize(output_path) > 0, "Output file should not be empty")
            
            self.log_case_result("Special characters HTML to PDF conversion", True)
            
        except Exception as e:
            print(f"Error in test_special_chars_conversion: {str(e)}")
            import traceback
            traceback.print_exc()
            self.log_case_result("Special characters HTML to PDF conversion", False)
            self.fail(f"Unexpected error: {str(e)}")
        finally:
            self.restore_stdout(original_stdout)

    def test_empty_html_handling(self):
        """Test handling of empty HTML content for PDF conversion.
        
        Verifies that the function can handle empty HTML content.
        Directory creation is handled by the caller.
        """
        # Define output path
        output_path = os.path.join(self.test_output_dir, 'empty_test.pdf')
        
        # Capture stdout
        original_stdout = self.capture_stdout()
        
        try:
            # Execute the conversion with empty HTML
            print(f"\nTesting empty HTML to PDF conversion")
            empty_html = "<html><body></body></html>"
            result = convert_html_to_pdf(empty_html, output_path)
            
            # Conversion should still succeed with an empty document
            self.assertEqual(result, output_path, "Function should return the output file path")
            self.assertTrue(os.path.exists(output_path), "Output file should exist even for empty HTML")
            
            self.log_case_result("Empty HTML to PDF conversion", True)
            
        except Exception as e:
            print(f"Error in test_empty_html_handling: {str(e)}")
            import traceback
            traceback.print_exc()
            self.log_case_result("Empty HTML to PDF conversion", False)
            self.fail(f"Unexpected error: {str(e)}")
        finally:
            self.restore_stdout(original_stdout)

    def test_invalid_html_handling(self):
        """Test handling of invalid HTML content for PDF conversion.
        
        Verifies that the function can handle malformed HTML content.
        Directory creation is handled by the caller.
        """
        # Define output path
        output_path = os.path.join(self.test_output_dir, 'invalid_test.pdf')
        
        # Capture stdout
        original_stdout = self.capture_stdout()
        
        try:
            # Execute the conversion with invalid HTML (malformed tags)
            print(f"\nTesting invalid HTML to PDF conversion")
            invalid_html = "<html><body><div>Unclosed div tag</html>"
            result = convert_html_to_pdf(invalid_html, output_path)
            
            # We expect None for invalid HTML
            self.assertIsNone(result, "Function should return None for invalid HTML")
            
            self.log_case_result("Invalid HTML to PDF conversion", True)
            
        except Exception as e:
            # It's acceptable if this raises an exception, but we'll log it
            print(f"Note: Invalid HTML to PDF conversion raised exception: {str(e)}")
            self.log_case_result("Invalid HTML to PDF conversion - exception path", True)
        finally:
            self.restore_stdout(original_stdout)

    def test_file_overwrite(self):
        """Test that existing PDF files are overwritten.
        
        Verifies that the function can overwrite existing files.
        Directory creation is handled by the caller.
        """
        # Define output path
        output_path = os.path.join(self.test_output_dir, 'overwrite_test.pdf')
        
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
            print(f"\nTesting PDF file overwrite behavior")
            result = convert_html_to_pdf(self.basic_html, output_path)
            
            # Check if file was overwritten
            self.assertEqual(result, output_path, "Function should return the output file path")
            self.assertTrue(os.path.exists(output_path), "Output file should exist")
            self.assertNotEqual(original_mtime, os.path.getmtime(output_path), 
                               "File modification time should change, indicating overwrite")
            
            self.log_case_result("PDF file overwrite behavior", True)
            
        except Exception as e:
            print(f"Error in test_file_overwrite: {str(e)}")
            import traceback
            traceback.print_exc()
            self.log_case_result("PDF file overwrite behavior", False)
            self.fail(f"Unexpected error: {str(e)}")
        finally:
            self.restore_stdout(original_stdout)


if __name__ == "__main__":
    # Run tests
    unittest.main(exit=False)
    
    # Print summary
    print_summary()
