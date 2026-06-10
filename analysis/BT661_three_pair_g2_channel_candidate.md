# BT661 — Three-Pair / G2 Channel Candidate

BT658 found that the six regular 24-flag S4 carriers do not couple uniformly to the 16-flag complement.  Instead, relative to the four K4 complement cells, the six carriers split as

```text
6 = 2 far + 2 middle + 2 active.
```

The aggregate distance profiles are

```text
far pair:    d3=96, d4=288
middle pair: d2=48, d3=192, d4=144
active pair: d1=24, d2=96, d3=120, d4=144
```

## Candidate G2 reading

The positive roots of G2 have six elements.  A rank-two G2 root system also admits a natural pairing by opposite/dual radial channels.  The verified carrier split has exactly the same outer cardinality:

```text
six carrier channels = three paired channels.
```

So the safe candidate dictionary is

```text
active pair  -> near/contact channel
middle pair  -> transfer channel
far pair     -> terminal/noncontact channel
```

or symbolically

```text
G2^+ candidate = {active_1, active_2, middle_1, middle_2, far_1, far_2}.
```

This matches the earlier project pattern in which six one-factorization frames or six positive root directions appear as a quotient carrier.

## What is verified

The verified content is only the metric carrier split:

```text
6 regular S4 carriers split as 2+2+2 around the 4K4 complement layer.
```

The raw distance-one adjacency selects only the active pair:

```text
adjacency vector = (0,0,24,0,24,0).
```

The middle and far pairs appear only after including distance shells d2,d3,d4.

## What is not yet verified

No canonical Weyl group action has been constructed on these six carriers.  In particular, this theorem does not claim

```text
W(G2) acts on the six S4 carriers.
```

The current result is a G2-channel **candidate**, not a Weyl-equivariant module.

## Next verifier target

The next honest test is to build a secondary relation on the six carrier labels whose graph is either

```text
K3,3
```

or the hexagon/root graph of the six positive G2 directions, and then test whether the induced symmetries preserve the three distance-pair classes.
