# BT1807-BT1809 breakthrough summary

Executed the requested full-audit / internet / outside-the-box pass after BT1787.

## BT1807: post-BT1787 audit synthesis

Added `analysis/BT1807_post1787_audit_synthesis.md`.

The repo advanced by 62 commits after BT1787. The new work splits into two layers:

```text
A. arithmetic / seven-face closure
B. fibre geometry / H27-Schlaefli obstruction
```

The arithmetic layer closes the q=3 integer ledger. The fibre layer remains unresolved but has become highly localized: the 9980 tuple count requires a nonuniform 12-symbol fibre rule, and the F3 double-six syndrome is repaired by a tiny three-table even correction.

## BT1808: three-table defect geometry

Added `analysis/bt1808_three_table_defect_geometry.py` and `data/bt1808_three_table_defect_geometry.json`.

BT1805 isolated the F3 defect to:

```text
T010: -2
T210: -2
T222: +2
```

BT1808 analyzes this support inside the Hesse table cube. It has:

```text
support size = 3
L1 repair size = 6
net delta = -2
pairwise Hamming profile = [1,2,3]
```

So the defect is not a random anomaly, line, or plane. It is a hinged three-point path in the Hesse 3x3x3 table cube.

## BT1809: BC/D5/H27 fibre-law synthesis

Added `analysis/BT1809_bc_d5_h27_fibre_law.md`.

The synthesis connects three active clocks:

```text
30-clock = BC ring length = h(E8) = Coxeter bus period
27-shell = Schlaefli/H27/Hessian q^3 shell
36-shell = double-six count = magic-ray shell
```

The new working law is:

```text
12 = 3 x 4
3 = BC/Hesse strand coordinate
4 = local D4/GKP/matter-magic fibre coordinate
```

The missing nonuniformity should be treated as a fibre-section twist over the H27/Schlaefli transport. The immediate falsifiable target is orbit-theoretic:

```text
Does W(E6) distinguish the hinged defect path {T010,T210,T222}?
```

If yes, the missing fibre law is probably the Schlaefli/E6 lift of the BC/D5 three-strand geometry. If no, the defect is transport gauge and the true law must live in a quotient-invariant elsewhere.
