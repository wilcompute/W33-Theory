# Part CXXI — Binary-Octahedral Lift and Entangled-Hexad Chirality

Status: theorem-grade structural extension  
Date: April 29, 2026

Part CXX found the projective S4 derangement rule:

```text
even product skeleton -> six 4-cycles,
odd product skeleton  -> three double transpositions with both lifts.
```

This part lifts the statement from projective S4 to GL(2,3).

## Binary-octahedral lift

The group GL(2,3) has order

```text
48.
```

Its projective action on P^1(F3) gives

```text
PGL(2,3) ≅ S4.
```

The kernel is

```text
{+I, -I}.
```

Thus GL(2,3) is the double cover

```text
2.S4,
```

the finite binary-octahedral lift in this qutrit setting.

## Even skeletons: two chiral completions

For an even product skeleton, the relative entangled hexad lies over the six projective 4-cycles of S4.

At the GL(2,3) level there are exactly two possible relative hexads.

They are exchanged by central multiplication:

```text
H -> -H.
```

Every matrix in either even relative hexad has order

```text
8.
```

One chiral hexad has trace class +1 mod 3, and the other has trace class -1 mod 3.

So even product skeletons have two central-opposite chiral completions.

## Odd skeletons: one achiral completion

For an odd product skeleton, the projective relative package is the three double transpositions.

At the GL(2,3) level, the relative hexad contains both central lifts of each double transposition:

```text
{R, -R}
```

for each of the three projective double transpositions.

Every matrix in the odd relative hexad has order

```text
4.
```

and trace

```text
0 mod 3.
```

So the odd completion is centrally self-conjugate and unique.

## Completion law

This explains the previous frame count:

```text
36 = 12 even skeletons * 2 chiral completions
   + 12 odd skeletons  * 1 achiral completion.
```

## Physical meaning

The complete two-qutrit stabilizer MUB-frame completion law is a spin-lift/chirality law:

```text
even local product matchings -> two chiral entangled hexads,
odd local product matchings  -> one achiral entangled hexad.
```

## Structural slogan

```text
The 36 complete two-qutrit MUB frames are controlled by the binary-octahedral lift 2.S4: even skeletons are chiral, odd skeletons are self-conjugate.
```
