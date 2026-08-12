# Passes 4951–4958 — executed outcomes and correction ledger

Status: **EXECUTED ON MASTER; exact replay workflow queued/unobserved at close time**.

This packet began as a second-wave continuation of Passes 4940–4947. It produced one covering-radius improvement and one major geometry correction that reorganizes several earlier results without discarding their valid orbital/module arithmetic.

## Pass 4951 — third-moment covering-radius ceiling

For `K=[360,36,20]_2`, frozen dual data give

- `A1(K^perp)=A2(K^perp)=0`,
- `A3(K^perp)=1080`,
- every coset has mean weight `180` and variance `90`,
- the third centered moment obeys `|mu3| <= 810`.

For a coset leader of weight `delta`, positivity of `(X+a)(X-t)^2` with `a=180-delta` and optimized `t=90/a` gives

`mu3 >= 90*(90/a-a)`.

This excludes every `delta>=175`. Equality at `delta=174` would force all coset weights to be only `174` or `195` in population ratio `5:2`, impossible because the coset size is `2^36` and is not divisible by `7`.

Current exact interval:

`134 <= rho(K) <= 173`.

The lower endpoint is the exact Pass4940 hard-word distance. The exact covering radius remains open.

## Pass 4952 — incidence singular filter

The corrected 40×40 non-splitting quotient is W33 point-line incidence `Z`.

Rows: 40 W33 points.  
Columns: 40 W33 lines, whose collinearity/intersection graph is the odd-q dual `Q(4,3)`.

Exact identities:

- `ZZ^T = 4I + A_W`,
- `Z^T Z = 4I + A_Q43`.

Singular spectrum:

`4^1, sqrt(6)^24, 0^15`, rank `25`.

Thus incidence transmits the common `1+24` sector and kills a distinct 15-dimensional `-4` constituent on each side.

## Pass 4953 — standard W33 triad baseline

The standard symplectic W(3,3) point graph has `3240` independent triples with common-neighbor census

`1^2880 4^360`.

The 360 four-center triples are exactly the 3-subsets of the 90 non-isotropic projective lines of `PG(3,3)`.

This is the correct W33 point-triad law.

## Pass 4954 — major correction: Steiner quotient is Q(4,3), not W33 points

Rebuilding the Pass4870 forty-fiber quotient and comparing it to both degree-40 generalized-quadrangle actions proves:

- it is **not** isomorphic to the standard W33 point graph;
- it **is** isomorphic to the W33 line-intersection graph;
- equivalently it is the point graph of `Q(4,3)`, the nonisomorphic odd-q dual generalized quadrangle;
- its independent-triad center census is `0^1080 2^2160`;
- it has no spread.

This resolves the Pass4947 tension: its `0/2` arithmetic was correct, but it was attached to the wrong degree-40 action.

The legacy Pass4870 certificate, manuscript insert, addendum, and public page have been corrected. The quadratic-Hom theorem survives; only the quotient label changes from W33 point adjacency to Q43/W33-line adjacency.

## Pass 4955 — maximum cuts are W33 points; Steiner fibers are W33 lines

The Pass4946 cross-incidence was rebuilt from scratch.

- 120 maximum-cut rows collapse into 40 identical triples;
- 120 Steiner columns collapse into 40 identical triples;
- the quotient non-splitting matrix has row/column weight four and rank 25;
- the row collinearity graph is the standard W33 point graph;
- the column collinearity graph is the Q43/W33-line graph.

Therefore:

`120 maximum cuts / 3 = 40 W33 points`,

`120 Steiner triangles / 3 = 40 W33 lines`,

and the quotient matrix is literal point-line incidence.

## Pass 4956 — canonical 24-dimensional point-line intertwiner

The incidence identities imply an exact representation bridge:

`A_W Z = Z A_Q`.

On the shared 24-dimensional `+2` sectors,

`Z^T Z = ZZ^T = 6I`,

so `Z` is an isomorphism with inverse `Z^T/6`.

On the two 15-dimensional `-4` sectors, `Z` vanishes identically.

This gives a canonical rational point/line intertwiner on `24`, while preserving the known inequivalence of the two `15`s.

## Pass 4957 — Q43 ovoids are exactly W33 spreads

Under the corrected interpretation, a size-10 coclique in Q43 is ten pairwise disjoint W33 lines, hence a spread.

Exact enumeration:

- maximal cocliques of size 5: `432`,
- size 8: `135`,
- size 10: `36`.

The 36 maximum cocliques are set-equal to the 36 W33 spreads.

Their pair intersections reproduce the independently frozen Pass2000 census:

`1^360 4^270`.

Each W33 line belongs to exactly nine spreads.

## Pass 4958 — complementary point/spread transceiver

Prior-art credit is explicit:

- Pass173 already owns the point-line transceiver and its `1+24` nonzero sector;
- Part CXXVI already owns the spread-line Morita spectrum `90^1,18^15,0^24` and rank 16.

The new result is their exact complementarity after the corrected W33/Q43 identification.

Let `Z` be point-by-line incidence and `B` line-by-spread incidence. Then

- point channel: transmits `1+24`, kills `15`;
- spread channel: transmits `1+15`, kills `24`;
- stacked map `[Z;B^T]` has full rank `40`.

Exact reconstruction identity:

`18 I_40 = 3 Z^T Z + B B^T - 3 J_40`.

Hence every line vector is recovered by

`x=(1/6)Z^T(Zx)+(1/18)B(B^T x)-(1/6)Jx`.

Primitive projectors:

- `E24=(5 Z^T Z-2J)/30`,
- `E15=(4 B B^T-9J)/72`,
- `E0=J/40`.

Fraction-free completeness:

`9J + 12(5Z^TZ-2J) + 5(4BB^T-9J) = 360I`.

## Publication and regression state

Integrated/corrected:

- `analysis/PASS4870_steiner_w33_quadratic_bridge_insert.tex`
- `data/PART_W33_PASS4870_STEINER_W33_QUADRATIC_BRIDGE.json`
- `analysis/PASS4870_BREAKTHROUGH_ADDENDUM.md`
- `docs/pass4870-steiner-w33-quadratic.html`
- `analysis/PASS4940_4947_radius_quartic_holonomy_duality_insert.tex`
- `docs/pass4940-4947-radius-quartic-holonomy.html`
- `analysis/PASS4951_4958_radius_q43_transceiver_insert.tex`
- `analysis/W33_CURRENT_FRONTIER_MANIFEST.tex`

Regression:

- `tests/test_w33_pass4951_4958_radius_q43_transceiver.py`
- `.github/workflows/w33_pass4951_4958_radius_q43_correction.yml`

At close time the dedicated Actions run is **queued**, not green or failed. Do not report remote replay as passed until observed.

## Hard boundaries

1. `rho(K)` is not closed; only `134 <= rho <= 173` is proved.
2. `W(3,3)` and `Q(4,3)` share SRG parameters but are not isomorphic at q=3.
3. The Steiner quotient is the line action / Q43 graph; do not call it a second W33 point graph.
4. The quadratic and quartic adjoint maps remain finite characteristic-three module constructions, not continuum couplings.
5. Pass4958 combines previously known individual incidence spectra; the new theorem is the complementary full-rank reconstruction identity.
