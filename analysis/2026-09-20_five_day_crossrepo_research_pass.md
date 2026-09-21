# Five-day cross-repository research pass — 20 September 2026

## Scope

Exact GitHub API window:

- start: 2026-09-16T02:29:00Z
- end: 2026-09-21T02:29:00Z
- W33-Theory commit records enumerated: **367**
- Holotrade commit records enumerated: **178**
- total: **545**

The counts are commit records in the exact five-day window, not theorem counts.
Later corrections/retractions in the same causal chain are treated as authoritative
over earlier intermediate claims.

## Full manuscript-body structural scan

The three canonical root TeX files are wrappers around large body files plus the
shared frontier tail. The full body files were loaded and scanned line-by-line for
section structure, imports, evidence/boundary language, errata, and current frontier
handoffs:

| body | bytes | lines | headings | evidence/boundary flagged lines |
|---|---:|---:|---:|---:|
| w33_paper_body.tex | 827,488 | 16,964 | 585 | 205 |
| photonic_holonet_body.tex | 563,859 | 9,753 | 159 | 168 |
| holonet_machine_blueprint_body.tex | 196,359 | 3,986 | 73 | 42 |

All three wrappers also import
`analysis/W33_CURRENT_FRONTIER_MANIFEST` and
`analysis/W33_SHARED_FRONTIER_TAIL`; the current shared tail was followed through
the September 15--20 inserts.

## Five-day frontier map

The dominant current themes, counted only as rough keyword occurrences in commit
messages, are:

### W33-Theory

- FI: 138
- E8: 44
- formula: 43
- packet: 37
- holonomy: 33
- W33: 32
- qutrit: 25
- correction: 21
- hypercharge: 13
- heterotic: 10
- Higgs: 7
- Yukawa: 6
- proton: 5
- explicit retraction markers: 5

### Holotrade

- FI: 115
- freeze: 33
- hypercharge: 24
- correction: 22
- E8: 20
- Higgs: 16
- qutrit: 16
- W33: 13
- Yukawa: 10
- heterotic: 9
- proton: 6
- retraction: 6

These counts show where the frontier moved; they are not evidence weights.

## Current authoritative cross-repo chain used in this pass

1. The flagship physical anomalous-U(1) trace is nonzero; the earlier vanishing
   trace was a chirality double-count and is superseded.
2. The physical FI generator is orthogonal to canonical hypercharge on the
   A5 organizer and has exact W33 star vector
   [
   (-5,3,1,-5,6).
   ]
3. W33 independently identifies the neutral bracket cokernel as
   [
   5=Y(1)+A_4(4),
   ]
   and the physical FI vector lands in the A4 factor.
4. The flagship Wilson line has exact SU(9) defining multiplicities (5+2+2)
   and is cospectral with qutrit (CZ_3); the canonical tensor-factor Clifford
   identification remains open.
5. Projected Abelian rank closure is not a D/F-flat vacuum. Current Holotrade
   files preserve this boundary and retain exact Farkas/no-go data for sparse
   candidate vacua.
6. The newest Yukawa/proton-protection chain is a model-class no-go statement,
   not a general theorem of heterotic compactifications.

## New result from this pass

The physical FI vector itself carries previously unrecorded finite structure:

[
v=(-5,3,1,-5,6)
]

has S5 orbit 60 and an odd order-two stabilizer, hence a **regular Alt(5)
torsor** of 60 integral orientations.

The distinct-value collision discriminant is

[
15840=2^5,3^2,5,11.
]

Exactly those four primes collapse the torsor:

[
p=2,3,5,11
quadLongrightarrowquad
|mathcal O_p|=5,10,30,20,
]

with uniform integral fibers

[
12,6,2,3.
]

At (p=3),

[
vmod3=(1,0,1,1,0),
]

so the physical FI ray selects an exact (3+2) partition of the five
hypercharge-star coordinates. The ten quotient states are the ten 3-subsets
(equivalently 2-subsets) of a five-set.

This theorem is executable in
`analysis/w33_physical_fi_alt5_prime_shadow_torsor.py` and has a frozen
certificate and regression test. It is also mirrored model-side in Holotrade.

## Firewalls preserved

- The charge-space A4 and the non-Abelian SU(5) A4 root block are distinct
  certified objects; their shared 3+2 coset combinatorics is not an intertwiner.
- The appearance of 11 as both an FI collision prime and (k-1), the W33
  nonbacktracking branching number, is not promoted to physics without an
  operator map.
- No D-flat/F-flat vacuum follows from the prime-shadow theorem.
- No claim is made that W33 has become an experimentally established TOE.
