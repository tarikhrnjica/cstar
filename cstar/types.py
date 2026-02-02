from typing import List, Optional

import numpy as np

_CONTEXT_STACK = []


class ObstructionError(SyntaxError):
    """Raised when physical constraints (commutativity, cohomology) are violated."""

    pass


class Observable:
    """
    Represents a physical observable (Hermitian operator).
    In C*, data is not a value, but an operator awaiting a context.
    """

    def __init__(self, name: str, matrix: np.ndarray):
        self.name = name
        self.matrix = np.array(matrix, dtype=complex)

        if not np.allclose(self.matrix, self.matrix.conj().T):
            raise ObstructionError(f"Observable '{name}' is not Hermitian.")

    def __repr__(self):
        return f"<Observable: {self.name}>"

    def __eq__(self, eigenvalue: float) -> "Sieve":
        """
        Creates a Sieve representing the proposition (Observable == val).
        Mathematically: Returns the Spectral Projector for this eigenvalue.
        """
        evals, evecs = np.linalg.eigh(self.matrix)

        indices = np.where(np.isclose(evals, eigenvalue))[0]

        if len(indices) == 0:
            return Sieve.Empty()

        P = np.zeros_like(self.matrix)
        for idx in indices:
            v = evecs[:, idx].reshape(-1, 1)
            P += v @ v.conj().T

        return Sieve(projector=P, context=_get_current_context())


class Context:
    """
    A commutative subalgebra of operators.
    Represents a 'Classical Snapshot' or measurement setup.
    """

    def __init__(self, name: str, observables: List[Observable]):
        self.name = name
        self.observables = observables
        self._validate_commutativity()

    def _validate_commutativity(self):
        """
        Enforce the Law of the Subalgebra:
        All operators within a context must commute ([A, B] = 0).
        """
        for i, op_a in enumerate(self.observables):
            for op_b in self.observables[i + 1 :]:
                comm = op_a.matrix @ op_b.matrix - op_b.matrix @ op_a.matrix
                if not np.allclose(comm, 0, atol=1e-9):
                    raise ObstructionError(
                        f"Context '{self.name}' is invalid. "
                        f"'{op_a.name}' and '{op_b.name}' do not commute."
                    )

    def __repr__(self):
        return f"<Context: {self.name}>"

    def __enter__(self):
        _CONTEXT_STACK.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _CONTEXT_STACK.pop()


def _get_current_context() -> Optional[Context]:
    return _CONTEXT_STACK[-1] if _CONTEXT_STACK else None


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


class System:
    def __init__(self, n_qubits: int):
        self.dim = 2**n_qubits

    def measure(self) -> Observable:
        """
        Returns a placeholder observable representing the
        active measurement in the current context.
        """
        ctx = _get_current_context()
        if not ctx:
            raise ObstructionError("Cannot measure outside a Context.")
        return ctx.observables[0]

    @property
    def Min(self):
        """The Minimal Truth for this system."""
        return Sieve.Min(self.dim)

    @property
    def Max(self):
        """The Maximal Truth for this system."""
        return Sieve.Max(self.dim)
