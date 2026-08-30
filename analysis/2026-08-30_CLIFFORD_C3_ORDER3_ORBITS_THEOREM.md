# Affine orbit geometry of the local C3 Clifford obstruction

## Result

The quotient in the certified central extension

\[
1\to C_3\to K\to Q\to1,
\qquad Q\cong \operatorname{ASL}(2,3),
\]

has 80 order-three elements and hence 40 cyclic subgroups of order three.  The preceding lift-charge audit proved that 16 of those cyclic subgroups have split preimage `C3 x C3`, whereas 24 have nonsplit preimage `C9`.

An independent explicit construction of

\[
\operatorname{ASL}(2,3)=\mathbb F_3^2\rtimes \operatorname{SL}(2,3)
\]

resolves the 40 cyclic order-three subgroups into exactly three conjugacy orbits:

\[
\boxed{40=4+12+24}.
\]

Their affine geometry is:

- **4 pure-translation subgroups.**  Their nonidentity elements have identity linear part and no affine fixed points.
- **12 fixed-line unipotent subgroups.**  Their nonidentity elements have order-three unipotent linear part and exactly three affine fixed points.
- **24 fixed-point-free nontranslation unipotent subgroups.**  Their nonidentity elements have order-three unipotent linear part but no affine fixed point.

The group-order census of this explicit model is

\[
1^1,\quad 2^9,\quad 3^{80},\quad 4^{54},\quad 6^{72},
\]

matching the certified quotient census used in the central-cover calculation.

## Why the 24-orbit is exactly the obstruction locus

Whether the restriction of a central extension to a cyclic subgroup splits is invariant under conjugacy in the quotient.  Therefore the split and nonsplit populations must each be unions of complete conjugacy orbits of cyclic `C3` subgroups.

The exact lift audit gives 24 nonsplit subgroups.  Among the orbit sizes `4,12,24`, the only conjugacy-invariant subset of size 24 is the single 24-orbit itself.  Hence

\[
\boxed{4_{\rm translation}+12_{\rm fixed\ line}\ \text{lift to }C_3\times C_3}
\]

while

\[
\boxed{24_{\rm fixed\text{-}point\text{-}free\ nontranslation}\ \text{lift to }C_9}.
\]

Thus the previously numerical `3/5` obstruction is one geometrically homogeneous Clifford conjugacy class.  It is not simply “the fixed-point-free elements,” because the four pure-translation directions are also fixed-point-free but split.  The discriminant is **fixed-point-free plus nontrivial unipotent linear part**.

## Interpretation

This localizes the nonsplit deck charge much more sharply.  The central `C3` cover thickens precisely the 24 affine unipotent order-three directions with incompatible translation component into cyclic order nine.  Pure phase-space translations and affine fixed-line unipotents remain split.

This is an exact finite-group statement in the canonical `ASL(2,3)` quotient model.  Mapping these affine directions to a specific optical qutrit phase, OAM coordinate, or hardware control phase still requires a separately proved coordinate intertwiner.

## Reproducibility

- executable: `analysis/w33_20260830_clifford_c3_order3_orbits.py`
- input: `data/PART_W33_20260830_CLIFFORD_C3_LIFT_CHARGE.json`
- output: `data/PART_W33_20260830_CLIFFORD_C3_ORDER3_ORBITS.json`
