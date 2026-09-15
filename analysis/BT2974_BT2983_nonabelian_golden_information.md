# Passes 2974–2983 — Nonabelian routing, golden control, and an honest general-isotropic M36 frontier

## Executive result

This packet executes the five requested continuations, adds two deliberately outside-box fronts, and audits the recent `R4/U6` golden-ratio work against the live repository.

1. **Nonabelian route memory:** a ten-mode `D4` connection on `K10` is completely classified, after spanning-tree gauge fixing, by 36 chord holonomies in `D4`, modulo one simultaneous conjugation. The exact orbit count is `81,129,638,418,148,456,557,941,239,054,336`. The existing 36-bit sign-curvature decoder is the abelian shadow of this much larger quotient.
2. **Constructive `S6` curvature:** the ten spread modes are identified with the ten unordered `3+3` partitions of a six-set. Choosing one distinguished symbol identifies them with the two-subsets of a five-set, where Petersen adjacency by disjointness produces the exact 60-triple `2-(10,3,4)` two-graph. The 720 explicit `S6` permutations preserve the triple set, and an explicit vertex map identifies it with the W33 spread-router curvature.
3. **Adaptive chirality receiver:** for a known conjugate pair with squared overlap `1/3`, Bayesian adaptive individual measurements attain the collective finite-copy optimum `(1+sqrt(1-3^-n))/2`. Synthetic readout-flip and erasure channels quantify degradation without being mislabeled as laboratory data.
4. **General-isotropic M36:** the complete search space contains `213,648,435` rank-four isotropic subspaces of `F2^12`. It is partitioned exactly into 495 duplicate-free RREF pivot shards. A deterministic pilot over `649,940` distinct general subspaces found six non-CSS quadratic-collinearity projectors; all six accept only stabilizer clean states, with success `1/27`. The full 495-shard sweep remains pending and is not claimed complete.
5. **Priority evidence lane:** a path-isolated workflow runs only this packet's exact verifiers, small-shard M36 regression, manuscript/front-door integrator, and focused tests. It removes repository-wide trigger fan-out and dependency coupling, but cannot bypass GitHub's global runner queue.
6. **Outside-box golden scheduler:** the canonical golden word `R4^2 U6` is selected not by having the smallest spectral radius, but by being the shortest expanding word preserving a rational line and inducing the Fibonacci map on the quotient. Its mechanical word of slope `1/phi^2` is balanced with subword complexity `n+1`, giving a deterministic no-burst scheduler.
7. **Outside-box hybrid obstruction:** modulo two, the Fibonacci quotient has order three and acts transitively on the three nonzero `V4` parity labels, producing `V4 semidirect C3 ≅ A4`. This action cannot lift faithfully to the full `D4` core because `Aut(D4)` has order eight and no element of order three. Golden control belongs on the abelian syndrome shell, not inside the protected nonabelian holonomy.

## Pass 2974 — full nonabelian route quotient

Let `g_ij in D4` be the directed transport on the 45 edges of `K10`, with inverse transport on the reverse edge. A vertex gauge `h_i in D4` acts as

```text
g_ij -> h_j g_ij h_i^{-1}.
```

Fixing a rooted spanning tree sets its nine edge transports to the identity. The remaining 36 chord transports are the fundamental cycle holonomies. The only residual gauge freedom is simultaneous conjugation by the root gauge. Consequently the complete gauge invariant is

```text
D4^36 / diagonal conjugation.
```

Burnside's lemma, using the `D4` centralizer sizes `8,8,4,4,4,4,4,4`, gives the exact orbit count

```text
(2*8^36 + 6*4^36)/8
= 81,129,638,418,148,456,557,941,239,054,336.
```

This is a complete discrete connection classifier, not a continuum gauge-field or optical-phase measurement.

## Pass 2975 — analytic `S6` two-graph derivation

The ten unordered `3+3` partitions of `{0,1,2,3,4,5}` carry the exceptional degree-ten `S6` action. Selecting the block containing `0` maps each partition to a two-subset of `{1,2,3,4,5}`. Declare two vertices adjacent when those two-subsets are disjoint; this is the Petersen graph.

A triple is selected when it spans an odd number of Petersen edges. Direct counting gives:

```text
selected triples       60
point replication      18
pair replication        4
four-set parity         even
```

Thus the selected triples form a `2-(10,3,4)` two-graph. All 720 permutations of the six symbols preserve it. The exact W33 spread-router transport gives an isomorphic triple system under the frozen map

```text
0→0, 1→8, 2→9, 3→7, 4→4, 5→6, 6→2, 7→5, 8→1, 9→3.
```

The abstract Petersen switching class and two-graph language are standard; the repository-specific theorem is their exact emergence from every W33 spread-router parity connection.

## Pass 2976 — adaptive finite-copy chirality receiver

For each known conjugate M36 pair,

```text
|<psi+|psi->|^2 = 1/3.
```

