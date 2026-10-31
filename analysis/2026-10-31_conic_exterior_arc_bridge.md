# The cube-family matching is a classical exterior arc

Status: exact dictionary, literature corollary, finite verification. No TOE,
particle spectrum, continuum dynamics or novel classification is claimed.

## What this adds to the repository

Pass 12489 (`PASS12482_12489_EVEN_LINE_SETS_PAIR_STRUCTURE.md`) built even line
sets from a regulus and a matching with nonsquare cross-ratios and no concurrent
chord triples. Passes 12490-12497 distinguished the square-cross-ratio Moore
family. Their counts and even-line-set constructions remain their results.

Here the **nonsquare** condition is identified explicitly with an established
object: an exterior arc of a conic of size `(q+1)/2`. This connects the observed
cube/icosahedron sporadicity to older finite-plane literature. The contribution
is the repository dictionary and its executable cross-check, not rediscovery of
the examples or their classical conjecture.

Producer: `analysis/w33_20261031_conic_exterior_arc_bridge.py`.
Certificate: `data/w33_20261031_conic_exterior_arc_bridge.json`.

## Exact map, over every odd finite field

Use the conic `C: Y^2 = XZ` in `PG(2,q)`, parametrised by
`c(t)=(t^2,t,1)` and `c(infinity)=(1,0,0)`.

For each pair `{a,b}` of the matching, take the **pole of its chord** under the
polarity of C. For finite a,b it is

`P_ab = (ab, (a+b)/2, 1)`.

For `{infinity,b}`, it is `P_inf,b=(2b,1,0)`. These points are external: their
polar chords are secants, and `Y^2-XZ=(a-b)^2/4` in the finite chart.

For disjoint pairs `{a,b}`, `{c,d}`:

1. The line `P_ab P_cd` is external to C **iff** `cr(a,b,c,d)` is nonsquare.
   By projectivity reduce the first pair to `{infinity,0}`. The joining line
   then has equation `X-cd Z=0`, with conic-intersection discriminant `4cd`.
   The cross-ratio is `d/c`, which has the same square class as `cd`.
2. Three chord poles are collinear **iff** the three chords are concurrent,
   by polarity. The latter is the repo's common-Moebius-involution condition.

Consequently a cube-family good matching gives `(q+1)/2` external points, all
joining lines external, with no three collinear: an exterior arc.

The converse is exact as well. An external point has two tangent contacts on C.
Two points of an exterior set cannot share a tangent, since their joining line
is external. Thus `(q+1)/2` points use all `q+1` tangent contacts exactly once.
Pair those contacts: the pole of their chord is the original external point.
This reconstructs the matching, with both repo predicates satisfied.

## A literature theorem removes half the field orders

Blokhuis, Seress and Wilbrink (1992) classify exterior sets of `(q+1)/2`
external points for `q = 1 mod 4`: they are collinear, on an external line.
For q >= 5 their size is at least three, violating the arc condition. Therefore:

> **For every odd prime power q congruent to 1 modulo 4, the nonsquare-good
> matching of Pass 12489 does not exist.**

This is a corollary of a known classification through the map above, not a new
classification theorem. It concerns this matching family only. It neither
excludes general even line sets at those q nor applies to the square-good Moore
family (which has the Petersen example at q=5).

Van de Voorde's paper, Section 3, explicitly discusses the no-three-collinear
examples at q=7,11, the computer exclusions for 11<q<=31, and the older
conjecture about larger exterior sets. Thus the repo's question whether only
q=3,7,11 occur has substantial prior art. The q=3 two-point arc is a small
vacuous-no-three-collinear case. The retrieved sources do not settle all larger
q congruent to 3 modulo 4; that question remains open here. No claim about the
literature's status after those sources is made.

## An additional coding connection, with the parity distinction checked

Let E be such an arc and `S=C union E`. It is a set without tangents, of size
`3(q+1)/2` (also a known construction in Van de Voorde, Section 3).

Each external point has two tangent lines to C. These use every conic tangent
once. Each point of E has `(q-1)/2` external lines through it; the other
`(q-1)/2` points of E occupy exactly those lines, since no three are collinear.
The remaining `(q-1)/2` secants through it each contain one E point and two C
points. Hence every projective line meets S in 0, 2 or 3 points, with

`n_3=(q^2-1)/4`, `n_2=3(q+1)(q+3)/8`,
`n_0=q^2+q+1-n_2-n_3`.

For the **line-check / point-variable incidence matrix of PG(2,q)**, S is an
LDPC stopping set: no check meets it exactly once. It is **not a binary even
codeword**, since n_3>0. This incidence matrix differs from the W(3,q)
point-check / line-variable matrix that defines Pass 12489's even line set.
There is no distance claim or quantum-code parameter inferred from the analogy.

## Verification

The producer independently evaluates conic discriminants and 3x3 determinants,
and compares them with the existing cross-ratio and Moebius implementation.
It exhausts disjoint pair configurations and triple configurations at
q=3,5,7,11,13, then enumerates every perfect matching geometrically. The counts
are 3,0,14,22,0 respectively, reproducing the earlier repo computations.
For surviving examples it enumerates every line of PG(2,q):

| q | size of S | n_0 | n_2 | n_3 |
|---|---:|---:|---:|---:|
| 3 | 6 | 2 | 9 | 2 |
| 7 | 12 | 15 | 30 | 12 |
| 11 | 18 | 40 | 63 | 30 |

The computation uses prime fields only; the all-prime-power statement above
comes from the coordinate proof and cited theorem, not extrapolation.

## Intake coverage and remaining work

At the fetched baseline `ca631cfabede6e586252ab8108aebb7ebad71d33`, the local
history query for the week beginning 2026-10-24 returned 262 commits. The
current `papers/forty_points/main.pdf` has 215 pages; its full text was extracted
to a temporary local file. **Extraction and commit inventory are not full
intellectual review.** The full-paper and every-commit reading requested by
the user remains incomplete. This note records a focused continuation and
must not be cited as evidence that the entire corpus was reviewed.

Remote Desktop Commander reported TheHeavyCrown offline. Work ran through the
direct local execution tool; no additional remote compute was available.
Existing unrelated working-tree edits were preserved.

## Sources

- A. Blokhuis, A. Seress, H. A. Wilbrink, *Characterization of complete exterior
  sets of conics*, Combinatorica 12 (1992), 143-147.
  https://doi.org/10.1007/BF01204717
  Primary institutional abstract: https://research.tue.nl/en/publications/characterization-of-complete-exterior-sets-of-conics/
- G. Van de Voorde, *On sets without tangents and exterior sets of a conic*,
  Discrete Mathematics 311 (2011), 2253-2258, Section 3.
  https://arxiv.org/abs/1201.0484

## Five independent research fronts

- Classify exterior arcs for larger q=3 mod 4, using the polynomial and exterior-set literature.
- Determine the full stabilizer action on the q=5 Petersen twin-pair graph.
- Establish rigorous code-distance bounds for general odd-q even line sets outside the regulus families.
- Derive an action selecting the clock real form with physical observables independent of basis choices.
- Test a predictive continuum/chiral-matter mechanism against the repo's existing no-go certificates.
