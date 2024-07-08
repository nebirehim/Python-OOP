"""
Tests the validator functions
Command line: python -m pytest tests/test_validators.py
"""
import pytest

from database.validator import validate_integer


class TestIntegerValidator:
    def test_valid_integer(self):
        validate_integer('arg', 10, 0, 20, 'custom min msg', 'custom max msg')

    def test_type_error(self):
        with pytest.raises(TypeError):
            validate_integer('arg', 1.5)

    def test_min_std_error_msg(self):
        with pytest.raises(ValueError) as ex:
            validate_integer('arg', 10, 100)
        assert 'arg' in str(ex.value)
        assert '100' in str(ex.value)

    def test_min_custom_error_msg(self):
        with pytest.raises(ValueError) as ex:
            validate_integer('arg', 10, 100, custom_max_message='custom')
        assert str(ex.value) == 'custom'

    def test_max_std_error_msg(self):
        with pytest.raises(ValueError) as ex:
            validate_integer('arg', 10, 1, 5)
        assert 'arg' in str(ex.value)

    def test_max_custom_error_msg(self):
        with pytest.raises(ValueError) as ex:
            validate_integer('arg', 10, 1, 5, custom_max_message='custom')
        assert str(ex.value) == 'custom'
