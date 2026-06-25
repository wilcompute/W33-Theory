# BT1788 Hesse relation materializer and counts-only falsifier

## Commit-audit synthesis

The last two days moved the architecture through three increasingly exact layers:

1. **Holonet physics layer.** The June 23 run pushed the reading that computation is gauge curvature, the matter graph supplies a discrete Yang-Mills field strength, the SRG expander gap is the mass gap, and the network boundary is a holographic code with `c=f=24`.
2. **Hesse/Fano/torus solver layer.** The June 24-25 BT1710-BT1787 run pushed the concrete finite object: Hesse square functors, Heawood/K7,7 torus schedulers, q2025 bus charts, 16-cell/Cl4/Q4 atlas fusion, self-frame punctures, 600-cell BC-ring embeddings, D5 rephased hexagon buses, and finally the relational-solver frontier.
3. **q=3 cyclotomic skeleton layer.** The newest synthesis makes `{Phi_3,Phi_4,Phi_6}(3)={13,10,7}` the substrate constant generator with sum `30=h(E8)`, opens the neutrino `13/9` as `|PG(2,3)|/|AG(2,3)|`, and corrects the D4-GKP gain to an error-rate-dependent finite-decoder curve.

BT1788 attacks the exact bottleneck left by BT1784/BT1787: the solver has table counts but not table contents.

## Exact schema reconstructed

The nine variables are:

```text
R0,R1,R2, C0,C1,C2, D0,D1,D2
```

The 18 ternary constraints are the **nonconcurrent Hesse row-column-diagonal triples**:

```text
(R_i, C_j, D_s) is a table exactly when s != (j-i) mod 3.
```

This gives `27-9=18` constraints: all row-column-diagonal triples except the 9 concurrent affine-Hesse point incidences.

NetworkX verifies the primal graph is exactly the complete tripartite graph `K_{3,3,3}`:

```text
nodes = 9
edges = 27
degree sequence = 6^9
approx treewidth = 6
incidence graph nodes = 27
incidence graph edges = 54
pair-frontier projections = 27
```

That is the important structural punchline: the missing solver object is not just 18 lists. It is a **27-pair-frontier sheaf** over a `K_{3,3,3}` Hesse skeleton.

## Counts-only falsifier

BT1781 records:

```text
raw entries = 31104
accepted entries = 9980
entry counts = [528,562,578,528,612,580,528,528,480,528,612,564,562,528,578,562,562,560]
every slot still has 12 choices
incumbent remains present in every local table
```

BT1788 materializes deterministic synthetic tuple tables with exactly these counts, full unary support in every table, and the all-zero incumbent. The synthetic tables are explicitly not the real BT1781 data. They are a falsifier for the idea that counts alone can certify the solve.

Across eight deterministic same-count materializations:

```text
all runs keep the incumbent = true
pair-consistent tuple total range = 9608..9722
DFS solution count range = 5..11
solution-count histogram = {5:2, 7:1, 8:3, 10:1, 11:1}
```

Therefore the BT1781 counts plus unary saturation do **not** determine the global solve. Different saturated tuple contents with identical counts produce different pair-consistent remnants and different incumbent-first DFS solution counts.

## Practical next artifact

The next real solver should commit either:

1. the 18 accepted ternary tuple lists, or
2. the 27 canonical pair-frontier projections plus enough provenance to reconstruct/prune the ternary lists.

The second form is probably the better architectural object: it treats the solve as a Hesse sheaf gluing problem, not a blind CSP. Each pair projection is a boundary chart; the 18 ternary tables are local patches; pair consistency is the sheaf-overlap check; DFS is section enumeration; quotienting by BT1758 plateau symmetries is then gauge reduction of global sections.

## Outside-the-box reading

The strongest new connection is:

```text
18 nonconcurrent local patches + 27 pair-boundary charts + K_{3,3,3} primal graph
```

This looks like the solver-level version of the architecture's current triad:

```text
Hesse affine square  ->  q=3 cyclotomic skeleton  ->  E6/Hessian 27-frontier
```

The number `27` is not just a count here. It is the complete set of row-column, row-diagonal, and column-diagonal pair charts. In other words, the missing table materialization should be treated as a **27-boundary object** whose global sections are the stabilizer solutions. That gives a clean bridge from the BT1787 solver frontier to the E6/Hessian generation layer from the June 24 synthesis.

## Files

- `analysis/bt1788_hesse_relation_materializer.py`
- `data/bt1788_hesse_relation_materializer.json`
- `analysis/BT1788_hesse_relation_materializer.md`
