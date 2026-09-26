# Pass 10970 — Projective clock-code lattice tower

Producer: `analysis/w33_pass10970_projective_clock_code_lattice_tower.py`
Certificate: `data/w33_pass10970_projective_clock_code_lattice_tower.json`
Regression: `tests/test_w33_pass10970_10971_clock_tower_and_selector.py`

## Result

The Pass-10946 tetracode clock construction is the first nontrivial member of an odd-prime
projective-line code/lattice tower. For an odd prime (q), put

[
k=(q+1)/2,qquad
C_q={(f(0),ldots,f(q-1),f_{k-1}):deg f<k}.
]

This is the extended Reed–Solomon code on (mathbf P^1(mathbb F_q)), with parameters

[
[q+1,(q+1)/2,(q+3)/2]_q.
]
The evaluation monomials are mutually orthogonal. The finite-field power sums vanish below
degree (q-1); for the top row the finite sum is (-1) and the infinity coordinate contributes
(+1). Thus (C_q=C_q^perp).

Use (C_q) as glue in

[
(A_{q-1}^*/A_{q-1})^{q+1}congmathbb F_q^{q+1}.
]

The root lattice has determinant (q^{q+1}), while the glue index is
(q^{(q+1)/2}), so the extension is unimodular. For a discriminant coordinate
(c), the minimal coset norm is (c(q-c)/q). Self-orthogonality makes the total norm
integral, and odd (q) makes it even. Hence the glued lattice is even unimodular of rank

[
(q-1)(q+1)=q^2-1.
]

That number is independently the number of nonzero determinant-zero vectors in
(operatorname{Sym}_2(mathbb F_q)): (q+1) projective null directions, each carrying
(q-1) nonzero vectors.
## Why (q=3) is exceptional

The MDS distance gives

[
|v_{
m glue}|^2ge {q+3over2}{q-1over q}.
]

This equals (2) at (q=3) and is strictly greater than (2) for every (qge5).
Therefore the projective glue can create new roots only at the qutrit rung.

At (q=3),

[
C_3=[4,2,3]_3,qquad W_C(y)=1+8y^3,
]

the tetracode. The base (A_2^4) contributes (24) roots; the eight nonzero glue words
each contribute (3^3=27) norm-two vectors:

[
24+8cdot27=240.
]

The extension is (E_8), reproducing the already-certified W33 tetracode bridge.
## The new q=5 rung

At (q=5),

[
C_5=[6,3,4]_5,
]

with exact weight enumerator

[
1+60y^4+24y^5+40y^6.
]

Its actual minimum nonzero discriminant-coset norm is (4), not merely the MDS lower
bound (16/5). Thus the extension creates no new roots. It is the unique even unimodular
rank-24 lattice with root system (A_4^6): the Niemeier lattice (N(A_4^6)).

This is not just a six-coordinate count. The verifier enumerates all (120) elements of
(PGL_2(5)) and proves they act by exact monomial automorphisms of (C_5). Their
coordinate permutation action is faithful of order (120).
Pass 593 had independently identified the repository's six-object Singer fibre with
(PGL_2(5)) acting on (mathbf P^1(mathbb F_5)), equivalently the six Sylow-5 subgroups
of (S_5) / six fivefold axes of an icosahedron. Therefore the quinary glue coordinates are
welded objectwise and equivariantly to an existing repo carrier.

The executable q=7 control also passes:

[
C_7=[8,4,5]_7,qquad operatorname{rank}L_7=48,
]

with even unimodular glue and minimum nonzero glue norm (6). It again creates no roots.

## Prior-art boundary

Extended generalized Reed–Solomon codes and MDS self-dual constructions are classical coding
theory; self-dual codes over GF(5), including the exceptional length-six code, are classical;
and the (A_4^6) Niemeier lattice is classical. No novelty claim is made for those ingredients
in isolation.

The repository increment is their common **clock/null-direction weld**:
1. the (q+1) code coordinates are the projective null directions of
   (operatorname{Sym}_2(mathbb F_q));
2. the resulting even-unimodular rank is exactly the nonzero null-shell size (q^2-1);
3. q=3 reproduces the internal W33 tetracode/(E_8) certificate;
4. q=5 lands equivariantly on the already-certified Pass-593 (P^1(F_5)) Singer carrier;
5. the root-norm inequality explains exactly why the first rung, q=3, is exceptional.

Useful literature boundary: Leon–Pless–Sloane, *Self-dual codes over GF(5)*,
JCTA 32 (1982) 178–194; modern extended-GRS self-dual constructions include
Fang–Lebed–Liu–Luo (2018) and subsequent work.

## Boundary

This is an exact finite code/lattice theorem and an objectwise repo weld. It does **not**
supply a continuum limit, physical spacetime, a Hamiltonian, or measured couplings. It also
does not claim that the general code/lattice construction is new to lattice theory.
