# Part DCCLXXII - Formula-Regime Registry Bridge

**Bridge:** `verify_dcclxxii_formula_regime_registry_bridge.py` - Verified
**Tests:** `tests/test_dcclxxii_formula_regime_registry_bridge.py`
**Data:** `data/dcclxxii_formula_regime_registry_bridge.json`

---

## 1. Why this part exists

The May 16 audit found formula-level drift in public theory artifacts. The
right response is not to choose a favorite expression in prose. The right
response is a small executable registry that forces formulas to carry lineage,
status, and regime labels.

---

## 2. Alpha variants

Two fine-structure expressions are currently visible:

```text
docs/script lineage:  137 + 40/1111
paper/report lineage: 137 + 880/24445
```

They are not equal. The exact difference is:

```text
| (137 + 40/1111) - (137 + 880/24445) | = 24/5431679.
```

That is small numerically but too large conceptually for an unlabeled
zero-parameter theorem claim. DCCLXXII therefore marks both as:

```text
unresolved_variant
```

until a later theorem promotes one expression or separates the two by a
physical regime.

---

## 3. Electroweak regimes

Two Weinberg-angle expressions are allowed only with explicit shell labels:

```text
bare/internal shell:       2q/(q+1)^2 = 3/8
dressed/projective shell:  q/(q^2+q+1) = 3/13
```

The live promoted electroweak bridge value is:

```text
3/13
```

The older `3/8` value remains valid as the bare/internal unification-shell
diagnostic. The two must not be presented as the same observable without
regime language.

---

## 4. Policy

Future theorem scripts should import or mirror this registry before presenting
public numerical formulas. If a formula appears in `docs/index.html`, TeX, or a
script without a regime label, the fix is to add the label or promote one
canonical source of truth.

---

## 5. Honest boundary

This is a reproducibility and claim-hygiene theorem. It does not derive the
fine-structure constant, decide the unresolved alpha variants, or perform
renormalization-group matching.
