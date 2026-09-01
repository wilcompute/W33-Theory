# Five-front execution: obstruction representation, binary D4 homology, and chart holonomy

Date: 1 September 2026

This synthesis records the five non-sequential attacks launched from the new
`1080 = 27 x 40` obstruction factorization.  It distinguishes positive theorems
from exact no-go results and preserves the correction boundary uncovered by the
chart-holonomy audit.

## 1 / 4. Complete the 1080 permutation module and materialize Steinberg

The earlier product-representation audit proved that the 1080-point obstruction
carrier is transitive under `PSp(4,3)`, has stabilizer order 24 and orbital rank
59, and contains the unique degree-81 Steinberg representation with
multiplicity three.  The new 59-orbital Wedderburn computation closes the full
ordinary decomposition.

Over the complex numbers the carrier has the constituent pattern

\[
1+6+2(15)+3(20)+2(24)+30
+2(30+\overline{30})+(40+\overline{40})+(45+\overline{45})
+3(60)+3(64)+3(81).
\]

The three non-rational central factors are exactly the degree-30, degree-40 and
degree-45 conjugate pairs.  Their quadratic discriminants are all `-3` times a
rational square, so the common splitting field is

\[
\boxed{\mathbb Q(\sqrt{-3})}.
\]

The Steinberg isotypic component has rank `243=3*81`.  A deterministic symmetric
orbital operator `B` has multiplicity-space eigenvalues `+4,0,-4`, producing
three exact rational primitive projectors

\[
P_+=\frac{B(B+4E)}{32},\qquad
P_0=E-\frac{B^2}{16},\qquad
P_-=\frac{B(B-4E)}{32}.
\]

Each has rank 81; they are pairwise orthogonal and sum to the central Steinberg
projector.  Thus the three copies are no longer abstract character
multiplicities: there are explicit `PSp(4,3)`-equivariant rank-81 projectors on
the obstruction carrier.

Artifacts:

- `analysis/w33_20260901_obstruction_wedderburn_steinberg_projectors.py`
- `data/PART_W33_20260901_OBSTRUCTION_WEDDERBURN_STEINBERG.json`

## 2. Completion-chart cuts do not survive even chart-stabilizer compression

The Holotrade depth-five frontier remains

\[
13\le s_5\le22.
\]

The first full-group chart-cut test showed that the 27 completion-chart
coordinates become identical after quotienting by all of `PSp(4,3)`.  We then
performed the stronger test proposed as the next step: fix one completion
chart and quotient only by its order-960 stabilizer.

The fixed chart contains ten all-isotropic reguli partitioning the forty W33
lines.  For each line `ell`, delete `ell` from its unique regulus and use the
ordered depth-five witness

```text
(bad1,bad2,bad3,ell,ell).
```

All six bad-triple orders give 240 witness tiles.  Exact enumeration gives:

```text
chart stabilizer                         960
ordered witness tiles                    240
witness tile H-orbits                      1
leaves enumerated                    245,760
distinct leaves                      243,600
relevant H-leaf orbits                    269
```

Every one of the 269 relevant leaf orbits intersects every one of the 240
witness tiles.  Hence both the fractional and integer restricted cover optima
are exactly one.

This closes the canonical 40-coordinate regulus cut family negatively:
breaking only to a chart stabilizer is still too symmetric.  A cut capable of
moving the global lower bound 13 must break below the chart stabilizer
(packet/line/flag level) or incorporate a genuinely different nonlinear or
integer witness.

Holotrade artifacts:

- `analysis/depth5_chart_stabilizer_cut_nogo.py`
- `data/depth5_chart_stabilizer_cut_nogo.json`

## 3. The binary D4-prism H1 is a nonsplit 24-by-24 extension

The 90-D4 lift has integral curvature

\[
\widetilde R\widetilde N=6Q
\]

and therefore becomes a genuine complex modulo two, with

\[
\dim H_1(\mathbb F_2)=48.
\]

In characteristic two the pair-injection space satisfies
`im(J)=ker(J^T)`, dimension 45.  This gives a canonical invariant filtration

