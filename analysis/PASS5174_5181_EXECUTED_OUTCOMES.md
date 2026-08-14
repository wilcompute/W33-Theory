# Pass5174–5181 executed outcomes

**Status:** EXECUTED 2026-08-14. This packet deliberately avoided the collision-owned q=5 leader-31 continuation in Pass5182–5189. It closes four independent open fronts, introduces a fourth-order leader tool, and exposes the correct point/line asymmetry in the q=5 equality-shell problem.

## Pass5174 — full all-q theta spectral gap

In canonical maximal-unipotent coordinates,

`(a,b,c,d)*(A,B,C,D)=(a+A,b+B,c+C-Ab,d+D-2Ac+A^2b)`.

Right root subgroups `H1,H2,H3` therefore translate `b,c,d`. Fourier transform in those coordinates diagonalizes `P1+P2+P3`. The uniform linear-character sector is exactly the `q^2`-dimensional space independent of `c,d`; on its orthogonal complement at least one of the `c,d` frequencies is nonzero, so `P1+P2+P3<=2I`. Since `P0<=I`,

`sum_i P_i <= 3I`

on the complete nonlinear sector. With `A_theta=q sum_i P_i-4I`, and with the already-proved linear eigenvalue `3q-4`,

`lambda_2(A_theta)=3q-4`, `gap=q`

for every finite field.

## Pass5175 — characteristic-two root metric

Characteristic two collapses one two-root ordering family because the `(0,2)` commutator correction contains a factor `2`. The exact shells for `q=2^f` are

`1`, `4(q-1)`, `7(q-1)^2`, `4(q-1)^2(2q-3)`, `(q-1)^2(q-2)(q-4)`.

Exact BFS anchors are q2 `1,4,7,4`, q4 `1,12,63,180`, and q8 `1,28,343,2548,1176`. Together with Pass5143 and Pass5165, the root-direction Cayley word metric is now symbolically classified over every finite field.

## Pass5176 — the hub-only decoder is falsified, then global radius six closes

Pure max-vote plus minimum tie-degree fails on

`{0,219,492,493,526,527}`.

Its max-vote tie has nine vertices, all tie-degree four, including false candidates `216,494,525`. The repair uses vote provenance:

`maximum vote -> maximum singleton-source count -> minimum tie-degree`.

A false candidate cannot receive a singleton-source vote because a singleton local mask decodes to its occupied coordinate. An exact C++ scan covers all `11,401,011` connected weight-six sets through a base apartment. Every one has a nonempty first correction contained in the true error set. Connected weights one through five replay with zero failures and maximum three sweeps. A component argument excludes false candidates in every disconnected partition of six. Therefore every q3 error of weight at most six clears under the refined rule in at most four sweeps.

## Pass5177 — q5 P-side tensor heavy-shell theorem, with asymmetry correction

For P/opposite-point charts, the chart-intersection graph splits into 325 copies of `K_15,15`. The theta restriction code on one component is

`Cut(K6) tensor Cut(K6) = [225,25,25]_2`.

All `2^25=33,554,432` component states were enumerated, yielding 140 `(weight,h8,h9,active)` profiles. Under `h8<=2,h9<=1`, only

`(0,0,0,0)`, `(25,0,0,10)`, `(48,2,0,18)`

occur. The old P-side profile `(h8,h9)=(2,1)` is impossible. At total P-weight 625, the minimum positive coarea cost `3h8+4h9` is 50, so any P-heavy weight-625 word satisfies `A_P<=240`; consequently total active charts are at most 490 **conditional on P-side heaviness**.

A critical correction was made before release: for odd q the L/opposite-line chart graph is not the same tensor decomposition. At q3 and q5 it is connected. Therefore this pass does not eliminate an L-heavy-only exotic minimum word.

## Pass5178 — fourth-order parity frontier

For apartment occupancy `0<=r<=8`,

`1_{r odd}=r-2*C(r,2)+4*C(r,3)-8*C(r,4)+R5(r)`

with remainder table

`0,0,0,0,0,16,64,176,384`.

Hence

`wt >= S1-2S2+4S3-8S4+16*N_{r>=5}`.

Pass5140 supplies the exact triple coefficient and Pass5159 the exact four-chamber coefficient. If every apartment has occupancy at most four, the quartic formula is exact. This is a collision-safe tool for the parallel leader frontier.

## Pass5179 — all-q P-component minimum shell

If `C=Cut(K_{q+1})=[m,q,q]`, `m=C(q+1,2)`, then the P-component code is `C tensor C=[m^2,q^2,q^2]`. Every weight-`q^2` tensor word is a simple tensor of two factor minimum words; therefore there are exactly `(q+1)^2` component minimum words. At q5 this explains the 36 weight-25 states from the exhaustive component census.

## Pass5180 — P atoms resolve line-panel chamber pairs

The restrictions of all chamber stars to P components exhaust the P tensor minimum shell in the exact q2,3,4,5 anchors. Every P atom has weight `q^2`, occurs in exactly two chamber stars, and those two chambers share a line panel. Every same-line chamber pair owns exactly `q` atoms. A chamber star is the disjoint union of `q^2` atoms.

Thus at q5 a P-heavy-free weight-625 candidate is exactly 25 disjoint P atoms. A chamber star is the special 25-atom pattern taking all five atom copies over each of the five same-line panel edges incident with one chamber. The equality problem is thereby reduced from 625 apartment coordinates to a labeled 25-atom gluing problem against the L constraints.

## Pass5181 — point/line duality firewall

The unexpected P/L asymmetry matches classical generalized-quadrangle duality. For even q, `W_3(q)` is self-dual, so the P tensor decomposition transfers to L. For odd q, `W_3(q)^D=Q_4(q)`, so no same-geometry duality permits that transfer. Exact repo anchors are:

- q2: P and L each 10 copies of `K_3,3`;
- q3: P has 45 copies of `K_6,6`, L is connected on 540 charts;
- q4: P and L each 136 copies of `K_10,10`;
- q5: P has 325 copies of `K_15,15`, L is connected on 9750 charts.

External prior-art boundary: Crnković–Hawtin–Švob, arXiv:2105.05833, Section 2, explicitly states that `W_3(q)` is self-dual for even q and has dual `Q_4(q)` for odd q.

## Evidence boundary

The q5/all-q apartment-code minimum-distance theorem remains open. The P-side tensor result does not eliminate L-heavy-only equality candidates. The q5 strict leader frontier is being advanced independently in the collision-owned Pass5182–5189 namespace and should be read from its latest certificate. The all-q theta gap and all-finite-field root metric are closed mathematical statements; decoder claims are for the exact finite hard-decision rule only.
