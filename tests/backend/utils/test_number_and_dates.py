import unittest
import sys
import os
from decimal import Decimal
from datetime import datetime

# Add project root to path to ensure imports work properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from backend.backend.utils.numbers_and_dates import (
    format_number_pt, 
    split_number_parts, 
    num_to_words_pt, 
    get_portuguese_month, 
    process_total_cost,
    to_number,
    process_date,
    process_costs_and_dates
)
from tests._utils.test_utils import BaseTestCase, print_summary

class TestSplitNumberParts(BaseTestCase):
    """Tests for the number parts splitting functionality."""

    def setUp(self):
        super().setUp()

    def test_basic_number_splitting(self):
        """Test basic number splitting with various number types."""
        test_cases = [
            (1000, (1000, 0)),
            (1000.00, (1000, 0)),
            (1234.56, (1234, 56)),
            (0, (0, 0)),
            (-1000, (-1000, 0)),
            (-1234.56, (-1234, 56))
        ]
        
        for number, expected in test_cases:
            try:
                result = split_number_parts(number)
                self.assertEqual(result, expected, 
                               f"Failed to split {number}. Expected {expected}, got {result}")
                self.log_case_result(f"Basic splitting: {number}", True)
            except Exception as e:
                print(f"Error splitting {number}: {str(e)}")
                self.log_case_result(f"Basic splitting: {number}", False)
                self.fail(f"Unexpected error: {str(e)}")

    def test_edge_cases(self):
        """Test edge cases and None value handling."""
        try:
            # Test cases for edge cases
            test_cases = [
                (1e12, (1000000000000, 0)),  # Scientific notation
                (0.0001, (0, 0)),             # Very small number
                (1000.00, (1000, 0)),         # Trailing zeros
                (0, (0, 0)),                  # Zero
                (-1000, (-1000, 0)),          # Negative number
                (None, None)                  # None value
            ]
            
            for number, expected in test_cases:
                if number is None:
                    with self.assertRaises(TypeError):
                        split_number_parts(number)
                else:
                    result = split_number_parts(number)
                    self.assertEqual(result, expected)
            
            self.log_case_result("Edge cases", True)
            
        except Exception as e:
            self.log_case_result("Edge cases", False, str(e))
            raise

