# Clifford C3 species on the 72 central circuit fibres

The exact central cover has 216 sentinel five-circuits grouped into 72 free central-`C3` fibres. The projective one-qutrit Clifford quotient `Q ~= ASL(2,3)` acts faithfully on those fibres in two 36-orbits, with point stabilizers `S3` and `C6`.

The 40 cyclic order-three subgroups of `Q` split into conjugacy classes `4+12+24`. Their action on the two 36-orbits is exact:

- the four pure-translation `C3`s lift split as `C3 x C3`, have cycle shape `1^9 3^21` on 72 fibres, fix 9 fibres in the `S3` orbit, and fix none in the `C6` orbit;
- the twelve fixed-line unipotent `C3`s lift split as `C3 x C3`, have cycle shape `1^3 3^23`, fix none in the `S3` orbit, and fix 3 fibres in the `C6` orbit;
- the twenty-four fixed-point-free nontranslation unipotents lift nonsplit as `C9`, have cycle shape `3^24`, and fix no fibre in either orbit.

Double counting sharpens this to a stabilizer-incidence theorem: `4*9=36`, so each `S3`-stabilized fibre contains the unique order-three subgroup from the translation class; `12*3=36`, so each `C6`-stabilized fibre contains the unique order-three subgroup from the fixed-line class. The nonsplit 24-class belongs to neither point-stabilizer species.

Therefore the `C9` obstruction is exactly the order-three Clifford species that avoids both 36-fibre stabilizer geometries.

Reproducibility:
- `analysis/w33_20260830_clifford_c3_fibre_stabilizer_geometry.py`
- `data/PART_W33_20260830_CLIFFORD_C3_FIBRE_STABILIZER_GEOMETRY.json`
- exact-continuation run `33337524115` passed.

Boundary: this is an exact finite permutation representation. A physical qutrit/OAM phase interpretation still needs an explicit coordinate intertwiner.
