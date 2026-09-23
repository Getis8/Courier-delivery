"""
value_objects.py

Завдання 1. Незмінний об'єкт-значення.

Реалізовано два класи з однаковою поведінкою:

    Weight   — незмінність зроблена вручну через __slots__ і
               перевизначений __setattr__ (пункт 1.1);
    WeightDC — та сама поведінка, отримана "безкоштовно" за допомогою
               декоратора @dataclass(frozen=True, slots=True) (пункт 1.2).

Обидва класи представляють вагу посилки в грамах.
"""

from dataclasses import dataclass
from functools import total_ordering


# ---------------------------------------------------------------------------
# 1.1 Ручна реалізація незмінності
# ---------------------------------------------------------------------------
@total_ordering
class Weight:
    """Незмінний об'єкт-значення "вага посилки" (у грамах)."""

    __slots__ = ("grams", "_frozen")

    def __init__(self, grams: float) -> None:
        # На етапі ініціалізації обходимо власну заборону __setattr__,
        # звертаючись напряму до object.__setattr__.
        object.__setattr__(self, "grams", grams)
        # Прапорець виставляємо ОСТАННІМ — доки його немає, __setattr__
        # ще дозволяє присвоєння (див. нижче).
        object.__setattr__(self, "_frozen", True)

    # -- заборона зміни атрибутів після створення -------------------------
    def __setattr__(self, name, value):
        if getattr(self, "_frozen", False):
            raise AttributeError("об'єкт Weight незмінний")
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        # Видаляти поля теж не можна — об'єкт повністю незмінний.
        raise AttributeError("об'єкт Weight незмінний")

    # -- рядкові подання (1.3) ---------------------------------------------
    def __repr__(self) -> str:
        return f"Weight(grams={self.grams!r})"

    def __str__(self) -> str:
        return f"{self.grams} г"

    # -- порівняння та впорядкування (1.4) ----------------------------------
    def __eq__(self, other):
        if not isinstance(other, Weight):
            return NotImplemented
        return self.grams == other.grams

    def __lt__(self, other):
        if not isinstance(other, Weight):
            return NotImplemented
        return self.grams < other.grams

    # -- хешованість (1.5) ---------------------------------------------------
    def __hash__(self) -> int:
        return hash(self.grams)


# ---------------------------------------------------------------------------
# 1.2 Альтернативна реалізація через @dataclass(frozen=True, slots=True)
# ---------------------------------------------------------------------------
@total_ordering
@dataclass(frozen=True, slots=True)
class WeightDC:
    """
    Той самий об'єкт-значення "вага посилки", але отриманий за допомогою
    dataclass. frozen=True сам генерує __setattr__/__delattr__, що
    підіймають dataclasses.FrozenInstanceError (підклас AttributeError)
    при спробі зміни; slots=True додає __slots__ і забороняє нові
    атрибути. __eq__ та __hash__ dataclass теж генерує сам (за полями),
    а __lt__ і __repr__ дописуємо самі, бо це не типова поведінка
    dataclass "з коробки".
    """

    grams: float

    def __repr__(self) -> str:
        return f"WeightDC(grams={self.grams!r})"

    def __str__(self) -> str:
        return f"{self.grams} г"

    def __lt__(self, other):
        if not isinstance(other, WeightDC):
            return NotImplemented
        return self.grams < other.grams