class TestNumberFormatting(BaseTestCase):
    """Tests for the Portuguese number formatting functionality."""

    def setUp(self):
        super().setUp()

    def test_basic_number_formatting(self):
        """Test basic number formatting with various number types."""
        test_cases = [
            (1000, "1.000,00 €"),
            (1000000, "1.000.000,00 €"),
            (0, "0,00 €"),
            (-1000, "-1.000,00 €"),
            (-1234.56, "-1.234,56 €")
        ]
        
        for number, expected in test_cases:
            try:
                result = format_number_pt(number)
                self.assertEqual(result, expected, 
                               f"Failed to format {number}. Expected {expected}, got {result}")
                self.log_case_result(f"Basic formatting: {number}", True)
            except Exception as e:
                print(f"Error formatting {number}: {str(e)}")
                self.log_case_result(f"Basic formatting: {number}", False)
                self.fail(f"Unexpected error: {str(e)}")

    def test_decimal_places(self):
        """Test decimal places handling."""
        try:
            # Test cases for decimal places
            test_cases = [
                (1234.56, True, "1.234,56 €"),  # With decimals
                (1234.56, False, "1.234 €"),     # Without decimals
                (1000.00, True, "1.000,00 €"),   # Whole number with decimals
                (1000.00, False, "1.000 €"),     # Whole number without decimals
                (0.00, True, "0,00 €"),          # Zero with decimals
                (0.00, False, "0 €"),            # Zero without decimals
                (-1234.56, True, "-1.234,56 €"), # Negative with decimals
                (-1234.56, False, "-1.234 €")    # Negative without decimals
            ]
            
            for number, show_decimals, expected in test_cases:
                try:
                    result = format_number_pt(number, show_decimals=show_decimals)
                    self.assertEqual(result, expected, 
                                   f"Failed to format {number} with show_decimals={show_decimals}. "
                                   f"Expected {expected}, got {result}")
                    self.log_case_result(f"Decimal places: {number} (show_decimals={show_decimals})", True)
                except Exception as e:
                    print(f"Error formatting {number}: {str(e)}")
                    self.log_case_result(f"Decimal places: {number} (show_decimals={show_decimals})", False)
                    self.fail(f"Unexpected error: {str(e)}")
            
        except Exception as e:
            self.log_case_result("Decimal places", False, str(e))
            raise

    def test_currency_symbols(self):
        """Test number formatting with different currency symbols."""
        test_cases = [
            (1000, "€", "1.000,00 €"),
            (1000, "$", "1.000,00 $"),
            (1000, "£", "1.000,00 £"),
            (1000, "", "1.000,00"),
            (1000, "€€", "1.000,00 €€")
        ]
        
        for number, symbol, expected in test_cases:
            try:
                result = format_number_pt(number, currency_symbol=symbol)
                self.assertEqual(result, expected, 
                               f"Failed to format {number} with symbol '{symbol}'. "
                               f"Expected {expected}, got {result}")
                self.log_case_result(f"Currency symbol: {number} ({symbol})", True)
            except Exception as e:
                print(f"Error formatting {number}: {str(e)}")
                self.log_case_result(f"Currency symbol: {number} ({symbol})", False)
                self.fail(f"Unexpected error: {str(e)}")

    def test_edge_cases(self):
        """Test number formatting with edge cases."""
        test_cases = [
            (1e12, "1.000.000.000.000,00 €"),  # Very large number
            (0.0001, "0,00 €"),  # Very small number
            (1.23e-4, "0,00 €"),  # Scientific notation
            (1000.0, "1.000,00 €"),  # Zero decimal places
            (1000.00, "1.000,00 €"),  # Trailing zeros
            (1000.001, "1.000,00 €")  # Rounding
        ]
        
        for number, expected in test_cases:
            try:
                result = format_number_pt(number)
                self.assertEqual(result, expected, 
                               f"Failed to format edge case {number}. Expected {expected}, got {result}")
                self.log_case_result(f"Edge case: {number}", True)
            except Exception as e:
                print(f"Error formatting edge case {number}: {str(e)}")
                self.log_case_result(f"Edge case: {number}", False)
                self.fail(f"Unexpected error: {str(e)}")
        
        # Test None value separately to expect TypeError
        try:
            format_number_pt(None)
            self.fail("Expected TypeError for None value")
        except TypeError as e:
            self.log_case_result("None value handling", True)
        except Exception as e:
            self.log_case_result("None value handling", False)
            self.fail(f"Expected TypeError, got {type(e).__name__}: {str(e)}")

    def test_formatting_rules(self):
        """Test specific formatting rules for Portuguese numbers."""
        test_cases = [
            (1000, "1.000,00 €"),  # Thousand separator
            (1000000, "1.000.000,00 €"),  # Multiple thousand separators
            (1234.56, "1.234,56 €"),  # Decimal separator
            (1000.00, "1.000,00 €"),  # Currency symbol placement
            (1000, "1.000,00 €")  # Space between number and currency
        ]
        
        for number, expected in test_cases:
            try:
                result = format_number_pt(number)
                self.assertEqual(result, expected, 
                               f"Failed to format {number} according to Portuguese rules. "
                               f"Expected {expected}, got {result}")
                self.log_case_result(f"Formatting rules: {number}", True)
            except Exception as e:
                print(f"Error formatting {number}: {str(e)}")
                self.log_case_result(f"Formatting rules: {number}", False)
                self.fail(f"Unexpected error: {str(e)}")

