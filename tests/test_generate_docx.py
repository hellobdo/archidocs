"""
Tests for functions in generate_docx.py.
"""
import unittest
import sys
import os
import json
import tempfile
from unittest.mock import patch, MagicMock
import io
import glob

# Setup path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, current_dir)

# Import base test utilities
from _utils.test_utils import BaseTestCase, print_summary

# Import the module we want to test
from backend.generate_docx import load_variables, format_number_pt, num_to_words_pt, process_total_cost, get_portuguese_month, get_available_templates, to_number, generate_document

# Module specific test fixtures
def create_module_fixtures():
    """Create test fixtures specific to this module's tests"""
    fixtures = {}
    
    # Add test data
    fixtures['sample_variables'] = {
        "author_name": "Daniela Cristina",
        "author_title": "Arquiteta",
        "qty": 100,
        "cost_per_unit": 150.50
    }
    
    return fixtures

class TestGenerateDocxImports(BaseTestCase):
    """Test basic imports and module setup"""
    
    def test_imports(self):
        """Test that imports are working correctly"""
        # Case 1: Check that functions are callable
        try:
            self.assertTrue(callable(load_variables))
            self.assertTrue(callable(format_number_pt))
            self.assertTrue(callable(num_to_words_pt))
            self.assertTrue(callable(process_total_cost))
            self.assertTrue(callable(get_portuguese_month))
            self.assertTrue(callable(get_available_templates))
            self.assertTrue(callable(to_number))
            self.assertTrue(callable(generate_document))
            self.log_case_result("Functions are callable", True)
        except AssertionError:
            self.log_case_result("Functions are callable", False)
            raise

