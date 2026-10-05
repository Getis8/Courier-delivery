from dataclasses import dataclass
from functools import total_ordering
 
 
# ---------------------------------------------------------------------------
# 1.1 Ручна реалізація незмінності
# ---------------------------------------------------------------------------
@total_ordering
class Weight:
    __slots__ = ("grams", "_frozen")
 
    def __init__(self, grams: float) -> None:
        object.__setattr__(self, "grams", grams)
        object.__setattr__(self, "_frozen", True)
 
    def __setattr__(self, name, value):
        if getattr(self, "_frozen", False):
            raise AttributeError("об'єкт Weight незмінний")
        object.__setattr__(self, name, value)
 
    def __delattr__(self, name):
        raise AttributeError("об'єкт Weight незмінний")
 
    def __repr__(self) -> str:
        return f"Weight(grams={self.grams!r})"
 
    def __str__(self) -> str:
        return f"{self.grams} г"
 
    def __eq__(self, other):
        if not isinstance(other, Weight):
            return NotImplemented
        return self.grams == other.grams
 
    def __lt__(self, other):
        if not isinstance(other, Weight):
            return NotImplemented
        return self.grams < other.grams
 
    def __hash__(self) -> int:
        return hash(self.grams)
 
    # -- арифметика (4.2) -----------------------------------------------------
    def __add__(self, other: "Weight") -> "Weight":
        if not isinstance(other, Weight):
            return NotImplemented
        return Weight(self.grams + other.grams)
 
    def __sub__(self, other: "Weight") -> "Weight":
        if not isinstance(other, Weight):
            return NotImplemented
        difference = self.grams - other.grams
        if difference < 0:
            raise ValueError(
                "результат віднімання ваг не може бути від'ємним "
                f"({self} - {other} < 0)"
            )
        return Weight(difference)
 
    def __mul__(self, factor):
        if not isinstance(factor, (int, float)) or isinstance(factor, bool):
            return NotImplemented
        return Weight(self.grams * factor)
 
    def __rmul__(self, factor):
        return self.__mul__(factor)
 
 
# ---------------------------------------------------------------------------
# 1.2 Альтернативна реалізація через @dataclass(frozen=True, slots=True)
# ---------------------------------------------------------------------------
@total_ordering
@dataclass(frozen=True, slots=True)
class WeightDC:
    grams: float
 
    def __repr__(self) -> str:
        return f"WeightDC(grams={self.grams!r})"
 
    def __str__(self) -> str:
        return f"{self.grams} г"
 
    def __lt__(self, other):
        if not isinstance(other, WeightDC):
            return NotImplemented
        return self.grams < other.grams