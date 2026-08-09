# Part MCLXXXI: Q4 Plaquette Directed-Change Lift

## Claim Boundary

MCLXXXI is a finite hypercube-router theorem. It identifies the square faces of
`Q4` with the directed-change layer of the self-entangled qutrit and with the
24-dimensional W33 positive gap/gauge shell. It is not a continuum
gauge-curvature proof and does not upgrade `Q4` beyond local routing hardware.

## Statement

MCLXXX showed that the four-ray qutrit now-context squares to a 4x4 toroidal
board whose knight graph is the hypercube graph `Q4`.

The next invariant is the square-face packet of `Q4`:

```text
faces(Q4) = C(4,2) * 2^(4-2) = 6 * 4 = 24.
```

The two factors have a direct qutrit reading:

```text
6 = directed past/future changes,
4 = Bell now-context rays.
```

So the `Q4` plaquettes are not arbitrary squares. They are exactly the finite
router lift of the self-entangled qutrit's directed-change sector across its
four-ray present context.

## Local Incidence Laws

Every vertex of `Q4` lies in

```text
C(4,2) = 6
```

square faces. This matches the six directed changes

```text
(0,1), (0,2), (1,0), (1,2), (2,0), (2,1).
```

Each directed change owns four faces, one for each frozen now-slot:

```text
6 directed changes * 4 now slots = 24 faces.
```

The two basic incidence counts both close at `96`:

```text
24 faces * 4 edges = 32 edges * 3 faces = 96,
24 faces * 4 vertices = 16 vertices * 6 directed changes = 96.
```

## W33 Lock

The same `24` is the positive normalized-gap multiplicity from the W33
Yang-Mills deformation envelope:

```text
m_r = 24 = dim SU(5).
```

Thus the finite reading is:

```text
Q4 plaquettes = directed qutrit changes over now-context rays
              = W33 positive gap/gauge shell count.
```

This gives a clean router-level model for where the 24-dimensional gap/gauge
packet lives in the self-entangled qutrit control geometry.

## Artifacts

- Analysis: `analysis/w33_q4_plaquette_directed_change_lift.py`
- Tests: `tests/test_w33_q4_plaquette_directed_change_lift.py`
- Result: `PART_MCLXXXI_Q4_PLAQUETTE_DIRECTED_CHANGE_results.json`
