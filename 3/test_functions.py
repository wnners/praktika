# test_functions.py


import pytest
from functions import validate_password, safe_divide




# ============================================
# Тесты для validate_password()
# ============================================


def test_valid_password_basic():
    # TC-01: обычный корректный пароль
    assert validate_password('Password1') == True


def test_valid_password_long():
    # TC-02: длинный пароль со спецсимволами
    assert validate_password('MyP@ss99word') == True


def test_password_too_short():
    # TC-03: меньше 8 символов
    assert validate_password('Pass1') == False


def test_password_no_digit():
    # TC-04: нет цифры
    assert validate_password('Password') == False


def test_password_no_letter():
    # TC-05: только цифры
    assert validate_password('12345678') == False


def test_password_has_space():
    # TC-06: есть пробел
    assert validate_password('Pass 123') == False


def test_password_empty_string():
    # TC-07: пустая строка
    assert validate_password('') == False


def test_password_exactly_8_chars():
    # TC-08: ровно 8 символов — граница
    assert validate_password('Passw0rd') == True




# ============================================
# Параметризованный тест для validate_password
# ============================================


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




# ============================================
# Тесты для safe_divide()
# ============================================


def test_divide_basic():
    # TC-09: обычное деление
    assert safe_divide(10, 2) == 5.0


def test_divide_floats():
    # TC-10: дробные числа
    assert safe_divide(7.5, 2.5) == 3.0


def test_divide_by_zero_returns_none():
    # TC-11: деление на ноль — ключевой тест
    assert safe_divide(10, 0) is None


def test_divide_zero_numerator():
    # TC-12: ноль в числителе
    assert safe_divide(0, 5) == 0.0


def test_divide_negative():
    # TC-13: отрицательное число
    assert safe_divide(-9, 3) == -3.0


def test_divide_non_integer_result():
    # TC-14: нецелый результат
    assert safe_divide(5, 2) == 2.5




# ============================================
# Тест на исключение (TypeError)
# ============================================


def test_divide_type_error():
    # При передаче строки Python бросает TypeError
    with pytest.raises(TypeError):
        safe_divide('abc', 2)

