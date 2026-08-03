# Passes 2901–2907 — intrinsic selector channels, a real butterfly engine, exact observer quotients, and two falsifiers

## Executive result

This packet executes the five continuations left open by Passes 2854–2860 and follows two deliberately unconventional probes until they either close or fail exactly.

1. The three residual selector channels do not admit a globally canonical numbering. Their intrinsic object is an affine line of order three: the multiplier-one stabilizer supplies the translation group `C3`, while the full similitude stabilizer supplies `AGL(1,3)=S3` transition functions.
2. The symbolic `q`-Hadamard identity is promoted to a literal `q=3` sequential architecture: 32 local butterflies and 15 output cycles, 47 cycles total, versus 225 cycles for a serial dense reference.
3. The complete congruence atlas for every nonempty subset of the four-operation micro-ISA proves that the full ISA has no nontrivial exact support-refining execution quotient. The observer chain `16 -> 40 -> 78 -> 81` terminates only at the discrete frame partition.
4. The natural order-96 tomotope embedding has two 48-state orbits. A determinant-twisted order-96 signed-permutation group instead acts freely and transitively on the 96 selector–tomotope control tokens, making the token space an exact group torsor.
5. The 210 directed support first-passage costs reduce to 39 `D8` orbits and 15 exact feature classes. Held–Karp optimization gives a 15-mask diagnostic cycle of total cost `315`, with 8,336 rooted optima.
6. **Outside-box I:** no `GL(4,2)` Singer cycle is optimal for that directed passage objective. The best linear recurrence costs `1317/4`, leaving an exact nonlinear advantage of `57/4`.
7. **Outside-box II:** the tempting identification of the first 40 observer classes with the 40 points of `W(3,3)` is false. Class sizes are wrong, symplectic orthogonality does not descend, and no union of signature-Hamming relations produces `SRG(40,12,2,4)`.

The release contains **64 exact theorem checks** and **7 focused regression tests**.

## Reconciliation with the current repository

The packet was developed after absorbing:

- Passes 2847–2853, which separate support telemetry, protected observation, and active diagnosis;
- Passes 2854–2860, which identify the polarization groupoid, the Boolean/Terwilliger support module, the 96 typed runtime tokens, the exact quantum coarse-graining boundary, the `q`-Hadamard identity, and the support Green function;
- Passes 2861–2868, which establish the directed micro-ISA diameter, the actual frame scrambling time, the no-quadratic two-copy stabilizer bound, the information-flow diode, and the part-specific hardware measurements;
- the Pass 2869 correction that `SRG(40,12,2,4)` parameters alone do not identify `W(3,3)`.

The last correction is essential. Spence's classification contains 28 nonisomorphic strongly regular graphs with parameters `(40,12,2,4)`. The blueprint must therefore identify `W(3,3)` using the projective symplectic construction and generalized-quadrangle incidence axiom, not from the four SRG parameters alone.

## Pass 2901 — the selector channel is an affine-line torsor, not a numbered set

For a noncollinear pair `x,y` in `W(3,3)`, the common-neighbour set has four points. Choosing one common neighbour `c` as the distinguished center leaves three residual centers.

Five canonical transvections generate the projective symplectic action of order `25920`. Adding one anti-symplectic similitude extends this to the projective similitude action of order `51840`.

For a pointed hyperbolic line `(x,y;c)`:

```text
number of pointed hyperbolic lines                     2160
multiplier-one stabilizer order                         12
induced residual-channel action under multiplier one    C3
full projective similitude stabilizer order              24
induced residual-channel action under all similitudes    S3
```

Orbit–stabilizer closes exactly:

```text
51840 / 24 = 2160.
```

Thus the residual fiber is canonically the affine line

```text
C(x,y) \ {c}  ~=  F3,
```

but it has no geometry-supplied origin or orientation. The correct global object is an affine-line bundle whose orientation-preserving transition maps are translations and whose full transition group is `AGL(1,3)=S3`.

**Claim boundary.** The theorem removes the arbitrary lexicographic numbering from the mathematical specification. It does not assert that all already-frozen `2160 x 160` sheet matrices have been transported through a newly chosen gauge; the bundle is the intrinsic replacement for such a choice.

## Pass 2902 — the `q=3` Hadamard quotient becomes a 47-cycle engine

The dense 15-state quotient was compared against a literal four-stage transform on all fifteen basis vectors and thirty-two deterministic signed probes.

