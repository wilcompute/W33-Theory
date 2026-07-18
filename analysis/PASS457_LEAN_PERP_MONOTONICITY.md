# Pass 457 — Lean perp antitonicity

`formal/W33/Pass457PerpMonotonicity.lean` closes the linear-algebraic step immediately after Pass 447's shifted-span theorem.

It proves:

1. the axis line lies in the plane spanned by the point and axis vector;
2. bilinear orthogonal complement reverses this inclusion;
3. after replacing the shifted pair by Pass 447's equal span, the shifted-pair orthogonal is contained in the axis orthogonal.

Formally,

\[
\operatorname{span}\{x,x+c p\}^{\perp_B}
\subseteq
\operatorname{span}\{p\}^{\perp_B},
\qquad c\ne0.
\]

The module imports Mathlib's bilinear-form orthogonal theory and uses its `orthogonal_le` antitonicity theorem. The source audit finds no `sorry` and no custom axioms.

**Boundary.** Identifying the abstract vectors with the finite-geometric elation center and proving the rim/bulk cardinality statement remain outside this module. Remote Lean compilation is delegated to the pinned CI workflow and is not claimed until a run is visible.
