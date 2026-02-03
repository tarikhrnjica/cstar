import numpy as np

from cstar.core import Context


class Sieve:
    def __init__(
        self, projector: np.ndarray, context: Context = None, is_undefined: bool = False
    ):
        self.projector = projector
        self.context = context
        self._is_undefined = is_undefined

    @classmethod
    def Undefined(cls, dim: int, context: Context = None):
        """
        Represents a logical category error.
        Example: Asking for Position inside a Momentum context.
        """
        # We use a zero matrix as placeholder, but the flag is what matters.
        return cls(np.zeros((dim, dim)), context, is_undefined=True)

    @classmethod
    def Min(cls, dim: int, context: Context = None):
        """False / Bottom"""
        return cls(np.zeros((dim, dim)), context)

    @classmethod
    def Max(cls, dim: int, context: Context = None):
        """True / Top"""
        return cls(np.eye(dim), context)

    def __repr__(self):
        if self._is_undefined:
            return "<Sieve: Undefined (Context Mismatch)>"

        dim_trace = np.trace(self.projector).real
        # Check for Max/Min constants for cleaner printing
        dims = self.projector.shape[0]
        if np.isclose(dim_trace, dims):
            return "<Sieve: True (Max)>"
        if np.isclose(dim_trace, 0):
            return "<Sieve: False (Min)>"

        return f"<Sieve: dim={dim_trace:.1f} in {self.context.name}>"

    # --- Three-Valued Logic (Propagating Undefined) ---

    def __invert__(self):
        if self._is_undefined:
            return self  # ~Undefined is still Undefined

        id = np.eye(self.projector.shape[0])
        return Sieve(id - self.projector, self.context)

    def __and__(self, other: "Sieve"):
        # Poison logic: If any part is undefined, the intersection is undefined.
        if self._is_undefined or other._is_undefined:
            return Sieve.Undefined(self.projector.shape[0], self.context)

        return Sieve(self.projector @ other.projector, self.context)

    def __or__(self, other: "Sieve"):
        # Poison logic: Undefined | True is typically Undefined in strict verification
        if self._is_undefined or other._is_undefined:
            return Sieve.Undefined(self.projector.shape[0], self.context)

        p, q = self.projector, other.projector
        return Sieve(p + q - p @ q, self.context)
