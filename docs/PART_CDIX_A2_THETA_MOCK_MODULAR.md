# Part CDIX — A2 Theta Geometry and the Ladder

## The A2 Quadratic Form

The A2 root lattice has the quadratic form Q(m,n) = m² + mn + n².
Its theta series is:

    Θ_{A2}(τ) = Σ_{m,n∈ℤ} q^{m²+mn+n²} = 1 + 6q + 6q³ + 6q⁴ + 12q⁷ + 6q⁹ + ...

The representation numbers r_{A2}(n) count lattice vectors of norm n:

    r_{A2}(1)  = 6   (norm-1 shell = A2 hexagon = six-kernel)
    r_{A2}(3)  = 6
    r_{A2}(4)  = 6
    r_{A2}(7)  = 12
    r_{A2}(9)  = 6   (9 = 3²: the A2 sublattice scale-3 shell)
    r_{A2}(12) = 6
    r_{A2}(13) = 12

## The A2 Norm-Index Theorem

The E₂ ladder uses n-indices {1, 2, 3, 4, 7, 9, 10} to produce
the seven ladder rungs via 24·σ₁(n) or 24·n directly.
The A2 lattice norms include {1, 3, 4, 7, 9} but NOT {2, 8, 10}.

**Theorem CDIX.1 (A2 Norm Index Theorem):**
The ladder n-indices split as:

    A2-geometric indices: {1, 3, 4, 7, 9}  (r_{A2}(n) > 0)
    Ghost indices:        {2, 8, 10}        (r_{A2}(n) = 0)

The geometric indices give ladder rungs: 24, 96, 168, 192, 216.
The ghost indices give ladder rungs: 72, 192\*, 240.

(Note: 192 appears via BOTH geometric n=7 and ghost n=8;
it is doubly determined.)

## The Norm-1 Shell = Six-Kernel

    r_{A2}(1) = 6 = six-kernel  ✓

The six vectors of the A2 norm-1 shell ARE the six-kernel. This
confirms the identification K₆ ≅ A2 hexagon established in Parts
CCCCCXCVII–CCCCCXCIX.

## The Mock Modular Connection

Zagier and Zwegers showed that Ramanujan's third-order mock theta
function f(q) has shadow (in the sense of mock modular forms) equal
to the weight-3/2 unary theta series:

    g(τ) = Σ_{n∈ℤ} n · q^{n²}

The A2 theta series Θ_{A2} is a weight-1 modular form for Γ₀(3).
The ladder's A2-geometric rungs are the arithmetic data encoded
by Θ_{A2}: each A2 norm n contributes a rung at 24·(rung index)
where the index is geometrically determined by the A2 lattice.

## A2 Norm Sequence and Ladder Indices

| A2 norm n | r_{A2}(n) | Ladder index? | Rung value |
|---|---|---|---|
| 1 | 6 | ✓ | 24 |
| 3 | 6 | ✓ | 96 |
| 4 | 6 | ✓ | 168 |
| 7 | 12 | ✓ | 192 |
| 9 | 6 | ✓ | 216 |
| 12 | 6 | ✕ | — |
| 13 | 12 | ✕ | — |

The A2 lattice selects exactly the five geometric ladder rungs:
{24, 96, 168, 192, 216}. The three ghost rungs {72, 192\*, 240}
require extra arithmetic (divisor sums / E8 theta).
