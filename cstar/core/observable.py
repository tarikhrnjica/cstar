import numpy as np

from cstar import ObstructionError, _get_current_context
from cstar.core import Sieve


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
        current_ctx = _get_current_context()

        # 1. Check Context Availability
        # If we are in a context, and this observable is NOT in it:
        if current_ctx and (self not in current_ctx.observables):
            # This is the "Category Error"
            # We cannot formulate this proposition here.
            dim = current_ctx.observables[0].matrix.shape[0]
            return Sieve.Undefined(dim, current_ctx)

        # 2. Standard Logic (same as before)
        evals, evecs = np.linalg.eigh(self.matrix)
        indices = np.where(np.isclose(evals, eigenvalue))[0]

        if len(indices) == 0:
            return Sieve.Min(self.matrix.shape[0], current_ctx)

        P = np.zeros_like(self.matrix)
        for idx in indices:
            v = evecs[:, idx].reshape(-1, 1)
            P += v @ v.conj().T

        return Sieve(P, current_ctx)
