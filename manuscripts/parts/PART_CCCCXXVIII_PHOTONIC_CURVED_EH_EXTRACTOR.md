# Part CCCCXXVIII: Photonic Curved Einstein-Hilbert Extractor

**Status:** verified exact coefficient extractor for the protected photonic finite-to-curved handoff.

## Result

Part CCCCXXVII attached the protected photonic runtime to explicit curved 4D seeds. This part connects that handoff to the exact curved coefficient machinery already in the repo:

```text
projector channel -> residue channel -> three-sample extractor
-> finite spectral reconstruction -> Rosetta / Weinberg roundtrip
```

The extracted coefficient package is:

```text
c6                  = 12480
cEH                 = 320
rank-39 lock        = 12480 / 39 = 320
a2                  = 2240
a2 / cEH            = 7
c6 / cEH            = 39
x = sin^2(theta_W)  = 3/13
x * c6 / cEH        = 9
```

## Curved Extractor Stack

The barycentric first-moment tower splits exactly into three channels:

```text
120-mode: cosmological/local channel
6-mode:   Einstein-Hilbert-like curvature channel
1-mode:   topological channel
```

The shift operator has characteristic polynomial:

```text
x^3 - 127x^2 + 846x - 720
```

and exact projectors:

```text
P_120 = ((E-6)(E-1))/13566
P_6   = -((E-120)(E-1))/570
P_1   = ((E-120)(E-6))/595
```

Equivalently, the generating function has pole decomposition:

```text
A/(1 - 120 z) + B/(1 - 6 z) + C/(1 - z)
```

The 6-pole residue divided by the seed six-mode coefficient recovers `c6=12480` on both `CP2_9` and `K3_16`; dividing by the universal rank-39 lock recovers `cEH=320`.

## Three-Sample Closure

For either curved seed, any three successive refinement samples recover the same package:

```text
discrete EH coefficient   = 12480
continuum EH coefficient  = 320
topological coefficient   = 2240
```

The same samples reconstruct the finite Dirac/Hodge package:

```text
chain dimensions = (40,240,160,40)
boundary ranks   = (39,120,40)
Betti numbers    = (1,81,0,0)
D_F^2 spectrum   = 0^82, 4^320, 10^48, 16^30
moments          = a0=480, a2=2240, a4=17600
```

## Inverse Rosetta

The coefficient package reconstructs the internal W33 geometry:

```text
q      = 3
Phi3   = 13
Phi6   = 7
SRG    = SRG(40,12,2,4)
spectrum = (12,2,-4)
```

The Weinberg master variable comes back from the curved coefficients:

```text
x = 9 * cEH / c6 = 3/13
```

So the photonic finite-to-curved architecture now has an exact roundtrip:

```text
protected photonic runtime
-> curved CP2_9/K3_16 refinement tower
-> EH coefficient extractor
-> finite D_F^2 package
-> W33 / Rosetta / Weinberg generator
```

## Boundary

This is an exact coefficient-extractor and roundtrip theorem for the current finite-plus-curved package. It is still not the final Einstein-Hilbert spectral-action asymptotic theorem for a smooth continuum limit.

Artifacts:

- Script: `exploration/PART_CCCCXXVIII_PHOTONIC_CURVED_EH_EXTRACTOR.py`
- Results: `PART_CCCCXXVIII_photonic_curved_eh_extractor_results.json`
- Tests: `tests/test_photonic_curved_eh_extractor_ccccxxviii.py`
