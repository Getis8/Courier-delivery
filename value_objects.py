from dataclasses import dataclass
from functools import total_ordering


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
