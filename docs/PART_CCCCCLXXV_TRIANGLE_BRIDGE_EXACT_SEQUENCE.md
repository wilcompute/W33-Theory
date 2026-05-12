# Part CCCCCLXXV — Triangle Bridge Exact Sequence

This part packages the incidence-frame Higgs/Yukawa synthesis results into an exact sequence.

Previous results:

```text
triangle weights: R^160
line-sum kernel:  R^40
active image:     120
vertex subimage:  39
remaining quotient: 81
```

The exact finite sequence is

```text
0 -> L_40 -> Tri_160 -> Y_tri,120 -> 0,
```

where:

- `Tri_160` is the real vector space spanned by W(3,3) triangles,
- `L_40` is the span of the 40 K4-line triangle sums,
- `Y_tri,120` is the active triangle bridge image under `T_tri`.

Thus

```text
Y_tri,120 ~= Tri_160 / L_40.
```

Part CCCCCLXXIII showed that vertex synthesis sits inside triangle synthesis:

```text
Y_vert,39 subset Y_tri,120.
```

Therefore there is a second exact quotient:

```text
0 -> Y_vert,39 -> Y_tri,120 -> Q_81 -> 0.
```

The dimension is

```text
dim Q_81 = 120 - 39 = 81.
```

So the full exact-sequence package is

```text
0 -> L_40 -> Tri_160 -> Y_tri,120 -> 0
0 -> Y_vert,39 -> Y_tri,120 -> Q_81 -> 0
```

or compressed:

```text
Q_81 ~= (Tri_160 / L_40) / Y_vert,39.
```

This identifies the 81-dimensional complement as a quotient, not just a dimension count.

Interpretation:

```text
line sums       = invisible triangle redundancies,
vertex image    = exact/gradient flavor subspace,
Q_81            = homological triangle-bridge quotient.
```

The numerical match is exact:

```text
40  = number of W(3,3) K4 lines,
160 = number of W(3,3) triangles,
120 = active triangle/Higgs bridge dimension,
39  = rank(d1)=|V|-1,
81  = dim H1.
```

This suggests the active triangle bridge space is the finite Higgs/Yukawa analogue of a Hodge decomposition:

```text
active triangle bridge = exact vertex-gradient sector + homological matter sector.
```

The next computational target is to construct an explicit projector

```text
Pi_Q : Y_tri,120 -> Q_81
```

and compare the resulting `Q_81` bridge singular spectra with the cellular harmonic projector onto `H1`.
