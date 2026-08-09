# PART LXVI — Chain-Homology Diagonalization Theorem

**Status:** structural breakthrough; verified by `PART_LXVI_chain_homology_diagonalization.py`.

Part LXV found a signed non-backtracking turn operator

```text
C = T - O
```

on the 480 directed-edge carrier. Its complex spectrum contained an `81 + 81` sector, suggesting the expected `81 = 27 + 27 + 27` matter/homology carrier was not being assigned by hand but emerging from signed transport.

Part LXVI sharpens that result: after antisymmetrizing the directed-edge carrier to ordinary oriented 1-chains, the `81` sector becomes exactly the first homology sector.

This is a real structural upgrade.

---

## 1. From 480 directed edges to 240 oriented 1-chains

Let `D` be the 480 directed-edge space and let `C1` be the 240-dimensional oriented edge-chain space.

For each undirected edge `{i,j}` with canonical orientation `i<j`, define the antisymmetric embedding

```text
Q(e_ij) = (i -> j) - (j -> i).
```

Then the signed turn operator from Part LXV induces the integer symmetric 1-chain operator

```text
K = Q^T C Q.
```

The verifier confirms:

```text
K is 240 x 240,
K is symmetric,
K entries are in {-1,0,+1}.
```

This is the clean chain-level version of signed open/closed transport.

---

## 2. Spectrum of the chain operator

The spectrum is exactly

```text
Spec(K) = {10^(15), 4^(24), 2^(120), (-6)^(81)}.
```

Equivalently,

```text
(K-10I)(K-4I)(K-2I)(K+6I)=0.
```

The polynomial residual is verified exactly as zero with integer arithmetic.

This is already suggestive:

```text
15  = gauge block,
24  = SU(5)/adjoint-like block,
120 = exact triangle-boundary block,
81  = H1 matter/generation block.
```

But the real result is that these multiplicities are not merely spectral. They align exactly with the chain complex.

---

## 3. The W33 triangle chain complex

Use the 2-complex whose 2-cells are the 160 triangles of W(3,3), four per isotropic `K4` line.

The chain dimensions are

```text
C0: 40 vertices
C1: 240 edges
C2: 160 triangles
```

with boundary maps

```text
d1: C1 -> C0,
d2: C2 -> C1.
```

The verifier confirms

```text
rank(d1) = 39,
rank(d2) = 120,
d1*d2 = 0.
```

Therefore

```text
dim ker(d1) = 240 - 39 = 201,
dim H1 = dim ker(d1) - rank(d2) = 201 - 120 = 81.
```

So the known topological fact

```text
H1(W33 triangle complex) = Z^81
```

is recovered directly.

---

## 4. Diagonalization theorem

The new theorem is that `K` diagonalizes the chain complex:

```text
C1 = cut space ⊕ triangle-boundary space ⊕ homology space
```

with exact dimensions

```text
240 = 39 + 120 + 81.
```

More precisely:

### Cut space

The cut space is

```text
im(d1^T), dimension 39.
```

It decomposes under `K` as

```text
24-dimensional eigenvalue 4 sector,
15-dimensional eigenvalue 10 sector.
```

The induced vertex operator is, on the mean-zero quotient,

```text
6I - A.
```

Since `A` has eigenvalues `2` and `-4` on the nontrivial vertex modules,

```text
6 - 2  = 4  with multiplicity 24,
6 - (-4) = 10 with multiplicity 15.
```

So the `24+15` block is the gradient/cut-space image of the vertex Bose-Mesner decomposition.

### Triangle-boundary space

The exact triangle-boundary space is

```text
im(d2), dimension 120.
```

The verifier proves the exact identity

```text
K d2 = 2 d2.
```

Thus all 120 exact triangle boundaries are eigenvectors of `K` with eigenvalue `2=lambda`.

### Homology space

The cycle space is

```text
ker(d1), dimension 201.
```

Because `im(d2)` is the 120-dimensional eigenvalue-2 subspace inside `ker(d1)`, the remaining cycle sector has dimension

```text
201 - 120 = 81.
```

The verifier confirms this remaining sector is exactly the eigenvalue `-6` eigenspace:

```text
E_{-6}(K) subset ker(d1), dim E_{-6}=81.
```

Therefore

```text
H1 ≅ E_{-6}(K).
```

This is the strongest result so far:

```text
The first homology carrier is the -q! eigenspace of the signed chain-turn operator.
```

At `q=3`, this reads

```text
H1(W33) = eigenspace(K, -6), dim = 81.
```

---

## 5. Why this matters

Earlier versions of the theory used

```text
H1 = Z^81
```

as a topological fact and then identified it with `27+27+27` matter structure.

Part LXVI makes this identification more structural:

```text
81 is not just Betti number arithmetic.
81 is the distinguished -q! eigenspace of a canonical signed transport operator.
```

The operator is built from no fitted physics constants:

1. build W(3,3) from the symplectic form;
2. form the directed-edge non-backtracking carrier;
3. split turns into triangle and open turns;
4. sign them as `T-O`;
5. antisymmetrize to 1-chains.

The result is the Hodge-like decomposition

```text
C1 = im(d1^T) ⊕ im(d2) ⊕ H1
```

with operator eigenvalues

```text
cut:       4^(24) + 10^(15),
exact:     2^(120),
homology: (-6)^(81).
```

This is precisely the sort of dynamical spine the theory needed.

---

## 6. Proposed canonical theorem statement

> **Theorem (Signed-turn Hodge diagonalization).** Let `K=Q^T(T-O)Q` be the antisymmetric 1-chain reduction of the signed non-backtracking turn operator on the directed edges of `W(3,3)`. Then `K` is a symmetric signed integer operator on `C1` with spectrum
>
> ```text
> 10^15, 4^24, 2^120, (-6)^81.
> ```
>
> Moreover, with respect to the triangle chain complex,
>
> ```text
> C1 = im(d1^T) ⊕ im(d2) ⊕ H1,
> ```
>
> `K` acts as `6I-A` on `im(d1^T)`, as scalar `2` on `im(d2)`, and as scalar `-6` on `H1`. Hence
>
> ```text
> H1(W33) = E_{-6}(K), dim H1 = 81.
> ```

---

## 7. Physical interpretation

The natural physical dictionary should be reordered:

```text
vertex adjacency A        -> coarse Bose-Mesner geometry
Seidel sector S           -> isotropic/non-isotropic signed projective geometry
Hashimoto B               -> directed transport carrier
signed turn C=T-O         -> directed open/closed transport oscillator
chain operator K=Q^T C Q  -> Hodge/homology diagonalizer
```

Then matter should be attached first to

```text
E_{-6}(K) = H1,
```

not to a manually chosen 81-dimensional module.

This also suggests a sharper path to the Standard Model dictionary:

```text
E_{-6}(K) should split under order-3 automorphisms as 27+27+27.
```

That is the next test.

---

## 8. Next target

Now that `H1` is an eigenspace of a canonical operator, the next move is to pick an order-3 automorphism `g` of `W(3,3)` and restrict it to

```text
E_{-6}(K).
```

The target factorization is

```text
charpoly(g | H1) = (x^2+x+1)^27
```

or an equivalent real decomposition into three 27-dimensional cyclic sectors.

If verified, this gives the sequence

```text
signed transport -> H1 eigenspace -> Z3 generation splitting -> 27+27+27.
```

That would be a major step toward replacing numerical matching with a canonical representation-theoretic pipeline.
