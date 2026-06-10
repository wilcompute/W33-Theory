# BT670 — Paper Insert: Codec Cube to Six-Frame G2 Quotient

## Manuscript-ready statement

The complement to the six regular tetrahedral carriers has a raw-versus-codec distinction.

Raw Levi flag adjacency gives

```tex
C_{16}^{raw} \cong K_4 \sqcup K_4 \sqcup K_4 \sqcup K_4,
```

not the hypercube.  The hypercube appears only after choosing the secondary product-codec chart

```tex
C_{16}=A\times B, \qquad A\cong B\cong \mathbb F_2^2.
```

Thus the safe chain is

```tex
4K_4
\xrightarrow{secondary\ codec}
Q_4
\xrightarrow{antipodal}
K_{4,4}.
```

## Fano hinge chart

Use the hinge chart

```tex
O=\{001,010,100,111\},
\qquad
E=\{000,011,101,110\}.
```

The quotient graph is

```tex
K_{4,4}\cong \operatorname{Cay}(\mathbb F_2^3,O),
```

with bipartition `E | O`.

For each `s in O`, define the matching

```tex
M_s=\{(e,e+s): e\in E\}.
```

The four matchings form the canonical Fano one-factorization.

## Six one-factorization frames

After choosing an origin and identifying the two bipartite sides, the `24` perfect matchings of `K44` are modeled by `S4`.

The canonical frame is the Klein four subgroup

```tex
V_4=\{(),(12)(34),(13)(24),(14)(23)\}\subset S_4.
```

Hence the six one-factorization frames are

```tex
S_4/V_4 \cong S_3.
```

Equivalently,

```tex
24\text{ perfect matchings}=6\text{ frames}\cdot4\text{ matchings per frame}.
```

## K33 and W(G2)

The six-frame graph is the transposition Cayley graph of `S3`:

```tex
g\sim h
\Longleftrightarrow
g^{-1}h\text{ is a transposition}.
```

Therefore

```tex
\operatorname{Cay}(S_3,\text{transpositions})\cong K_{3,3}.
```

Using the BT666 chart,

```tex
011\leftrightarrow\text{far},
101\leftrightarrow\text{middle},
110\leftrightarrow\text{active},
```

label the six frames

```tex
F_+,M_+,A_+ \mid F_-,M_-,A_-.
```

The metric matching is

```tex
F_+F_-,\qquad M_+M_-,\qquad A_+A_-.
```

Its stabilizer is

```tex
\operatorname{Aut}(K_{3,3},M_{metric})\cong D_6\cong W(G_2).
```

## Chain to cite

```tex
4K_4
\to Q_4
\to K_{4,4}
\to \operatorname{Match}(K_{4,4})
\to S_4/V_4\cong S_3
\to K_{3,3}
\to W(G_2).
```

## Boundary

This is a secondary quotient statement.  It does not assert that the raw complement is `Q4`, and it does not claim that the folded cubic propagator supplies a real flag-level `W(G2)` reflection.
