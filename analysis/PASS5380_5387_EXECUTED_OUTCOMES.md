# Pass5380–5387 executed outcomes

Status: **EXECUTED WITH PASS5383 HOFFMAN SOLVER PENDING**.

This packet was deliberately rebased against fast-moving parallel work. Two inherited targets were already solved elsewhere before this packet finished: Pass5262 had already closed q=5 apartment distance at `[73125,625,625]_2`, and Pass5263 had already closed q=3 eventual decoder radius eight. A parallel Pass5376–5379 packet also closed the all-odd binary footprint rank/kernel theorem while this packet was running. The work below consumes those results rather than duplicating them.

## Pass5380 — q=5 distance-filtered code extension

The q=5 apartment code, its zero-footprint kernel, and the footprint quotient fit into

\[
0\to K_0\to C_A\to C_F\to0
\]

with exact parameters

\[
C_A=[73125,625,625]_2,\qquad
K_0=[73125,560,1000]_2,\qquad
C_F=[325,65,25]_2.
\]

The minimum shells have sizes 936, 2340, and 156 respectively. Thus every apartment-code word of weight below 1000 has nonzero point footprint, and the zero-footprint kernel is separated from the physical chamber-star minimum by the exact gap `1000/625=8/5`.

## Pass5381 — q=3 global eventual radius nine

The deterministic decoder is `maximum vote -> maximum singleton provenance -> minimum tie degree`.

For a fixed false center, a false candidate has vote at most four. The complete weight-nine analysis gives:

* `V=1`: exact stopping-set MILP infeasible.
* `V=2`: exact MILP with total weight nine, false center absent, exactly two false votes, and at least three spoiled charts per selected true error is infeasible.
* `V=3`: exactly 32 rooted candidates survive the necessary condition; every one clears `9 -> 10 -> 1 -> 0`.
* `V=4`: all 25,648 rooted configurations clear. The dominant trace is `9 -> 8 -> 9 -> 1 -> 0`.

Therefore every weight-nine error either makes a nonempty true-only first correction and enters the certified radius-eight basin, or lies in an explicitly classified false-survivor family and self-heals. Hence the **global eventual guaranteed radius is nine**. The monotone true-only radius remains sharply seven because the radius-eight echo family still makes a false first move.

## Pass5382 — q=5 connected-L characteristic-two primary projectors

Pass5240's exact Jordan data imply

\[
m_A(x)=x^3(x+1)^4.
\]

Over \(\mathbb F_2\), \((x+1)^4=x^4+1\), so the primary projectors are simply

\[
P_1=A_L^4,\qquad P_0=I+A_L^4.
\]

Their ranks are 6034 and 3716. This is an exact nonsemisimple scalar theorem. It does not repair the known Pass5266 failure of raw channelwise transport; rather, any correct twisted ten-channel lift must respect these canonical primary projections after channel coordinates are forgotten.

## Pass5383 — Hoffman shortened-code exact SAT replay

The exact full `[312,52,d]_2` XOR-SAT model from Pass5348 is now an executable packet producer. It asks whether a nonzero shortened word of weight at most 39 exists. The current rigorous state remains

\[
d\in\{28,32,36,40\}.
\]

No solver conclusion is promoted here until clean PySAT execution completes. UNSAT proves `[312,52,40]_2`; SAT is reconstructed and verified as an explicit counterexample.

## Pass5384 — all-odd apartment/footprint gauge exact sequence

Using the parallel all-odd footprint theorem,

\[
0\to D_q=K_0\to C_A\to C_F\to0
\]

is exact for every odd prime power \(q\). The dimensions are

\[
\dim C_A=q^4,
\qquad
\dim C_F=\frac{q(q^2+1)}2,
\qquad
\dim D_q=\frac{q(q-1)(2q^2+q+1)}2.
\]

Thus the all-odd footprint quotient is no longer a rank problem. The remaining all-odd apartment-distance problem is a Hamming-weight problem inside `D_q` and its nonzero footprint cosets.

## Pass5385 — the q=5 K0 minimum shell reconstructs W(3,5)

The multiplicity-one `65_a` central frame collapses every 15-word minimum-shell fiber to one vector. Quotienting 2340 words by that duplicate relation leaves 156 vectors. Their off-diagonal frame relations are:

* inner product `-1/5`: 30 vectors,
* inner product `+1/25`: 125 vectors.

Joining the `-1/5` pairs reconstructs exactly `SRG(156,30,4,6)=W(3,5)`. Thus the zero-footprint minimum-shell algebra remembers the point geometry that labels its block supports.

## Pass5386 — all-q consecutive-gallery intersection tower

For \(1\le k\le5\) consecutive chambers on an apartment,

\[
\left|\bigcap_{i=1}^k \operatorname{Star}(c_i)\right|=q^{5-k}.
\]

The exact tower is

\[
q^4,\;q^3,\;q^2,\;q,\;1.
\]

The new `k=5` step follows from the generalized-quadrangle projection axiom: a five-edge gallery leaves a point opposite a terminal line, which determines the unique closing point and line. This gives rigorous geometric content to the earlier derivative-looking power drop, while explicitly **not** asserting a calculus identity.

## Pass5387 — local `(16,6,2)` K0 difference sets

On each q=5 point footprint, the restricted K0 kernel is \(\mathbb F_2^4\). Translating the six chamber-star restrictions by one chosen star gives a six-element set \(D\) whose 15 unordered pair differences are exactly all 15 nonzero elements of \(\mathbb F_2^4\). Therefore \(D\) is a

\[
(16,6,2)
\]

difference set. Its 16 translates form a symmetric `2-(16,6,2)` design, and every nontrivial additive character has magnitude 2 on `D`.

## Evidence boundary

Seven slots are theorem/computational-theorem level. Pass5383 remains solver-pending. The q=5 distance theorem, q=3 radius-eight theorem, and all-odd footprint rank theorem are parallel dependencies that were already closed outside this packet; this packet uses them but does not claim to rediscover them.
