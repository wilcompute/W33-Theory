# Part DCCVII — Holonomy Selector-Polarization-Charge Bridge

## Why this part exists

`Part DCCVI` proved the exact conditioned packet-budget law:

$$
162 = 81 + 81
$$

for each live selector value.

The next step is to give this budget a signed channel interpretation.

This part proves that closure.

## Signed polarization-charge law

Using the DCCV selector ledger and DCCVI conditioned budget, the verifier assigns for each live selector value:

- `+81` to the selected ordered line type,
- `-81` to the complementary ordered line type.

It then proves:

1. each charge profile is exactly `{-81,+81}` across the two ordered types,
2. net charge is always `0`,
3. absolute charge budget is always `162`.

So the two-value selector is exactly a signed polarization-charge choice on the fixed `162` envelope.

## Selector flip involution

The verifier also proves the selector flip map

$$
1 \leftrightarrow 2
$$

is involutive and negates the charge vector componentwise.

So switching selector value does not change the total budget; it reverses channel sign.

## Why this is a breakthrough

The remaining wall is now compressed into a physically suggestive invariant form:

> one selector bit determines one signed polarization-charge orientation, with conserved absolute budget `162` and zero net balance.

This makes the post-DCCVI frontier both operational (budgeted) and oriented (signed).

## Executable artifact

Verifier:

```text
verify_dccvii_holonomy_selector_polarization_charge_bridge.py
```

Tests:

```text
tests/test_dccvii_holonomy_selector_polarization_charge_bridge.py
```

Generated summary:

```text
data/dccvii_holonomy_selector_polarization_charge_bridge.json
```

---
*W33-Theory | Part DCCVII | the two-value slot selector is exactly a signed polarization-charge choice: `+81/-81` across ordered line types, zero net charge, conserved absolute budget `162`, and selector flip as involutive sign reversal.*