class TestNumberToWords(BaseTestCase):
    """Test number to words conversion functionality."""
    
    def test_basic_number_conversion(self):
        """Test basic number to words conversion."""
        try:
            # Test cases for basic numbers
            test_cases = [
                (0, "zero"),
                (1, "um"),
                (10, "dez"),
                (100, "cem"),
                (1000, "mil"),
                (1000000, "um milhão"),
                (1000000000, "mil milhões"),  # Updated to match Portuguese convention
                (-1, "menos um"),
                (-1000, "menos mil")
            ]
            
            for number, expected in test_cases:
                result = num_to_words_pt(number)
                self.assertEqual(result, expected)
                self.log_case_result(f"Basic number: {number}", True)
            
        except Exception as e:
            self.log_case_result("Basic number conversion", False)
            raise
    
    def test_decimal_numbers(self):
        """Test numbers with decimal parts."""
        try:
            # Test cases for decimal numbers
            test_cases = [
                (1.23, "um, vinte e três"),
                (1000.50, "mil, cinquenta"),
                (0.01, "zero, um"),
                (1.00, "um"),
                (1000.00, "mil")
            ]
            
            for number, expected in test_cases:
                result = num_to_words_pt(number)
                self.assertEqual(result, expected)
                self.log_case_result(f"Decimal number: {number}", True)
            
        except Exception as e:
            self.log_case_result("Decimal numbers", False)
            raise
    
    def test_currency_conversion(self):
        """Test number to words with currency."""
        try:
            # Test cases for currency
            test_cases = [
                (1, "um euro"),
                (2, "dois euros"),
                (1.50, "um euro e cinquenta centavos"),
                (2.50, "dois euros e cinquenta centavos"),
                (1000, "mil euros"),
                (1000.01, "mil euros e um centavo")
            ]
            
            for number, expected in test_cases:
                result = num_to_words_pt(number, currency="euro")
                self.assertEqual(result, expected)
                self.log_case_result(f"Currency: {number}", True)
            
        except Exception as e:
            self.log_case_result("Currency conversion", False)
            raise
    
    def test_special_cases(self):
        """Test special cases and edge cases."""
        try:
            # Test cases for special cases
            test_cases = [
                (1e12, "um bilião"),  # Scientific notation
                (0.0001, "zero"),  # Very small number
                (1000.999, "mil"),  # Rounding to 2 decimal places
                (1000000.00, "um milhão"),  # Whole number with trailing zeros
                (1000000.01, "um milhão, um")  # Large number with small decimal
            ]
            
            for number, expected in test_cases:
                result = num_to_words_pt(number)
                self.assertEqual(result, expected)
                self.log_case_result(f"Special case: {number}", True)
            
        except Exception as e:
            self.log_case_result("Special cases", False)
            raise

class TestPortugueseMonth(BaseTestCase):
    """Test Portuguese month name conversion functionality."""
    
    def test_month_conversion(self):
        """Test conversion of month numbers to Portuguese names."""
        try:
            # Test cases for all months
            test_cases = [
                (1, "janeiro"),
                (2, "fevereiro"),
                (3, "março"),
                (4, "abril"),
                (5, "maio"),
                (6, "junho"),
                (7, "julho"),
                (8, "agosto"),
                (9, "setembro"),
                (10, "outubro"),
                (11, "novembro"),
                (12, "dezembro")
            ]
            
            for month_number, expected in test_cases:
                result = get_portuguese_month(month_number)
                self.assertEqual(result, expected)
                self.log_case_result(f"Month: {month_number}", True)
            
        except Exception as e:
            self.log_case_result("Month conversion", False)
            raise

