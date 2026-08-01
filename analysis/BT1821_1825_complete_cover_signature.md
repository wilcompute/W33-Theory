# Passes 1821–1825 — complete exact-cover census and nonlinear octet obstruction

## Executive result

This packet closes the finite exact-cover census for the canonical W33 frame carrier and identifies the first orbit-sensitive quotient beyond the linear Bockstein signature.

The deterministic verifier rebuilds `W(3,3)`, its 540 canonical frames, the 240 edge constraints, the 45 intrinsic induced `K4,4` octets, and the full `PSp(4,3)` action. A compiled Algorithm-X search exhausts every exact cover through frame zero:

\[
\boxed{|\mathcal C_{f_0}|=394200.}
\]

Frame transitivity and double counting give

\[
60|\mathcal C|=540|\mathcal C_{f_0}|,
\qquad
\boxed{|\mathcal C|=3547800.}
\]

The previous Pass-1505 lower bound was therefore the exact global count. The complete cover set has exactly

\[
\boxed{327}
\]

`PSp(4,3)`-orbits, with stabilizer-order census

\[
\boxed{2^{228},\;4^{84},\;8^{15}.}
\]

The selected four-cover packing remains nonextendible. The new result is that its obstruction is already visible in a 45-coordinate nonlinear quotient, strictly before the residual frame-level exact-cover search.

---

## Pass 1821 — complete exact-cover census

The search fixes frame zero and uses the 240 edge equations as an exact-cover instance. It visits every branch; no target count or timeout terminates the search. Every emitted cover has 60 frames and partitions all 240 W33 edges.

The fixed-frame census contains exactly 394200 covers. Orbit reduction under the four standard symplectic transvections and their inverses marks every one of those covers and produces 327 complete full-group orbits. Their sizes sum to 3547800, independently agreeing with the frame-transitivity double count.

Thus

\[
\boxed{|\mathcal C|=3547800,\qquad |\mathcal C/PSp(4,3)|=327.}
\]

This upgrades Pass 1505 from an exact lower-bound frontier to a complete classification count.

---

## Pass 1822 — four nonlinear signature types

The frame/octet coherent configuration has five cross orbitals. Exactly one has degree one from the frame fiber and degree twelve from the octet fiber. For an exact-cover indicator `x`, define

\[
t_o(x)=\#\{f\in\operatorname{supp}(x):(f,o)\text{ lies in that degree-one orbital}\}.
\]

Then

\[
t(x)\in\mathbb Z_{\ge0}^{45},\qquad \sum_o t_o=60.
\]

All five cross-orbital signatures collapse to this one vector:

\[
\boxed{(8\mathbf1,\;32\mathbf1,\;16\mathbf1-4t,\;4\mathbf1+3t,\;t).}
\]

Let `A45` be the adjacency matrix of `SRG(45,32,22,24)`. Every exact cover satisfies

\[
\boxed{(A_{45}+4I)t=48\mathbf1.}
\]

Equivalently,

\[
t-\frac43\mathbf1\in E_{-4}(A_{45}),
\]

so the nonlinear variability lives entirely in the canonical 20-dimensional octet constituent.

Every signature has a unique anchor octet: the coordinate with value four whose 32 octet-graph neighbors all have value one. The anchor's 12 nonneighbors induce the complete tripartite graph $K_{4,4,4}$, giving three canonical independent four-cells. The values on those cells are respectively

\[
(2,2,2),\quad(0,3,3),\quad(1,2,3),\quad(0,2,4).
\]

Thus the orbit count is explained geometrically as

\[
45(1+3+6+6)=720.
\]

The complete cover census realizes exactly 720 global signature vectors in four `PSp(4,3)`-orbits:

| Type | coordinate histogram | \(\|t\|^2\) | signature orbit | stabilizer | cover orbits | global covers |
|---|---:|---:|---:|---:|---:|---:|
| T128 | \(0^4 1^{32}2^4 4^5\) | 128 | 270 | 96 | 270 | 3,149,280 |
| T120 | \(0^4 1^{32}3^8 4^1\) | 120 | 135 | 192 | 6 | 38,880 |
| T104 | \(1^{36}2^4 3^4 4^1\) | 104 | 270 | 96 | 24 | 233,280 |
| T96 | \(1^{32}2^{12}4^1\) | 96 | 45 | 576 | 27 | 126,360 |

The cover-orbit counts sum to 327 and the global-cover counts sum to 3547800.

The affine eigenspace equation alone is not sufficient. The verifier freezes three bounded integer solutions—including max-4, max-3, and max-2 examples—that satisfy the same linear equation but occur nowhere in the complete cover census.

---

## Pass 1823 — exact nonlinear obstruction to completing the four-packing

For the certified four covers, their signature types are

\[
\boxed{T128,\;T96,\;T104,\;T128.}
\]

Because the degree-one cross orbital partitions the 540 frames into twelve frames above each octet, five additional covers would have to supply the exact residual capacity

\[
c=12\mathbf1-t_1-t_2-t_3-t_4.
\]

Its coordinate histogram is

\[
\boxed{2^1 4^1 5^9 6^6 7^{13}8^{13}9^2.}
\]

Of the 720 globally realizable single-cover signatures, 632 fit beneath this capacity coordinatewise. The exact meet-in-the-middle verifier enumerates 119642 admissible signature-pair multisets, collapsing to 117548 unique pair sums, and checks all 305488 admissible triple sums. No triple has a complementary pair sum:

\[
\boxed{\nexists\;u_1,\ldots,u_5\in\mathcal T\text{ with }u_1+\cdots+u_5=c.}
\]

Here `T` is the complete set of 720 globally realizable signatures. Therefore the known four-packing cannot acquire a fifth cover and cannot extend to a nine-cover resolution already in the 45-coordinate nonlinear quotient.

This is stronger than the earlier residual Algorithm-X certificate: it gives a small orbit-sensitive obstruction that can be applied before frame-level branching.

---

## Pass 1824 — correction to the linear-signature shortcut

Passes 1601–1810 proved that every cover has the same linear Bockstein signature. The present packet shows exactly where discrimination first appears:

\[
\boxed{\text{linear octet incidence is constant, but the degree-one cross-orbital count }t\text{ has four global types.}}
\]

The equation `(A45+4I)t=48*1` identifies the correct 20-dimensional carrier but does not characterize realizability. Exact-cover incidence imposes additional nonlinear constraints that cut the bounded lattice down to the four realized orbits.

---

## Pass 1825 — solver export and evidence boundary

The release exports all 720 signatures in deterministic compressed form, together with class labels, hashes, the four-packing capacity, and the exact pair/triple noncompletion certificate. A solver can introduce one choice among these signatures for each prospective color before opening the 540 frame variables.

All counts, orbit reductions, signatures, and the meet-in-the-middle obstruction are finite exhaustive computations. This packet proves that the selected four-packing has no completion and closes the global exact-cover census. It does **not** prove that no unrelated nine-cover resolution exists.
