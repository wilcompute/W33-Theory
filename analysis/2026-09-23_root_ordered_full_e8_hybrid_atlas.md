# Root-ordered full E8 hybrid atlas

The completed matter-81 chart is an exact basis over `Q(omega)`:

```text
B81 = 73 cubic pivots + 2 external Fourier modes
      + 3 V_omega modes + 3 V_omega^2 modes.
```

The physical FI certificate independently grades the E8 adjoint as

```text
248 = 86_0 + 81_1 + 81_2
    = (78,1) + (1,8) + (27,3) + (27bar,3bar).
```

The combined verifier now fixes the row order, which was missing from the
first block descriptor.  The landed H27 compiler assigns each of the 81
`K = H27 x C3` addresses to one frozen E8 matter root.  Listing those roots in
the exact `K` order used by `B81` anchors every grade-one row.  The ordered
negative roots anchor grade two, and coefficient conjugation
`omega <-> omega^2` supplies its chart.  The resulting graded block atlas is

```text
I86 direct_sum B81 direct_sum conjugate(B81),
```

with ranks `86+81+81=248` and exact FI-center trace
`86+81 omega+81 omega^2=5`.  The certificate stores all 81 addresses and both
ordered root lists, together with a digest of their joint assignment.

This closes the vector-space row-order gap.  It does not yet transport the E8
Lie bracket.  A full Lie-algebra compiler still needs the structure constants
for

```text
g1 x g1 -> g2,  g2 x g2 -> g1,  g1 x g2 -> g0
```

in hybrid coordinates, and an explicit labeled basis for the neutral `I86`
block.  Matter/antimatter field conjugation is an exact algebraic relation; no
physical CP-selection claim follows from it.

Evidence:

- `analysis/w33_e8_full_graded_hybrid_atlas.py`
- `data/w33_e8_full_graded_hybrid_atlas.json`
- `tests/test_w33_e8_full_graded_hybrid_atlas.py`

## Subsequent executable transport

The merged `analysis/w33_e8_full_hybrid_chevalley_compiler.py` now implements
the bracket in a separately explicit signed current-H27 chart, with source
Cartan and grade-zero root indices defining its neutral block. The historical
open statement above concerns this atlas alone. See
`analysis/2026-09-23_affine_hull_and_executable_e8.md` for the implemented maps
and the distinction between the two row conventions.
