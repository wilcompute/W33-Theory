# Part CCCCXXV: Theta / U(5) Stabilizer Completion

**Status:** verified stabilizer-rank completion from the local Csaszar theta packet to the full W33 CSS carrier.

## Result

Part CCCCXXIV promotes the five Csaszar input blocks to the local theta packet:

```text
5 * [[21,2,>=3]] = [[105,10,>=3]]
```

The packet has check rank:

```text
105 - 10 = 95
```

The five input modes also carry the natural `U(5)` input-mode algebra:

```text
dim U(5) = 5^2 = 25
```

Therefore the local theta packet closes exactly onto the W33 triangle-check rank:

```text
95 + 25 = 120
```

Adding the W33 vertex-star rank gives the full CSS stabilizer rank:

```text
120 + 39 = 159 = 240 - 81
```

Equivalently, the whole W33 edge carrier decomposes as:

```text
95 + 25 + 39 + 81 = 240
```

This is the clean rank-level completion:

- `95`: local Csaszar toric checks
- `25`: `U(5)` input-mode completion
- `39`: W33 vertex-star completion
- `81`: protected `H1` logical matter sector

## Physical Split

The same architecture gives a physical-carrier split:

```text
105 + 135 = 240
```

with

```text
105/240 = 7/16
135/240 = 9/16
135 = 45 * 3
```

The `105` side is the five-block Csaszar theta packet. The `135` side is the transport bundle complement, matching the quotient-triangle/line incidence scale already promoted in the W33 center-quad and packet-transport layers.

## Protected Lift

Under the three Steane/Phi6 lifts, one block has size:

```text
Phi6^3 = 7^3 = 343
```

The theta/transport split is preserved inside the active protected carrier:

```text
105 * 343 = 36015
135 * 343 = 46305
240 * 343 = 82320
```

So the protected code remains:

```text
[[82320,81,>=81]]
```

with guaranteed correctable weight `40`, the W33 vertex count.

## Boundary

This is a stabilizer-rank and physical-carrier compiler. It does not assert that the `U(5)` rank completion is a canonical W33 triangle operator isomorphism. It also does not replace the existing Steane/Phi6 protection or the Q4 routing boundary.

Artifacts:

- Script: `exploration/PART_CCCCXXV_THETA_U5_STABILIZER_COMPLETION.py`
- Results: `PART_CCCCXXV_theta_u5_stabilizer_completion_results.json`
- Tests: `tests/test_theta_u5_stabilizer_completion_ccccxxv.py`
