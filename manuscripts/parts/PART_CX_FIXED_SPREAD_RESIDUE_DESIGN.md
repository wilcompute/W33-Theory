# Part CX — Fixed-Spread Residue Design and C9 Eigenspace

Status: theorem-grade structural extension  
Date: April 28, 2026

Part CIX found the hidden 20 as the degree of the one-line spread-intersection graph. This part localizes the result inside a single fixed spread.

## Main result

For every spread S in W(3,3):

```text
S has 10 lines.
20 other spreads meet S in exactly 1 line.
15 other spreads meet S in exactly 4 lines.
```

The 20 one-line neighbors form a double cover of the 10 lines:

```text
2 one-line neighbors through each line of S.
```

The 15 four-line neighbors define 15 blocks of size 4 on the 10 lines of S. These blocks form a design:

```text
2-(10,4,2).
```

If N is the 10 by 15 incidence matrix of this design, then

```text
N N^T = 4 I_10 + 2 J_10.
```

Therefore

```text
Spec(N N^T) = 24^1, 4^9.
```

The nonconstant line-residue eigenspace has dimension 9. This is the C9 rank.

## Block-intersection graphs

On the 15 design blocks, adjacency by intersection size 2 gives

```text
SRG(15,6,1,3)
```

with spectrum

```text
6^1, 1^9, (-3)^5.
```

Adjacency by intersection size 1 gives

```text
T(6)=SRG(15,8,4,4)
```

with spectrum

```text
8^1, 2^5, (-2)^9.
```

## Local rank reconstruction

Inside every fixed spread:

```text
20 = one-line spread neighbors,
9 = nonconstant eigenspace dimension of N N^T.
```

Therefore

```text
29 = 20 + 9.
```

So the B29/C9 rank pair is visible locally:

```text
C9 = residue eigenspace,
B29 = 20 + C9.
```

## Structural slogan

```text
Every spread contains a local 2-(10,4,2) design whose nonconstant eigenspace is C9; adding the 20 one-line neighbors gives B29.
```
