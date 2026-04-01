from cstar.compiler.daseinisation import project
from cstar.core import Context, System
from cstar.math.operators import PauliX, PauliZ


def main():
    # 1. Initialize the topos
    qubits = System(n=1)

    # 2. Define contexts
    ctx_z = Context("Z", [PauliZ])
    ctx_x = Context("X", [PauliX])

    # 3. Specify the logic (Lazy Evaluation)
    with ctx_z:
        # Appends to DAG, doesn't execute immediately
        spin_up = qubits.measure() == 1.0
        print(f"Defined constraint in Z: {spin_up}")

    # 4. Change the context (Daseinisation)
    with ctx_x:
        # Map Z-truth to X-basis
        maybe_spin_up = project(spin_up, ctx_x)
        print(f"Projected Sieve in X: {maybe_spin_up}")

        # Apply intuitionistic logic in the new context
        inverted = ~maybe_spin_up
        print(f"Adjoint Sieve in X: {inverted}")

    # 5. Compile the DAG
    qubits.compile()


if __name__ == "__main__":
    main()