class TestProcessTotalCost(BaseTestCase):
    """Test total cost calculation functionality."""
    
    def test_basic_calculations(self):
        """Test basic cost calculations with whole and decimal numbers."""
        try:
            # Test cases for basic calculations
            test_cases = [
                (2, 10, 20.00),      # Simple whole numbers
                (2.5, 10.5, 26.25),  # Decimal numbers
                (1000, 1000, 1000000.00),  # Large numbers
                (2.5, 2.5, 6.25)     # Numbers that would normally round differently
            ]
            
            for qty, cost_per_unit, expected in test_cases:
                result = process_total_cost(qty, cost_per_unit)
                self.assertEqual(result, expected)
                self.log_case_result(f"Basic calculation: {qty} * {cost_per_unit}", True)
            
        except Exception as e:
            self.log_case_result("Basic calculations", False)
            raise
    
    def test_precision_handling(self):
        """Test handling of numbers that would result in repeating decimals."""
        try:
            # Test cases for precision handling
            test_cases = [
                (1/3, 3, 1.00),      # Repeating decimal
                (2/3, 3, 2.00),      # Repeating decimal
                (1.333333, 3, 4.00), # Many decimal places
                (1.666666, 3, 5.00)  # Many decimal places
            ]
            
            for qty, cost_per_unit, expected in test_cases:
                result = process_total_cost(qty, cost_per_unit)
                self.assertEqual(result, expected)
                self.log_case_result(f"Precision handling: {qty} * {cost_per_unit}", True)
            
        except Exception as e:
            self.log_case_result("Precision handling", False)
            raise
    
    def test_exact_decimal_places(self):
        """Test numbers that result in exactly 1 or 2 decimal places."""
        try:
            # Test cases for exact decimal places
            test_cases = [
                (2, 10.5, 21.00),    # Exactly 2 decimal places
                (2, 10.25, 20.50),   # Exactly 2 decimal places
                (2, 10.1, 20.20),    # Exactly 1 decimal place
                (2, 10.05, 20.10)    # Exactly 1 decimal place
            ]
            
            for qty, cost_per_unit, expected in test_cases:
                result = process_total_cost(qty, cost_per_unit)
                self.assertEqual(result, expected)
                self.log_case_result(f"Exact decimal places: {qty} * {cost_per_unit}", True)
            
        except Exception as e:
            self.log_case_result("Exact decimal places", False)
            raise
    
    def test_input_validation(self):
        """Test handling of invalid inputs."""
        try:
            # Test cases for invalid inputs
            invalid_inputs = [
                (None, 10),
                (2, None),
                (None, None),
                ("2", 10),
                (2, "10"),
                ("2", "10"),
                ("", 10),
                (2, "")
            ]
            
            for qty, cost_per_unit in invalid_inputs:
                with self.assertRaises(TypeError):
                    process_total_cost(qty, cost_per_unit)
                self.log_case_result(f"Invalid input handling: {qty}, {cost_per_unit}", True)
            
        except Exception as e:
            self.log_case_result("Input validation", False)
            raise

