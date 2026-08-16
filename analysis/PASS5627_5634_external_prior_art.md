# Passes 5627–5634 — external prior-art boundary

This packet makes no novelty claim for the general free-fermion/BdG classification machinery.

## Majorana quadratic Hamiltonians / real skew generators

Alexei Kitaev, *Periodic table for topological insulators and superconductors*, arXiv:0901.2686.

Primary source: https://arxiv.org/abs/0901.2686

Kitaev writes a general free-fermion Hamiltonian without particle-number conservation in Majorana form
\(\widehat H_A=(i/4)\sum_{jk}A_{jk}c_jc_k\) with \(A\) real skew-symmetric, and develops the real/complex K-theoretic classification of gapped free-fermion phases.  Pass5632 uses only this standard algebraic comparison: the repo's deck-odd matrix is exactly `i times real-skew`, and complex conjugation reverses its sign.

## Tenfold-way symmetry classification

Andreas Schnyder, Shinsei Ryu, Akira Furusaki, Andreas Ludwig,
*Classification of Topological Insulators and Superconductors*, arXiv:0905.2029; see also arXiv:0803.2786.

Primary sources:
- https://arxiv.org/abs/0905.2029
- https://arxiv.org/abs/0803.2786

The standard Altland–Zirnbauer/tenfold-way framework distinguishes particle-hole and time-reversal antiunitary symmetries and their squares.  The phrase `class-D-like` in Pass5632 is deliberately scoped to this algebraic symmetry pattern only.  The W33 finite carrier is not claimed to be a physical topological superconductor, and no bulk topological invariant is assigned in this packet.

## Packet-specific boundary

The new content here is internal to the repository's finite objects: the exact Segre carrier stabilizers, signed central action, module decomposition, commutant dimensions, E6 bundle-action no-go, C2-tower obstruction, q5/q3 module map, gauge-cochain-degree test, and exact sheet Schur/Feshbach resolvent.  Standard Majorana/BdG and symmetry-class language is used only as external vocabulary for those finite algebraic results.
