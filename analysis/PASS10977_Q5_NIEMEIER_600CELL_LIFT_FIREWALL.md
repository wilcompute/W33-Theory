# Pass 10977 — The q=5 six-carrier survives; the 120-shell lift does not

Producer: `analysis/w33_pass10977_q5_niemeier_600cell_lift_firewall.py`
Certificate: `data/w33_pass10977_q5_niemeier_600cell_lift_firewall.json`
Regression: `tests/test_w33_pass10977_q5_niemeier_600cell_lift_firewall.py`

## Why this pass exists

Pass 10970 identifies the q=5 projective clock code with the Niemeier lattice
[
N(A_4^6),
]
whose root system has six (A_4) components and (6cdot20=120) roots.

Pass 599 independently identifies the same six-object Singer carrier
[
mathbf P^1(mathbf F_5)
]
with the six fivefold axes of an actual 600-cell vertex-figure icosahedron.
The 600-cell itself also has 120 vertices.

The tempting next guess is therefore a 120-to-120 lift. It is false.
## The exact A4^6 root model

Label the six (A_4) components by the six Sylow-5 subgroups of (S_5).
Inside one (A_4), write its 20 roots as
[
e_i-e_j,qquad i
e j,qquad i,jin{0,1,2,3,4}.
]

Thus the full root packet is
[
(H,i,j),qquad
Hinoperatorname{Syl}_5(S_5),quad i
e j,
]
with
[
6cdot5cdot4=120.
]

Let (S_5) act simultaneously by conjugation on (H) and by permutation on
(i,j). The executable census proves that this action is **regular**:
one orbit of size 120 and trivial stabilizer.
Restricting to (A_5) gives two regular 60-orbits.

Root negation is
[
(H,i,j)longmapsto(H,j,i).
]
It preserves each of those 60-orbits. After quotienting by (rsim-r), the
60 projective roots therefore split under (A_5) as
[
oxed{30+30},
]
and each projective root has stabilizer of order two.

This already gives a strong fingerprint for the q=5 Niemeier shell above the
common six-object carrier.

## The exact 600-cell multiplication shell

Pass 599 stores exact 600-cell coordinates in (mathbf Z[phi]).
Using those same coordinates as scaled quaternions, the verifier checks all
(120^2) products and finds closure after the repository's factor-of-two
normalization.
The resulting 120-element group has element-order histogram
[
1^1,2^1,3^{20},4^{30},5^{24},6^{20},10^{24}.
]
Its center has order two, and it has exactly one involution.

This is the classical binary icosahedral group
[
2.A_5.
]

Quotienting by antipodes gives 60 projective vertices. Left multiplication
induces a group of order 60 with order histogram
[
1^1,2^{15},3^{20},5^{24},
]
its derived subgroup is all 60 elements, and its action on the 60 projective
vertices is regular. Thus the quotient is (A_5).

So the projective 600-cell shell is
[
oxed{60}
]
as one regular (A_5)-orbit.
## The firewall

The two projective 60-sets are therefore not the same (A_5)-set:
[
	ext{projective }A_4^6	ext{ roots}: 30+30,
]
while
[
	ext{projective 600-cell vertices}: 60.
]

An equivariant bijection is impossible because orbit sizes and stabilizers are
invariants.

The full 120-shells disagree even more strongly. The diagonal q=5 root model
carries a regular (S_5) action, whose involution count is 25. The exact
600-cell multiplication shell carries (2.A_5), whose involution count is 1.
Hence
[
S_5
otcong2.A_5.
]

The common cardinality 120 is therefore not an objectwise identification.
## What survives

The coarse six-object bridge remains exact:
[
oxed{
mathbf P^1(mathbf F_5)
;leftrightarrow;
6	ext{ Sylow-5 subgroups}
;leftrightarrow;
6 A_4	ext{ components}
;leftrightarrow;
6	ext{ icosahedral fivefold axes}.
}
]

What fails is the attempted lift above that sixfold base.

This is useful structurally: the q=5 tower now has an explicit **extension
firewall**. Two geometries can share the same projective clock base and the same
120 shell count while carrying inequivalent covering actions above the base.

That is exactly the kind of distinction the TOE program needs to preserve if
cardinality coincidences are not to become false identifications.
## Prior-art boundary

The following ingredients are classical:

- (A_4) has 20 roots, so (A_4^6) has 120 roots;
- the Niemeier lattice with root system (A_4^6) is classical;
- the 600-cell has 120 vertices;
- its unit-icosian realization is the binary icosahedral group.

The new repository increment is the common Singer-labelled setup followed by
the explicit action comparison:

1. the 120 Niemeier roots form a regular diagonal (S_5)-set;
2. their (A_5) restriction is (60+60);
3. antipodal quotient gives (30+30);
4. the exact 600-cell coordinates close to (2.A_5);
5. its antipodal quotient is one regular (A_5)-orbit of 60;
6. those orbit fingerprints rule out the natural 120-shell and 60-shell lifts.

## Boundary

This no-go applies to the stated objectwise equivariant lift respecting the
certified Singer actions. It does not rule out other relations between
(N(A_4^6)), (H_4), the 600-cell, modular forms, or icosian arithmetic.

No physical equivalence is inferred from either the surviving six-object bridge
or the failed 120-object lift.
