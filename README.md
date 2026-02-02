# C* Language

This recreational and highly experimental project aims to construct a domain-agnostic, logic-centric programming language for quantum computers. Built as a Python embedded DSL, it explores how standard circuit manipulation can be replaced by the **Grothendieck-Isham topos** framework.

## Background

The name C* (pronounced "C-Star") is both, a lighthearted pun relating it to the lineage of C languages, as well as an explicit nod to the C*-algebras that power it mathematically.

## Introduction

As quantum computers scale, it becomes convenient to transition from an imperative ("do this") approach to a more declarative ("make this true") paradigm. Rather than scheduling quantum gates manually, similar to writing Assembly, we wish to rely on a compiler to "glue" together our desired truths into a valid (globally consistent) quantum circuit. This shift in perspective turns an instruction like *"Apply Hadamard to the given qubit"* into the request *"Ensure my system is entangled in a Bell state"*.

## Syntax

Conceptually, C* abstracts away the Hilbert space. Developers declare logical truths within **context windows** into the quantum system, scoped by `with` blocks.

```py
# 1. Initialize the topos
qubits = System(n=2)

# 2. Define context windows
# "I speak the language of Z-axis spin"
ctx_z = Context("Z", [PauliZ]) 

# 3. Specify the logic
with ctx_z:
    # This is a local section of the presheaf
    spin_up = (qubits.measure() == +1)

# 4. Switch the context (Daseinisation)
# "Transport this truth to a new context"
with Context("X", [PauliX]):
    # The compiler automatically projects 'spin_up' to the X-basis
    # resulting in a "Sieve" (a partial truth). The tilde denotes taking
    # the adjoint
    uncertain_truth = ~spin_up
```

## Types

The type system mirrors the **Bohr topos** of Isham-Döring.

### Primitives

Data is not treated as fixed values, but as contextual fields &mdash; mappings defined over the topology of contexts.

- `System`: The topos defining the physical substrate (qudit).
- `Context`: A commutative subalgebra of operators. This represents a classical snapshot where all observables commute and the logic stays Boolean.
- `Observable<Context>`: A physical quantity (operator) definable within the specified context.
- `State`: A global section of the spectral presheaf (the quantum state seen from all possible angles).

### Logical

Instead of `bool`, we use the `Sieve` type. This reflects the switch from propositional logic in a Boolean algebra to intuitionistic logic in a Heyting algebra.

- `Sieve(Context)`: The core logical unit. A sieve is a topological set indicating *where* in the context graph (measurement setup) a specific statement holds.
- `True`: The maximal sieve (identity): universally true in all contexts (e.g., global constants).
- `False`: The minimal sieve (empty set): true in no context.
- `Undefined`: Symbolizes a proposition that cannot be formulated in the current context (such as asking for the precise position value while observing momentum).

## Casting

An important feature of C* is **daseinisation**, which handles type casting between incompatible quantum contexts.

This mechanism leverages the partial ordering of contexts ($V \subseteq U$). When a variable defined in context $U$ (e.g., position) is accessed in context $V$ (e.g., momentum), standard physics says the value is undefined. In C*, the compiler traverses the context lattice to conduct **spectral projection**:

- **Outer daseinisation** ($\delta^0$): Approximates the proposition from **above** in the lattice. It poses the question: "What is the smallest property in context $V$ that is consistent with (fully encloses) the truth in context $U$?" This often results in a "fuzzy" or coarse-grained sieve.
- **Inner daseinisation** ($\delta^i$): Approximates the proposition from **below** in the lattice. It poses the question: "What property in context $V$ is guaranteed by (fully contained in) context $U$?".

This allows the program to deal with Heisenberg uncertainty not as a runtime error, but as a logical constraint (lattice approximation) during compile-time.

## Compilation

The C* compiler does not merely transliterate source code into gate sequences; it acts as a **homological geometer**. By viewing your program as a topology, it finds the global section that satisfies your constraints.

More formally, the compiler constitutes a functor $\mathcal{F}: \mathcal{V}(\mathcal{H}) \to \mathrm{Circ}$ between the category of contexts and the category of quantum circuits, mapping categorical logic into physical operations. 

### Steps

#### 1. Graph wiring

The compiler starts by assembling the **cover's nerve**, a simplicial complex where

- **Nodes** are the `Context` instances that appear in your code.
- **Edges** correspond to the intersections of contexts (shared observables).
- **Faces** represent triple intersections.

#### 2. Spectral analysis

Next, the compiler populates this graph with local data. For every context node $V$, it computes the **Gelfand spectrum** $\Sigma_V$ of the operators defined there, thus producing the spectral presheaf $\underline{\Sigma}$.

#### 3. Cohomology validation

Before generating a quantum gate, the compiler calculates the **sheaf cohomology group** $H^1(\mathcal{N}(\mathcal{U}), \underline{\Sigma})$ of your logic using the combinatorial Laplacian $\Delta_0$.

- If $H^1 = 0$ the logic is consistent; a global section $s$ exists such that $\delta_s = 0$, i.e., all local truths are fulfilled.
- Otherwise, the cohomology is obstructed. A paradox such as the Kochen-Specker contradiction occurred, where local truths form a "Möbius strip" that cannot be flattened into a valid state.

This prevents the construction of physically impossible circuits by raising a compilation error.

#### 4. Circuit synthesis

If the logic is valid, the geometer proceeds to minimize the **Dirichlet energy** $\braket{s, \Delta s}$ of the graph and finally generates the morphism in the target category:

$$
\mathcal{F}(V \xrightarrow{i} U) = U_{gate}
$$

In other words, it solves for the optimal path of unitary gates (basis rotations) required to transport the state between contexts with minimal information loss.

### Quantum Error Correction

The mechanism C* uses to verify logic (cohomology check) is isomorphic to the **surface code** (or toric code) that hardware uses to correct errors.


|C* Compiler (Software)|Surface Code (Hardware)|Homological Connection                 |
|----------------------|-----------------------|---------------------------------------|
|Logic graph           |Qubit lattice          |Manifold or simplicial complex         |
|Inconsistency         |Bit-flip error         |Chain $C_1$                            |
|Validation check      |Stabilizer measurement |Boundary operator ($\partial / \delta$)|
|Constraint violation  |Syndrome (anyon)       |Boundary and coboundary                |
|Logical paradox       |Logical error          |Nontrivial homology cycle              |

In a surface code, the decoder identifies syndromes (topological defects) and attempts to pair them off to restore the vacuum state. C* generalizes this by considering logical inconsistencies in your source code as **semantic syndromes**. The compiler essentially behaves like a high-level QEC decoder, making sure that the topology of your *concepts* is free of obstructions before the program ever touches the physical qubits.

### Self-Hosting

For small systems, the cohomology checks can run on a classical CPU. However, the number of possible contexts grows exponentially in the number of qubits, rendering classical verification intractable.

Hence C* is designed to be bootstrapped on a QPU to compile its own logic:

1. Step 3 requires inverting the Laplacian matrix. While classically this is $O(N^3)$, the **Harrow–Hassidim–Lloyd (HHL) algorithm** can perform this in $O(\log N)$ time.
2. Step 2 depends on diagonalization. The **quantum phase estimation (QPE) algorithm** replaces classical eigendecomposition, collapsing wavefunctions into their spectral components natively.

This creates a recursive hierarchy where the quantum state *is* the logic graph, "cooled" to its ground state (consistent logic) via quantum annealing or variational circuits.
