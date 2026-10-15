# TOE84 — A faithful H27 logical Clifford action and a characteristic-three clock polarization

**15 October 2026.** Continuation of TOE83's exact `[[135,26,6,4]]_2` and `[[135,26,6,4]]_3` tritangent CSS codes. This is a finite stabilizer-code automorphism theorem, not a demonstration of a physical quantum gate, temporal process, or Theory of Everything.

## Construction

Rebuild the 27 native Heisenberg addresses, 45 tritangent triangles and 135 edges from TOE82's five coset directions. Load TOE83's **two selected H27-orbits of 27 squares each** (54 square faces). The augmented chain complex has ranks

```text
C2 = F_q^99 --d2--> C1 = F_q^135 --d1--> C0 = F_q^27
rank(d2)=83, rank(d1)=26, H1 dimension=26, H2 dimension=16.
```

For each `g in H27`, its left translation on the 27 vertices induces a permutation of the 135 undirected edges. Over F3, attach the orientation sign `sgn_g(e)=+1` or `-1` according as the image of the oriented edge preserves or reverses its chosen vertex ordering. This is an integral signed-permutation (monomial) chain map.

The verifier checks **all 27 elements** and all 99 face boundaries: the monomial action preserves the vertex-check row set and the triangle/square face-check row set up to orientation. Consequently it preserves the CSS stabilizer group over F2 and F3. On physical qutrits, signed local basis inversions together with wire permutations are Clifford operations; they therefore induce logical Clifford automorphisms. No geometric locality, fault-tolerance threshold, or native optical implementation is inferred.

## Faithful action on the 26 logical qudits

Construct 109 fundamental graph cycles using a spanning tree, and extend the rank-83 face span by **26** cycles to obtain a logical homology basis over each field. For every `g`, calculate the rank of `g-I` on the quotient `ker(d1)/im(d2)` using exact finite-field elimination.

The full rank distribution is:

| Elements | rank(g−I) over F2 | rank(g−I) over F3 |
|---:|---:|---:|
| 1 (identity) | 0 | 0 |
| 8 | 18 | 16 |
| 18 | 18 | 17 |

Thus the logical action has **trivial kernel over both fields**:

```text
H27 -> Aut(H1(F2))  is injective
H27 -> Aut(H1(F3))  is injective.
```

This is stronger than merely knowing that the physical check geometry has H27 symmetry: the entire nonabelian Heisenberg group survives on the encoded logical information.

## A new modular clock signature

Exactly eight nonidentity elements have rank 16 over F3. Together with the identity they form

```text
A = {(0,b,c) : b,c in F3},
|A|=9, A is abelian.
```

The script enumerates all **four** maximal abelian subgroups of H27 containing its center and proves that this rank-defined `A` is precisely one of them. The other 18 nonidentity elements have rank 17. In characteristic two, all 26 nonidentity elements have rank 18, so this distinction is specifically **modular**.

The four order-nine maximal abelian subgroups correspond to the four one-dimensional subspaces of `H27/Z(H27) ~= F3^2` — the same four commuting qutrit Pauli directions that label the Hesse/MUB striations. Hence the code's modular logical action **selects one of four qutrit clock polarizations by a basis-independent rank criterion**.

This selection is an exact finite-algebraic fact relative to TOE83's chosen two-orbit code. It is **not** a proof of an arrow of time, an emergent metric, or an identification with a physical clock. In particular, the full outer action permuting the four polarizations is not shown to preserve the selected code.

The paper `papers/forty_points/main.pdf` discusses Choi versus temporal self-entanglement on page 17 and a state-selected qutrit clock on page 18. TOE84 supplies a new coding-theoretic realization of a four-to-one *finite polarization selector*, without claiming those distinct notions of time have been physically identified.

## Reproduce

```bash
python analysis/w33_20261015_toe84_h27_logical_clifford.py
python -m pytest -q tests/test_w33_20261015_toe84_h27_logical_clifford.py
```

The frozen certificate includes all 27 group elements and their exact logical `rank(g-I)` values.

## Five independent research directions

1. Compute the complete modular Loewy/radical filtration of the 26-dimensional F3 logical H27 module and compare with Pass11980's 64-dimensional module.
2. Classify all 468 admissible two-orbit TOE83 codes by which of the four Pauli/MUB polarizations their logical rank distribution selects.
3. Construct explicit encoded Clifford matrices and gate synthesis circuits for two Heisenberg generators, with locality and SWAP-depth estimates.
4. Study the 16-dimensional H2 relation module under H27, and test whether its extension class controls the 26-dimensional logical action.
5. Test whether a symmetric orbit-average code can preserve the full outer D8 action without collapsing the 26 logical degrees of freedom.
