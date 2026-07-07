# Pass 74 — The Zeta Frontier of W(3,3) (six tracks)

**Status: PASS** — witness `w33_pass74_zeta_frontier.py` (12/12 checks), test `tests/test_pass74_zeta_frontier.py` (7/7), paper compiles clean (tectonic).

Executes the six starred next-steps from Pass 73. Each track was checked against
`docs/index.html` and `w33_paper.tex` **first** (the doc is encyclopedic — Weil conjectures,
Deligne–Lusztig, Langlands over F₃, Krein/Terwilliger, octonions/Freudenthal are all present),
so each track states what is already documented and computes only the genuine delta.

## Genuinely new (absent even with correct search: Bartholdi/edge-zeta/explicit-formula/Hashimoto-on-incidence = 0 hits)

- **Track A — Quadrangle primes (idea 1).** The 80-vertex point–line **incidence (Levi) graph**
  (4-regular, spectrum {±4¹, ±2²⁴, 0³⁰}) has **girth 8** and is Ramanujan (non-trivial Hashimoto
  eigenvalues of modulus √3). Its first Ihara primes are the **oriented ordinary quadrangles**:
  **π_G^inc(8) = 3240 = 2 × 1620**, the 1620 cross-checked by direct 8-cycle enumeration
  (N_m = 0 for m < 8). This is the exact analog of the collinearity graph's π_G(3) = 320 = 2×160
  triangles — **the two W(3,3) graphs' shortest primes are the GQ's triangles and quadrangles.**

- **Track B — Explicit formula & dim E₆ (idea 4).** Exact:
  `N_m = 11^m + 201 + 200(−1)^m + 48·Re((1+i√10)^m) + 30·Re((−2+i√7)^m)`. The two oscillatory
  frequencies are the Frobenius-eigenvalue arguments (the graph's "Riemann zeros"), with
  cos²(arg(1+i√10)) = 1/11 (they encode the Ihara norm, not a mixing angle). Total oscillatory
  amplitude **48 + 30 = 78 = dim(E₆)** (index.html line 18118) — the periodic-orbit fluctuation is
  bounded by dim E₆, tying the graph PNT to the Sp(4,3)=W(E₆) spine.

- **Track C — Functional equation (idea 6).** Each factor 11u²−λu+1 has roots of product 1/11, so
  **u ↦ 1/(11u)** swaps them: the pole set is invariant, the trivial pair u=1↔u=1/11 self-maps, and
  the critical circle |u|=1/√11 is fixed. The u→1 tree residue is the complexity
  **τ = 10²⁴·16¹⁵/40 = 2⁸¹·5²³** (matches index.html).

- **Track D — What the zeta cannot hear (idea 3).** Ihara and Bartholdi zeta are both functions of
  the adjacency spectrum, hence **identical on all 28 cospectral SRG(40,12,2,4)** graphs (Spence
  2000) — every one has the same π_G(m). You cannot hear which W(3,3)-parameter graph you are on
  from the (Bartholdi–)Ihara zeta; the finer **edge zeta** (2|E|×2|E|, non-spectral) is the
  distinguishing invariant. (Bartholdi/edge-zeta: 0 hits in the doc — new statement.)

## Doc-covered, made explicit

- **Track E — Artin–Ihara (idea 2).** The eigenspace multiplicities f=24, g=15 are irreducible
  representation degrees of PSp(4,3)=PSU(4,2); the Ihara quadratic factors are the equivariant
  L-factors for those irreps. (The doc already develops Deligne–Lusztig/Langlands for Sp(4,3).)
- **Track F — Weil vs Ihara (idea 5).** The symplectic polar space over F₃ has point counts
  |W(F_{3ⁿ})| = (3ⁿ+1)(3²ⁿ+1) = 3³ⁿ+3²ⁿ+3ⁿ+1 (=40 at n=1); its Weil (arithmetic) zeta is a
  different object from the Ihara (dynamical/graph) zeta of the same W(3,3). (The doc develops the
  Weil/Deligne–Lusztig side; this makes the point-count zeta explicit for contrast.)

## Enrichments folded back into the Pass 73 / paper narrative
- 78 = dim(E₆) is the error-bound / oscillatory-amplitude constant.
- disc_r = 40 = v, disc_s = 28 = v−k = dim SO(8) (index.html line 18122).

## Files
- `w33_pass74_zeta_frontier.py`, `w33_pass74_zeta_frontier.json` — witness + certificate.
- `tests/test_pass74_zeta_frontier.py` — 7 assertions.
- `w33_paper.tex` — new subsection "The Zeta Frontier" after the Prime-Geodesic Expansion.
