# BT750 — Duo Bit = Central Half-Turn, Not Pure Gauge

BT749 left the local selector problem factored as

```text
12 chiral lifts = 6 dihedral phases x 2 duo bit.
```

Claude's next hypothesis was the right one to test:

```text
in a free Z12 action, if a reflection fixes lift k, the other lift fixed by
that same reflection should be r^6 k, where r^6 is the unique central
half-turn of Z12.
```

BT750 confirms the first half and refutes the tempting stronger conclusion.

## Result

For a centered rectangle `R`, the inner stabilizer is

```text
Stab_PSp(R) ~= Z12.
```

It has exactly one involution:

```text
z = r^6.
```

The full rectangle stabilizer is the BT749 dihedral group

```text
Stab_PGSp(R) ~= D12 = Z12 + 12 reflections.
```

Every one of the 12 reflections fixes exactly two of the 24 lifts, and those two fixed lifts are exactly a `z`-orbit.

So:

```text
reflection-fixed duo = {k, z k}.
```

Equivalently, the duo bit is the central half-turn coordinate inside the cyclic `Z12` selector clock.

## Crucial correction

The sharper conjecture was:

```text
do duo partners present the same apartment / Levi octagon?
```

The answer is no:

```text
duo partners share the same octagon: 0/24
duo partners differ as octagons:     24/24
```

Type-A has 12 distinct octagons, Type-B has 12 distinct octagons, and the local 24 lifts present 24 distinct Levi apartments.

Thus the duo bit is **not** pure gauge.  It is real apartment geometry inside the local dihedral reflection fiber.

## The corrected local selector factorization

BT749 gave

```text
hinge = phase(6) x duo(2).
```

BT750 sharpens this to

```text
phase = reflection class representative in D12/Z2_center,
duo  = central half-turn z = r^6 inside Z12,
```

but both are still needed to select a single apartment.

So a constant-dihedral-phase selector is not enough by itself.  A genuinely root-natural selector must choose:

```text
(root triple tau, chirality eps, phase phi, duo delta).
```

BT748's root coordinates give the global carrier

```text
540 x 2 x 48,
```

and BT749/BT750 now resolve the local 24-lift fiber as

```text
2 chirality x 6 phase x 2 central-half-turn duo.
```

## Boundary

This theorem is local per rectangle, transported by transitivity.  It does not yet construct the global root-natural selector.  It tells us that the next selector candidate must be constant in both dihedral phase and central-half-turn duo, not phase alone.

The executable verifier is:

```text
analysis/bt750_duo_bit_half_turn.py
```

The compact result certificate is:

```text
data/bt750_duo_bit_half_turn.json
```
