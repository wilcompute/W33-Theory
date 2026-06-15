# BT1065 — Search for a 96-dimensional projector

BT1065 turns the BT1064 split clue into a sharper W33-native projector target.

## Key decomposition

The 162-slot carrier factors as

```text
162 = 3 generations * 54 slots per generation.
```

The physically interesting split from BT1064 was

```text
162 = 96 + 66.
```

Dividing by the three generation fibers gives

```text
54 = 32 + 22
```

per generation.

## Why 22 matters

The number 22 is not random in the W33 corpus. Under the long-root/transvection generation symmetry, the 40-point carrier splits as

```text
22 + 9 + 9.
```

BT876 reads the 22 block as the fixed/diagonal piece: gauge plane plus diagonal matter. Therefore the 66-dimensional complement candidate is

```text
66 = 3 * 22.
```

## Candidate projector

Define a per-generation projector template

```text
P_phys(g) = I_54(g) - P_22(g)
```

where `P_22(g)` is the W33 transvection fixed/diagonal block lifted into generation `g`.

Then

```text
rank P_phys(g) = 54 - 22 = 32
rank P_phys    = 3 * 32 = 96
rank P_comp    = 3 * 22 = 66
```

## Interpretation

The 32-dimensional per-generation physical block is exactly the size of a 16-state Weyl generation plus conjugate/dual bookkeeping.

```text
32 = 16 + 16
```

This gives the first dimensionally plausible route from the 162 carrier to a 96-state physical ledger without a uniform quotient.

## What remains missing

The actual matrix `P_22(g)` is not yet constructed on the 162 carrier. BT1065 identifies the target projector and its W33 source; it does not claim the projector has been built.

## Next exact computation

Lift the BT876 transvection fixed/diagonal decomposition into the 162-slot carrier and construct an idempotent projector with ranks

```text
rank(P_comp)=66, rank(P_phys)=96.
```