\[
\boxed{0\longrightarrow A_{24}\longrightarrow H_{1,48}
\longrightarrow B_{24}\longrightarrow0},
\]

where

\[
A_{24}=\operatorname{im}(J)/\operatorname{im}(\widetilde N),
\]

and `B24` is the corresponding 24-dimensional pair-sum quotient/kernel.
The exact generator cocycle blocks have ranks

```text
18, 6, 18, 14.
```

Solving the full splitting equation over `F2` gives no solution.  Hence the
extension is nonsplit.  Moreover

\[
\dim\operatorname{Hom}_G(B_{24},A_{24})=2,
\]

with deterministic basis-map ranks `1` and `10`, so there is no invertible
intertwiner identifying the two 24s.  Their global fixed dimensions differ as
well: `1` for `A24`, `0` for `B24`.

The tempting independent E8/Kummer `48` from the Z12 common refinement also
fails an object-level comparison: a product of two E6 root reflections, hence
an even `W(E6)` element on the inner `PSp(4,3)` side, sends a root from the
Z12-48 joint grade to the neighboring Z12-30 joint grade.  Therefore that
48-root grade is not itself `PSp(4,3)`-invariant and cannot be this binary H1
carrier.

Artifacts:

- `analysis/w33_20260901_binary_h1_48_nonsplit.py`
- `data/PART_W33_20260901_BINARY_H1_48_NONSPLIT.json`

## 5. Corrected chart compiler: S3 port gauge, not a global C3 sheet

The holonomy attack uncovered a necessary correction.  On the native
polar-pair/sentinel 45-packet action used by the new E8 completion catalogue,
a packet stabilizer has order 576 and induces the **full `S3`** on the three
completion charts through that packet.  There is therefore no global
`PSp(4,3)` cyclic-orientation sheet on this specific 45-action.

That must not be silently conflated with the older residue/cube degree-45
action of Pass 4795, where the inner local image is `C3` and a global
orientation sheet is certified.  The graph-level degree-45 identifications can
be outer-twisted as group actions.

The corrected compiler fixes a complete ordering of the three incident chart
ports at every packet.  Relative to that port gauge every group element has a
unique local correction

\[
\sigma_g(p)\in S_3,
\]

and the exact nonabelian cocycle identity

\[
\boxed{\sigma_{ab}(p)=\sigma_a(b\cdot p)\circ\sigma_b(p)}
\]

holds in all `4*25920*45 = 4,665,600` generator/group/packet checks.  The only
group element with zero correction at all 45 packets is the identity.

For every packet there are exactly 24 order-three global elements fixing the
packet and inducing a chosen positive three-cycle in its port gauge.
Deterministically selecting one per packet gives local triality rotations.
Four rotations, at packet indices

```text
0, 9, 11, 33
```

generate the full chart group, with subgroup growth

```text
3 -> 9 -> 288 -> 25,920.
```

The 27-chart overlap graph has 135 edges.  A spanning tree has 26 edges and
leaves 109 fundamental cycles.  Their holonomy order profile is

```text
1:15, 2:25, 3:5, 4:14, 5:25, 6:25.
```

After transport to one base chart these 109 cycle holonomies generate a group
of order 960, exactly the full base-chart stabilizer.

Thus the corrected finite compiler theorem is

\[
\boxed{
\text{full three-port gauge}
+\text{ packet triality rotations}
\Longrightarrow PSp(4,3),
}
\]

with chart-loop holonomy equal to the full order-960 chart stabilizer.

Artifacts:

- `analysis/w33_20260901_e8_chart_port_holonomy.py`
- `data/PART_W33_20260901_E8_CHART_PORT_HOLONOMY.json`

## Evidence boundary

All results in this packet are exact finite incidence, representation, modular
homology, or permutation-group statements.  The E8 labels refer to the
already-certified selected root/packet realization.  No new optical dynamics,
physical error rate, coupling, mass, or hardware capability is inferred from
these finite carriers.
