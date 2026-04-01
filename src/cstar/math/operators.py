from typing import List, Tuple

import numpy as np

PauliX = np.array([[0, 1], [1, 0]])
PauliY = np.array([[0, -1j], [1j, 0]])
PauliZ = np.array([[1, 0], [0, -1]])
PauliI = np.array([[1, 0], [0, 1]])


def simultaneous_diagonalization(
    operators: List[np.ndarray],
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes the common eigenbasis for a set of mutually commuting Hermitian matrices.

    Args:
        operators: A list of commuting Hermitian matrices (numpy arrays).

    Returns:
        basis: A 2D array where columns are the common eigenvectors.
        eigenvalues: A 2D array of shape (num_operators, num_eigenvectors) containing
                     the corresponding eigenvalues for each operator in the context.
    """
    if not operators:
        raise ValueError("Cannot diagonalize an empty set of operators.")

    dim = operators[0].shape[0]

    # 1. Verify commutation (Optional but recommended for compile-time safety)
    # For a production compiler, you might want to bypass this for speed if
    # the algebra is pre-validated, but it's crucial for catching bad context definitions.
    for i in range(len(operators)):
        for j in range(i + 1, len(operators)):
            commutator = operators[i] @ operators[j] - operators[j] @ operators[i]
            if not np.allclose(commutator, 0, atol=1e-6):
                raise ValueError(
                    f"Operators at index {i} and {j} do not commute. Invalid Context."
                )

    # 2. Construct a random linear combination to break degeneracies.
    # We use a fixed seed to ensure deterministic compiler behavior across runs.
    rng = np.random.default_rng(seed=42)
    coeffs = rng.uniform(0.1, 1.0, size=len(operators))

    composite_op = sum(c * op for c, op in zip(coeffs, operators))

    # 3. Diagonalize the composite Hermitian operator
    _, basis = np.linalg.eigh(composite_op)

    # 4. Extract the eigenvalues for each individual operator in this shared basis
    # Because they commute, the basis diagonalizes all of them: V^\dagger A V = D
    eigenvalues = np.zeros((len(operators), dim))

    for i, op in enumerate(operators):
        # Apply the basis transformation
        diag_matrix = basis.conj().T @ op @ basis

        # Extract the diagonal. We take the real part as observables must be Hermitian.
        eigenvalues[i] = np.real(np.diag(diag_matrix))

    # Round to avoid floating point noise from the transformation
    return basis, np.round(eigenvalues, decimals=5)


__all__ = ["PauliX", "PauliY", "PauliZ", "PauliI", "simultaneous_diagonalization"]
