# Passes 5074–5081 — gauge-test distance reduction, sharbly dictionary, q=4/q=5 shell attacks, local decoder, and three outside-box closures

**Status:** EXECUTED 2026-08-14. The packet begins from Pass5066, which already proved the all-prime-power presentation `F2[apartments]/Theta ~= Z1(Levi;F2)`. Nothing below reclaims that theorem. The all-q minimum-distance statement and complete q=4 minimum shell remain open unless explicitly stated otherwise.

## 5074 — the distance wall is an exact Z2 gauge/local-test inequality
Pass5066 identifies the theta quotient with the Levi cycle space. Dualizing gives the apartment code as character evaluation of edge 1-cochains modulo cuts. For an edge cochain `y`, the apartment coordinate is the Wilson parity `<y,∂A>`. For an opposite same-type pair `O`, evaluate `y` on its `q+1` length-four geodesics. The local apartment values are pairwise sums of these path parities, so the chart is inactive iff all path parities agree; otherwise its restriction is a nonzero cut of `K_{q+1}`.

Therefore the exact global identity is

`4 wt(c_y) = sum_O wt(c_y|_O)`,

and the local cut theorem gives

`wt(c_y) >= q A(y)/4`,

where `A(y)` is the number of active opposite-pair charts. Consequently the still-open family distance theorem is equivalent to the sharp tester inequality `A(y)>=4q^3` for every non-cut cochain. A single chamber/edge cochain saturates both inequalities: it has `wt=q^4`, exactly `4q^3` active charts, split equally between point and line charts, and every active local cut has minimum weight `q`. This saturation was rebuilt exactly for q=2,3,4,5.

This is a substantial reduction, not the missing lower-bound proof.

## 5075 — exact part of the Pal/sharbly dictionary, with a firewall on the unproved part
Urshita Pal's 2026 symplectic sharbly resolution presents the symplectic Steinberg module by apartment-type `V0` generators and two first-relation types `V1,1` and `V1,2`. In rank two, a `V0` generator is a tensor of two genus-one `Sh_0` factors on perpendicular symplectic planes, exactly the data of a symplectic-basis apartment. A `V1,1` generator replaces one genus-one pair by a three-line `Sh_1` generator; its ordinary three-term sharbly boundary, after reduction mod 2 and with the other plane fixed, is exactly the three apartments through the two fixed opposite point vertices. Thus the `V1,1 -> point-theta` relation-type dictionary is explicit.

Pal's `V1,2` differential is a sum of genus-two split terms. It is structurally the right slot for the dual/line-side theta relations, but this pass did **not** build the literal chain map identifying every `V1,2` split term with every line-theta generator. Pass5066 remains the actual all-q finite-field theta-presentation theorem. Pal and Brück–Patzt–Sroka are independent corroboration of the apartment-generator/presentation architecture, not a substitute proof.

## 5076 — q=4 minimum shell pushed three generator layers deep
The exact q=4 code is `[13600,256,256]_2`; Pass5067 could not classify all weight-256 words. This pass exhaustively enumerates all sums of one, two, and three distinct chamber-star generators among the 425 stars.

- one generator: weight 256;
- every pair: minimum 384, with exact histogram `384^1700, 480^6800, 504^27200, 510^54400`;
- every triple: minimum 384. The complete triple histogram is frozen by the producer.

Hence any hypothetical non-chamber-star word of weight 256 has no representation using at most three distinct chamber-star generators. This is an exact strengthening of the q=4 shell frontier, but the 169-dimensional dependency kernel prevents promotion to a complete minimum-shell classification.

## 5077 — q=5 distance survives a symmetry-aware falsifier
Pass5066 gives dimension 625 and a chamber-star upper bound 625 for the q=5 code of length 73,125. All `C(936,2)` pairs of chamber stars were enumerated exactly. Their minimum XOR weight is 1000, with histogram

`1000^4680, 1200^23400, 1240^117000, 1248^292500`.

The pair intersections are therefore `125,25,5,1`, matching the four chamber gallery distances. A deterministic-seeded multi-star local descent (200 starts, 1200 moves/start) found no nonzero word below 625; its best word was again one chamber star. Thus `d=625` survives this attack, but no q=5 minimum-distance theorem is claimed.

