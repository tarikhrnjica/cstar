from cstar import ObstructionError, _get_current_context
from cstar.core import Observable, Sieve


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
