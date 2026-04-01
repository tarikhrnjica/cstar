import numpy as np

PauliX = np.array([[0, 1], [1, 0]])
PauliY = np.array([[0, -1j], [1j, 0]])
PauliZ = np.array([[1, 0], [0, -1]])
PauliI = np.array([[1, 0], [0, 1]])

__all__ = ["PauliX", "PauliY", "PauliZ", "PauliI"]