class TestLoadVariables(BaseTestCase):
    """Test cases for load_variables function"""
    
    def setUp(self):
        """Set up test fixtures"""
        super().setUp()
        self.fixtures = create_module_fixtures()
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_path = os.path.join(self.temp_dir.name, "test_variables.json")
    
    def tearDown(self):
        """Clean up after tests"""
        super().tearDown()
        # Clean up temporary directory
        self.temp_dir.cleanup()
    
    def test_load_variables_success(self):
        """Test successful loading of variables from a JSON file"""
        # Create a test JSON file
        test_data = self.fixtures['sample_variables']
        with open(self.test_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        # Call function under test
        result = load_variables(self.test_path)
        
        # Assertions
        self.assertEqual(result, test_data)
        self.assertEqual(result["author_name"], "Daniela Cristina")
        self.assertEqual(result["qty"], 100)
        self.assertEqual(result["cost_per_unit"], 150.50)
        
        self.log_case_result("Successfully loads variables from JSON", True)
    
    def test_load_variables_file_not_found(self):
        """Test handling of file not found error"""
        # Use a path that doesn't exist
        non_existent_path = os.path.join(self.temp_dir.name, "doesnt_exist.json")
        
        # Check that it raises the appropriate exception
        with self.assertRaises(FileNotFoundError):
            load_variables(non_existent_path)
        
        self.log_case_result("Correctly raises FileNotFoundError for missing file", True)
    
    def test_load_variables_invalid_json(self):
        """Test handling of invalid JSON"""
        # Create a file with invalid JSON
        with open(self.test_path, 'w', encoding='utf-8') as f:
            f.write("{invalid: json, content}")
        
        # Check that it raises the appropriate exception
        with self.assertRaises(json.JSONDecodeError):
            load_variables(self.test_path)
        
        self.log_case_result("Correctly raises JSONDecodeError for invalid JSON", True)
    
    def test_load_variables_unicode(self):
        """Test loading variables with Unicode characters"""
        # Create a test JSON file with Unicode characters
        test_data = {
            "author_name": "Jôão Çãmpos",
            "special_chars": "àáâãäåæçèéêëìíîï"
        }
        with open(self.test_path, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
        
        # Call function under test
        result = load_variables(self.test_path)
        
        # Assertions
        self.assertEqual(result["author_name"], "Jôão Çãmpos")
        self.assertEqual(result["special_chars"], "àáâãäåæçèéêëìíîï")
        
        self.log_case_result("Successfully handles Unicode characters", True)

class TestFormatNumberPt(BaseTestCase):
    """Test cases for format_number_pt function"""
    
    def test_basic_formatting_with_decimals(self):
        """Test basic number formatting with decimals and default currency symbol"""
        # Case 1: Regular number with decimals
        result = format_number_pt(1234.56)
        self.assertEqual(result, "1.234,56 €")
        self.log_case_result("Regular number with decimals formats correctly", True)
        
        # Case 2: Large number with decimals
        result = format_number_pt(1000000.00)
        self.assertEqual(result, "1.000.000,00 €")
        self.log_case_result("Large number with decimals formats correctly", True)
    
    def test_formatting_without_decimals(self):
        """Test number formatting with show_decimals=False"""
        # Case 1: Regular number without decimals
        result = format_number_pt(1234.56, show_decimals=False)
        self.assertEqual(result, "1.235 €")  # Should round up
        self.log_case_result("Regular number without decimals rounds correctly", True)
        
        # Case 2: Large number without decimals
        result = format_number_pt(1000000, show_decimals=False)
        self.assertEqual(result, "1.000.000 €")
        self.log_case_result("Large number without decimals formats correctly", True)
    
    def test_custom_currency_symbol(self):
        """Test with custom currency symbols"""
        # Case 1: Dollar symbol
        result = format_number_pt(1234.56, currency_symbol="$")
        self.assertEqual(result, "1.234,56 $")
        self.log_case_result("Currency symbol can be changed to dollar", True)
        
        # Case 2: No currency symbol
        result = format_number_pt(1234.56, currency_symbol="")
        self.assertEqual(result, "1.234,56")
        self.log_case_result("Currency symbol can be removed", True)
    
    def test_edge_cases(self):
        """Test edge cases for the function"""
        # Case 1: Zero value
        result = format_number_pt(0)
        self.assertEqual(result, "0,00 €")
        self.log_case_result("Zero value formats correctly", True)
        
        # Case 2: Negative numbers
        result = format_number_pt(-1234.56)
        self.assertEqual(result, "-1.234,56 €")
        self.log_case_result("Negative numbers format correctly", True)
        
        # Case 3: Very large number
        result = format_number_pt(1234567890.12)
        self.assertEqual(result, "1.234.567.890,12 €")
        self.log_case_result("Very large numbers format correctly", True)
        
        # Case 4: Very small decimal
        result = format_number_pt(0.01)
        self.assertEqual(result, "0,01 €")
        self.log_case_result("Very small decimals format correctly", True)
    
    def test_thousands_separators(self):
        """Test correct placement of thousands separators"""
        # Case 1: Four digit number
        result = format_number_pt(1234.56)
        self.assertEqual(result, "1.234,56 €")
        self.log_case_result("Four digit number has correct separator", True)
        
        # Case 2: Five digit number
        result = format_number_pt(12345.67)
        self.assertEqual(result, "12.345,67 €")
        self.log_case_result("Five digit number has correct separator", True)
        
        # Case 3: Six digit number
        result = format_number_pt(123456.78)
        self.assertEqual(result, "123.456,78 €")
        self.log_case_result("Six digit number has correct separator", True)
        
        # Case 4: Seven digit number
        result = format_number_pt(1234567.89)
        self.assertEqual(result, "1.234.567,89 €")
        self.log_case_result("Seven digit number has correct separators", True)

class TestNumToWordsPt(BaseTestCase):
    """Test cases for num_to_words_pt function"""
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_basic_integer_conversion(self, mock_stdout):
        """Test converting basic integers to Portuguese words"""
        # Case 1: Single digit
        result = num_to_words_pt(1)
        self.assertEqual(result, "um")
        self.log_case_result("Single digit converts correctly", True)
        
        # Case 2: Two digits
        result = num_to_words_pt(21)
        self.assertEqual(result, "vinte e um")
        self.log_case_result("Two digit number converts correctly", True)
        
        # Case 3: Three digits
        result = num_to_words_pt(100)
        self.assertEqual(result, "cem")
        self.log_case_result("Three digit number converts correctly", True)
        
        # Case 4: Large number
        result = num_to_words_pt(1234)
        self.assertEqual(result, "mil, duzentos e trinta e quatro")
        self.log_case_result("Four digit number converts correctly", True)
        
        # Case 5: Very large number
        result = num_to_words_pt(1000000)
        self.assertEqual(result, "um milhão")
        self.log_case_result("Large number converts correctly", True)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_decimal_number_conversion(self, mock_stdout):
        """Test converting decimal numbers to Portuguese words"""
        # Case 1: Number with 50 cents
        result = num_to_words_pt(1.50)
        self.assertEqual(result, "um, cinquenta")
        self.log_case_result("Number with 50 cents converts correctly", True)
        
        # Case 2: Number with 1 cent
        result = num_to_words_pt(10.01)
        self.assertEqual(result, "dez, um")
        self.log_case_result("Number with 1 cent converts correctly", True)
        
        # Case 3: Number with 99 cents
        result = num_to_words_pt(100.99)
        self.assertEqual(result, "cem, noventa e nove")
        self.log_case_result("Number with 99 cents converts correctly", True)
        
        # Case 4: Number with zero decimal part
        result = num_to_words_pt(10.00)
        self.assertEqual(result, "dez")
        self.log_case_result("Number with zero decimal part converts correctly", True)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_currency_formatting(self, mock_stdout):
        """Test converting numbers with currency formatting"""
        # Case 1: Singular currency
        result = num_to_words_pt(1, currency="euro")
        self.assertEqual(result, "um euro")
        self.log_case_result("Singular currency formats correctly", True)
        
        # Case 2: Plural currency
        result = num_to_words_pt(2, currency="euro")
        self.assertEqual(result, "dois euros")
        self.log_case_result("Plural currency formats correctly", True)
        
        # Case 3: Currency with decimal part
        result = num_to_words_pt(1.50, currency="euro")
        self.assertEqual(result, "um euro e cinquenta centavos")
        self.log_case_result("Currency with 50 cents formats correctly", True)
        
        # Case 4: Currency with 1 cent
        result = num_to_words_pt(2.01, currency="euro")
        self.assertEqual(result, "dois euros e um centavo")
        self.log_case_result("Currency with 1 cent formats correctly", True)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_special_formatting_cases(self, mock_stdout):
        """Test special formatting cases"""
        # Case 1: Numbers with "mil" followed by hundreds
        result = num_to_words_pt(1101)
        self.assertEqual(result, "mil, cento e um")
        self.log_case_result("Number with 'mil' followed by hundreds formats correctly", True)
        
        # Case 2: Numbers with "mil" not followed by hundreds
        result = num_to_words_pt(1000)
        self.assertEqual(result, "mil")
        self.log_case_result("Number with 'mil' not followed by hundreds formats correctly", True)
        
        # Case 3: Complex case with "mil" in middle
        result = num_to_words_pt(1234567)
        self.assertTrue("mil," in result, f"Expected 'mil,' in result, got {result}")
        self.log_case_result("Complex number with 'mil' formats correctly", True)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_language_parameter(self, mock_stdout):
        """Test language parameter works correctly"""
        # Test Portuguese from Portugal (default)
        result_pt = num_to_words_pt(1)
        self.assertEqual(result_pt, "um")
        
        # Test Portuguese from Brazil
        result_br = num_to_words_pt(1, lang='pt_br')
        self.assertEqual(result_br, "um")
        
        self.log_case_result("Language parameter works correctly", True)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_edge_cases(self, mock_stdout):
        """Test edge cases"""
        # Case 1: Zero
        result = num_to_words_pt(0)
        self.assertEqual(result, "zero")
        self.log_case_result("Zero converts correctly", True)
        
        # Case 2: Negative number
        result = num_to_words_pt(-10)
        self.assertEqual(result, "menos dez")
        self.log_case_result("Negative number converts correctly", True)
        
        # Case 3: Very large number
        result = num_to_words_pt(1000000000)  # 1 billion
        self.assertEqual(result, "mil milhões")
        self.log_case_result("Very large number converts correctly", True)
        
        # Case 4: Invalid input (test exception handling)
        result = num_to_words_pt("not_a_number")
        self.assertEqual(result, "not_a_number")  # Should return the input as string
        self.log_case_result("Invalid input handled correctly", True)

class TestToNumber(BaseTestCase):
    """Test cases for to_number function"""
    
    def test_basic_number_conversion(self):
        """Test basic number conversion"""
        # Case 1: Integer
        result = to_number(100)
        self.assertEqual(result, 100.00)
        self.log_case_result("Integer conversion works correctly", True)
        
        # Case 2: Float with 2 decimal places
        result = to_number(123.45)
        self.assertEqual(result, 123.45)
        self.log_case_result("Float with 2 decimal places works correctly", True)
        
        # Case 3: String number
        result = to_number("50.75")
        self.assertEqual(result, 50.75)
        self.log_case_result("String number conversion works correctly", True)
    
    def test_rounding_behavior(self):
        """Test rounding behavior with Decimal"""
        # Case 1: Round up from 5
        result = to_number(1.005)
        self.assertEqual(result, 1.01)
        self.log_case_result("Rounding up from exactly x.xx5 works correctly", True)
        
        # Case 2: Round down from 4
        result = to_number(1.004)
        self.assertEqual(result, 1.00)
        self.log_case_result("Rounding down from x.xx4 works correctly", True)
        
        # Case 3: Multiple decimal places rounded to 2
        result = to_number(10.12345)
        self.assertEqual(result, 10.12)
        self.log_case_result("Multiple decimal places rounded correctly", True)
    
    def test_edge_cases(self):
        """Test edge cases"""
        # Case 1: Zero
        result = to_number(0)
        self.assertEqual(result, 0.00)
        self.log_case_result("Zero handled correctly", True)
        
        # Case 2: Negative number
        result = to_number(-10.126)
        self.assertEqual(result, -10.13)  # Should round up
        self.log_case_result("Negative number handled correctly", True)
        
        # Case 3: Very small number that rounds to zero
        result = to_number(0.00001)
        self.assertEqual(result, 0.00)
        self.log_case_result("Very small number handled correctly", True)
        
        # Case 4: Large number
        result = to_number(1234567890.123)
        self.assertEqual(result, 1234567890.12)
        self.log_case_result("Large number handled correctly", True)

class TestProcessTotalCost(BaseTestCase):
    """Test cases for process_total_cost function"""
    
    def test_basic_calculation(self):
        """Test basic multiplication calculations"""
        # Case 1: Simple integers
        result = process_total_cost(10, 5)
        self.assertEqual(result, 50)
        self.log_case_result("Simple integer multiplication works correctly", True)
        
        # Case 2: Integer and decimal
        result = process_total_cost(100, 1.5)
        self.assertEqual(result, 150)
        self.log_case_result("Integer and decimal multiplication works correctly", True)
    
    def test_rounding(self):
        """Test rounding behavior"""
        # Case 1: Result with exactly 2 decimal places
        result = process_total_cost(3, 1.11)
        self.assertEqual(result, 3.33)
        self.log_case_result("Result with 2 decimal places works correctly", True)
        
        # Case 2: Result requiring rounding up
        result = process_total_cost(1, 1.005)
        self.assertEqual(result, 1.01)
        self.log_case_result("Rounding up works correctly", True)
        
        # Case 3: Result requiring rounding down
        result = process_total_cost(1, 1.004)
        self.assertEqual(result, 1.00)
        self.log_case_result("Rounding down works correctly", True)
    
    def test_edge_cases(self):
        """Test edge cases"""
        # Case 1: Zero quantity
        result = process_total_cost(0, 10)
        self.assertEqual(result, 0)
        self.log_case_result("Zero quantity works correctly", True)
        
        # Case 2: Zero cost
        result = process_total_cost(10, 0)
        self.assertEqual(result, 0)
        self.log_case_result("Zero cost works correctly", True)
        
        # Case 3: Very large numbers
        result = process_total_cost(1000000, 1000000)
        self.assertEqual(result, 1000000000000)
        self.log_case_result("Very large numbers work correctly", True)
        
        # Case 4: Very small numbers
        result = process_total_cost(0.0001, 0.0001)
        self.assertEqual(result, 0.00)  # Should round to 0.00
        self.log_case_result("Very small numbers work correctly", True)
    
    def test_negative_numbers(self):
        """Test negative number handling"""
        # Case 1: Negative quantity
        result = process_total_cost(-5, 10)
        self.assertEqual(result, -50)
        self.log_case_result("Negative quantity works correctly", True)
        
        # Case 2: Negative cost
        result = process_total_cost(5, -10)
        self.assertEqual(result, -50)
        self.log_case_result("Negative cost works correctly", True)
        
        # Case 3: Both negative (should result in positive)
        result = process_total_cost(-5, -10)
        self.assertEqual(result, 50)
        self.log_case_result("Both negative values work correctly", True)
    
    @patch('backend.generate_docx.to_number')
    def test_uses_to_number_for_rounding(self, mock_to_number):
        """Test that process_total_cost uses to_number for rounding"""
        # Setup mock return value
        mock_to_number.return_value = 42.42
        
        # Call the function
        result = process_total_cost(10, 10)
        
        # Verify to_number was called with the product
        mock_to_number.assert_called_once_with(100)
        
        # Verify result matches what to_number returned
        self.assertEqual(result, 42.42)
        self.log_case_result("Uses to_number for rounding", True)

class TestGetPortugueseMonth(BaseTestCase):
    """Test cases for get_portuguese_month function"""
    
    def test_valid_months(self):
        """Test valid month numbers return correct Portuguese month names"""
        # Case 1: January
        result = get_portuguese_month(1)
        self.assertEqual(result, "janeiro")
        self.log_case_result("January returns correct Portuguese name", True)
        
        # Case 2: March (with special character ç)
        result = get_portuguese_month(3)
        self.assertEqual(result, "março")
        self.log_case_result("March returns correct Portuguese name with special character", True)
        
        # Case 3: December
        result = get_portuguese_month(12)
        self.assertEqual(result, "dezembro")
        self.log_case_result("December returns correct Portuguese name", True)
    
    def test_invalid_months(self):
        """Test invalid month numbers return empty string"""
        # Case 1: Month 0 (invalid)
        result = get_portuguese_month(0)
        self.assertEqual(result, "")
        self.log_case_result("Month 0 returns empty string", True)
        
        # Case 2: Month 13 (invalid)
        result = get_portuguese_month(13)
        self.assertEqual(result, "")
        self.log_case_result("Month 13 returns empty string", True)

class TestGetAvailableTemplates(BaseTestCase):
    """Test cases for get_available_templates function"""
    
    @patch('os.listdir')
    def test_template_extraction(self, mock_listdir):
        """Test that template names are correctly extracted from paths"""
        # Setup mock to return sample file paths
        mock_listdir.return_value = [
            'invoice.docx',
            'contract.docx',
            'report-2023.docx'
        ]
        
        # Call the function
        result = get_available_templates()
        
        # Verify mock was called with the right directory
        mock_listdir.assert_called_once_with('backend/templates/files')
        
        # Verify the result contains the correct template names
        self.assertEqual(result, ['invoice', 'contract', 'report-2023'])
        self.log_case_result("Template names correctly extracted from file paths", True)
    
    @patch('os.listdir')
    def test_empty_directory(self, mock_listdir):
        """Test behavior when no templates are found"""
        # Setup mock to return empty list
        mock_listdir.return_value = []
        
        # Call the function
        result = get_available_templates()
        
        # Verify mock was called
        mock_listdir.assert_called_once_with('backend/templates/files')
        
        # Verify the result is an empty list
        self.assertEqual(result, [])
        self.log_case_result("Empty list returned when no templates exist", True)

class TestGenerateDocument(BaseTestCase):
    """Test cases for generate_document function"""
    
    def setUp(self):
        """Set up test fixtures"""
        super().setUp()
        self.template_name = "invoice"
        self.template_path = "backend/templates/files/invoice.docx"
        self.output_path = "outputs/invoice.docx"
        self.variables = {"author_name": "Test Author", "total_cost": "100,00 €"}
    
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('backend.generate_docx.DocxTemplate')
    def test_successful_document_generation(self, mock_docx_template, mock_makedirs, mock_exists):
        """Test successful document generation"""
        # Setup mocks
        mock_exists.side_effect = lambda path: path == self.template_path  # Template exists, output dir doesn't
        mock_doc = MagicMock()
        mock_docx_template.return_value = mock_doc
        
        # Call the function
        result = generate_document(self.template_name, self.variables, self.output_path)
        
        # Verify template was loaded
        mock_docx_template.assert_called_once_with(self.template_path)
        
        # Verify render was called with variables (should now include enriched variables)
        render_vars = mock_doc.render.call_args[0][0]
        
        # Check that the variables dictionary was enriched with date
        self.assertIn('date', render_vars)
        
        # Verify output directory was created
        mock_makedirs.assert_called_once_with("outputs")
        
        # Verify document was saved
        mock_doc.save.assert_called_once_with(self.output_path)
        
        # Verify function returned True
        self.assertTrue(result)
        self.log_case_result("Document generation success scenario works correctly", True)
    
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('backend.generate_docx.DocxTemplate')
    @patch('backend.generate_docx.datetime')
    @patch('backend.generate_docx.get_portuguese_month')
    def test_date_enrichment(self, mock_get_month, mock_datetime, mock_docx_template, mock_makedirs, mock_exists):
        """Test date enrichment in generate_document"""
        # Setup mocks
        mock_exists.return_value = True
        mock_doc = MagicMock()
        mock_docx_template.return_value = mock_doc
        
        # Mock datetime
        mock_now = MagicMock()
        mock_now.month = 6
        mock_now.year = 2023
        mock_datetime.now.return_value = mock_now
        mock_get_month.return_value = "junho"
        
        # Call the function
        result = generate_document(self.template_name, self.variables, self.output_path)
        
        # Verify date was added
        render_vars = mock_doc.render.call_args[0][0]
        self.assertEqual(render_vars['date'], "junho de 2023")
        self.assertTrue(result)
        self.log_case_result("Date enrichment works correctly", True)
    
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('backend.generate_docx.DocxTemplate')
    @patch('backend.generate_docx.to_number')
    @patch('backend.generate_docx.process_total_cost')
    @patch('backend.generate_docx.num_to_words_pt')
    @patch('backend.generate_docx.format_number_pt')
    def test_cost_enrichment(self, mock_format, mock_words, mock_total_cost, mock_to_number, 
                            mock_docx_template, mock_makedirs, mock_exists):
        """Test cost calculations enrichment in generate_document"""
        # Setup mocks
        mock_exists.return_value = True
        mock_doc = MagicMock()
        mock_docx_template.return_value = mock_doc
        
        # Setup values
        test_vars = {"qty": 10, "cost_per_unit": 20}
        mock_to_number.side_effect = lambda x: float(x)
        mock_total_cost.return_value = 200.0
        mock_words.return_value = "duzentos euros"
        mock_format.side_effect = ["200,00 €", "10,00", "20,00 €"]
        
        # Call the function
        result = generate_document(self.template_name, test_vars, self.output_path)
        
        # Verify cost calculations were added
        render_vars = mock_doc.render.call_args[0][0]
        self.assertEqual(render_vars['total_cost'], "200,00 €")
        self.assertEqual(render_vars['total_cost_words'], "duzentos euros")
        self.assertEqual(render_vars['qty'], "10,00")
        self.assertEqual(render_vars['cost_per_unit'], "20,00 €")
        self.assertTrue(result)
        self.log_case_result("Cost calculations enrichment works correctly", True)
    
    @patch('os.path.exists')
    def test_template_not_found(self, mock_exists):
        """Test behavior when template is not found"""
        # Setup mock to make template not exist
        mock_exists.return_value = False
        
        # Capture stdout to verify error message
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            # Call the function
            result = generate_document(self.template_name, self.variables, self.output_path)
            
            # Verify function returned False
            self.assertFalse(result)
            
            # Verify error message
            output = fake_stdout.getvalue()
            self.assertIn(f"Error: Template '{self.template_name}' not found", output)
        
        self.log_case_result("Template not found scenario works correctly", True)
    
    @patch('os.path.exists')
    @patch('backend.generate_docx.DocxTemplate')
    def test_exception_handling(self, mock_docx_template, mock_exists):
        """Test exception handling during document generation"""
        # Setup mocks
        mock_exists.return_value = True  # Template exists
        mock_doc = MagicMock()
        mock_doc.render.side_effect = Exception("Test error")
        mock_docx_template.return_value = mock_doc
        
        # Capture stdout to verify error message
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            # Call the function
            result = generate_document(self.template_name, self.variables, self.output_path)
            
            # Verify function returned False
            self.assertFalse(result)
            
            # Verify error message
            output = fake_stdout.getvalue()
            self.assertIn("Error generating document: Test error", output)
        
        self.log_case_result("Exception handling works correctly", True)
    
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('backend.generate_docx.DocxTemplate')
    def test_existing_output_directory(self, mock_docx_template, mock_makedirs, mock_exists):
        """Test when output directory already exists"""
        # Setup mocks
        mock_exists.side_effect = lambda path: True  # Both template and output dir exist
        mock_doc = MagicMock()
        mock_docx_template.return_value = mock_doc
        
        # Call the function
        result = generate_document(self.template_name, self.variables, self.output_path)
        
        # Verify makedirs was not called
        mock_makedirs.assert_not_called()
        
        # Verify function returned True
        self.assertTrue(result)
        self.log_case_result("Existing output directory scenario works correctly", True)
    
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('backend.generate_docx.DocxTemplate')
    def test_absolute_path_handling(self, mock_docx_template, mock_makedirs, mock_exists):
        """Test with absolute output path"""
        # Setup
        absolute_path = "/absolute/path/to/document.docx"
        mock_exists.side_effect = lambda path: path == self.template_path  # Template exists, output dir doesn't
        mock_doc = MagicMock()
        mock_docx_template.return_value = mock_doc
        
        # Call the function
        result = generate_document(self.template_name, self.variables, absolute_path)
        
        # Verify output directory was created
        mock_makedirs.assert_called_once_with("/absolute/path/to")
        
        # Verify document was saved to absolute path
        mock_doc.save.assert_called_once_with(absolute_path)
        
        # Verify function returned True
        self.assertTrue(result)
        self.log_case_result("Absolute path handling works correctly", True)
        
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('backend.generate_docx.DocxTemplate')
    def test_variables_not_modified(self, mock_docx_template, mock_makedirs, mock_exists):
        """Test that the original variables dictionary is not modified"""
        # Setup mocks
        mock_exists.return_value = True
        mock_doc = MagicMock()
        mock_docx_template.return_value = mock_doc
        
        # Create a copy of the original variables
        original_vars = self.variables.copy()
        
        # Call the function
        result = generate_document(self.template_name, original_vars, self.output_path)
        
        # Verify that the original variables dictionary is unchanged
        self.assertEqual(original_vars, self.variables)
        self.assertTrue(result)
        self.log_case_result("Original variables dictionary is not modified", True)

if __name__ == '__main__':
    print("\n🔍 Running tests for generate_docx.py...")
    
    # Run the tests with default verbosity
    unittest.main(exit=False, verbosity=0)
    
    # Print summary
    print_summary()
