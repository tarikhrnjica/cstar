import numpy as np

from cstar.core.context import Context
from cstar.core.sieve import Sieve


def project(source_sieve: Sieve, target_context: Context) -> Sieve:
    """
    Outer Daseinisation (delta^0).
    Finds the smallest property in the target context that fully encloses
    the truth of the source sieve.
    """
    source_basis = source_sieve.context.basis[:, source_sieve.mask]
    target_mask = np.zeros(target_context.basis.shape[1], dtype=bool)

    for i in range(target_context.basis.shape[1]):
        v_i = target_context.basis[:, i]

        for j in range(source_basis.shape[1]):
            u_j = source_basis[:, j]
            overlap = np.abs(np.vdot(v_i, u_j))

            if overlap > 1e-6:
                target_mask[i] = True
                break

    return Sieve(target_context, target_mask)


__all__ = ["project"]
