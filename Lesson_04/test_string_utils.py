import pytest
from string_utils import StringUtils

class TestStringUtils:
    def setup_method(self):
        self.utils = StringUtils()

    # Тесты для метода capitalize
    def test_capitalize_positive(self):
        assert self.utils.capitalize("skypro") == "Skypro"

    def test_capitalize_empty_string(self):
        assert self.utils.capitalize("") == ""

    def test_capitalize_single_char(self):
        assert self.utils.capitalize("a") == "A"

    def test_capitalize_already_capitalized(self):
        assert self.utils.capitalize("Skypro") == "Skypro"

    # Тесты для метода trim
    def test_trim_positive(self):
        assert self.utils.trim("   skypro") == "skypro"

    def test_trim_no_leading_spaces(self):
        assert self.utils.trim("skypro") == "skypro"

    def test_trim_only_spaces(self):
        assert self.utils.trim("    ") == ""

    def test_trim_empty_string(self):
        assert self.utils.trim("") == ""

    def test_trim_trailing_spaces(self):
        assert self.utils.trim("skypro   ") == "skypro   "

    # Тесты для метода contains
    def test_contains_positive(self):
        assert self.utils.contains("SkyPro", "S") is True

    def test_contains_negative(self):
        assert self.utils.contains("SkyPro", "U") is False

    def test_contains_empty_symbol(self):
        assert self.utils.contains("SkyPro", "") is True

    def test_contains_empty_string(self):
        assert self.utils.contains("", "S") is False

    def test_contains_substring(self):
        assert self.utils.contains("SkyPro", "ky") is True

    # Тесты для метода delete_symbol
    def test_delete_symbol_positive(self):
        assert self.utils.delete_symbol("SkyPro", "k") == "SyPro"

    def test_delete_symbol_substring(self):
        assert self.utils.delete_symbol("SkyPro", "Pro") == "Sky"

    def test_delete_symbol_not_found(self):
        assert self.utils.delete_symbol("SkyPro", "X") == "SkyPro"

    def test_delete_symbol_empty_symbol(self):
        assert self.utils.delete_symbol("SkyPro", "") == "SkyPro"

    def test_delete_symbol_empty_string(self):
        assert self.utils.delete_symbol("", "S") == ""