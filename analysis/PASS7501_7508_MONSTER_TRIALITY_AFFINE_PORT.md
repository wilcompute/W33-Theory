# Pass7501–7508 — Monster triality/affine port

## Exact result

The current E8 mod-3 frontier constructs the classical D4(3) triality carrier

\[
1120_{\rm points}+1120_{+\rm generators}+1120_{-\rm generators}=3360,
\]

where the 1120 points are the projective radicals of the E8 A2 subsystems and the two 1120 generator families are the 2240 Eisenstein W33 leaves.

ATLAS supplies a maximal Monster subgroup

\[
H=(3^2{:}2\times O_8^+(3)).S_4
\]

and an intransitive permutation action on 3369 points.  Hash-pinned ATLAS generators give exactly two orbits:

\[
\boxed{3369=9+3360}.
\]

The 9-point image has order 432 and contains a normal regular C3^2 translation subgroup, so it is the natural affine action of AGL(2,3).  The 3360-point image has order

\[
118852315545600=|O_8^+(3):S_4|.
\]

Using the ATLAS order of H, the two kernels are 18 and |O8+(3)| respectively, and both actions share the quotient of order 24:

\[
432/18=24=|O_8^+(3):S_4|/|O_8^+(3)|.
\]

Therefore the group is the S4-coupled product

\[
\boxed{H\cong AGL(2,3)\times_{S_4}(O_8^+(3):S_4).}
\]

This is the mechanism behind the 9+3360 ATLAS action: an affine F3^2 plane and the D4(3) triality carrier are synchronized by one common S4 outer coordinate.

## Sporadic cross-check

ATLAS also lists O8+(3):S4 as a maximal subgroup of the Baby Monster.  Thus the same 3360 carrier has a direct Baby-Monster port, while the Monster maximal subgroup adds the affine 9-point sheet.

## Why this is stronger than the old Monster notes

Older repo material mostly connected W33 to the Monster through matching integers (24, 15, 240, 196883, etc.).  Those identities may be true arithmetic, but they do not define a map.  This pass does: the carrier is an explicit Q+(7,3) triality geometry constructed from E8/3E8, and the sporadic connection is an actual subgroup permutation action with pinned external generators.

## Boundary

This does **not** prove that the Monster acts on one W33 leaf by its internal W33 incidence automorphisms.  It proves that the *ambient 3360-object triality carrier containing all 2240 W33 leaves* is a natural O8+(3):S4 permutation carrier inside a Monster maximal subgroup.  It also does not derive monstrous moonshine or a physical model.
