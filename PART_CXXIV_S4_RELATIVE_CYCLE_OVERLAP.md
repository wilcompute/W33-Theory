# Part CXXIV — S4 Relative-Cycle Overlap Law for Qutrit MUB Frames

Status: theorem-grade structural extension  
Date: April 29, 2026

Part CXXIII found the A2 chirality quotient of the complete two-qutrit MUB-frame scheme.

This part resolves the pair-overlap relation by the relative local product skeleton.

## Relative skeleton

Each complete two-qutrit MUB frame has:

```text
type in {E+, E-, O}
```

and product skeleton

```text
p in S4.
```

For two frames F,G, define

```text
s = p_F^{-1} p_G.
```

Then:

```text
product overlap = number of fixed points of s.
```

The total frame overlap is always either

```text
1
```

or

```text
4.
```

Thus:

```text
entangled overlap = total overlap - fixed_points(s).
```

## O-O law

For two O-type frames:

```text
relative double transposition -> four-overlap.
relative 3-cycle              -> one-overlap.
```

This explains why the O-sector four-overlap graph is

```text
3 disjoint K4's.
```

The K4 blocks are the relative-V4 cosets.

## E/O law

For an E-type frame and an O-type frame:

```text
relative transposition -> four-overlap.
relative 4-cycle       -> one-overlap.
```

This holds for both E+ versus O and E- versus O.

## Same-chirality E/E law

For same-chirality E-type pairs:

```text
relative double transposition -> one-overlap.
```

The relative 3-cycle layer splits:

```text
18 four-overlap pairs,
30 one-overlap pairs.
```

So the internal chiral cubic residue lives inside the 3-cycle layer.

## Opposite-chirality E+/E- law

For opposite-chirality E+ and E- pairs:

```text
relative identity             -> four-overlap.
relative double transposition -> one-overlap.
```

The relative 3-cycle layer splits:

```text
60 four-overlap pairs,
36 one-overlap pairs.
```

## Meaning

The spread-intersection SRG is the coarse shadow.

The finer interaction law is:

```text
chirality type pair
+
relative S4 cycle type
+
binary-octahedral lift phase.
```

Where cycle type alone does not decide the overlap, the remaining split is exactly the lift-phase/chirality data.

## Structural slogan

```text
Product overlap is fixed points of the relative S4 skeleton; entangled overlap is the binary-octahedral lift-phase correction.
```
