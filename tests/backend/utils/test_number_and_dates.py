import unittest
import sys
import os

# Add project root to path to ensure imports work properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from backend.backend.utils.numbers_and_dates import format_number_pt, split_number_parts, num_to_words_pt, get_portuguese_month, process_total_cost
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

if __name__ == "__main__":
    # Run tests
    unittest.main(exit=False)
    
    # Print summary
    print_summary() 