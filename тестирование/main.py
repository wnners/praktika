
def add(a, b):
    return a + b
def divide(a, b):
    if b == 0:
        return None
    return a / b
def is_palindrome(s):
    return s == s[::-1]
assert add(2, 3) == 5, "Ошибка: 2+3 должно быть 5"
print("TC-01: PASS — сложение 2+3=5")

assert add(-1, 5) == 4, "Ошибка: -1+5 должно быть 4"
print("TC-02: PASS — сложение -1+5=4")

assert divide(10, 0) is None, "Ошибка: деление на 0 должно вернуть None"
print("TC-03: PASS — деление на 0 защищено")

assert divide(10, 2) == 5, "Ошибка: 10/2 должно быть 5"
print("TC-04: PASS — деление 10/2=5")

assert is_palindrome("level") == True, "Ошибка: level — палиндром"
print("TC-05: PASS — 'level' является палиндромом")

assert is_palindrome("hello") == False, "Ошибка: hello — не палиндром"
print("TC-06: PASS — 'hello' не является палиндромом")

print("\nВсе тест-кейсы пройдены успешно!")