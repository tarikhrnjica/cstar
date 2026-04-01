from typing import List, Protocol, Tuple

import numpy as np

from cstar.core.context import Context
from cstar.core.sieve import Sieve


class SystemProtocol(Protocol):
    dag: List[Tuple[str, Context, Sieve]]


class Measurement:
    """A symbolic object that overloads operators to build compile-time constraints."""

    def __init__(self, system: SystemProtocol, context: Context):
        self.system = system
        self.context = context

    def __eq__(self, value: float) -> Sieve:  # type: ignore
        """
        Operator overload for `==`.
        Acts as a functional assertion rather than a boolean check.
        """
        mask = np.isclose(self.context.eigenvalues, value)
        sieve = Sieve(self.context, mask)

        # Append this constraint to the compiler's logical DAG
        self.system.dag.append(("ASSERT", self.context, sieve))
        return sieve


__all__ = ["Measurement"]
