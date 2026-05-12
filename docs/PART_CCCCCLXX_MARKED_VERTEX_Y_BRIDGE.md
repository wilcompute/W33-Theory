# Part CCCCCLXX — Marked-Vertex Incidence Bridge for Y

Part CCCCCLXIX showed that a nonzero Higgs/Yukawa bridge

```text
Y : B_120 -> K_81
```

cannot commute with the internal 1-Hodge Laplacian.  Thus `Y` must be a controlled symmetry-breaking datum.  This part constructs the first explicit incidence-frame bridge.

---

## 1. Construction

Let

```text
H_F = C_1(W(3,3); C),
H_F = K direct_sum B direct_sum R direct_sum S,
```

where

```text
K = ker Delta_1,       dim K = 81,
B = im d2 sector,      dim B = 120,
R = 10-sector,         dim R = 24,
S = 16-sector,         dim S = 15.
```

Let `P_K` and `P_B` be the orthogonal spectral projectors onto the `0` and `4` eigenspaces of the cellular 1-Hodge Laplacian.

Choose a marked vertex

```text
v in W(3,3).
```

Let `M_v` be the diagonal operator on edges defined by

```text
(M_v)_{ee} = 1  if edge e is incident to v,
           = 0  otherwise.
```

Since W(3,3) is 12-regular, `M_v` marks exactly 12 edge coordinates.

Define the incidence-frame bridge

```text
Y_v = P_K M_v P_B.
```

This is a concrete symmetry-breaking Higgs/Yukawa candidate:

```text
B --P_B--> boundary sector --M_v--> marked local incidence frame --P_K--> K.
```

It is not spectral-canonical, because it depends on the chosen vertex `v`.  That is the point: it is an explicit class-3 incidence/frame-derived bridge.

---

## 2. Computed singular spectrum

For every marked vertex `v`, the singular values of `Y_v` are identical by vertex transitivity:

```text
rank(Y_v) = 8,
```

with eight equal nonzero singular values

```text
sigma = sqrt(81/640) = 9/(8 sqrt(10)).
```

Therefore

```text
S_2 = Tr(Y_v Y_v*) = 8 * 81/640 = 81/80,
```

and

```text
S_4 = Tr((Y_v Y_v*)^2) = 8 * (81/640)^2 = 6561/51200.
```

This is the first actual computable W(3,3) Yukawa bridge spectrum.

---

## 3. Interpretation

A marked vertex has valence 12, but after projecting through the physical sector split

```text
B_120 -> K_81,
```

the active incidence bridge has only rank 8.

So the marked local star compresses as

```text
12 local incident edges -> 8 equal K-B singular channels.
```

This is a sharp structural fact:

```text
one vertex-frame vacuum activates eight equal Yukawa channels.
```

The equality of the eight singular values means a single marked vertex by itself does not generate flavor hierarchy.  It creates a degenerate local multiplet.  Flavor hierarchy must come from combining several frames, weighting frames, using lower-symmetry incidence structures, or passing to subgroup-equivariant bridge spaces.

---

## 4. Triangle subframe

If instead one marks a triangle `tau` and lets `M_tau` be the diagonal mask on its 3 edges, then

```text
Y_tau = P_K M_tau P_B
```

has

```text
rank(Y_tau) = 2,
```

with the same nonzero singular value

```text
sqrt(81/640).
```

Thus

```text
S_2(Y_tau) = 81/320,
S_4(Y_tau) = 6561/204800.
```

This suggests a local rule:

```text
triangle frame -> 2 active K-B channels,
vertex star frame -> 8 active K-B channels.
```

---

## 5. Effective masses from the marked-vertex bridge

Using the minimal seesaw from Part CCCCCLXVIII with `H=hI_B`, the integrated boundary channel gives

```text
M_eff(v) = Y_v (4M_F^2 + h)^(-1) Y_v^*.
```

The eight nonzero mass eigenvalues are therefore

```text
m_i = (81/640)/(4M_F^2 + h),       i=1,...,8.
```

The remaining `81 - 8 = 73` kernel directions remain massless for a single vertex-frame bridge.

So a single vertex cannot be the full physical Yukawa structure.  It is a local elementary bridge atom.

---

## 6. Bridge atom principle

The marked-vertex bridge gives a new construction principle:

```text
Physical Y should be assembled from incidence-frame atoms:
Y = sum_v a_v Y_v + sum_tau b_tau Y_tau + ...
```

where the coefficients encode the chosen vacuum/frame and determine the singular-value hierarchy.

This turns flavor construction into a finite spectral synthesis problem:

1. choose incidence frames,
2. build projected bridge atoms `P_K M_frame P_B`,
3. combine them with symmetry/normalization constraints,
4. compute singular values,
5. read off effective masses.

---

## 7. Main conclusion

The first explicit incidence-derived bridge is

```text
Y_v = P_K M_v P_B.
```

It has the exact singular spectrum

```text
8 x sqrt(81/640).
```

This proves the pipeline works:

```text
finite W(3,3) incidence frame
  -> symmetry-breaking Y
  -> projected K-B bridge
  -> singular values
  -> effective fermion mass atoms.
```

The next target is no longer abstract.  It is to synthesize physical flavor by combining these bridge atoms and studying their singular spectra.
