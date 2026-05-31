# Line-Pair 12-Codec Structure

Date: 2026-05-30

This identifies the 12-state fiber from the previous theorem explicitly.

Previous theorem:

```text
ordered symplectic basis (a,b,c,d)
    -> ([a], L_in, L_out)
```

where

```text
L_in  = P(span(a,b))
L_out = P(span(c,d))
```

and `L_out` is disjoint from `L_in`.

The map has uniform fiber size 12.

This theorem explains exactly what those 12 states are.

## Setup

Fix:

```text
projective anchor A = [a]
input isotropic line L_in through A
output isotropic line L_out disjoint from L_in
```

Then a basis state above this data is a symplectic basis

```text
(a,b,c,d)
```

satisfying

```text
<a,c> = 1
<b,d> = 1
```

and all other pairings vanish.

## The 12 choices

There are two choices for the actual vector representative of the projective anchor:

```text
a or -a.
```

So:

```text
2 choices for a.
```

On the projective line `L_in`, there are four projective points. One is the anchor `A`; the other three are possible non-anchor projective directions for `b`.

Each of those three projective directions has two nonzero vector representatives.

So:

```text
3 * 2 = 6 choices for b.
```

Therefore:

```text
2 * 6 = 12 choices for (a,b).
```

The verifier proves that for each of these 12 choices of `(a,b)`, there is exactly one pair `(c,d)` on the disjoint output line `L_out` satisfying the symplectic duality equations:

```text
<a,c> = 1
<b,d> = 1
<a,d> = 0
<b,c> = 0
```

Thus:

```text
12 = signed anchor representative * signed non-anchor input-line vector.
```

## Dual forcing

The key result is:

```text
(a,b) determines (c,d) uniquely.
```

So the 12-codec is not arbitrary output data. It is an input-line orientation/basis codec, and the output basis is forced by symplectic duality.

## Verified result

The verifier checks for a deterministic anchored disjoint line pair:

```text
constructed states = 12
brute-force fiber states = 12
constructed states equal brute-force states
every (a,b) has exactly one dual (c,d)
every constructed state is a valid symplectic basis
```

So the 12-codec fiber is fully identified.

## Interpretation

The recurring 12 now has a concrete local meaning:

```text
12 = oriented/signed basis codec on an input isotropic projective line with first point fixed.
```

Equivalently:

```text
12 = 2 anchor signs * 3 non-anchor projective choices * 2 b-signs.
```

This is the exact basis/orientation refinement missing from the projective line-pair transport shadow.

## Relation to earlier 12-codecs

This 12 aligns with the previous appearances:

```text
genus denominator 12
local flag codec 12
Csaszar/Szilassi 84 = 7*12
tetrahedron 24 = 2*12
chain shell 480 = 40*12
```

Now we can add:

```text
symplectic basis over anchored disjoint line pair = 12 states.
```

## Compressed theorem

```text
Fix an anchor A, an input isotropic line L_in through A, and a disjoint output isotropic line L_out. The 12 symplectic bases above this projective data are exactly the choices of signed anchor representative a and signed non-anchor vector b on L_in. For every such (a,b), there is a unique symplectic dual pair (c,d) in L_out. Hence the 12-codec is an input-line signed basis/orientation codec whose output side is forced by duality.
```

## Honest boundary

This proves the 12-codec fiber for anchored disjoint line-pair transport. The next hard test is to compare this 12-state input-line codec with the earlier tetrahedral 12-flag chirality codec and determine whether they are canonically equivalent or only count-equivalent.
