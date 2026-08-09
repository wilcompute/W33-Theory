# Part CCCCXXVII: Photonic Curved Product Handoff

**Status:** verified finite-to-curved product handoff for the protected photonic kernel.

## Result

The protected finite photonic kernel is now ready to pair with the explicit curved 4D side:

```text
Delta_ext tensor 1 + 1 tensor D_F^2
```

The finite side contributes:

```text
H1 = 81
edge carrier = 240
classical selector = 40 trits
active protection = [[82320,81,>=81]]
```

The curved side contributes two explicit 4D simplicial seeds:

```text
CP2_9:  vertices 9,  Betti profile (1,0,1,0,1),  harmonic total 3
K3_16:  vertices 16, Betti profile (1,0,22,0,1), harmonic total 24
```

Their operator packages are already explicit: full external Hodge/Dirac-Kahler spectra, product heat-trace factorization against the W33 finite Dirac square, and exact barycentric refinement densities.

## H1 Curved Harmonic Lift

The protected logical tail lifts across external harmonic sectors:

```text
CP2_9: 81 * 3  = 243
K3_16: 81 * 24 = 1944
```

Degree-resolved:

```text
CP2_9: 81 + 81 + 81 = 243
K3_16: 81 + 1782 + 81 = 1944
```

The K3 middle channel is:

```text
81 * 22 = 1782
```

and its H2 signature split is:

```text
(b2+, b2-) = (3,19)
```

So `CP2_9` remains too small to host a rank-2 harmonic H2 branch, while `K3_16` is the first explicit seed in the repo that can.

## Barycentric 4D Density

The external barycentric refinement tower has exact universal local limits:

```text
chain density per top simplex = 120/19
Dirac-Kahler trace density    = 860/19
```

After pairing with the W33 finite Dirac package:

```text
product chain density = 19440/19
product trace density = 7512120/19
```

The important structural point is that the finite kernel does not fake a 4D Weyl law. The genuine scaling family is supplied by the curved external refinement tower.

## A2 Transport Product

The native A2 transport local system also pairs with the curved external operators. Its positive internal Laplacian has:

```text
dimension = 90
spectrum  = 24^20, 33^64, 48^6
gap       = 24
```

The curved A2 product dimensions are:

```text
CP2_9 product = 22950
K3_16 product = 153360
```

with zero product zero modes and exact density limits:

```text
A2 chain density = 10800/19
A2 trace density = 423000/19
```

## Boundary

This proves a finite-to-curved product handoff. It does not prove the final Einstein-Hilbert spectral-action asymptotic theorem. The remaining continuum theorem must show that the explicit external 4D refinement family and the finite internal package produce the correct curved spectral-action expansion.

Artifacts:

- Script: `exploration/PART_CCCCXXVII_PHOTONIC_CURVED_PRODUCT_HANDOFF.py`
- Results: `PART_CCCCXXVII_photonic_curved_product_handoff_results.json`
- Tests: `tests/test_photonic_curved_product_handoff_ccccxxvii.py`
