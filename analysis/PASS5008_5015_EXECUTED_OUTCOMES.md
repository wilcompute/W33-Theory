# Passes 5008–5015 — executed outcomes

**Date:** 2026-08-13  
**Status:** EXECUTED in exact finite computations and frozen certificates; remote replay status is reported separately.

## Pass5008 — global character closure compiler

The 1080 sigma-even A3 checks still span the full 324-dimensional dual code. Adding the 810 residual A4 equators does not increase that span. Therefore the 1890 low-shell observables are functions of exactly 324 Boolean character bits and obey

`1890 - 324 = 1566`

independent XOR closure relations.

The 270 octahedral 4-triangle/3-equator product equations are independent, but account for only 270 of those relations. Thus the exact cross-octahedron closure deficit is

`1566 - 270 = 1296`.

The 270 full-octahedron weight-12 words have binary rank 90. Full closure rejects the extremal parity character `T3=-1080` because it forces `T4=+10530`, and the degree-7 `(X+7)` localizing moment matrix then fails positivity. This still does not exclude every possible distance-173 character. The rigorous covering-radius interval remains

`134 <= rho(K) <= 173`.

Using the earlier cut/switching work, the exact decision problem can be stated as a signed Ising/MaxCut problem: a distance-173 coset requires both switching maxima for `w` and `w+sigma` to be at most 14, with one attaining 14. Pass4859/4867 retain ownership of the switching/cut enumerators; Pass5008 owns the 1890→324 compiler and the 1296 missing global-closure count.

## Pass5009 — the real octahedron 84 splits as 60+24

The share-three graph on the 270 octahedra has spectrum

`32^1, 14^20, 8^15, 2^84, (-4)^150`.

The exact polynomial projector

`(X-32I)(X-14I)(X-8I)(X+4I)`

has rank 84. Projecting the natural 270×45 tritangent-endpoint incidence into that space has rank 24. Since the construction is PGSp-equivariant, its orthogonal complement inside the 84-space is a full-group invariant 60-space:

`V84 = V60 (+) V24`.

Thus the real active octahedron carrier refines from `1+20+15+84` to

`1 + 20 + 15 + 60 + 24`.

No identification of the real V60 with the binary K60 is made.

## Pass5010 — K60 is a nonsplit modular extension

For the binary octahedron sequence

`0 -> K60 -> O90 -> C_Q43^perp(30) -> 0`,

the unique nonzero map from binary tritangent V20 into K60 has rank 14. Its kernel has dimension 6 and is explicitly isomorphic to the natural six-dimensional `O^-(6,2)`/E6 module. Hence

`0 -> N6 -> V20_trit -> S14 -> 0`.

The same S14 sits canonically inside K60. The quotient `Q46=K60/S14` has dimension 46 and scalar PSp endomorphism ring (`End` dimension one); it is therefore recorded as **Schurian**, not automatically called irreducible. No Hom was found in either direction between Q46 and the tested V20 carrier.

The exact affine section equations for

`0 -> S14 -> K60 -> Q46 -> 0`

have 2760 variables and 15823 equations and are inconsistent. Thus K60 is genuinely nonsemisimple/nonsplit rather than a naive `20+40` or `24+36` decomposition.

## Pass5011 — second reader correction and the first mixed circuits

Pass4998's support-eight `2K4` family remains correct as a family, but its **minimum** claim is superseded.

The pure tritangent block already has exactly 120 support-six dependencies. Each is a signed `K3,3`: `+1` on one independent tritangent triad and `-1` on another, with all nine cross pairs adjacent. The signed raw selector sum vanishes exactly.

For a centered tritangent dependency with nonzero coefficient sum, cubic-line/tritangent incidence gives

`N c = (sum c)/9 * 1_27`.

Thus its support must cover all 27 cubic lines; each tritangent covers three, so support is at least nine. Exact-cover enumeration finds exactly **200** partitions of the 27 cubic lines into nine pairwise line-disjoint tritangents. Each has raw selector sum `6 * 1_36`.

Combining one of the 40 four-line W33 point pencils with one of these 200 covers gives

`-6 * (four-line pencil) + (nine-tritangent cover) = 0`.

