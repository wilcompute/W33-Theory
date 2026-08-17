# Pass 4959 — point-line incidence is the Loewy-lowering compiler

## Result

Let \(I\) be the literal \(40\times40\) incidence matrix between the points
and lines of \(W(3,3)\), with the line side viewed as the point carrier of the
dual generalized quadrangle \(Q(4,3)\).  Over \(\mathbf F_3\), native GAP
proves

\[
 \operatorname{rank}I=25,
 \qquad
 II^{\mathsf T}=A_W+I_{40},
 \qquad
 I^{\mathsf T}I=A_Q+I_{40}.
\]

On the two 39-dimensional augmentation modules, incidence has rank 24 and
factors the nilpotent adjacency radicals from Passes 4948--4949.  This is the
defining-characteristic counterpart of Pass 4956's rational 24-dimensional
intertwiner, but its action on the modular Loewy layers is different and more
informative.

## Associated-graded compiler

Write the point and line filtrations as

\[
 W:10\mid19\mid10,
 \qquad
 Q:14\mid11\mid14.
\]

Incidence annihilates both bottom layers.  On the next layer it induces the
exact surjections

\[
 W_{19}\longrightarrow Q_{14},
 \qquad \operatorname{rank}=14,
 \qquad \ker=W_5,
\]

and

\[
 Q_{11}\longrightarrow W_{10},
 \qquad \operatorname{rank}=10,
 \qquad \ker=\mathbf1.
\]

Thus incidence does not identify the middle homologies: it acts as zero on
both homology quotients because it lowers Loewy degree by one.  In computing
language, it is a typed lowering instruction, not a reversible cast between
the two carriers.

## The Levi factorization

Pass 4949 found that the point middle module splits as
\(W_{19}=W_5\oplus W_{14}\), while the Levi module is the nonsplit extension
\(L_{19}=L_{14}\mathbin{\cdot}L_5\).  Pass 4959 solves the full equivariant Hom
systems and proves

\[
 Q_{14}\cong L_{14}
\]

with a unique rank-14 isomorphism up to scalar for both \(PSp(4,3)\) and
\(PGSp(4,3)\).  The outer-sign-twisted Hom space is zero.  Most importantly,
the unique Pass-4949 forward map factors as

\[
 W_{19}
 \xrightarrow{\ I\ }
 Q_{14}
 \xrightarrow{\ \sim\ }
 L_{14}
 \hookrightarrow
 L_{19},
\]

up to the unavoidable nonzero scalar.  The rank-14 bridge is therefore not an
abstract module coincidence: it is literal point-line incidence followed by
the unique line-radical/Levi identification.

This gives a precise structural reading of the nonsplit Levi module.  It is a
deformation of the split point module in which the shared fourteen-dimensional
piece is exactly the line-side radical selected by incidence, while the
five-dimensional quotient is glued nonsplitly.

## Evidence

- Shared GAP owner:
  `analysis/w33_pass4949_w33_levi_middle19_intertwiner.g`
- Frozen certificate:
  `data/PART_W33_PASS4959_POINT_LINE_INCIDENCE_LOEWY_COMPILER.json`
- Focused regression:
  `tests/test_w33_pass4959_point_line_incidence_loewy_compiler.py`
- Native result: `9/9 checks; status=PASS` together with the expanded
  Pass-4949 `46/46` carrier build

The owner is intentionally shared: Pass 4959 consumes the exact in-memory
carriers and Levi modules constructed by Pass 4949, avoiding a second
coordinate realization that could silently reintroduce the point/line error.

## Boundary

This is an exact finite \(\mathbf F_3\) module and incidence theorem.  It does
not split \(L_{19}\), identify the two middle homologies, or turn the Loewy
lowering map into a continuum propagator, a security guarantee, or implemented
hardware.
