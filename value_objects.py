"""
value_objects.py

Завдання 1. Незмінний об'єкт-значення.

Weight — незмінний об'єкт-значення "вага посилки" (у грамах).
Незмінність зроблена вручну: __slots__ + перевизначений __setattr__.
"""

from functools import total_ordering


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
