def validate_password(password):
    """
    Проверяет пароль по правилам:
    - минимум 8 символов
    - минимум 1 цифра
    - минимум 1 буква
    - без пробелов
    """
    if len(password) < 8:
        return False
    if ' ' in password:
        return False
    has_digit = any(c.isdigit() for c in password)
    has_letter = any(c.isalpha() for c in password)
    return has_digit and has_letter




def safe_divide(a, b):
    return a / b  
