# BT1810 Hesse hinge orbit

Source-side test for the defect path before running the full Schlaefli/W(E6) Sage handoff.

Objects:

```text
18 nonconcurrent Hesse tables
C(18,3) = 816 three-table supports
observed defect = {T010,T210,T222}
```

Hinge criterion:

```text
two tables share the same local (j,s) fibre coordinate
the second and third share the same strand i coordinate
pairwise Hamming profile is [1,2,3]
```

Result:

```text
54 of 816 triples satisfy the hinge criterion
{T010,T210,T222} is one of them
the Hesse source symmetry orbit of the observed defect equals the 54-element hinge class
```

Conclusion: the three-table defect is not arbitrary on the Hesse side. It is exactly the canonical source hinge type. The remaining decisive test is the BT1810 Sage script: whether this Hesse hinge remains tiny/distinguished under the Schlaefli/W(E6) stabilizer of the transported BT1795 image.
