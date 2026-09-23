# 2026-09-23 — Extended Clifford / Heisenberg symmetry saturation

## Why this is not a rediscovery of the parallel 1296 theorem

The parallel frontier already proved that the full W33 point stabilizer is

[
3_+^{1+2}:GL(2,3)
]

of order (1296), with determinant-one half

[
3_+^{1+2}:SL(2,3)
]

of order (648).

The new bridge here adds two pieces that were not present in that group-order decomposition:

1. an explicit gauge from the current qutrit Pauli normal form to the older Pass-408 Heisenberg-voltage coordinates,
2. a general odd-prime comparison between the full Heisenberg graph automorphism group and the extended Clifford normalizer.

## Exact coordinate/action intertwiner

In the qutrit normal form

[
Z^aX^bomega^c
leftrightarrow (a,b,c),
]

the product is

[
(a,b,c)(A,B,C)
=
(a+A,b+B,c+C-bA)
pmod 3.
]

Define

[
u=(a,b),
qquad
z=c+2ab.
]

Then the group law becomes

[
(u,z)(v,w)
=
(u+v,z+w+omega(u,v)),
]

with exactly the Pass-408 alternating voltage

[
omega((x,y),(x',y'))=yx'-xy'.
]

For every (Min GL(2,3)),

[
(u,z)mapsto (Mu,det(M)z)
]

is a Heisenberg automorphism. Left translation by ((a,c)in H_{27}) then yields

[
(u,z)mapsto
left(
Mu+a,,
det(M)z-omega(Mu,a)+c
ight),
]

which is exactly the frozen Pass-408 graph-automorphism formula.

The executable witness checks all (27^2=729) Heisenberg products, all
(48cdot27^2=34992) linear-action product identities, and all
(1296cdot27=34992) pointwise permutation evaluations. The resulting
1296 permutations equal the complete Pass-408 permutation set.

This also explains the phase-centre subtlety. The (648) determinant-one
subgroup centralizes its scalar (C_3), but the determinant-minus-one coset
inverts it. Hence the scalar (C_3) remains normal in the (1296)-group
while the full centre becomes trivial.

## New q=3 saturation theorem

For an odd prime (p), Pass 408 gives

[
operatorname{Aut}(Gamma_p)
=
H_p:GL(2,p).
]

The unitary/anti-unitary extended Clifford normalizer uses the extended
symplectic subgroup

[
ESL(2,p)
=
{Min GL(2,p):det M=pm1}.
]

Therefore the retained-phase extended Clifford action is

[
operatorname{ExtCliff}_p
=
H_p:ESL(2,p).
]

Since the determinant map

[
GL(2,p)	omathbb F_p^	imes
]

is onto with equal fibres and (ESL) keeps exactly two determinant fibres,

[
oxed{
[operatorname{Aut}(Gamma_p):operatorname{ExtCliff}_p]
=
rac{p-1}{2}.
}
]

Thus

[
oxed{
operatorname{ExtCliff}_p
=
operatorname{Aut}(Gamma_p)
iff
p=3.
}
]

At (p=3),

[
mathbb F_3^	imes={+1,-1},
]

so every linear similitude is already symplectic or anti-symplectic. At
(p=5), by contrast, determinant classes (2) and (3) give valid graph
automorphisms outside the unitary/anti-unitary Clifford normalizer, producing
index (2).

## Literature boundary

Appleby's finite-field extended Clifford construction supplies the
(ESL(2,mathbb F_d)) side: determinant (+1) matrices are represented
unitarily and determinant (-1) matrices anti-unitarily.

The full (H_p:GL(2,p)) graph-automorphism theorem is internal Pass 408.
The new contribution is the exact comparison and the saturation index.

## Physics boundary

This selects (p=3) only under a finite symmetry principle:

> the physical unitary/anti-unitary Weyl-Heisenberg normalizer saturates every
> unoriented automorphism of the associated Heisenberg bulk graph.

Nothing here establishes that this principle is mandatory in Nature. In
particular, this theorem does not by itself derive three generations,
spacetime dimension, CPT, the Standard Model, or a measured coupling.

## Artifacts

- `analysis/w33_extended_clifford_pass408_intertwiner.py`
- `data/w33_extended_clifford_pass408_intertwiner.json`
- `tests/test_w33_extended_clifford_pass408_intertwiner.py`
- `analysis/w33_q3_extended_clifford_saturation.py`
- `data/w33_q3_extended_clifford_saturation.json`
- `tests/test_w33_q3_extended_clifford_saturation.py`
