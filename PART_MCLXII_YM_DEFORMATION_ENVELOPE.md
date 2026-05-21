# Part MCLXII: Yang-Mills Gap-Shell Deformation Envelope

## Claim Boundary

MCLXII is a finite W33 normalized-Laplacian theorem. It proves the exact
substrate gap shell and the deformation envelope around it. It does not by
itself prove the continuum Clay Yang-Mills problem; that remains the
identification/limit bridge.

## Statement

For the W(3,3) point graph

```text
SRG(40,12,2,4), adjacency spectrum 12^1, 2^24, (-4)^15,
```

the normalized Laplacian has spectrum

```text
0^1, (5/6)^24, (4/3)^15.
```

Thus the finite mass gap is

```text
nu_gap = 5/6.
```

The holographic substrate entropy from the MCL packet is

```text
S_holo = |E|/(4G_N) = 240/(4*3) = 20.
```

Therefore the gap-shell ratio is exactly

```text
S_holo / nu_gap = 20 / (5/6) = 24.
```

This equals both the multiplicity of the gap shell and the adjoint dimension
of SU(5):

```text
S_holo / nu_gap = mult(5/6) = dim su(5) = 24.
```

The UV shell has multiplicity

```text
15 = dim su(4).
```

## Deformation Envelope

For the normalized edge-weight envelope used in the MCLI branch, the
Davis-Kahan operator-norm coefficient is

```text
2k/v = 24/40 = 3/5.
```

So the one-parameter lower bound is

```text
gap(epsilon) >= 5/6 - epsilon*(3/5).
```

The exact one-parameter closure radius is

```text
epsilon_c = (5/6)/(3/5) = 25/18.
```

The previously surfaced value

```text
25/144
```

is not the one-parameter phase-transition radius. It is the E8-rank
distributed per-channel safe radius:

```text
(25/18)/8 = 25/144.
```

At that per-channel radius the one-channel lower bound is still positive:

```text
5/6 - (25/144)*(3/5) = 35/48.
```

Eight such channels saturate the full radius:

```text
8*(25/144) = 25/18.
```

## Uniform Edge-Scale Invariance

The automorphism-uniform edge scaling branch is stronger than the perturbation
bound. If

```text
A -> cA, D -> cD,
```

then

```text
L_hat = I - D^(-1/2) A D^(-1/2)
```

is unchanged for every positive scalar `c`. The gap is exactly invariant on
that branch.

## Artifacts

- Analysis: `analysis/w33_ym_deformation_envelope.py`
- Tests: `tests/test_w33_ym_deformation_envelope.py`
- Result: `PART_MCLXII_YM_DEFORMATION_ENVELOPE_results.json`