class TestToNumber(BaseTestCase):
    """Test number conversion and rounding functionality."""
    
    def test_basic_conversions(self):
        """Test basic number conversions with various number types."""
        try:
            # Test cases for basic conversions
            test_cases = [
                (100, 100.00),           # Whole number
                (100.5, 100.50),         # Simple decimal
                (100.00, 100.00),        # Trailing zeros
                (100.000, 100.00),       # Many trailing zeros
                (100.001, 100.00),       # Small decimal
                (100.999, 101.00)        # Rounding up
            ]
            
            for input_value, expected in test_cases:
                result = to_number(input_value)
                self.assertEqual(result, expected)
                self.log_case_result(f"Basic conversion: {input_value}", True)
            
        except Exception as e:
            self.log_case_result("Basic conversions", False)
            raise
    
    def test_precision_and_rounding(self):
        """Test precision handling and rounding rules."""
        try:
            # Test cases for precision and rounding
            test_cases = [
                (2.5, 2.50),             # Exactly 2.5
                (2.55, 2.55),            # No rounding needed
                (2.555, 2.56),           # Round up
                (2.554, 2.55),           # Round down
                (2.5555, 2.56),          # Multiple decimal places
                (1/3, 0.33),             # Repeating decimal
                (2/3, 0.67)              # Repeating decimal
            ]
            
            for input_value, expected in test_cases:
                result = to_number(input_value)
                self.assertEqual(result, expected)
                self.log_case_result(f"Precision/rounding: {input_value}", True)
            
        except Exception as e:
            self.log_case_result("Precision and rounding", False)
            raise
    
    def test_input_types(self):
        """Test conversion from different input types."""
        try:
            # Test cases for different input types
            test_cases = [
                ("100", 100.00),         # String integer
                ("100.5", 100.50),       # String decimal
                ("100.00", 100.00),      # String with trailing zeros
                (100, 100.00),           # Integer
                (100.5, 100.50),         # Float
                (Decimal("100.5"), 100.50)  # Decimal
            ]
            
            for input_value, expected in test_cases:
                result = to_number(input_value)
                self.assertEqual(result, expected)
                self.log_case_result(f"Input type: {type(input_value).__name__}", True)
            
        except Exception as e:
            self.log_case_result("Input types", False)
            raise
    
    def test_edge_cases(self):
        """Test handling of edge cases."""
        try:
            # Test cases for edge cases
            test_cases = [
                (0, 0.00),               # Zero
                (-100, -100.00),         # Negative number
                (-100.5, -100.50),       # Negative decimal
                (1e12, 1000000000000.00),  # Scientific notation
                (1.23e-4, 0.00)          # Small scientific notation
            ]
            
            for input_value, expected in test_cases:
                result = to_number(input_value)
                self.assertEqual(result, expected)
                self.log_case_result(f"Edge case: {input_value}", True)
            
            # Test infinity values separately
            with self.assertRaises(ValueError):
                to_number(float('inf'))
            with self.assertRaises(ValueError):
                to_number(float('-inf'))
            self.log_case_result("Infinity handling", True)
            
        except Exception as e:
            self.log_case_result("Edge cases", False)
            raise

class TestProcessDate(BaseTestCase):
    """Test date processing functionality."""
    
    def test_date_formatting(self):
        """Test that dates are formatted correctly in Portuguese style."""
        try:
            # Get current date
            now = datetime.now()
            expected_month = get_portuguese_month(now.month)
            expected_year = now.year
            
            # Test with empty dictionary
            variables = {}
            result = process_date(variables)
            
            # Check the date format
            self.assertIn('date', result)
            self.assertEqual(result['date'], f"{expected_month} de {expected_year}")
            self.log_case_result("Basic date formatting", True)
            
        except Exception as e:
            self.log_case_result("Date formatting", False)
            raise
    
    def test_month_name_validation(self):
        """Test that month names are valid Portuguese with proper formatting."""
        try:
            # Test with empty dictionary
            variables = {}
            result = process_date(variables)
            
            # Get the month name from the result
            month_name = result['date'].split(' de ')[0]
            
            # Check month name properties
            self.assertTrue(month_name.islower())  # Should be lowercase
            self.assertIn(month_name, [
                "janeiro", "fevereiro", "março", "abril", "maio", "junho",
                "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
            ])
            self.log_case_result("Month name validation", True)
            
        except Exception as e:
            self.log_case_result("Month name validation", False)
            raise
    
    def test_variables_handling(self):
        """Test that the function properly handles input variables."""
        try:
            # Test with existing variables
            variables = {
                'existing_var': 'value',
                'another_var': 123
            }
            original_variables = variables.copy()
            
            # Process the date
            result = process_date(variables)
            
            # Check that original variables are preserved
            self.assertEqual(result['existing_var'], original_variables['existing_var'])
            self.assertEqual(result['another_var'], original_variables['another_var'])
            
            # Check that a new dictionary was created
            self.assertIsNot(result, variables)
            
            # Check that the date was added
            self.assertIn('date', result)
            self.log_case_result("Variables handling", True)
            
        except Exception as e:
            self.log_case_result("Variables handling", False)
            raise