Each local butterfly is

```text
(u,v) -> (u+2v, u-v).
```

The architecture uses:

```text
4 stages x 8 butterflies = 32 butterfly cycles
15 border-corrected output cycles
----------------------------------
47 cycles total
```

A serial dense reference requires

```text
15 outputs x 15 multiply-accumulates = 225 cycles.
```

The exact cycle saving is therefore

```text
(225-47)/225 = 178/225 = 79.111...%.
```

The checked-in hardware consists of:

- `rtl/w33_pass2902_q3_hadamard_engine.sv`;
- `rtl/w33_pass2902_q3_dense_reference.sv`;
- `rtl/tb_w33_pass2902_q3_hadamard_engine.sv`.

The testbench compares every emitted value with the dense reference over the same basis/probe corpus used by the exact certificate.

**Claim boundary.** Arithmetic equivalence and the 47-versus-225 cycle model are proved. Logic cells, routed clock frequency, switching activity, and energy remain measurements pending the dedicated open-tool workflow.

## Pass 2903 — exact execution quotients of every micro-ISA subset

For each of the fifteen nonempty operation subsets, start from the sixteen support classes and repeatedly refine by the selected deterministic transitions. The stable class counts are:

| operation subset | refinement profile | stable dimension |
|---|---:|---:|
| `F_p` | `16` | 16 |
| either single `CX` | `16 -> 25` | 25 |
| `Z_p` | `16 -> 24` | 24 |
| `F_p` + either `CX` | `16 -> 25 -> 39 -> 41` | 41 |
| `F_p + Z_p` | `16 -> 24 -> 36` | 36 |
| both `CX` | `16 -> 25` | 25 |
| either `CX + Z_p` | `16 -> 40 -> 45` | 45 |
| `F_p` + both `CX` | `16 -> 25 -> 39 -> 41` | 41 |
| both `CX + Z_p` | `16 -> 40 -> 45` | 45 |
| `F_p + Z_p` + either `CX` | `16 -> 40 -> 78 -> 81` | 81 |
| full four-operation ISA | `16 -> 40 -> 78 -> 81` | 81 |

Two minimal three-operation sets already force the complete frame:

```text
{F_p, CX_p->f, Z_p}
{F_p, CX_f->p, Z_p}.
```

Hence the coarsest exact support-refining congruence for the full micro-ISA is the singleton partition on all 81 affine frames.

**Interpretation.** `16 -> 40 -> 78 -> 81` is an observer hierarchy, not a hierarchy of compressed execution states. Support can be cheap, one-way telemetry precisely because execution must retain phase.

## Pass 2904 — a regular order-96 runtime group exists, but it is twisted

The 96 typed control tokens are

```text
4 faces x 3 matching channels x 8 full-support phases.
```

The natural projective signed-permutation embedding of the tomotope automorphism group has order 96, but preserves full-support phase parity. It therefore has two orbits:

```text
48 tetrahedral-parity tokens + 48 hemioctahedral-parity tokens.
```

A point stabilizer has order two, so the natural action is not regular.

Now impose the determinant-twisted projective condition

```text
(product of coordinate signs) x sign(permutation) = +1.
```

The resulting order-96 subgroup:

```text
orbit size        96
point stabilizer    1
```

and therefore acts freely and transitively. The token set is an exact torsor for this determinant-twisted group.

**Claim boundary.** This is a runtime control symmetry, not the natural parity-preserving incidence action of the tomotope. Odd coordinate permutations exchange the tetrahedral and hemioctahedral halves.

## Pass 2905 — exact first-passage geometry and the optimal 15-mask cycle

The `q=3` support walk has 210 ordered source–target pairs. Under the matching stabilizer `D8`, they form 39 orbits. Their passage times are determined by only three integers:

```text
|T|,
|T intersect tau(T)|,
|T intersect tau(S)|.
```

There are fifteen realized feature triples and thirteen distinct passage values.

An exact directed Held–Karp search, rooted at mask `0001`, gives:

```text
optimal cost                 315
rooted optimal cycles       8336
lexicographic cycle cost  1347/4
exact improvement           87/4
```

One optimum is:

```text
0001 -> 1001 -> 1000 -> 0101 -> 1010
     -> 0100 -> 0110 -> 0010 -> 0111 -> 1110
     -> 1101 -> 1011 -> 1100 -> 1111 -> 0011 -> 0001.
```

