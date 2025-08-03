import functools
import time


def logger(func):
    """
    Декоратор, що логує:
    - ім’я функції
    - аргументи
    - результат
    - час виконання
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = map(repr, args)
        kwargs_repr = (f"{k}={v!r}" for k, v in kwargs.items())
        signature = ", ".join([*args_repr, *kwargs_repr])

        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed = end_time - start_time

        print(f"[LOG] {func.__name__}({signature}) → {result!r} (executed in {elapsed:.6f}s)")
        return result

    return wrapper

# --- Демонстрація ---

@logger
def add(x, y):
    return x + y

@logger
def square_all(*args):
    return [arg ** 2 for arg in args]

@logger
def say_hello(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print("--- add(4, 5) ---")
add(4, 5)

print("\n--- square_all(1, 2, 3, 4) ---")
square_all(1, 2, 3, 4)

print("\n--- say_hello('Alice', greeting='Hi') ---")
say_hello("Alice", greeting="Hi")

print("\n--- add(x=20, y=10) ---")
add(y=10, x=20)