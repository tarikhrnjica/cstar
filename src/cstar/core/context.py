from typing import List, Optional

import numpy as np

# Global state to track the active context window for the AST builder
_ACTIVE_CONTEXT: Optional["Context"] = None


def get_active_context() -> Optional["Context"]:
    """Retrieves the currently scoped context."""
    return _ACTIVE_CONTEXT


class Context:
    """A commutative subalgebra representing a specific topological window."""

    def __init__(self, name: str, operators: List[np.ndarray]):
        self.name = name
        self.operators = operators

        # Determine the Gelfand spectrum (simultaneous eigenbasis).
        eigenvalues, eigenvectors = np.linalg.eigh(self.operators[0])
        self.eigenvalues = np.round(eigenvalues, 5)
        self.basis = eigenvectors
        self.previous_context: Optional["Context"] = None

    def __enter__(self) -> "Context":
        global _ACTIVE_CONTEXT
        self.previous_context = _ACTIVE_CONTEXT
        _ACTIVE_CONTEXT = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _ACTIVE_CONTEXT
        _ACTIVE_CONTEXT = self.previous_context


__all__ = ["Context", "get_active_context"]
