# Part DCCLXVI - Octahedral Matrix-Tree / Density-Denominator Bridge

**Bridge:** `verify_dcclxvi_octahedral_matrix_tree_density_bridge.py` - Verified
**Tests:** `tests/test_dcclxvi_octahedral_matrix_tree_density_bridge.py` - 16/16 pass
**Data:** `data/dcclxvi_octahedral_matrix_tree_density_bridge.json`

---

## 1. Why this part exists

DCCL-DCCLXII made the octahedral closure phase space into a complete finite
harmonic/Markov system: Laplacian, heat kernel, Green inverse, resistance,
hitting, mixing, recurrence, and Kemeny structure.

DCCLVI, in the parallel sphere-packing lane, identified the E8 optimal-density
denominator:

```text
rho_8 = pi^4 / 384.
```

This part proves that the same `384` is not only a stabilizer-cascade number.
It is also the exact Kirchhoff spanning-tree count of the octahedral closure
phase space.

---

## 2. Exact matrix-tree computation

The octahedral Laplacian has spectrum

```text
0, 4, 4, 4, 6, 6.
```

Therefore

```text
det'(L) = 4^3 * 6^2 = 2304.
```

Kirchhoff's matrix-tree theorem gives

```text
tau(O) = det'(L) / |V(O)| = 2304 / 6 = 384.
```

The verifier also checks every principal Laplacian cofactor directly:

```text
cofactors = [384, 384, 384, 384, 384, 384].
```

---

## 3. The density-denominator identity

From DCCLVI:

```text
rho_8 = pi^4 / 384.
```

From this part:

```text
tau(octahedron) = 384.
```

So the bridge identity is

```text
tau(O) = denominator(rho_8) = G_384.
```

Equivalently, the E8 density denominator is the octahedral matrix-tree count.

---

## 4. W(3,3) factorisations of the same 384

The same integer now carries all of these exact readings:

| formula | value | reading |
|---|---:|---|
| `tau(O)` | 384 | octahedral spanning trees |
| `2 * |W(D4)|` | 384 | double D4 Weyl/tomotope flags |
| `(q+1)^2 * f` | 384 | Cartan trace times the +2 eigenspace |
| `q! * (q+1)^3` | 384 | triality permutations times cubic closure axes |
| `G_384` | 384 | stabilizer-cascade step |
| `denominator(rho_8)` | 384 | E8 sphere-packing density denominator |

This is the first point where the octahedral finite harmonic layer and the E8
sphere-packing density tower meet by an exact graph-topological theorem rather
than only by arithmetic naming.

---

## 5. Spectral-zeta reading

For the nonzero octahedral Laplacian spectrum,

```text
zeta_L(s) = 3*4^(-s) + 2*6^(-s).
```

Hence

```text
zeta_L(0) = 5 = rank(L),
-zeta'_L(0) = log(2304),
exp(-zeta'_L(0)) = det'(L) = 2304.
```

Dividing the regularized determinant by the zero-mode quotient size `6` gives
the same tree count `384`.

---

## 6. Honest boundary

This part proves an exact finite graph identity and an exact equality with the
denominator used in the standard E8 density formula. It does not re-prove
Viazovska's E8 optimality theorem, and it does not derive continuum sphere
packing from the octahedron.

The new content is narrower and stronger: `384` is now simultaneously the E8
density denominator and the matrix-tree count of the validated octahedral
closure harmonic phase space.

---

## 7. One-line summary

```text
tau(octahedron) = 384 = denominator(rho_8) = G_384.
```
