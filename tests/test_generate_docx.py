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

# Setup path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, current_dir)

# Import base test utilities
from _utils.test_utils import BaseTestCase, print_summary

# Import the module we want to test
from generate_docx import load_variables, format_number_pt, num_to_words_pt, process_total_cost

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

if __name__ == '__main__':
    print("\n🔍 Running tests for generate_docx.py...")
    
    # Run the tests with default verbosity
    unittest.main(exit=False, verbosity=0)
    
    # Print summary
    print_summary()