## 5078 — the local theta theorem becomes a tiny exact decoder
A chart is the cut code of `K_{q+1}`. Fixing the potential at one root removes the global-complement gauge, leaving exactly `q` reconstruction bits. An independent syndrome basis is the set of triangles `(0,i,j)`, so the syndrome rank is `q(q-1)/2`. Exhaustive nearest-cut decoding gives finite exact ROMs:

- q=2: 1 syndrome bit, 2 entries, covering radius 1;
- **q=3: 3 syndrome bits, 8 entries, covering radius 2**;
- q=4: 6 syndrome bits, 64 entries, covering radius 4;
- q=5: 10 syndrome bits, 1024 entries, covering radius 6.

For the physical q=3 Holonet branch, the local theta correction primitive is therefore literally an eight-entry correction ROM. This is compiler arithmetic only; no global decoder threshold, optical loss model, or fabricated hardware performance is inferred.

## 5079 — BONKERS 1: all-q Tanner six-cycle law closes
Pass5073 had the q=2,3,4,5 anchors `N6=T(q)(q-2)` but left a no-cross-chart lemma. The lemma follows from the rank-two root geometry. If apartments `A=R∪R1` and `B=R∪R2` share root `R`, an apartment adjacent to both is either the theta companion `R1∪R2` or also contains `R`; any other two-root arrangement would produce two distinct geodesics between vertices at distance below four, contradicting girth eight. Thus a genuine Tanner six-cycle is exactly a choice of three apartments through one common root.

There are `q^3(q+1)^2(q^2+1)` roots and `C(q,3)` such triples per root, hence

`N6 = q^3(q+1)^2(q^2+1) C(q,3) = T(q)(q-2)`

for every q. This promotes the former four-anchor pattern to a theorem.

## 5080 — BONKERS 2: the distance problem is a sharp Fourier coefficient problem
Let `mu` be the uniform measure on apartment boundaries inside the Levi cycle space. For a cohomology character `chi_y`,

`wt(c_y) = N_A (1 - muhat(y))/2`.

Therefore `d=q^4` is exactly equivalent to

`max_{y nontrivial} muhat(y) <= 1 - 16/((q+1)^2(q^2+1))`,

with chamber/edge characters attaining equality. The complete q=2 code was enumerated (all `2^16` words): its minimum weight is 16 and its 45 minimum words are **exactly** the 45 chamber stars. The extremal q=2 Fourier value is `29/45`. This opens a representation/Hecke route to the all-q distance problem that is independent of the active-chart combinatorics.

## 5081 — BONKERS 3: theta checks are the complete dual minimum shell
For any finite generalized quadrangle apartment code, every theta triple is a weight-three dual word. Conversely, if three distinct apartments `A,B,C` satisfy `∂A+∂B+∂C=0`, then `C=A△B`. Since all three boundaries are 8-cycles, `A` and `B` share exactly four edges. In a girth-eight generalized-quadrangle incidence graph, such an overlap must be one contiguous length-four root; otherwise the symmetric difference splits or produces a shorter circuit. The complementary roots of `A` and `B` then form `C`. Hence the three apartments are exactly a local theta triple.

Thus the dual minimum distance is exactly 3 and the complete dual minimum shell is the theta hypergraph, with

`A_3(C^perp)=q^3(q+1)(q^2+1) C(q+1,3)`.

As a separate q=2 MacWilliams check, the complete `[90,16,16]` enumerator gives dual coefficients `A1=A2=0` and `A3=120`, exactly the 120 theta checks. The Tanner check set is therefore intrinsic to the code: it is recoverable as the complete set of dual minimum words.

## Synthesis and boundary
The five requested fronts were all executed. The Pal dictionary is partially exact and explicitly firewalled at `V1,2`; q=4 shell classification and all-q/q=5 minimum distance remain genuinely open. In exchange, the packet closes two family-level structural statements that were not on the original list: the all-q Tanner six-cycle formula and the complete dual-minimum theta shell. It also supplies a second all-q distance attack through Fourier extremality and turns the local cut theorem into an implementable q=3 eight-entry decoder primitive.
