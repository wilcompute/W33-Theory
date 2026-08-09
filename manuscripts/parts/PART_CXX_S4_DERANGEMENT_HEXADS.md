# Part CXX — S4 Parity Skeleton and Derangement Hexads

Status: theorem-grade structural extension  
Date: April 28, 2026

Part CXIX showed that a complete two-qutrit stabilizer MUB frame is:

```text
local product matching + compatible anti-symplectic hexad.
```

This part identifies the exact S4 mechanism behind the compatibility.

## PGL(2,3) as S4

The four local single-qutrit stabilizer bases are the projective line

```text
P^1(F3).
```

Therefore

```text
PGL(2,3) acts as S4
```

on the four local bases.

The determinant sign descends to this S4 action:

```text
det +1 -> A4,
det -1 -> S4 \ A4.
```

So the anti-symplectic entangled contexts are exactly the odd coset.

## Entangled contexts double-cover the odd coset

The 24 maximally entangled contexts project to the 12 odd permutations of S4.

Each odd projective permutation has two GL(2,3) lifts.

Thus:

```text
24 entangled contexts = 2 * 12 odd S4 maps.
```

## Relative derangement package

Let

```text
p in S4
```

be the product skeleton of a complete MUB frame, and let

```text
e
```

be an entangled projective map in its entangled hexad.

Compare them by

```text
r = p^{-1} e.
```

Then the compatible relative package depends only on the parity of p.

## Even product skeletons

If p is even, the six relative maps are exactly the six 4-cycles of S4:

```text
relative hexad = all six 4-cycles.
```

There are two completions over each even product skeleton. These are the two global choices of GL(2,3) lift through the double cover.

## Odd product skeletons

If p is odd, the relative maps are exactly the three nonidentity Klein-four elements:

```text
relative package = three double transpositions,
```

each appearing with both GL(2,3) lifts.

So:

```text
3 projective maps * 2 lifts = 6 entangled contexts.
```

There is one completion over each odd product skeleton.

## Parity-fiber law explained

The previous law

```text
36 = 12 even skeletons * 2 + 12 odd skeletons * 1
```

is now explained by derangement class:

```text
even skeleton -> 6 four-cycles, one lift each, two global choices.
odd skeleton  -> 3 double transpositions, both lifts, one global choice.
```

## Structural slogan

```text
The entangled hexad is the derangement package attached to the local S4 product skeleton: 4-cycles for even skeletons, double transpositions for odd skeletons.
```
