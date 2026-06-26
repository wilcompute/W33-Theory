# BT1807 post-BT1787 audit synthesis

Scope: read the commits added after BT1787, compare `ca389824...` to `master`, and fold the internet anchors back into the active W33/Holonet thread.

## What changed

The compare from BT1787 to `master` is large:

```text
62 commits ahead
new analysis/data/scripts spanning BT1788--BT1806
photonic_holonet.tex changed by 429 additions / 6 deletions
photonic_holonet.pdf rebuilt
```

The new work splits into two major layers.

## Layer A: arithmetic / seven-face closure

The `w33_*` stack builds a single-q=3 closure ledger:

```text
Phi_3 = 13
Phi_4 = 10
Phi_6 = 7
k = 12
v = 40
c=f = 24
Hessian = 27
h(E7) = 18
h(E8) = 30
E8 roots = 240
Leech = 196560
Monster = 196883
integer alpha anchor = 137
```

The strongest honest formulation is: the integer skeleton is closed; running couplings, absolute mass scales, and exact VEVs remain dynamics, not arithmetic.

## Layer B: fibre geometry / H27-Schlaefli obstruction

BT1788--BT1806 push the tuple-materialization question into H27/E6/Schlaefli geometry.

Key facts read from the commit summaries:

```text
BT1788: counts-only materialization is a falsifier/scaffold, not the true table data.
BT1795: one exact transport from 27 Hesse pair-frontier points to the H27/Payne shell.
BT1798: literal uniqueness is false; 1000 sampled transports give 504 distinct support images.
BT1801: double-six matrix has rank_F2=16, rank_F3=13.
BT1802: 9980 forces a nonuniform 12-symbol fibre rule.
BT1804: binary kernel is the Hesse delta split; ternary kernel remains unresolved.
BT1805: the F3 syndrome is repaired by changing only T010, T210, T222 by (-2,-2,+2).
BT1806: Schlaefli/E6 orbit handoff exported in DIMACS, GAP, and Sage.
```

## Internet anchors checked

External anchors agree with the repo's direction:

```text
600-cell / BC helix: 20 rings of 30 tetrahedra; each ring is bounded by three Clifford-parallel great decagons.
Schlaefli graph: 27 vertices, 216 edges, SRG(27,16,10,8), automorphism group order 51840.
Double-six: 36 double-six configurations among the 27 cubic-surface lines.
```

These are exactly the right outside objects for the repo's current triple:

```text
30 = BC ring / h(E8) / Coxeter-bus period
27 = Schlaefli-H27 / Hessian q^3
36 = double-six count / magic-ray shell
```

## New synthesis

The arithmetic closure should not be used to paper over the fibre obstruction. The cleaner statement is:

```text
The integer skeleton closes at q=3.
The fibre geometry does not yet close: it leaves a tiny, localized ternary defect.
That defect is not a failure; it is the next law to derive.
```

The three-table repair `T010, T210, T222` is now the most valuable target in the whole active thread. It is small enough to be a real law, and structured enough to connect Hesse transport, Schlaefli double-sixes, and the BC/D5 bus gauge.
