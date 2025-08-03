import functools
import string

def stop_words(words: list):
    """
    Декоратор, який замінює стоп-слова на '*', зберігаючи пунктуацію.
    Не використовує регулярні вирази.
    """
    stop_words_lower = set(word.lower() for word in words)
    punctuation = set(string.punctuation)

    def strip_trailing_punct(word):
        """Відокремлює всі символи пунктуації в кінці слова."""
        i = len(word)
        while i > 0 and word[i-1] in punctuation:
            i -= 1
        return word[:i], word[i:]

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if not isinstance(result, str):
                return result

            words_with_spaces = result.split(" ")
            censored = []

            for word in words_with_spaces:
                base_word, trailing_punct = strip_trailing_punct(word)
                if base_word.lower() in stop_words_lower:
                    censored.append("*" + trailing_punct)
                else:
                    censored.append(word)

            return " ".join(censored)
        return wrapper

    return decorator

# --- Приклад використання ---

@stop_words(['pepsi', 'BMW'])
def create_slogan(name: str) -> str:
    return f"{name} drinks Pepsi in his brand new BMW!"

assert create_slogan("Steve") == "Steve drinks * in his brand new *!"
print("✅ Test 1 passed.")

@stop_words(['pepsi', 'BMW'])
def create_slogan_with_punctuation(name: str) -> str:
    return f"{name} drinks Pepsi! In his brand new BMW..."

assert create_slogan_with_punctuation("Steve") == "Steve drinks *! In his brand new *..."
print("✅ Test 2 with punctuation passed.")