# BT779 — The Cube-Web Module, Fully Decomposed

BT779 closes the representation-theoretic question left open by BT778.  The
540-node cube web is not just a graph on W(3,3) skew-line pairs; it is a
PSp(4,3)-module whose eigenspaces can be read as genuine irreducible and
isotypic pieces.

The computation uses the BT742 character method: for every group element and
every spectral projector `P_E`, compute

```text
chi_E(g) = trace(P_E rho(g)) = sum_i P_E[i, g.i]
```

then take the exact character inner products over all 25920 elements.

## Computed data

```text
spectrum sectors:
  6^1,
  (1+sqrt(10))^24,
  ((-1+sqrt(73))/2)^15,
  3^60,
  2^84,
  1^81,
  (-1)^120,
  (1-sqrt(10))^24,
  (-3)^116,
  ((-1-sqrt(73))/2)^15

orbital rank of the skew-pair scheme = 32
```

The eigenspace character Gram matrix has diagonal norms

```text
6:1, 1+sqrt10:1, ((-1+sqrt73)/2):1, 3:2, 2:2,
1:1, -1:3, 1-sqrt10:1, -3:3, ((-1-sqrt73)/2):1
```

and the key overlaps are

```text
<24+, 24-> = 1
<15+, 15-> = 1
<St(1), -3> = 1
<15+, -3> = 1
<2, -3> = 1
<3, -1> = 2
```

## Forced decomposition

The character norms and overlaps force the 540-dimensional permutation module
into the following U4(2) / PSp(4,3) degree pattern:

```text
540 = 1 + 2*24 + 3*15 + 2*81 + 2*20 + 64 + 2*30a + 2*30b + 60
```

Sector-by-sector:

```text
  6                    = 1
  1 + sqrt(10)         = 24
  1 - sqrt(10)         = 24        same irrep, Galois-paired
  (-1 + sqrt(73))/2    = 15
  (-1 - sqrt(73))/2    = 15        same irrep, Galois-paired
  3                    = 30a + 30b
  2                    = 20 + 64
  1                    = 81        Steinberg, pure
 -1                    = 30a + 30b + 60
 -3                    = 81 + 20 + 15
```

The dimension check is exact:

```text
1 + 48 + 45 + 162 + 40 + 64 + 60 + 60 + 60 = 540
```

The rank check is exact:

```text
1^2 + 2^2 + 3^2 + 2^2 + 2^2 + 1^2 + 2^2 + 2^2 + 1^2 = 32
```

## Breakthrough interpretation

1. **Two Steinbergs.**  The eigenvalue-1 sector is a pure 81-dimensional
   Steinberg module.  A second Steinberg copy hides inside the eigenvalue -3
   sector.  The protected `81 = q^4` object appears twice in the web layer.

2. **Three copies of the 15.**  The `15 = g_neg` irrep appears with
   multiplicity `3 = q`.  BT778's non-Ramanujan sentinel is one member of a
   q-fold 15-family, while the -3 sector carries another copy.

3. **Galois conjugacy is representation-theoretic, not just spectral.**  The
   two 24-dimensional irrational sectors are isomorphic.  The two
   15-dimensional irrational sectors are also isomorphic.  Algebraic
   conjugacy swaps eigenvalues while preserving the underlying irrep.

4. **Rank 32 is the cube-web control rank.**  Since the permutation character
   has norm 32, the action has exactly 32 orbitals.  BT780 turns this
   character shadow into the explicit 32-state suborbit/routing atlas.

## Validation

Run:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 analysis/bt779_web_module_decomposition.py
```

The thread caps are not mathematically relevant; they only prevent BLAS
over-subscription on some machines.
