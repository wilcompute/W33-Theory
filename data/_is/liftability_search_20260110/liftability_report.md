# Liftability search: Z3-hyperplane → PG(3,2) support → Sp(4,2)

## Summary (computed from the 27 coefficient solutions)
We work with the affine hyperplane
\[
H = \{a\in\mathbb{Z}_3^4 : a_0-a_1-a_2+a_3\equiv 1\ (\mathrm{mod}\ 3)\}
\]
which has **27** points.

Define the support projection \(\pi:H\to \mathbb{F}_2^4\setminus\{0\}\) by
\[
\pi(a)_i = 1\ \text{iff}\ a_i\neq 0.
\]
Across all 27 solutions, \(\pi(H)\) hits **all 15** nonzero binary 4-vectors (the points of **PG(3,2)**).

## What “liftable” means here
A linear automorphism \(T\) of \(H\) (coming from a linear map on \(\mathbb Z_3^4\) that preserves the hyperplane)
is called **support-linear** if there exists a binary linear map \(M\in GL(4,2)\) such that
\[
\pi(T(a)) = M\,\pi(a) \quad \text{for all } a\in H.
\]
We then additionally require \(M\in Sp(4,2)\) (preserves the standard symplectic form; “doily symmetry”).

## Main result
Within a very large candidate class of \(H\)-preserving linear maps over \(\mathbb Z_3\) (including all 1–2 sparse row matrices; 18,512 candidates),
the **only** maps that are both support-linear and project to symplectic \(M\) form an **8-element subgroup** of \(Sp(4,2)\).

This subgroup is isomorphic to **D8** (dihedral group of order 8):
- it contains **two** elements of order 4, and
- **five** reflections (order 2), plus identity.

A random search over **60,000** additional uniformly random \(GL(4,3)\) samples (filtered by hyperplane preservation) found **no additional** liftable symplectic actions,
supporting the hypothesis that this D8 is the full liftable symplectic subgroup for this support model.

## Structural consequences
- The lift group **fixes** the PG point **1111** (the unique support point fixed by all 8 elements).
- The missing-support cap and the “apex cap” (from the sec0_m2 completion phenomenon) are **not** globally stabilized;
  each is stabilized only by identity and one reflection.

## Files
- `liftable_symplectic_lifts.csv`: all 8 lifts with (A over Z3) and induced (M over F2), plus element orders.
- `lift_group_multiplication_table_D8.csv`: group law.
- `support_point_orbits_under_lift_group.csv`: orbit decomposition of the 15 PG points.
- `action_on_27_hyperplane_points.csv`: permutation action on the 27 phase-functions.
- `tomotope15_image_under_lift_group.csv`: where your tomotope 15 land under each lift.
- `cap_stabilizers.csv`: which elements stabilize the two special 5-caps.
- `generator_r_order4_*` and `generator_s_order2_*`: explicit generators (with s r s = r^-1).
