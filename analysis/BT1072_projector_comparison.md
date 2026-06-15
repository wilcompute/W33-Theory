# BT1072 — Projector comparison

BT1072 compares the two rank-96 objects now present in the matter-sector ledger.

## Slot-side object

BT1068 defines a slot-side object on the 162-slot carrier:

```text
rank P96_slot = 96
rank complement = 66
```

## Chain-side object

BT1069 defines a chain-side object on the 240-chain carrier:

```text
P96_chain = P0 + P16
rank P96_chain = 81 + 15 = 96
```

## Main point

The ranks match, but the projectors live on different carriers:

```text
P96_slot  acts on dimension 162
P96_chain acts on dimension 240
```

So they cannot be equated until a carrier bridge map is built.

## Bridge target

A future bridge should map the slot-side 96 block into the chain-side 96 block and map the slot-side 66 complement into the remaining chain sectors.

## Boundary

BT1072 proves a rank match and a comparison target. It does not construct the bridge map.
