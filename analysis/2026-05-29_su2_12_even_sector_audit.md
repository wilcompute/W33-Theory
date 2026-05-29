# H7 Even-Sector Distance-Splitting / Projector Audit Theorem

Date: 2026-05-29

This note audits the uploaded PerplexitySave TQC lead. The useful object is the 7-sector matrix

```text
H_ab = sqrt(2/14) sin(pi (2a+1)(2b+1)/14),  a,b=0,...,6.
```

The important correction is that this is not the full modular SU(2)_12 S-matrix. Full SU(2)_12 has 13 simple labels. The uploaded 7x7 matrix is the even-label / integer-spin block with labels 0,2,4,6,8,10,12.

That correction does not invalidate the lead. It makes it sharper.

## Exact projector result

Let R be the reversal / simple-current pairing R(e_j)=e_(6-j) on the seven integer-spin labels. Then the 7-by-7 block satisfies

```text
H H^T = (I + R)/2.
```

Therefore

```text
(H H^T)^2 = H H^T.
```

So the uploaded H7 block is an exact projector, not a non-degenerate 7-sector modular S-matrix.

The spectrum is

```text
spec(H H^T) = 1^4 + 0^3.
```

Equivalently,

```text
rank(H)=4,  nullity(H)=3.
```

This is the breakthrough:

```text
4 = d_Z,  3 = d_X.
```

So the corrected TQC block recovers the already-computed minimal CSS distance pair of the canonical W(3,3) edge code:

```text
[[240,81,3]]_3,  d_X=3,  d_Z=4.
```

Thus

```text
Phi6 = 7 = d_X + d_Z,
k = 12 = d_X d_Z.
```

This is stronger than treating 7 as an informal anyon count: the 7-sector block splits exactly into the CSS distance pair.

## Verlinde-adjacency correction

Because H is singular, it cannot be used as a standalone non-degenerate modular S-matrix for a 7-object Verlinde algebra. The full SU(2)_12 S-matrix is 13-by-13 and rank 13, while the uploaded 7-by-7 even block has rank 4.

Fusion by integer spin 1, i.e. full SU(2)_12 label 2 restricted to the even labels, gives the 7-node path-with-loops matrix

```text
N1 =
[0 1 0 0 0 0 0]
[1 1 1 0 0 0 0]
[0 1 1 1 0 0 0]
[0 0 1 1 1 0 0]
[0 0 0 1 1 1 0]
[0 0 0 0 1 1 1]
[0 0 0 0 0 1 0]
```

This matrix commutes with reversal R, so it splits into a palindromic quotient and a radical quotient.

Palindromic quotient, dimension 4, on basis e0+e6, e1+e5, e2+e4, e3:

```text
N+ =
[0 1 0 0]
[1 1 1 0]
[0 1 1 1]
[0 0 2 1]
```

Radical quotient, dimension 3, on basis e0-e6, e1-e5, e2-e4:

```text
N- =
[0 1 0]
[1 1 1]
[0 1 1]
```

So the operator-level statement is

```text
N1 = N+ + N- as reversal sectors,
dim(N+) = 4 = d_Z,
dim(N-) = 3 = d_X.
```

The uploaded lead was right to focus on the seven-sector object, but the right interpretation is a rank/nullity distance splitting, not the claim that the Verlinde fusion ring is the W(3,3) adjacency.

## T-matrix collapse

The integer-spin conformal weights are

```text
h_j = j(j+1)/14, j=0,...,6.
```

Modulo 1 these are

```text
0, 1/7, 3/7, 6/7, 3/7, 1/7, 0.
```

So the twists collapse under the same reversal orbits:

```text
0~6, 1~5, 2~4, 3~3.
```

There are exactly four distinct twists:

```text
0, 1/7, 3/7, 6/7.
```

Again the quotient dimension is

```text
4 = chi = d_Z.
```

## Bridge to the existing minimal logical surface

Prior pushed code established the minimal logical surface:

```text
|X_min rays| = 160,
|Z_min rays| = 1620,
|X_min F3 vectors| = 320,
|Z_min F3 vectors| = 3240,
rank(A) = 81 = H_1 for the signed phase frame.
```

The corrected H7 block now explains the X-side counts cleanly:

```text
160 = v * rank(H) = 40 * 4,
320 = 2v * rank(H) = 80 * 4.
```

And the same block recovers the distance pair:

```text
nullity(H) = 3 = d_X,
rank(H) = 4 = d_Z.
```

This gives a corrected stack:

```text
H7 even block => H H^T=(I+R)/2 => (d_X,d_Z)=(3,4)
minimal logical phase frame => A A^T / 160 is rank 81 = H_1
unsigned minimal pairings => 51840 = |W(E6)|
```

The main upgrade is conceptual: the TQC lead should be treated as a projector layer matching the W(3,3) CSS distances, not as an already-complete physical braid model.

## Verified identities

All identities below are verified by analysis/w33_su2_12_even_sector_audit.py:

| Identity | Result |
|---|---:|
| uploaded formula equals even SU(2)_12 block | true |
| full SU(2)_12 rank | 13 |
| H7 rank | 4 |
| H7 nullity | 3 |
| H H^T=(I+R)/2 | true |
| (H H^T)^2=H H^T | true |
| rank + nullity | 4+3=7=Phi6 |
| rank times nullity | 4*3=12=k |
| H7 rank equals d_Z | 4=d_Z |
| H7 nullity equals d_X | 3=d_X |
| X_rays=v*rank(H) | 160=40*4 |
| X_vectors=2v*rank(H) | 320=80*4 |

## Interpretation

The uploaded code was pointing at a real structure, but the right theorem is not "SU(2)_12 has seven anyons." It is:

```text
The integer-spin SU(2)_12 block is a 7-sector degenerate carrier whose projector rank/nullity equals the W(3,3) CSS distance pair.
```

That is a clean operation-preserving bridge:

- 7 is not merely a count; it is the sum 3+4.
- 12 is not merely a level; it is the product 3*4.
- The matrix itself realizes the split by exact projection.

The next working slogan is:

```text
H7 is the TQC-facing distance splitter for the W(3,3) minimal logical surface.
```
