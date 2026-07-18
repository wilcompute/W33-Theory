# Pass 450 — Lean central Fourier scaffold

`formal/W33/Pass450CentralFourierScaffold.lean` adds the next formal layer above the Pass 441 Smith kernel.

It formalizes finite-group convolution, the character-eigenvector mechanism for convolution operators, the scalar cancellation lemma behind finite-character orthogonality, conductor active-rank and residual-rank identities, and the length-three conductor magnitude arithmetic.

The source contains no `sorry` and declares no custom axioms. It is imported into the repository's existing `W33` Lean root.

**Formal boundary.** The full Heisenberg irreducible representation, conductor classification, and integral lattice construction remain to be formalized. Lean/Lake is not installed in the local execution container, so actual compilation belongs to the pinned CI job and is not claimed locally.
