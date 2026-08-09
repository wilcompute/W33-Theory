# Part MCCCLXXXIX: E8 -> E6 x A2 Coordinate Decomposition

## Claim Boundary

MCCCLXXXIX is a finite root-system decomposition theorem.  It starts with the
exact `E8` roots from MCCCLXXXVIII and checks the coordinate branching

```text
E8 -> E6 x A2.
```

The theorem does not choose a physical compactification or a continuum gauge
breaking mechanism.  It proves the finite branching witness.

## Coordinate Meaning

MCCCLXXXVII read the W33 affine tetracode through the four lines through an
anchor point.  MCCCLXXXVIII lifted those four tetracode coordinates over four
`A2` planes to get exact `E8` roots.

Now choose any one of those four coordinates.  That choice splits the 240 roots
into:

```text
72 E6 roots
6 A2 roots
81 matter roots
81 conjugate matter roots
```

The identity is:

```text
240 = 72_E6 + 6_A2 + 81 + 81.
```

## Verification

For all four coordinate choices, the verifier checks:

```text
E6_zero_coordinate_roots = 72
A2_coordinate_roots = 6
matter_81_coset_1 = 81
matter_81_coset_2 = 81
```

The zero-coordinate roots form an exact `E6` subsystem:

```text
rank = 6
norm profile = {2:72}
local profile = {-2:1, -1:20, 0:30, 1:20, 2:1}
reflection closure failures = 0
```

The selected-coordinate roots form an exact `A2` subsystem:

```text
rank = 2
norm profile = {2:6}
orthogonal to E6 = true
```

The two remaining sectors are conjugate:

```text
|sector_1| = 81
|sector_2| = 81
sector_2 = -sector_1
```

## Reading

The old symbolic match

```text
240 = 72 + 6 + 81 + 81
```

is now an exact coordinate theorem inside the W33-derived `E8` root system.  A
line-coordinate choice in the W33 tetracode is precisely the finite operation
that selects an `E6 x A2` branch.

## Artifacts

- Analysis: `analysis/w33_e8_e6_a2_coordinate_decomposition.py`
- Tests: `tests/test_w33_e8_e6_a2_coordinate_decomposition.py`
- Result: `PART_MCCCLXXXIX_E8_E6_A2_COORDINATE_DECOMPOSITION_results.json`
