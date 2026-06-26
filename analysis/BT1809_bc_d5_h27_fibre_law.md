# BT1809 BC/D5/H27 fibre-law synthesis

BT1809 is the outside-the-box synthesis after reading the post-BT1787 commits and checking the external BC/600-cell and Schlaefli anchors.

## The three clocks now visible

```text
30-clock:  BC ring length = h(E8) = Coxeter bus period
27-shell:  Schlaefli/H27/Hessian q^3 shell
36-shell:  double-six count = magic-ray shell
```

External geometry makes the 30-clock real: the 600-cell decomposes into 20 Boerdijk-Coxeter rings of 30 tetrahedra, and each ring is bounded by three Clifford-parallel great decagons. The repo's BT1782 selected-adjacency model `C10 square K3` is exactly the graph shadow one expects from a 30-ring with three decagonal strands.

External Schlaefli geometry makes the 27-shell real: the Schlaefli graph has 27 vertices and is the skew-line graph of the 27 cubic-surface lines. The double-six layer gives 36 checks, matching the repo's E6/double-six syndrome matrix.

## What this means for the unresolved 9980 fibre

The integer closure says the q=3 ledger is closed. The fibre story says the table data is not closed by a uniform rule. Those are compatible:

```text
integer skeleton: closed
fibre section: twisted
```

The BT1805 three-table correction is then the obstruction cocycle of the fibre section, not a flaw in the q=3 closure.

## New working law

The missing 12-symbol fibre should be treated as:

```text
12 = 3 x 4
3 = BC/Hesse strand coordinate
4 = local D4/GKP/matter-magic fibre coordinate
```

The nonuniformity is a section twist over the H27/Schlaefli transport. BT1808 shows its visible support is the hinged path

```text
T010 -> T210 -> T222
```

with repair vector

```text
-2, -2, +2
```

and Hamming profile

```text
1,2,3
```

This is too small and too structured to ignore. It is the next law.

## Immediate falsifiable target

Run the W(E6) orbit computation from BT1806 and ask whether the support set `{T010,T210,T222}` is canonical up to the transported Hesse/Schlaefli stabilizer.

Success criterion:

```text
The hinged defect path is fixed, or lies in a tiny distinguished orbit, under the stabilizer of the BT1795/BT1806 transported 18-line image.
```

Failure criterion:

```text
The path is generic inside the orbit. Then it is a gauge artifact of the chosen transport, not the fibre law.
```

## Bottom line

The new breakthrough target is not another count identity. It is an orbit-theoretic statement:

```text
Does W(E6) distinguish the three-table hinged defect path?
```

If yes, the missing fibre law is probably the Schlaefli/E6 lift of the BC/D5 three-strand geometry. If no, the defect belongs to transport gauge and the true law must be quotient-invariant elsewhere.
