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

Data is not treated as fixed values, but as functions over the topology of contexts.

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

An important feature of C* is **daseinisation** (German for "being there"), which handles type casting between incompatible quantum contexts.

When a variable defined in context $A$ (e.g., position) is accessed in context $B$ (e.g., momentum), standard physics says the value is undefined. In C*, the compiler performs **spectral projection** to approximate the truth.

- **Outer daseinisation** ($\delta^0$): Approximates the proposition from the outside. It poses the question: "What is the smallest property in context $B$ that is consistent with the truth in context $A$?" This often results in a "fuzzy" or coarse-grained sieve.
- **Inner daseinisation** ($\delta^i$): Approximates the proposition from the inside. It poses the question: "What property in context $B$ is guaranteed by context $A$?".

This allows the program to deal with Heisenberg uncertainty not as a runtime error, but as a logical constraint during compile-time.

## Compilation

The C* compiler does not merely transliterate source code into gate sequences; it acts as a **homological geometer**. It views your program as a topology and solves for the global section that satisfies your constraints.

### Steps

#### 1. Graph wiring

The compiler assembles the **cover's nerve**, a simplicial complex where

- **Nodes** are the `Context` instances.
- **Edges** correspond to the intersections of contexts (shared observables).
- **Faces** represent triple intersections. 

#### 2. Spectral analysis

Next, the compiler populates this graph with local data. For every context node, it computes the **Gelfand spectrum** (eigenvalues) of the operators defined there, producing the spectral presheaf.

#### 3. Cohomology validation

Before generating a quantum gate, the compiler calculates the **sheaf cohomology group** $H^1$ of your logic using the combinatorial Laplacian.

- If $H^1 = 0$ the logic is consistent; a global section exists that fulfills all local truths.
- Otherwise, the cohomology is obstructed. A paradox such as the Kochen-Specker contradiction occurred, where local truths form a "Möbius strip" that cannot be flattened into a valid state.

This prevents the construction of physically impossible circuits by raising a compilation error.

#### 4. Circuit synthesis

If the logic is valid, the geometer proceeds to minimize the **Dirichlet energy** of the graph. This finds the optimal path of unitary gates (basis rotations) required to transport the state between contexts with minimal information loss.
