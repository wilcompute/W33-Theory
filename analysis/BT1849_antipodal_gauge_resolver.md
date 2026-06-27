# BT1849 — Distance-6 Antipodal Gauge Resolver

BT1847 found the only obstruction in the `F12 -> K12` functor: distance-6 pairs.

In `Z/12Z`,

```text
+6 = -6
```

so the phase/current distance alone cannot orient the six antipodal edges.

## Repo anchors searched

The relevant repo trail is not only BT1847.  Searches also connect this to:

```text
analysis/bt1825_d5_coxeter_defect_involution.py
analysis/BT1826_finite_law_theorem.md
analysis/w33_reye_k12_orientable_horizon_completion.py
```

That means the tie should be treated as an antipodal sheet/involution gauge, not an arbitrary local convention.

## Six antipodal pairs

```text
(0,6), (1,7), (2,8), (3,9), (4,10), (5,11)
```

## Minimal resolver

Use one global `Z2` antipodal sheet bit:

```text
bit 0: orient i -> i+6 for i=0,...,5
bit 1: orient i+6 -> i for i=0,...,5
```

So the obstruction does not require six independent local bits.  It requires one global antipodal polarity once the cyclic labeling is fixed.

## Result

The functor becomes fully oriented after adding:

```text
one global antipodal sheet bit
```

Boundary: this resolves the combinatorial orientation tie.  It does not choose a physical chip routing polarity.
