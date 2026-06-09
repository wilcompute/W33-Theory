# BT593 - Leakage and Homology Reviewer Response Note

This note answers two likely reviewer questions.

## 1. Is the cubic leakage just numerical noise?

No. The raw cubic transform of the protected W33 Levi cycle-frame Gram is structured inside the Levi flag Bose-Mesner algebra.

The protected Gram is

```text
G = (1/81) C C^T = (160/81) E4.
```

The raw cubic Gegenbauer transform fills all five primitive sectors. After removing the uniform component, it still occupies the companion stack and the protected sector:

```text
centered raw cubic: E1 + E2 + E3 + E4.
```

The conjugate companion sectors are locked to the middle sector by exact rational ratios:

```text
unweighted ratio = 244/121
multiplicity-weighted ratio = 976/605
trace = 13651200
```

So the leakage is not noise. It is a structured nonlinear response of the protected idempotent under entrywise cubic dynamics.

## 2. Does the phase-cover fiber replace Levi homology?

No. The W33 Levi graph homology and the scalar phase-cover fiber homology are distinct.

The point-line Levi graph has 80 vertices and 160 flag edges, so its cycle rank is 81. That is the protected W33 Levi homology.

The scalar phase cover starts from the 12960 Levi support incidences. Each support incidence has four nonzero scalar lifts, which form a square fiber in the minimal model. One square has beta-one equal to 1, so over all 12960 base incidences the fiber beta-one is 12960.

Thus:

```text
Levi H1 = 81
fiber beta-one = 12960
```

These are not equal and should not be identified.

The correct relationship is layering:

```text
Levi H1 -> Levi support incidences -> phase-cover lifts
81      -> 12960                  -> 51840
```

## 3. Why is the repaired cubic map legitimate?

The repair is explicitly a spectral selection rule. The raw cubic transform leaks into the companion stack. The repaired map projects to the E0 plus E4 sector, removes the E0 component, and then renormalizes the E4 diagonal amplitude.

After this sequence, the protected Gram returns exactly to itself. The first derivative, second-order shape Hessian, and all positive-order shape derivatives vanish on the nonzero E4-amplitude stratum.

The boundary is also clear: this is not claiming that the raw entrywise cubic is closed on E4. It is claiming that the repaired-center-normalize evolution selects the protected Hodge idempotent as a rigid fixed shape.

## Short reviewer answer

The cubic leakage result is a structured obstruction, not a failure. It shows why raw nonlinear evolution must be repaired. The phase-cover homology calculation is a separate fiber count and is intentionally not identified with the Levi H1 sector. The protected physical object remains the Levi Hodge projector, while the scalar cover supplies the nonzero phase-double layer.
