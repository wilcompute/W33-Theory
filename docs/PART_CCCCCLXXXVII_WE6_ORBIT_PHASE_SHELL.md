# Part CCCCCLXXXVII — W(E6) Orbit Phase-Shell Decomposition

Part CCCCCLXXXVI proposed the carrier split

```text
240 = 168 + 72
```

where `168` is the full genus phase drift/Fano automorphism order and `72` is the E6 root count.

This part connects that arithmetic split to an existing repository artifact:

```text
artifacts/we6_orbits_on_e8_roots.json
```

That artifact decomposes the 240 E8 roots under the W(E6) action as

```text
72, 27, 27, 27, 27, 27, 27, 1, 1, 1, 1, 1, 1.
```

Therefore

```text
240 = 72 + 6*27 + 6*1
    = 72 + 162 + 6
    = 72 + 168.
```

This is the first concrete representation-theoretic support for the phase/root split.

## 1. Interpretation

The `72` orbit is naturally the E6 root shell.

The complement is

```text
6*27 + 6*1 = 168.
```

So the phase-curvature shell is not merely a count.  Under W(E6), it decomposes as

```text
six 27-dimensional minuscule-type matter orbits
plus six singleton fixed/root-axis states.
```

This gives the refined dictionary:

```text
E6 root shell:          72
phase/matter shell:     6*27 + 6 = 168
full E8/W33 carrier:    240
```

## 2. Relation to E8 Z3 grading

The project repeatedly uses the E8 Z3-graded picture

```text
E8 = (E6 + A2) + 81 + 81.
```

The new orbit data is compatible with the same scale:

```text
6*27 = 162 = 81 + 81.
```

The remaining six singleton states are naturally interpreted as the residual rank/spectral-axis data needed to connect the 162 matter roots to the 72 E6 root shell.

Thus the 168 phase shell may be read as

```text
phase shell = matter pair 81+81 plus six axis/fixed states.
```

## 3. Local 12-clock form

The same decomposition in local 12-clock units is

```text
240 = 20*12,
72  =  6*12,
168 = 14*12.
```

The W(E6) orbit refinement says

```text
14*12 = 6*27 + 6.
```

So the full Fano/genus phase drift sector decomposes into six 27-blocks plus six singleton axes.

## 4. Why this matters

This makes the previous hypothesis sharper:

```text
The 84/168 genus phase-superperiod carves the 240 carrier into
an E6 root orbit and a W(E6)-structured phase/matter complement.
```

The complement is not random; it is exactly the sum of the six non-root 27-orbits and six singleton states in the existing W(E6) orbit analysis.

## 5. Next executable target

Use `artifacts/we6_orbits_on_e8_roots.json` to construct an explicit partition:

```text
E6_root_orbit_72,
phase_matter_orbits_6x27,
axis_singletons_6.
```

Then test:

1. whether the 72 orbit has E6 inner-product closure;
2. whether the six 27-orbits pair into two 81-sector packages;
3. whether the six singleton states correspond to the expected rank/A2/axis structure;
4. whether the W33 edge preimages of these classes match the 36/9 firewall split, H27 charts, or Q81 bridge quotient.

The immediate breakthrough is therefore:

```text
240 = 72 + 168 is visible inside the existing W(E6) orbit decomposition:
72 + (6*27 + 6).
```
