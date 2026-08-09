# Part CXIII — Petersen-Seidel Kernel of the Hidden Oriented-Triple Cover

Status: theorem-grade structural extension  
Date: April 28, 2026

Part CXII showed that the hidden 20 oriented triples form J(6,3), an antipodal double cover of K10, with splitting

```text
20 = 1 + 9 + 5 + 5.
```

This part identifies the hidden odd kernel:

```text
Petersen.
```

## Odd signed quotient

Choose one oriented triple representative over each bisection. The odd anti-complement quotient is a 10 by 10 symmetric sign matrix S satisfying

```text
S_ii = 0,
```

```text
S_ij = +/-1 for i != j,
```

and

```text
S^2 = 9 I_10.
```

Its spectrum is

```text
3^5, (-3)^5.
```

So S is a regular symmetric conference/Seidel matrix of order 10.

## Petersen graph

Writing

```text
S = J - I - 2P
```

produces a graph P on the 10 bisections.

In the canonical orientation used here,

```text
P = Petersen graph.
```

Thus

```text
P = SRG(10,3,0,1).
```

Its spectrum is

```text
3^1, 1^5, (-2)^4.
```

Changing oriented representatives switches S by diagonal signs, so the invariant object is the Petersen Seidel switching class.

## Voltage-cover interpretation

The hidden cover is

```text
J(6,3) -> K10.
```

It is a Z2-voltage double cover whose voltage/Seidel kernel is Petersen.

The even quotient is

```text
K10
```

with spectrum

```text
9^1, (-1)^9.
```

The odd quotient is

```text
S
```

with spectrum

```text
3^5, (-3)^5.
```

## Odd projectors

The two odd 5-dimensional eigenspaces are selected by

```text
P_+ = (1/2)(I + S/3),
```

and

```text
P_- = (1/2)(I - S/3).
```

Both have rank

```text
5.
```

## Local rank refinement

The hidden 20 splits as

```text
20 = (1+9) + (5+5).
```

Adding the extra C9 residue eigenspace gives

```text
B29 = 20 + 9.
```

Therefore

```text
B29 = 1 + 2*9 + 5 + 5.
```

## Structural slogan

```text
The hidden 20 is a Johnson cover over K10 whose odd Seidel kernel is Petersen.
```
