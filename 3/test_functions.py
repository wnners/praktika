
import pytest
from functions import validate_password, safe_divide





def test_valid_password_basic():

    assert validate_password('Password1') == True


def test_valid_password_long():
    assert validate_password('MyP@ss99word') == True


def test_password_too_short():
    assert validate_password('Pass1') == False


def test_password_no_digit():
    
    assert validate_password('Password') == False


def test_password_no_letter():

    assert validate_password('12345678') == False


def test_password_has_space():

    assert validate_password('Pass 123') == False


def test_password_empty_string():

    assert validate_password('') == False


def test_password_exactly_8_chars():
    
    assert validate_password('Passw0rd') == True






@pytest.mark.parametrize('password, expected', [
    ('Password1',  True),
    ('Pass1',      False),
    ('Password',   False),
    ('12345678',   False),
    ('Pass 123',   False),
    ('Passw0rd',   True),
])
def test_password_parametrized(password, expected):
    assert validate_password(password) == expected


def test_divide_basic():
    assert safe_divide(10, 2) == 5.0


def test_divide_floats():
    assert safe_divide(7.5, 2.5) == 3.0


def test_divide_by_zero_returns_none():
    
    assert safe_divide(10, 0) is None


def test_divide_zero_numerator():
    assert safe_divide(0, 5) == 0.0


def test_divide_negative():
    
    assert safe_divide(-9, 3) == -3.0


def test_divide_non_integer_result():

    assert safe_divide(5, 2) == 2.5


def test_divide_type_error():
    with pytest.raises(TypeError):
        safe_divide('abc', 2)

