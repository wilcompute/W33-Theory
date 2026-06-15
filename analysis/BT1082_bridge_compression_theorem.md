# BT1082 — Bridge-map compression theorem

BT1082 formalizes what the BT1078 bridge skeleton preserves, discards, and leaves as reservoir.

## Data

The bridge skeleton has shape

```text
F : C^162 -> C^240
```

with splits

```text
C^162 = S96 direct_sum S66
C^240 = C96 direct_sum C144
```

where

```text
C96  = E0 direct_sum E16
C144 = E4 direct_sum E10.
```

## Theorem

There exists a partial-isometry injection `F` satisfying

```text
F^T F = I_162
F(S96) subset C96
F(S66) subset C144.
```

Moreover, because `dim S96 = dim C96 = 96`, the first restriction is onto:

```text
F(S96) = C96.
```

The complement restriction embeds only 66 dimensions into a 144-dimensional target, leaving a reservoir of dimension

```text
144 - 66 = 78.
```

## Preserved structure

The bridge preserves:

```text
1. the physical-rank 96 block,
2. orthogonality of physical/complement split,
3. inner products on the 162-slot carrier,
4. the identification of the chain-side physical support with E0+E16.
```

## Not preserved or not yet defined

The bridge does not yet preserve:

```text
1. W33 incidence naturally,
2. the true BT876 linear P22 projector,
3. finite algebra action,
4. physical particle labels.
```

## Reservoir interpretation

The 78-dimensional reservoir is not an error term. It is the part of the 240-chain complement not reached by the first slot injection. It may carry chain curvature, local-boundary redundancy, heavy-sector bookkeeping, or constraints needed to turn the sparse bridge into a W33-natural map.

## Boundary

BT1082 is a compression theorem for the skeleton bridge. It is not yet the final W33-natural carrier functor.
