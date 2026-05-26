# Part MCCXLVI: Golden Selector Z20 Cochain Lift

## Claim Boundary

MCCXLVI is a finite cochain theorem for the draft Part XXIV golden selector. It
does not promote the original symplectic sign rule to a flat connection.
Instead, it proves that the obstruction is internally correctable by a
transport-edge C2 cochain, lifted to a Z20 half-period phase.

Line phases alone cannot do this: a line potential is a 0-cochain and
telescopes around every quadrangle.

## Obstruction Counts

The draft selector constructs:

```text
40 lines,
480 directed transport edges,
240 undirected transport edges.
```

Its quadrangle audit checks:

```text
ordered quadrangles = 12960 = v*k*q^3 = 40*12*27,
ordered violations  =   864 = 2^(mu+1)*q^3 = 32*27.
```

So:

```text
864 / 12960 = 1/15 = 1/g.
```

All failures are nonlocal:

```text
local violations    = 0,
nonlocal violations = 864.
```

After quotienting the ordered 4-cycles by dihedral symmetry:

```text
unique quadrangles = 1620,
unique violations  = 108 = mu*q^3 = 4*27.
```

The ordered count is exactly eight copies of the unique carrier.

## GF(2) Cochain System

Let each undirected transport edge carry one C2 correction bit. The cycle
equation is:

```text
sum(edge correction bits around Q) = obstruction(Q) mod 2.
```

The verifier computes:

```text
variables        = 240,
unique equations = 1620,
rank             = 200,
free dimension   = 40.
```

The system is consistent. The `40` free dimensions are the line-gauge degrees
of freedom: adding a line-phase coboundary changes edge labels but leaves every
quadrangle holonomy unchanged.

## Z20 Half-Period Lift

Using the Pisano period `pi(5)=20` as the phase clock, lift the C2 correction
to Z20 by assigning:

```text
phase20(e) = 10 on selected transport edges,
phase20(e) = 0 otherwise.
```

The sign correction is:

```text
tau(e) = (-1)^(phase20(e)/10).
```

Around every unique quadrangle:

```text
phase sum = 10 mod 20  exactly on the 108 originally failing cycles,
phase sum =  0 mod 20  on the 1512 originally passing cycles.
```

Therefore the corrected holonomy is flat:

```text
corrected unique failures  = 0,
corrected ordered failures = 0.
```

## Gauge-Fixed Support

The deterministic row-reduction gauge used by the verifier sets free variables
to zero. In that gauge, the correcting support has:

```text
54 selected edges = 2*q^3,
27 positive-sigma edges,
27 negative-sigma edges.
```

This support is not claimed to be unique or minimum weight; it is one exact
internal lift.

## Consequence

The golden selector did not fail randomly. The obstruction rate is
spectrally quantized by `g=15`, and the obstruction is cohomologically exact on
transport edges. The next target is to make the Z20 edge cochain canonical from
the W33 phase geometry rather than from row reduction.

## Artifacts

- Analysis: `analysis/w33_golden_selector_z20_cochain_lift.py`
- Tests: `tests/test_w33_golden_selector_z20_cochain_lift.py`
- Result: `PART_MCCXLVI_GOLDEN_SELECTOR_Z20_COCHAIN_LIFT_results.json`
