def validate_password(password):
    if len(password) < 8:
        return False
    if ' ' in password:
        return False
    has_digit = any(c.isdigit() for c in password)
    has_letter = any(c.isalpha() for c in password)
    return has_digit and has_letter




def safe_divide(a, b):
    return a / b  