The schedule visits every nonzero support exactly once and returns to its start.

**Claim boundary.** The objective is exact mean-first-passage cost in the finite support walk. Turning the number `315` into elapsed time requires a measured implementation of one walk transition.

## Pass 2906 — outside-box I: optimal support diagnosis is provably nonlinear

Every invertible linear recurrence on `F2^4` whose nonzero orbit has length fifteen is generated by a Singer element of `GL(4,2)`.

Exact enumeration gives:

```text
|GL(4,2)|                   20160
Singer elements              2688
number of distinct costs       19
best Singer-cycle cost      1317/4
worst Singer-cycle cost     1383/4
unrestricted optimum          315
```

Therefore

```text
best linear cost - global optimum = 1317/4 - 315 = 57/4.
```

No linear feedback shift-register schedule is optimal for this directed objective. The best diagnostic order is genuinely nonlinear.

This is useful architecturally: the mask controller should store a fifteen-entry ROM or an equivalent nonlinear permutation rather than forcing a mathematically elegant but suboptimal LFSR traversal.

## Pass 2907 — outside-box II: the 40-state observer mirage is falsified

The first observer refinement has forty classes, matching the number of projective Pauli points. That numerical coincidence is extremely tempting—and false.

Exact class sizes are:

```text
7 singleton classes
29 two-state classes
4 four-state classes.
```

A projective quotient of `F3^4` would instead have one zero class plus forty two-state `v ~ -v` classes, hence 41 classes.

More decisively:

- symplectic orthogonality is ambiguous on 216 unordered class pairs;
- the twenty-bit one-step signatures have many Hamming distances;
- 1,459 subsets of those distances have the correct total of 240 graph edges;
- none produces degree 12 with common-neighbour parameters `(lambda,mu)=(2,4)`.

Thus the first 40-class observer quotient is not `W(3,3)` and does not even recover its collinearity graph through a union of signature-Hamming relations.

**Claim boundary.** This kills one count-based identification. It does not touch the independent projective symplectic construction of `W(3,3)`.

## Blueprint improvements, not just additions

The release integrator rewrites the canonical machine blueprint in place. Its critical changes are:

1. replace the stale promise “every number is measured or proved; nothing is estimated” with the evidence ladder `proved / measured / published / derived / modelled / open`;
2. correct “a support readout erases 8/3 of a bit” to “support-only observation discards 8/3 bits of conditional phase information”;
3. separate UP5K and HX8K measurements instead of mixing the 72.40 MHz and 208.86 MHz figures;
4. label the reported `0.92` photonic-gate fidelity as published prior art, not an internal measurement;
5. remove the false claim that SRG parameters uniquely identify `W(3,3)` and state the 28-graph classification boundary;
6. replace the false “no triangles / unique shortest path” gloss with the actual generalized-quadrangle incidence axiom; the collinearity graph contains line `K4`s and hence triangles;
7. separate four distinct machine representations: seven-bit execution state, four-bit support telemetry, protected observer words, and 96-state typed control;
8. insert the exact observer-congruence theorem so the blueprint no longer suggests that support is a compressed execution state;
9. insert the butterfly engine and nonlinear diagnostic ROM as actual architectural alternatives with pending-versus-proved labels;
10. add the observer-40 falsifier to the errata/evidence story so a matching count can no longer be promoted as an identification.

The workflow applies the rewrite idempotently, compiles `holonet_machine_blueprint.tex`, `w33_paper.tex`, and `photonic_holonet.tex`, rejects overfull boxes and undefined controls, and commits the regenerated blueprint/PDF on the research branch before merge.

## Reproduction

```bash
python analysis/bt2901_2907_seven_frontiers.py --verify-frozen
pytest -q tests/test_bt2901_2907_seven_frontiers.py
```

The exact gate is `64/64`; focused regressions are `7/7`. RTL simulation, synthesis, placement, timing, and document compilation are delegated to `.github/workflows/w33_pass2901_2907_seven_frontiers.yml`.

## External anchor used by the blueprint correction

- E. Spence, *The Strongly Regular (40,12,2,4) Graphs*, Electronic Journal of Combinatorics 7 (2000), Research Paper R22. This is the primary classification source for the count of 28 nonisomorphic graphs; it is exactly why SRG parameters alone cannot identify the symplectic generalized quadrangle.
