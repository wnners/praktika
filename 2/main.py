def add(a, b):
    return a + b
def divide(a, b):
    if b == 0:
        return None
    return a / b
def is_palindrome(s):
    return s == s[::-1]

assert add(2, 3) == 5
print('TC-01: PASS — add(2, 3) = 5')

assert add(-1, 5) == 4
print('TC-02: PASS — add(-1, 5) = 4')

assert add(-3, -7) == -10
print('TC-03: PASS — add(-3, -7) = -10')

assert add(0, 0) == 0
print('TC-04: PASS — add(0, 0) = 0')

assert divide(10, 2) == 5
print('TC-05: PASS — divide(10, 2) = 5.0')

assert divide(10, 0) is None
print('TC-06: PASS — divide(10, 0) = None')

assert divide(-9, 3) == 3
print('TC-07: PASS — divide(-9, 3) = -3.0')

assert divide(0, 5) == 0
print('TC-08: PASS — divide(0, 5) = 0.0')

assert is_palindrome('level') == True
print('TC-09: PASS — level является палиндромом')

assert is_palindrome('hello') == False
print('TC-10: PASS — hello не является палиндромом')

result = is_palindrome('Level')
if result != True:
    print('TC-11: FAIL — BUG-01: регистр не игнорируется!')
    print('        Получено:', result, '| Ожидалось: True')
else:
    print('TC-11: PASS')

assert is_palindrome('') == True
print('TC-12: PASS — пустая строка = палиндром')


print()
print('Тестирование завершено. 11 PASS, 1 FAIL (BUG-01)')
