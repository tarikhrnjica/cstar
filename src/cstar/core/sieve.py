import numpy as np

from cstar.core.context import Context


class Sieve:
    """The core unit of intuitionistic logic (a topological subset)."""

    def __init__(self, context: Context, mask: np.ndarray):
        self.context = context
        self.mask = mask.astype(bool)

    def __and__(self, other: "Sieve") -> "Sieve":
        if self.context != other.context:
            raise TypeError(
                "Cannot intersect Sieves from different contexts. Cast first."
            )
        return Sieve(self.context, self.mask & other.mask)

    def __or__(self, other: "Sieve") -> "Sieve":
        if self.context != other.context:
            raise TypeError("Cannot union Sieves from different contexts. Cast first.")
        return Sieve(self.context, self.mask | other.mask)

    def __invert__(self) -> "Sieve":
        # Local adjoint (pseudo-complement)
        return Sieve(self.context, ~self.mask)

    def __repr__(self) -> str:
        return f"Sieve({self.context.name}, {self.mask})"


__all__ = ["Sieve"]
