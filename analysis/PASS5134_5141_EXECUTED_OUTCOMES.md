# Passes 5134–5141 — executed outcomes

**Status:** science producers executed/committed on 2026-08-14; clean replay and homepage materializer workflows are tracked separately. Do not describe a queued workflow as green.

## 5134 — q=5 leader 18 is the exact second-order wall
The sharp adjacent selected-chamber pair cap for an 18-edge cut-minimal leader is 27. Exact Delsarte optimization at that cap gives `(N1,N2,N3,N4)=(27,73,53,0)`, pair overlap 5465, and only `wt>=320`. Thus pairwise Bonferroni/Delsarte is rigorously insufficient at leader 18. Pass5140 then supplies the missing cubic information and closes the shell.

## 5135 — q=5 heavy equality shells have a cubic defect
For local K6 cuts of weights 5,8,9, the selected theta-line-graph triangle counts are 10,8,6. At global weight 625,

`T_type = 2500 - 8 h8 - 12 h9`.

Together with `5 A_type + 3 h8 + 4 h9=1250`, the unique smallest exotic heavy profile `(h8,h9)=(2,1)` has `A_type=248`, `T_type=2472`: a third-moment defect of 28 from a chamber star on that chart type.

## 5136 — q=3 max-vote decoder radius is exactly five
Pass5131 proves every error of weight at most five is corrected. A structured weight-six word `{1,2,3,6,27,54}` makes false apartment 0 tie at global max vote 3; the first correction is `{0,1,2,3,6,27,54}` and therefore introduces a false bit. The mechanism is three charts through the false center with two errors in each, each local syndrome voting for the center. Thus the guaranteed radius of this specific hard-decision decoder is exactly five.

## 5137 — all-q linear theta spectrum plus exact full q=2,3,4,5 spectra
For the root-direction Cayley graph on U(q), the q^2-dimensional linear-character sector is

`4(q-1)^[1], (3q-4)^[2(q-1)], (2q-4)^[(q-1)^2]`.

For q=2,3,4,5 the complete spectrum is certified without floating diagonalization: a square-free integer annihilator polynomial is checked on `delta_e`, Cayley translation promotes it to the whole regular module, and exact closed-walk traces determine multiplicities. In all four anchors the second eigenvalue is `3q-4`, hence spectral gap q. A uniform nonlinear proof remains open.

## 5138 — state/program compiler preserves the Jennings filtration
The state and program coordinate laws on U(q) are intertwined by the Pass5133 polynomial compiler. Exhaustive product checks are performed at q=2,3,4,5. The k-linear extension is the same group-element basis map, so it preserves the augmentation ideal J, every J^r, and every associated Jennings layer. Protected root-height memory is therefore coordinate-independent under the compiler.

## 5139 — all-q chamber dependency code is closed
The chamber-generator dependency code is

`[(q+1)^2(q^2+1), 2(q+1)(q^2+1)-1, q+1]_2`.

Every minimum dependency is exactly a point- or line-panel star, giving `2(q+1)(q^2+1)` minimum words. Girth eight handles small cuts; the Levi nontrivial eigenvalue `sqrt(2q)` handles all larger cuts. This is the dependency/cut code, not the apartment-code distance theorem.

## 5140 — all-q triple law closes q=5 leader 18
For three distinct chamber stars, the common apartment count depends only on the sorted gallery-distance signature:

`(1,1,2)->q^2`, `(1,2,3)->q`, `(1,3,4)->1`, `(2,2,4)->1`, `(2,3,3)->1`, all other signatures `->0`.

These are exactly the five three-edge distance patterns available in an apartment C8. Complete rooted censuses verify the law at q=2,3,4,5, including GF(4). At q=5 the fixed-base histogram is `25^75,5^750,1^7500,0^428320`.

This exact cubic coefficient closes the m=18 shell. If `N1` is the number of adjacent selected chamber pairs in an 18-edge leader, then the number of selected three-edge paths satisfies

`P3 = sum_edges (d(u)-1)(d(v)-1) >= max(0,4(N1-18))`.

Each such path has signature `(1,1,2)` and therefore contributes 25 common apartments. The parity minorant

`1_{r odd} >= r - 2 C(r,2) + (6/17) C(r,3)` for `0<=r<=18`

combined with exact Delsarte pair maxima for every `N1<=27` has its worst shell at `N1=27`: the pair-only lower bound is 320, `P3>=36`, triple overlap is at least 900, and

`17 wt >= 17*320 + 6*900 = 10840`.

Hence `wt>=638>625`. Therefore every q=5 word of weight below 625 has minimum chamber leader at least **19**.

## 5141 — root-direction word metric has diameter at most four
Canonical four-positive-root factorization proves diameter at most four. Exact BFS anchors are frozen for q=2,3,4,5,7,11,13. At q=5,7,11,13 the shell counts agree with

`1`, `4(q-1)`, `8(q-1)^2`, `(q-1)^2(10q-21)`, `(q-1)^2(q-4)^2`,

which sum identically to q^4. This odd-q polynomial shell family remains conjectural beyond the exact anchors until a symbolic word-factorization count is supplied; q=2,3,4 exhibit small-field compression.

## Evidence boundary
The q=5/all-q apartment-code minimum distance remains open for leaders at least 19. Pass5140 closes leader 18 cubically; higher leader shells may require fourth and higher parity intersections. Radius six is false only for the specified hard-decision max-vote decoder; it is not a statement about ML decoding or code distance. The full nonlinear all-q theta spectrum/gap theorem is open. The odd-q metric shell polynomial is an anchored conjecture, not yet an all-q theorem. Controller/compiler/Jennings statements are finite algebra, not hardware performance.
