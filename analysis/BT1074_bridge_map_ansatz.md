# BT1074 — Bridge-map ansatz

BT1074 gives the first bridge target between the 162-slot carrier and the 240-chain carrier.

## Slot side

```text
162 = 96 + 66
```

## Chain side

```text
240 = (81 + 15) + (120 + 24) = 96 + 144
```

## Ansatz

Use an injective bridge map

```text
F: slot carrier -> chain carrier
```

with

```text
96-slot block maps into 81+15 chain block
66-slot complement maps into part of the 120+24 chain block
```

The second target has 144 dimensions, so after embedding the 66-slot complement it leaves

```text
144 - 66 = 78
```

chain dimensions unused by this first bridge.

## Intertwining target

The bridge should satisfy:

```text
chain_96 F = F slot_96
chain_complement F = F slot_complement
```

## Boundary

This is an ansatz for the missing carrier bridge, not a constructed numerical matrix.
