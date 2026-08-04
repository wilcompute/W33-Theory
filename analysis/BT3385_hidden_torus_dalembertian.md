# BT3385 — Hidden-torus finite d'Alembertian

The hidden 27-state sector from the exact barycentric decomposition is

\[
D=A(C_3)_{3}-A(C_3)_{1}-A(C_3)_{2}.
\]

Writing the graph Laplacian of one ternary cycle as

\[
\Delta_i=2I-A(C_3)_i,
\]

gives the exact identity

\[
\boxed{D+2I=\Delta_1+\Delta_2-\Delta_3.}
\]

Thus the shifted hidden operator is a finite discrete d'Alembertian on the ternary torus \(C_3^3\): two Laplacian factors enter positively and one negatively.

For Fourier frequency \(k=(k_1,k_2,k_3)\in\mathbb F_3^3\), the one-coordinate Laplacian eigenvalue is zero at frequency zero and three at either nonzero frequency. Therefore

\[
\lambda(k)=3\bigl([k_1\ne0]+[k_2\ne0]-[k_3\ne0]\bigr).
\]

The exact spectrum is

\[
\boxed{6^4,\quad3^{12},\quad0^9,\quad(-3)^2.}
\]

The operator has rank 18 and nullity 9. Its Fourier null set is the disjoint union of:

- the constant mode \((0,0,0)\);
- four modes with \(k_1=0\) and \(k_2,k_3\ne0\);
- four modes with \(k_2=0\) and \(k_1,k_3\ne0\).

Hence the exact null profile is

\[
\boxed{1+4+4=9.}
\]

This is a theorem about a finite signed graph operator. The d'Alembertian terminology describes the algebraic sign pattern only; no physical spacetime, causal cone, Lorentz symmetry, or continuum limit is claimed.

Reproduction:

```bash
python analysis/bt3385_hidden_torus_dalembertian.py \
  --json /tmp/bt3385.json
cmp /tmp/bt3385.json \
  data/PART_BT3385_HIDDEN_TORUS_DALEMBERTIAN_results.json
```
