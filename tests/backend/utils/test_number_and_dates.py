import unittest
import sys
import os

# Add project root to path to ensure imports work properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from backend.backend.utils.numbers_and_dates import format_number_pt, split_number_parts
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


if __name__ == "__main__":
    # Run tests
    unittest.main(exit=False)
    
    # Print summary
    print_summary() 