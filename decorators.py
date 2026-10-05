"""
decorators.py

Завдання 5. Валідаційний декоратор.

validated(**rules) — декоратор із параметрами: для кожного іменованого
аргумента методу задається правило перевірки. Складається з трьох
рівнів вкладених функцій: validated (приймає правила) -> decorator
(приймає функцію) -> wrapper (власне перевіряє аргументи й викликає
функцію). Метадані обгорнутого методу (ім'я, докстрінг тощо)
зберігаються через functools.wraps.

Підтримані правила:
    "positive"       — значення є числом і строго більше за нуль;
    "non_empty"      — значення є рядком, який після strip() не порожній;
    "one_of:a,b,c"   — значення належить переліченій множині варіантів.

Приклад:
    @validated(name="non_empty", mass="positive", kind="one_of:rocky,gas")
    def add_planet(self, *, name, mass, kind):
        ...
"""

import functools

_ONE_OF_PREFIX = "one_of:"


def _check_rule(arg_name: str, rule: str, value) -> None:
    if rule == "positive":
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
            raise ValueError(
                f"аргумент '{arg_name}' повинен бути додатним числом "
                f"(отримано {value!r})"
            )
    elif rule == "non_empty":
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"аргумент '{arg_name}' не може бути порожнім рядком "
                f"(отримано {value!r})"
            )
    elif rule.startswith(_ONE_OF_PREFIX):
        allowed = rule[len(_ONE_OF_PREFIX):].split(",")
        if value not in allowed:
            raise ValueError(
                f"аргумент '{arg_name}' повинен бути одним із {allowed} "
                f"(отримано {value!r})"
            )
    else:
        raise ValueError(f"невідоме правило валідації для '{arg_name}': {rule!r}")


def validated(**rules):
    """Декоратор-фабрика: приймає правила перевірки іменованих аргументів."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for arg_name, rule in rules.items():
                if arg_name in kwargs:
                    _check_rule(arg_name, rule, kwargs[arg_name])
            return func(*args, **kwargs)

        return wrapper

    return decorator
