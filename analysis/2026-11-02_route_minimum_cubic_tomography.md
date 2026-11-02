# Cubic tomography from the 216 W33 minimum route supports (2026-11-02)

**Status:** independently reproduced exact integer certificate; mathematical finite-geometry result, **not** a physical Theory of Everything.

**Producer:** `analysis/w33_20261102_route_216_cubic_tomography.py`  
**Certificate:** `data/w33_20261102_route_216_cubic_tomography.json`

## Relation to existing results

Pass 173 already identifies the route-side integral dark lattice, its 432 signed norm-10 vectors / 216 projective minimum supports, the [40,15,10] binary code, and the lack of point-line self-duality. Passes 12482–12483 independently enumerate the complete 216-element minimum orbit under `PSp(4,3)`. The results here do **not** claim those constructions anew.

The new object is the **cubic tensor of the point-coverage patterns** of those 216 line supports. It yields a direct reconstruction of the original GQ incidence and the two inequivalent noncollinear-triad classes.

## 216-by-40 incidence frame

Let `N` be the point-by-line incidence matrix and `B` the 216-by-40 incidence matrix of minimum supports of 10 lines. Every minimum support contains exactly 10 lines and covers each point either zero times or twice. Therefore

\[
H=\tfrac12 BN^{\mathsf T}\in\{0,1\}^{216\times40}
\]

is a binary point-coverage matrix: each row covers exactly 20 points, and every point occurs in exactly 108 rows.

Let `A_P` and `A_L` be the distinct point- and line-collinearity graphs, with identical strongly regular parameters `(40,12,2,4)`. **They are not identified by an incidence duality.** Exact integer multiplication gives:

\[
B^{\mathsf T} B=44I+8A_L+10J,\qquad
H^{\mathsf T} H=60I+15A_P+48J.
\]

Consequently,

\[
\operatorname{spec}(H^{\mathsf T}H)
=2160^1\oplus90^{24}\oplus0^{15}.
\]

The 15-dimensional point-dark constituent is annihilated by this route-to-point conversion.

## A 216-point spherical 2-design in 24 dimensions

Define the centered sign frame `Z=2H-J`. Every column sums to zero, every row has 20 positive and 20 negative coordinates, and

\[
Z^{\mathsf T}Z=360E_2,
\qquad\mathrm{rank}(Z)=24,
\]

where `E_2` is the rank-24 primitive W33 idempotent associated to adjacency eigenvalue `2`. Therefore the 216 sign rows, normalized by `\sqrt{40}`, form a tight spherical 2-design on the 24-dimensional eigenspace (frame constant 9). They have five distinct pairwise inner products.

## The cubic moment reconstructs W33

For three *distinct* points define

\[
T_{abc}=\sum_{s=1}^{216}Z_{sa}Z_{sb}Z_{sc}.
\]

The complete exact 9,880-triple census is:

| Point-triple orbit type | Cubic moment | Count |
|---|---:|---:|
| Three points on one isotropic line | 108 | 160 |
| Exactly two collinear pairs | -24 | 2,160 |
| Exactly one collinear pair | 12 | 4,320 |
| Pairwise noncollinear, exactly one common center | 0 | 2,880 |
| Pairwise noncollinear, four common centers | -48 | 360 |

Thus `T_abc=108` **if and only if** the points lie on one W33 line. The 160 detected triples coalesce four-to-one into the 40 four-point lines. The value -48 selects precisely the four-centric triads; zero selects the one-centric triads.

This provides a new, finite reconstruction principle:

> The third moments of a complete minimum-codeword shell determine the point-line incidence relation and triad-center type even after passing from the original 10-line routes to their 20-point coverage patterns.

An arbitrary 216-by-40 binary incidence array with the same row and column counts need not satisfy these identities; the result depends on the W33 orbit.

## Reproducibility and limits

Run `python analysis/w33_20261102_route_216_cubic_tomography.py`, followed by the focused regression. The script builds the projective symplectic geometry from scratch, grows the 216-support orbit from a checked seed using all 40 point transvections, verifies the full Gram identities with integers, and exhausts every distinct point triple. It relies on the earlier exhaustive classification for the assertion that this orbit is the *entire* minimum shell.

This is a **potential mathematical tomography and measurement-design interface**, not a physical photon state, not a derivation of the Standard Model, not a continuum light cone, and not a universal quantum gate implementation. A physical promotion requires a specified quantum state or channel, implementable observables, finite-shot noise estimates, and a comparison with independent controls.