The project-local Pauli receiver remains useful but is not Helstrom-optimal:

```text
P_local(1)    = (1 + 1/sqrt(3))/2 = 0.788675...
P_Helstrom(1) = (1 + sqrt(2/3))/2 = 0.908248...
```

For `n` copies, exact Bayesian updating of the prior after each optimized binary von Neumann measurement reproduces

```text
P_opt(n) = (1 + sqrt(1 - 3^-n))/2.
```

This finite-copy adaptive attainability is published prior art: Acín, Bagan, Baig, Masanes, and Muñoz-Tapia, *Physical Review A* **71**, 032338 (2005), DOI `10.1103/PhysRevA.71.032338`.

The included synthetic detector profiles introduce readout flips and erasures after the ideal measurement. They are engineering models, not experimental calibration.

## Pass 2977 — general-isotropic three-copy M36 search

The number of rank-four totally isotropic subspaces of a twelve-dimensional binary symplectic space is

```text
product_{i=0}^{3} (2^{2(6-i)} - 1)/(2^{4-i} - 1)
= 213,648,435.
```

The generator enumerates each subspace exactly once in reduced-row-echelon form. The 495 pivot sets are independent exhaustive shards. Exact smaller-space self-tests reproduce `15`, `315`, `135`, and `5355` isotropic subspaces for `(n,k)=(2,2),(3,2),(3,3),(4,2)`.

The deterministic pilot examined `649,940` distinct rank-four isotropic subspaces. Six projectors passed the correct first-order collinearity condition, and all six were non-CSS. Each had clean success `1/27`, but every accepted clean state was a six-qubit stabilizer state. These witnesses prove that leaving CSS enlarges the projector family, while simultaneously showing that the first exact non-CSS hits do not distill the deep M36 resource.

The exhaustive `213,648,435`-subspace sweep is **not complete**. Run one shard with

```bash
python analysis/bt2977_general_isotropic_m36_search.py --pivot-index 494
```

and distribute all indices `0..494` for the full duplicate-free census.

## Pass 2978 — priority evidence lane

The dedicated workflow is intentionally narrow:

- `workflow_dispatch` and same-packet pull-request paths only;
- one concurrency group for this pass range;
- exact 2974–2981 verifier;
- fast M36 pilot plus an optional exact pivot shard;
- focused tests and manuscript/front-door integration;
- no invocation of unrelated legacy workflows.

This removes trigger fan-out and dependency coupling inside the repository. It cannot guarantee immediate runner allocation because GitHub's global queue remains external.

## Pass 2979 — what actually selects the golden word

With

```text
R4 = [[0,-1,0],[1,0,0],[0,0,1]],
U6 = [[1,0,0],[0,0,1],[0,-1,1]],
```

the symmetric word ball through length ten was rebuilt exactly. The shortest expanding elements with reducible characteristic polynomial occur at length three. Up to inverse, cyclic, and conjugate word symmetries, the canonical representative is

```text
R4^2 U6.
```

It fixes the primitive rational line `<(1,0,0)>` with eigenvalue `-1` and induces

```text
[[0,-1],[-1,1]]
```

on the quotient, with characteristic polynomial `t^2-t-1`. Therefore the golden ratio is selected by **shortest rational-line reduction and Fibonacci quotient action**, not by minimum spectral radius among all controller words.

## Pass 2980 — golden Sturmian schedule

The lower mechanical word

```text
a_n = floor((n+1)/phi^2) - floor(n/phi^2)
```

was tested through 10,000 slots. Its prefix discrepancy stays below one, it has no consecutive `1` slots, and its factor complexity is exactly `p(n)=n+1` for `n=1..12`. It is therefore a deterministic balanced scheduler for expensive calibration, pilot, or refresh events with no short burst.

The Sturmian balance and complexity statements are classical. The new proposal is to place this scheduler on the Holonet controller's expensive-event lane.

## Pass 2981 — the `A4` syndrome shell and the `D4` lift obstruction

Reducing the Fibonacci quotient modulo two gives an order-three matrix cycling the three nonzero vectors of `F2^2`. Therefore

```text
V4 semidirect C3 ≅ A4,
```

with element-order histogram `1:1, 2:3, 3:8`.

But

```text
|Aut(D4)| = 8,
orders in Aut(D4) = 1,2,4 only.
```

No faithful order-three action exists on the full `D4` holonomy. The architecture must therefore be layered:

```text
golden/Fibonacci controller -> A4 abelian syndrome shell
protected route memory       -> D4 nonabelian core.
```

This is both a constructive fusion and an exact obstruction against over-unifying the two layers.

## Reproduction

```bash
python analysis/bt2974_2981_nonabelian_golden_information_closure.py
python analysis/bt2977_general_isotropic_m36_search.py --quick 50000
pytest -q tests/test_bt2974_bt2983_nonabelian_golden_information.py
python tools/integrate_bt2974_bt2983.py
```
