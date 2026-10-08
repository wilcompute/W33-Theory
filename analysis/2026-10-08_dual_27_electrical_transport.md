# 2026-10-08 — W33 dual-27 electrical transport defect

**Status:** exact finite computation. **Producer:** `analysis/w33_20261008_dual_27_electrical_transport.py`. **Certificate:** `data/w33_20261008_dual_27_electrical_transport.json`. **Regression:** `tests/test_w33_20261008_dual_27_electrical_transport.py`.

## Scope and already-established prior result

The September 24 proof `analysis/w33_20260924_history_pointline_cospectral_firewall.py` **already** established that the 27 opposite W33 **points** (point-side H27) and 27 W33 **lines** disjoint from a fixed Bell line (symmetric-matrix/null-history chart) are cospectral, nonisomorphic, have 108 edges and 36 triangles, and differ in their induced independent-triad common-neighbor counts. This pass does **not** claim rediscovery of that firewall. The attached script independently reconstructs the objects and obtains a new exact electrical-network invariant comparison.

## Exact dual electrical transport theorem

For either degree-8 graph write its integral adjacency as `A`, its Laplacian as `L=8I-A`, and the unit-edge electrical resistance between vertices `i,j` as `R(i,j)=(e_i-e_j)^T L^+ (e_i-e_j)`.

Both share adjacency spectrum `8^1,2^12,(-1)^8,(-4)^6`, hence Laplacian spectrum `0^1,6^12,9^8,12^6`. Interpolating the reciprocal function on these four eigenvalues gives the **same exact integer polynomial** on both graphs:

```
L^+ = L (13 L^2 - 315 L + 2070) / 23328.
L (13 L^3 -315 L^2 +2070 L) = 23328 I -864 J.
diag(L^+) = 61/486.
```

The second identity and zero row sums certify the Moore–Penrose inverse without numerical inversion.

| Pair invariant | 27 opposite points | 27 transverse lines |
|---|---:|---:|
| Adjacent pairs | 108 at R=13/54 | 108 at R=13/54 |
| Nonadjacent pairs | 216 at R=29/108 (distance 2); 27 at R=5/18 (distance 3) | 162 at R=22/81 (distance 2); 81 at R=43/162 (distance 2) |
| Graph diameter | 3 | 2 |
| Kirchhoff index, sum over unordered vertex pairs of R | **183/2** | **183/2** |

Thus the **total electrical resistance** is equal (as required by cospectrality), while the **pairwise distribution** is different. Even among graph-distance-2 line-history pairs, resistance splits into two values. This is strictly stronger as an operational separator than agreement/disagreement of the adjacency eigenvalues alone.

The physical interpretation is conditional: effective resistance and random-walk transport on **unit-conductance graphs** are mathematically well-defined, but no measured edge conductance, physical kinetic operator, or spacetime metric has been derived from W33. The two carrier dynamics must not be interchanged merely because their global spectra match.

## External context

The relation between effective resistance and a Laplacian pseudoinverse is classical (Kirchhoff/Electrical Networks); comparing cospectral but nonisomorphic graphs is also standard spectral-graph theory. The contribution here is the exact W33 point/line comparison and its reproducible separation, not a claim of general mathematical priority.

## Suggested use

When promoting a W33 point-side or line-side kernel to a physical propagator, require the *pairwise* Green/resistance fingerprint as well as spectral moments and representation data. This acts as a fail-closed point/line transport ABI.
