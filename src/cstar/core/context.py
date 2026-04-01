from typing import Dict, Optional

import numpy as np

from cstar.math.operators import simultaneous_diagonalization

# Global state to track the active context window for the AST builder
_ACTIVE_CONTEXT: Optional["Context"] = None


def get_active_context() -> Optional["Context"]:
    """Retrieves the currently scoped context."""
    return _ACTIVE_CONTEXT


class Context:
    """A commutative subalgebra representing a specific topological window."""

    def __init__(self, name: str, operators: Dict[str, np.ndarray]):
        """
        Args:
            name: Identifier for the context (e.g., "Z1_Z2").
            operators: Mapping of an observable's name to its matrix representation.
        """
        self.name = name
        self.operator_names = list(operators.keys())
        self.operator_matrices = list(operators.values())

        # Compute the Gelfand spectrum (the topological base space)
        self.basis, eigenvalues_matrix = simultaneous_diagonalization(
            self.operator_matrices
        )

        # Map each observable to its spectrum over the common basis
        self.spectra: Dict[str, np.ndarray] = {
            name: eigenvalues_matrix[i] for i, name in enumerate(self.operator_names)
        }

    def get_spectrum(self, name: str) -> np.ndarray:
        if name not in self.spectra:
            raise KeyError(
                f"Observable '{name}' is not defined in context '{self.name}'."
            )
        return self.spectra[name]

    def __enter__(self):
        global _ACTIVE_CONTEXT
        self.previous_context = _ACTIVE_CONTEXT
        _ACTIVE_CONTEXT = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _ACTIVE_CONTEXT
        _ACTIVE_CONTEXT = self.previous_context


__all__ = ["Context", "get_active_context"]
