# BT1064 — Quotient/submodule particle-table search

BT1064 searches for a dimensionally plausible route from the 162-slot carrier to a physical 48/96-state fermion ledger.

## Starting point

The carrier dimension is

```text
162 = 2 * 3 * 3 * 3 * 3.
```

A three-generation Standard Model Weyl table with a right-handed neutrino has

```text
48
```

states, or

```text
96
```

with antiparticles.

## Direct quotient ratios

```text
162 / 96 = 27/16     not integral
162 / 48 = 27/8      not integral
```

So the physical table cannot be a simple uniform quotient of all 162 slots.

## Submodule options

The natural factor dimensions are

```text
chirality = 2
generation = 3
fiber = 3
weakslot = 3
color = 3
```

Removing a factor gives:

```text
remove fiber:       54
remove weakslot:    54
remove color:       54
remove chirality:   81
remove generation:  54
```

No single-factor removal gives 48 or 96.

## Closest structured candidates

1. `96 = 2 * 3 * 16`: requires a 16-state internal block per generation with chirality/antiparticle structure. This is not visible as a direct factor of the 162 carrier.
2. `48 = 3 * 16`: requires quotienting both chirality/antiparticle bookkeeping and producing a 16-state generation block.
3. `54 = 3 generations * 18`: the 162 carrier naturally contains three 54-blocks, but 54 differs from 48 by six states per generation.
4. `162 = 96 + 66`: the excess 66 is a familiar W33/toroidal number, but no projector realizing this split is currently constructed.
5. `162 = 48 + 114`: less structurally suggestive in the current carrier.

## Best current hypothesis

The physical table is not a quotient of the raw 162 slots. It is more likely a selected submodule after imposing a representation constraint, with the complement carrying gauge/scalar/heavy bookkeeping rather than physical fermions.

The promising numerical target is

```text
162 = 96 + 66
```

because 66 already appears elsewhere in the W33/toroidal corpus, but this is only a search clue until a W33-native projector is built.

## Boundary

BT1064 does not solve the particle table. It proves the naive quotient route fails and isolates the representation-selection problem as a projector/submodule search, probably targeting a 96-dimensional physical submodule.
