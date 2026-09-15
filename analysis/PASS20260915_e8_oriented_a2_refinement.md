# Pass 2026-09-15 addendum — oriented A2 triangles are the Pauli labels

This addendum sharpens the exact weld between Pass 1021's E8 root fibration and the Z3-twisted E8 register without changing the underlying quotient theorem.

Let `c` be the canonical Pass-1021 Coxeter element, `g=c^10`, and `u=c^5`. The base weld proves

\[
E_8/(1-g)E_8\cong \mathbb F_3^4
\]

and identifies its 80 nonzero vectors with the 80 three-root `g`-orbits on the E8 root shell.

Because `g` is fixed-point-free of order three,

\[
1+g+g^2=0.
\]

The exact addendum certificate checks every one of the 80 root orbits and finds

\[
r+gr+g^2r=0,
\qquad
\langle r,gr\rangle=
\langle gr,g^2r\rangle=
\langle g^2r,r\rangle=-1.
\]

Hence each nonzero quotient vector / nonidentity two-qutrit Pauli label is represented by an **oriented A2 root triangle**

\[
v\longleftrightarrow\{r,gr,g^2r\}.
\]

Negation reverses the triangle:

\[
-v\longleftrightarrow\{-r,-gr,-g^2r\}.
\]

The 80 oriented triangles therefore pair into 40 opposite-orientation pairs. Each pair contains six roots and is exactly one full A2 root subsystem. The certificate then checks that every such six-root subsystem is exactly the corresponding Pass-1021 unit orbit under

\[
\langle c^5\rangle=\langle -1,g\rangle\cong C_6.
\]

So the sharpened finite dictionary is

\[
240\ E_8\text{ roots}
\;\longrightarrow\;
80\ \text{oriented }A_2\text{ triangles / nonzero Pauli labels}
\;\longrightarrow\;
40\ \text{unoriented }A_2\text{ systems / }W(3,3)\text{ points}.
\]

This explains structurally why the six-root Eisenstein fibre splits into two three-root pieces: they are the two nonzero scalar multiples `v` and `-v` of the same projective Pauli point.

## Reproduction

Run `python analysis/w33_e8_oriented_a2_refinement.py`. The stored certificate `data/w33_e8_oriented_a2_refinement.json` contains 8 exact checks, all PASS.

## Ownership and scope

Pass 1021 owns the canonical six-root Coxeter/Eisenstein fibration. The base weld `data/w33_e8_twisted_fibration_weld.json` owns the equality with the twisted-register quotient. This addendum contributes only the oriented-A2 refinement. It is an exact finite root-system statement and makes no additional continuum or experimental claim.
