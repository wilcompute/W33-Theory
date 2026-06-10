# BT751 — Root-Natural Selector Harness

BT748 gave complete global coordinates for presentation pairs:

```text
(root triple, chirality, centralizer element) = 540 x 2 x 48 = 51840.
```

BT749 then gave the local dihedral factorization over one rectangle:

```text
24 lifts -> 12 reflections of D12, 2-to-1,
chirality = the two reflection classes.
```

BT750 resolves the remaining local duo ambiguity:

```text
duo partners = {k, r^6 k},
```

where `r^6` is the unique central half-turn of the inner `Z12` stabilizer.  But BT750 also proves the crucial correction:

```text
duo partners do not present the same Levi octagon.
```

So the duo bit is not pure gauge.  It is a real apartment choice.

## Selector consequence

A constant-dihedral-phase selector is insufficient.  It still leaves two candidate apartments per rectangle.  A root-natural selector must choose all of:

```text
chirality eps,
dihedral phase phi in {0,...,5},
duo bit delta in {0,1}.
```

Thus the local selector factorization is now:

```text
24 = 2 chirality x 6 phase x 2 duo.
```

## Harness tests

The executable scaffold is:

```text
analysis/bt751_root_natural_selector_harness.py
```

The compact machine-readable contract is:

```text
data/bt751_root_natural_selector_harness.json
```

A completed root-natural selector must pass:

1. **One lift per rectangle**: exactly `2160` selected rows.
2. **Rank**: signed selector matrix rank `81` over `GF(1000003)`.
3. **Root uniformity**: every one of the `540` root-triple fibers hit exactly `4` times.
4. **Gluing flatness**: BT741-style gluing quotient is connected and leaves `F2^4`.
5. **Chirality stability**: all selected lifts stay in one absolute chirality torsor.
6. **Apartment noncollapse**: central half-turn partners remain distinct octagons.

## Boundary

BT751 is a harness/specification, not the final heavy enumerator.  It records the corrected target after BT750: the canonical selector, if it exists, must be constant in both phase and duo coordinates after a global base choice.