class TestProcessCostsAndDates(BaseTestCase):
    """Test cost and date processing functionality."""
    
    def test_basic_cost_processing(self):
        """Test basic cost calculations and formatting."""
        try:
            # Test with simple numbers
            variables = {
                'qty': 2,
                'cost_per_unit': 10
            }
            result = process_costs_and_dates(variables)
            
            # Check all required fields are present
            self.assertIn('total_cost', result)
            self.assertIn('total_cost_words', result)
            self.assertIn('qty', result)
            self.assertIn('cost_per_unit', result)
            self.assertIn('date', result)
            
            # Check values
            self.assertEqual(result['total_cost'], "20,00 €")
            self.assertEqual(result['total_cost_words'], "vinte euros")
            self.assertEqual(result['qty'], "2,00")
            self.assertEqual(result['cost_per_unit'], "10,00 €")
            
            self.log_case_result("Basic cost processing", True)
            
        except Exception as e:
            self.log_case_result("Basic cost processing", False)
            raise
    
    def test_decimal_numbers(self):
        """Test handling of decimal numbers."""
        try:
            # Test with decimal numbers
            variables = {
                'qty': 2.5,
                'cost_per_unit': 10.5
            }
            result = process_costs_and_dates(variables)
            
            # Check values
            self.assertEqual(result['total_cost'], "26,25 €")
            self.assertEqual(result['total_cost_words'], "vinte e seis euros e vinte e cinco centavos")
            self.assertEqual(result['qty'], "2,50")
            self.assertEqual(result['cost_per_unit'], "10,50 €")
            
            self.log_case_result("Decimal numbers", True)
            
        except Exception as e:
            self.log_case_result("Decimal numbers", False)
            raise
    
    def test_missing_cost_variables(self):
        """Test behavior when cost variables are missing."""
        try:
            # Test with missing variables
            variables = {
                'other_var': 'value'
            }
            result = process_costs_and_dates(variables)
            
            # Check that only date is added
            self.assertIn('date', result)
            self.assertIn('other_var', result)
            self.assertEqual(result['other_var'], 'value')
            
            # Check that cost fields are not present
            self.assertNotIn('total_cost', result)
            self.assertNotIn('total_cost_words', result)
            self.assertNotIn('qty', result)
            self.assertNotIn('cost_per_unit', result)
            
            self.log_case_result("Missing cost variables", True)
            
        except Exception as e:
            self.log_case_result("Missing cost variables", False)
            raise
    
    def test_large_numbers(self):
        """Test handling of large numbers."""
        try:
            # Test with large numbers
            variables = {
                'qty': 1000000,
                'cost_per_unit': 1000000
            }
            result = process_costs_and_dates(variables)
            
            # Check values
            self.assertEqual(result['total_cost'], "1.000.000.000.000,00 €")
            self.assertEqual(result['qty'], "1.000.000,00")
            self.assertEqual(result['cost_per_unit'], "1.000.000,00 €")
            
            self.log_case_result("Large numbers", True)
            
        except Exception as e:
            self.log_case_result("Large numbers", False)
            raise
    
    def test_input_preservation(self):
        """Test that input dictionary is not modified."""
        try:
            # Test with existing variables
            variables = {
                'qty': 2,
                'cost_per_unit': 10,
                'existing_var': 'value'
            }
            original_variables = variables.copy()
            
            # Process the variables
            result = process_costs_and_dates(variables)
            
            # Check that original variables are preserved
            self.assertEqual(variables, original_variables)
            
            # Check that result is a new dictionary
            self.assertIsNot(result, variables)
            
            # Check that existing variables are in result
            self.assertEqual(result['existing_var'], 'value')
            
            self.log_case_result("Input preservation", True)
            
        except Exception as e:
            self.log_case_result("Input preservation", False)
            raise

if __name__ == "__main__":
    # Run tests
    unittest.main(exit=False)
    
    # Print summary
    print_summary() 