import functools

def arg_rules(type_: type, max_length: int, contains: list):
    """
    Декоратор-фабрика для перевірки аргументів функції за трьома критеріями:
    - Тип
    - Максимальна довжина
    - Наявність обов’язкових підрядків
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not args:
                print(f"[{func.__name__}] ❌ Валідація неможлива: не передано позиційних аргументів.")
                return False

            arg = args[0]

            if not isinstance(arg, type_):
                print(f"[{func.__name__}] ❌ '{arg}' має бути типу '{type_.__name__}'.")
                return False

            if len(arg) > max_length:
                print(f"[{func.__name__}] ❌ '{arg}' перевищує {max_length} символів (має {len(arg)}).")
                return False

            for symbol in contains:
                if symbol not in arg:
                    print(f"[{func.__name__}] ❌ '{arg}' не містить обов'язкового елементу '{symbol}'.")
                    return False

            return func(*args, **kwargs)
        return wrapper
    return decorator

# --- Приклад використання ---

@arg_rules(type_=str, max_length=15, contains=['05', '@'])
def create_slogan(name: str) -> str:
    return f"{name} drinks pepsi in his brand new BMW!"

# Приклад 1: Виклик з аргументом, що не відповідає правилам (довжина > 15)
print("--- Тестування 'johndoe05@gmail.com' (має повернути False) ---")
result1 = create_slogan('johndoe05@gmail.com')
print(f"Результат: {result1}")
assert result1 is False
print("-" * 50)

# Приклад 2: Виклик з аргументом, що відповідає всім правилам
print("--- Тестування 'S@SH05' (має повернути слоган) ---")
result2 = create_slogan('S@SH05')
print(f"Результат: {result2}")
assert result2 == 'S@SH05 drinks pepsi in his brand new BMW!'
print("-" * 50)

# Додаткові тести
print("--- Додаткове тестування (не містить '@') ---")
result3 = create_slogan('S05_invalid')
print(f"Результат: {result3}")
assert result3 is False
print("-" * 50)

print("--- Додаткове тестування (не містить '05') ---")
result4 = create_slogan('S@SH')
print(f"Результат: {result4}")
assert result4 is False
print("-" * 50)