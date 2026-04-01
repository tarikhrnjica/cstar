from typing import Dict, List, Set, Tuple

from cstar.compiler.daseinisation import project
from cstar.core.context import Context
from cstar.core.sieve import Sieve


class SpectralPresheaf:
    """
    Constructs the contravariant functor representing the spectral presheaf.
    Maps contexts (the base category) to their topological spectra, and defines
    the restriction morphisms between them.
    """

    def __init__(self, dag: List[Tuple[str, Context, Sieve]]):
        self.dag = dag
        self.contexts: Dict[str, Context] = {}
        self.local_sections: Dict[str, List[Sieve]] = {}

        self._build_base_space()
        self._bind_local_sections()

    def _build_base_space(self):
        """Extracts all unique contexts from the DAG to form the poset base."""
        for _, context, _ in self.dag:
            if context.name not in self.contexts:
                self.contexts[context.name] = context
                self.local_sections[context.name] = []

    def _bind_local_sections(self):
        """Assigns the developer's logical assertions to their respective topological fibers."""
        for op, context, sieve in self.dag:
            if op == "ASSERT":
                self.local_sections[context.name].append(sieve)

    def is_subalgebra(self, V: Context, U: Context) -> bool:
        """
        Determines the partial ordering V ⊆ U.
        V is a subalgebra if all its observables are contained within U.
        """
        v_ops: Set[str] = set(V.operator_names)
        u_ops: Set[str] = set(U.operator_names)
        return v_ops.issubset(u_ops)

    def restriction_map(self, U: Context, V: Context, sieve_u: Sieve) -> Sieve:
        """
        The contravariant morphism res_{U,V} : Σ_U -> Σ_V.

        If V ⊆ U, we can restrict a truth from the larger context U
        down to the smaller context V. In the Bohr topos, this restriction
        is achieved via Outer Daseinisation (spectral projection).
        """
        if not self.is_subalgebra(V, U):
            raise ValueError(
                f"Restriction map fails: Context '{V.name}' is not a valid "
                f"subalgebra of '{U.name}'."
            )

        # Apply the projection logic to map the sieve across the boundary
        restricted_sieve = project(sieve_u, V)
        return restricted_sieve

    def evaluate_consistency(self) -> bool:
        """
        Performs a preliminary local consistency check across the restriction maps.
        Ensures that intersecting truths do not immediately annihilate each other
        (i.e., evaluate to Sieve.Min) before we even reach the global cohomology check.
        """
        ctx_list = list(self.contexts.values())

        for i, U in enumerate(ctx_list):
            for V in ctx_list[i + 1 :]:
                # Check both directions for subalgebra relationships
                if self.is_subalgebra(V, U):
                    larger, smaller = U, V
                elif self.is_subalgebra(U, V):
                    larger, smaller = V, U
                else:
                    continue  # No direct restriction map exists; handled later by cohomology

                # Restrict all sections from the larger context to the smaller one
                for section in self.local_sections[larger.name]:
                    restricted = self.restriction_map(larger, smaller, section)

                    # Intersect the restricted section with native sections in the smaller context
                    for native_section in self.local_sections[smaller.name]:
                        combined = restricted & native_section

                        # If the intersection is the empty set (Sieve.Min), we have a local paradox
                        if not combined.mask.any():
                            print(
                                f"Syntax Error: Local logical contradiction detected "
                                f"between contexts {larger.name} and {smaller.name}."
                            )
                            return False

        return True