Therefore the first genuinely mixed reader circuits occur at

`4 + 9 = 13`,

not 9. There are exactly `40*200 = 8000` such minimum mixed circuits, and none at supports 9–12. The global reader erasure distance remains 6 because both pure blocks already have support-six failures.

## Pass5012 — the 24-dimensional failure space is the canonical shared V24

Let `Z` be W33 point-line incidence, `C` the spread-line reader, and for every one of the 240 W33 point-graph edges `{p,q}` define

`D_(p,q)=Z_p-Z_q`.

Then

- `rank(D)=24`;
- `D C^T=0`;
- `rank(C)=16`.

Hence

`rowspan(D) = ker(C) = V24_line`.

Moreover

`D^T D = -A_Q^2 + 8 A_Q + 48 I = 60 P24`,

and

`Z^T Z D^T = 6 D^T`.

Thus point-line incidence is the explicit isomorphism between line V24 and point V24, with inverse `Z^T/6` on the sector. The minimum line-failure frame is therefore not merely 24-dimensional; it is exactly the canonical shared W33 degree-24 carrier.

## Pass5013 — 120 tritangent K3,3 circuits are the 120 Steiner triangles

For each signed K3,3 tritangent circuit, exactly three double-sixes are missed by all six tritangents. Those three double-sixes form a Steiner triangle. This construction is bijective over all 120 circuits and all 120 Steiner triangles.

So the corrected pure-tritangent minimum family has a canonical cubic-surface interpretation:

`120 support-six K3,3 circuits <-> 120 Steiner triangles`.

## Pass5014 — 40 of the 200 exact covers are literally W33 points

Each W33 line has three Steiner triangles, hence three K3,3 circuits. Choosing one side of each K3,3 gives `2^3=8` nine-tritangent exact covers. Across all 40 W33 lines this gives 320 line-cover incidences but only 200 distinct covers.

Their incidence multiplicities split as

- 40 covers occurring over four W33 lines;
- 160 covers occurring over exactly one W33 line.

For each of the special 40 covers, its four W33 lines meet in a unique W33 point. This maps the 40 covers bijectively to the 40 W33 points. The 40×40 line/cover incidence matrix has row and column weight four, rank 25, and exact Gram identities

`B B^T = 4I + A_Q43`,

`B^T B = 4I + A_W33`.

Thus the cubic-surface nine-tritangent cover construction reconstructs the W33 point action directly.

## Pass5015 — the remaining 160 covers are the 160 W33 incidences

Each of the remaining 160 covers lies over one unique W33 line `q`. Flip all three K3,3 side choices to obtain its opposite cover. That opposite lies in the 40-point cover orbit and hence determines a unique W33 point `p`. The resulting pair `(p,q)` is incident.

All 160 incident point-line pairs occur exactly once. Therefore the 200 exact covers decompose canonically as

`200 = 40 W33 points + 160 W33 incident point-line pairs`.

The 160-set has stabilizer order 324, exactly the W33 point-line incidence stabilizer. Locally, each W33 line supports an eight-cover cube of three binary K3,3 side choices; four covers belong to the point orbit and four to the 160 incidence orbit. Any parity labeling of that cube depends on side-coordinate choices and is not promoted as canonical.

## Packet synthesis

1. The radius frontier is now sharply localized: 270 local closure equations leave exactly **1296** missing cross-octahedron character relations. No radius improvement is claimed without a full 324-bit UNSAT certificate.
2. The real octahedron carrier contains a new invariant 60 plus the canonical 24; the modular K60 has a very different nonsplit `14 -> 60 -> 46` architecture.
3. The reader has two different support-six pure failure geometries: 240 W33 line-gradient circuits and 120 Steiner/K3,3 tritangent circuits. The first mixed failures occur only at support 13.
4. The 200 cubic-surface nine-tritangent exact covers provide a new literal W33 carrier: **40 points plus 160 incident point-line pairs**.

Pass4959 remains untouched. The finite outer sign is not spacetime CP/CPT, Q46 is not called irreducible from a scalar endomorphism ring alone, and real/binary 60-dimensional carriers are not identified without an explicit cross-characteristic map.
