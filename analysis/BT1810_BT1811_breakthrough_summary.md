# BT1810-BT1811 breakthrough summary

Executed the two requested targets and skipped paper patching.

## BT1810: W(E6) / Hesse hinge orbit

Added:

```text
analysis/bt1810_we6_hinged_path_orbit_test.sage
analysis/BT1810_hesse_hinge_orbit.md
```

The Sage file extends the BT1806 export. It builds the Schlaefli graph, computes its automorphism group, induces the action on the 45 tritangent supports, takes the stabilizer of the BT1795 transported 18-support image, and computes the orbit of the defect support:

```text
T010 -> support 10
T210 -> support 22
T222 -> support 44
```

The Hesse-side orbit calculation already gives a strong result:

```text
18 nonconcurrent Hesse tables
C(18,3) = 816 three-table supports
54 of 816 satisfy the strand/local hinge criterion
{T010,T210,T222} is one of them
its Hesse source-symmetry orbit is exactly the 54-element hinge class
```

So the defect is not arbitrary at the Hesse end. It is the canonical Hesse hinge type. The full W(E6) Sage test will decide whether this hinge remains tiny/distinguished after Schlaefli transport or becomes transport gauge.

## BT1811: 12=3x4 fibre hinge rule

Added:

```text
analysis/bt1811_fibre_3x4_hinge_rule.py
data/bt1811_fibre_3x4_hinge_rule.json
```

The explicit working law is:

```text
12 = 3 x 4
3 = Hesse/BC strand coordinate i
4 = local D4/GKP quartet above the local (j,s) fibre
```

At table level the quartet is only visible as oriented pairs, hence correction size 2. The rule is:

```text
remove one oriented pair from two tables sharing the same local (j,s) fibre
return one oriented pair at the strand-continuation corner
```

For the observed path:

```text
A = T010
B = T210
C = T222
```

we have:

```text
A and B share local fibre (j,s)=(1,0)
B and C share strand i=2
Hamming profile = [1,2,3]
repair vector = [-2,-2,+2]
```

This derives the support and sign pattern of the BT1805 repair from the 3x4 hinge ansatz. The remaining unknown is internal: which four D4/GKP quartet states realize the oriented-pair transfer.

## New frontier

The breakthrough target is now sharper:

```text
Does the W(E6) stabilizer of the transported BT1795 image distinguish the 54 Hesse hinges, and in particular the defect hinge {T010,T210,T222}?
```

If yes, the fibre law is real Schlaefli/E6 geometry. If no, the hinge is source-gauge structure and the law must live deeper in the 4-state D4/GKP quartet.
