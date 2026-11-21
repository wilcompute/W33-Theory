# Odd/even characteristic obstruction: orthogonal-reflection fibers and the nucleus escape

**November 21, 2026.** Exact finite geometry; not a physical TOE result. See
[executable certificate](toe_20261121_orthogonal_projection_reflection.py),
[regressions](../tests/test_toe_20261121_orthogonal_projection_reflection.py)
and [data](../data/toe_20261121_orthogonal_projection_reflection.json).

## Repository provenance and genuinely incremental conclusion

The November 20 five-front study, \`analysis/toe_20261120_nextfive_falsifiers.py\`,
already enumerates **all 1,093 projective centers** of the natural seven-coordinate
split Cayley hexagon model and correctly finds fiber totals 112+126*2=364 and
130+117*2=364. The preceding \`analysis/toe_20261120_octonion_mereology_radon.py\`
constructs its 364 octonionic hexagon points. This note **does not** claim
to discover the 364-point obstruction or the classical theory of orthogonal
quadrics. Its independent addition is the structural reflection-orbit proof,
the characteristic-two nucleus contrast, the generalized odd-prime formulas,
and explicit comparison to an earlier orthogonal-sign obstruction in the repo.

## Orthogonal reflection explains the collisions

Work over a finite field F_q, initially odd characteristic, with n=3 and

    Q(a,u,v) = -a^2 - u·v,

on a 7-dimensional vector space. The isotropic points of Q(6,q) form
the point set of the natural split Cayley hexagon H(q). Write
B(x,c)=Q(x+c)-Q(x)-Q(c).

For an anisotropic center [c], the quotient map V -> V/<c> identifies
exactly the two roots on each secant to [c]. They are

    x and R_c(x)=x-B(x,c)/Q(c) c.

Indeed Q(x+t c)=t[B(x,c)+t Q(c)] when Q(x)=0, so the second
root is unique. Direct substitution shows R_c^2=1 and
Q(R_c x)=Q(x). Points are fixed precisely when B(x,c)=0.
Thus the 1-point fibers are exactly the singular points of the
nondegenerate hyperplane section c^perp intersect Q.

Crucially the two *distinct* members of a 2-point fiber are not
orthogonal in the ambient quadratic form:

    B(x,R_c(x)) = -B(x,c)^2/Q(c) != 0.

The reflection is an ambient orthogonal symmetry. It is NOT asserted
to preserve the distinguished octonionic G2 hexagon lines.

An isotropic kernel point is itself in Q and makes projective projection
undefined there, so all linear kernels are covered.

## Exact formulas for every odd prime power

Let N=|Q(6,q)|=(q^6-1)/(q-1). Every anisotropic polar hyperplane
section is a nondegenerate Q+(5,q) or Q-(5,q), with fixed-point totals

    T+ = (q^2+1)(q^2+q+1)
    T- = (q^3+1)(q+1).

Burnside counting of the reflection involution gives

    #images = (N+T)/2
    #double fibers = (N-T)/2.

In reduced form:

    D+ = (q^5-q^2)/2
    D- = (q^5+q^2)/2.

Therefore D- - D+ = q^2, while the hyperplane fixed-point
totals differ by 2q^2. Neither option is injective for odd q>1.

At q=3: 364 null points, 364 isotropic centers and 729 anisotropic
centers. Norm-square centers: 351 instances, Q- tangency 112,
126 doubletons, 238 images. Norm-nonsquare centers: 378 instances,
Q+ tangency 130, 117 doubletons, 247 images. The verifier independently
checks every one of the 729 tangent-hyperplane intersection counts and
constructs reflection orbits + projected fibers for representatives.

At q=5: 3,906 null points; Q+ has 806 fixed points/1,550 double
fibers/2,356 images, while Q- has 756 fixed points/1,575 double
fibers/2,331 images. Independent representative-orbit verification passes.

## Why even characteristic admits the special symplectic quotient

In characteristic 2 the same quadratic form has polar form

    B((a,u,v),(b,s,t)) = u·t+s·v.

It is alternating and has the 1-dimensional radical generated
by the nonsingular nucleus (1,0,0). Projecting from this nucleus onto
the (u,v) coordinates is **bijective** on Q(6,q): for every nonzero
(u,v), the equation a^2=u·v admits one and only one solution
a because the Frobenius squaring map is an automorphism of F_q.
The quotient inherits a nondegenerate symplectic form.

The stand-alone verifier independently checks all 63 source and target
projective points at q=2 and explicitly implements GF(4) arithmetic to
check all 1,365 source/target points at q=4. The general argument applies
to every q=2^k.

This gives an algebraic reason that the classical perfect symplectic
embedding of H(q) exists in even characteristic, while projection
from the natural seven-coordinate representation cannot deliver the
same identification for odd q.

## Orthogonal-sign connection inside this repository

Pass 9253-9260 and Pass 9749-9756 independently distinguish
Q-(5,3), 112 singular projective points, from Q+(5,3), 130 such
points, in the Niemeier/Suzuki exchanger polarization problem.
The two branch strata here have these **same Witt types**, not just
equal cardinalities. A proof of a canonical intertwiner between
these distinct six-dimensional quadratic modules is still missing.
Indeed Pass9749-9756 proves that the currently fixed two polarizations
cannot be congruently transported because their types differ.

## Physical boundary and next discriminant

A projective cardinality match is not an incidence, group, or quantum
operator map. The odd-characteristic reflection does not manufacture a
three-qutrit symplectic commutator form, and neither branch is an
experimentally selected vacuum. A viable operator bridge must explicitly
supply (i) an incidence-respecting nonlinear map or a larger module,
(ii) a functorial group action/commutator, and (iii) a genuine physical
channel with tests. A proof of no linear map in this *natural* embedding
does not forbid every other embedding or nonlinear correspondence.

## External corroboration

- FinInG generalized hexagon documentation: https://gap-packages.github.io/FinInG/doc/chap12_mj.html
- Characterization of natural H(q) embedding: https://arxiv.org/abs/1307.8262
- Odd/even orthogonal/symplectic distinction: https://fossies.org/linux/gap/pkg/fining/doc/chap12_mj.html


## Additional exact H(3) incidence obstruction: all 729 reflections

A further independent test goes beyond the point projection. The ambient
orthogonal reflection R_c fixes the polar hyperplane and preserves Q(6,3),
but **does not preserve the selected octonionic hexagon lines**. The new
[exhaustive verifier](toe_20261121_octonionic_reflection_line_test.py)
uses the existing, directly constructed split-octonion zero-product line
relation and enumerates all 729 nonsingular centers.

| Q(c) | Centers | Surviving H(3) lines / 364 | Surviving edges / 2184 |
|---|---:|---:|---:|
| 1 | 351 | 28 | 168 |
| 2 | 378 | 52 | 312 |

For every one of those centers, **the only H(3) lines whose images
remain H(3) lines are the lines pointwise fixed in c-perp**. This is
verified by enumerating all 364 maximal K4 hexagon lines, transporting
their vertices through R_c, and checking equality of the transported
line set with the fixed-line set. Every hexagon line contains six
unordered point pairs, explaining the edge multiplicities 6*28 and
6*52. Tests and frozen JSON are respectively
[test](../tests/test_toe_20261121_octonionic_reflection_lines.py) and
[data](../data/toe_20261121_octonionic_reflection_lines.json).

This rules out the reflection as an H(3) incidence automorphism and
strengthens the geometric warning about treating its two-point
projection orbits as exceptional-geometry gauge equivalence. It is
still **not** a no-go theorem for arbitrary nonlinear or
higher-dimensional Pauli/Clifford encodings.
