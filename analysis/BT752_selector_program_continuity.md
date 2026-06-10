# BT752 — Selector Program Continuity Ledger

This note records the corrected state after reading BT738--BT749 and extending the chain through BT750--BT751.

## Confirmed frontier before this pass

BT739--BT749 established:

- `chart81 = LeviE4 = Steinberg` and the selector bridge is unique up to scalar by Schur.
- Levi graph is the rank-2 Tits building of `Sp(4,3)`; Levi octagons are apartments.
- Presentation pairs form two free `PSp(4,3)` torsors; chirality is D4 mask parity.
- Full collineation group preserves chirality; every pair has a canonical outer involution.
- The pair-involutions form the `3A1` class of `W(E6)`, giving a 540-root-triple fibration.
- Each root-triple/chirality half-fiber is a torsor for the order-48 inner centralizer.
- The old BT718 sheet is rank-complete but not root-uniform.
- Locally, rectangle stabilizer is `D12`; lifts map 2-to-1 onto reflections; reflection classes are chiralities.

## New correction from BT750

The duo bit is exactly the central half-turn partner:

```text
{k, r^6 k}
```

inside the inner `Z12` clock.  But those two partners are different Levi octagons:

```text
duo partners share octagon: 0/24.
```

Therefore the duo bit is not pure gauge and cannot be quotient-collapsed.

## Correct selector target

The root-natural selector candidate must be specified by

```text
(root triple tau, chirality epsilon, dihedral phase phi, duo bit delta).
```

Equivalently, per rectangle:

```text
24 = 2 chirality x 6 phase x 2 duo.
```

A constant phase without a constant duo leaves two apartments per rectangle and is not a selector.

## Next tests

The next heavy verifier should implement the BT751 harness and test candidate selectors for:

1. exactly one selected lift per rectangle;
2. rank `81` over `GF(1000003)`;
3. root-uniform distribution `4^540`;
4. BT741-style flat global register `F2^4`;
5. one absolute chirality torsor;
6. no apartment collapse across the central half-turn duo.

The files added in this pass are:

```text
analysis/bt750_duo_bit_half_turn.py
data/bt750_duo_bit_half_turn.json
analysis/BT750_duo_bit_half_turn.md
analysis/bt751_root_natural_selector_harness.py
data/bt751_root_natural_selector_harness.json
analysis/BT751_root_natural_selector_harness.md
analysis/BT752_selector_program_continuity.md
```
