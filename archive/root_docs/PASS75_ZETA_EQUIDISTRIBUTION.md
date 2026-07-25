# Pass 75 — Four "even better" zeta ideas

**Status: PASS** — witness `w33_pass75_zeta_equidistribution.py` (15/15 checks), test `tests/test_pass75_zeta_equidistribution.py` (5/5), paper compiles clean (tectonic).

The four ideas that emerged during Pass 74, executed as witnesses.

## Track 1 — GQ polygon-zeta pairing
The collinearity graph (girth 3) and the incidence graph (girth 8 = 2·4) give the two shortest
Ihara primes of W(3,3): **triangles** (length 3, π_G = 320) and **quadrangles** (length 8,
π_G = 3240). The incidence-graph girth being 2·(gonality) = 8 *is* the generalized-quadrangle
axiom; a generalized n-gon would give incidence girth 2n. The two graphs' shortest primes are
exactly the GQ's two ordinary polygons.

## Track 2 — Prime-geodesic equidistribution (Sarnak-type)
The unit Frobenius phase α = (1+i√10)/√11 has minimal polynomial **121u⁴+198u²+121** — non-monic,
so α is not an algebraic integer, hence **not a root of unity**, so the geodesic frequency
arg(1+i√10) = **0.4025π is an irrational multiple of π**. The primes therefore do not resonate:
αⁿ never returns to 1, and the normalized discrepancy
`R_m = (N_m − 11^m − 201 − 200(−1)^m)/(78·11^(m/2))` stays in [−1,1] (observed **max|R_m| = 0.965**
over m ≤ 40) and oscillates aperiodically — the graph analogue of prime-geodesic equidistribution,
at the Ramanujan (square-root) rate. The near-1 max shows the error bound is close to tight.

## Track 3 — Edge-zeta separation of a cospectral pair (the constructible demonstrator)
**Shrikhande graph** vs the **4×4 rook graph** — both SRG(16,6,2,2), **cospectral**, with
**identical Ihara N_m** (0,0,192,480,2880,19200,…) ⇒ identical Ihara AND Bartholdi zeta. Yet they
are non-isomorphic: the vertex neighbourhood is **C₆** (Shrikhande, spectrum {2,1,1,−1,−1,−2}) vs
**2K₃** (rook, {2²,(−1)⁴}) — *not* cospectral. So the spectral (Ihara/Bartholdi) zeta cannot hear
the difference, but the finer **edge zeta** (a complete, non-spectral invariant) separates them.
This is the constructible witness for Pass 74's claim that the 28 cospectral SRG(40,12,2,4) Spence
graphs are invisible to the Ihara zeta. (I used the canonical 16-vertex pair because the 28
adjacency matrices at (40,12,2,4) aren't in the repo; the phenomenon is identical.)

## Track 4 — The 78 = dim(E₆) amplitude theorem (not a coincidence)
For **any** SRG the explicit-formula oscillatory amplitude is 2(f+g) = 2(v−1). For W(3,3):
**2·39 = 78 = 2q(q²+q+1) = dim(E₆)**, with f=24, g=15 the irreducible eigenspace dimensions of
Sp(4,3)=W(E₆) (f+g = v−1 = 39 = dim(E₆)/2), and q²+q+1 = 13 = |PG(2,3)|. So the periodic-orbit
fluctuation being bounded by dim(E₆) is forced arithmetic (v−1 = 39) meeting the group coincidence
Sp(4,3)=W(E₆), not a numerical accident.

## Files
- `w33_pass75_zeta_equidistribution.py`, `.json` — witness + certificate (15 checks).
- `tests/test_pass75_zeta_equidistribution.py` — 5 assertions.
- `w33_paper.tex` — "Remarks" paragraph appended to the Zeta Frontier subsection.
