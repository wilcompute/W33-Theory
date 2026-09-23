# 2026-09-23 — Anti-linear completion of Hessian 216 and the affine-hull null cone

The last 24 hours close a factor-two symmetry bridge that was not visible before
the ramified affine hull and the corrected anti-linear E8 involution landed.

The repository already certifies the nonsplit central extension
[
1	o C_3	o {m Cliff}_1(3)	o ASL(2,3)	o1,
qquad 648/3=216.
]
The order-216 quotient is the projective one-qutrit Clifford/Hessian group.

In the frozen qutrit normal form
[
Z^aX^bomega^c,
]
entrywise complex conjugation acts by
[
(a,b,c)mapsto(-a,b,-c).
]
Hence on the phase-space quotient (H_{27}/Z(H_{27})congmathbb F_3^2)
it is the determinant-minus-one reflection
[
kappa=operatorname{diag}(-1,1).
]

Adjoining (kappa) to (ASL(2,3)=mathbb F_3^2:SL(2,3)) gives
[
oxed{mathbb F_3^2:GL(2,3)=AGL(2,3),quad |AGL(2,3)|=432.}
]
This is exactly the affine factor independently recovered as the automorphism
group of the ramified ([45,12,6]_3) VM code.

The four affine direction classes are represented by
[
(1,0),(0,1),(1,1),(1,2).
]
The determinant-one subgroup induces (A_4) on them.  The reflection
(kappa) acts as the odd transposition
[
(1,1)leftrightarrow(1,2),
]
so the extended group induces all of (S_4).

The new affine hull supplies an independent realization of that same (S_4).
Its nondegenerate quotient has dimension three over (mathbb F_3) with Gram
matrix
[
Q=egin{pmatrix}0&1&1\\1&0&1\\1&1&0end{pmatrix}.
]
Its projective isotropic vectors are exactly
[
[1,0,0], [0,1,0], [0,0,1], [1,1,1].
]
Exhaustion of all (3^9) matrices gives
[
|O(Q)|=48,qquad |SO(Q)|=24.
]
The special orthogonal group acts faithfully on the four null rays, hence as
(S_4).  Under
[
(1,0)leftrightarrow[1,0,0],quad
(0,1)leftrightarrow[0,1,0],quad
(1,1)leftrightarrow[0,0,1],quad
(1,2)leftrightarrow[1,1,1],
]
the permutation set is exactly the same as the (GL(2,3)) direction action.

Thus the four Hesse direction classes are literally the projective null cone of
the affine-hull quotient.  The unitary projective Clifford/Hessian group gives
the orientation-preserving (A_4) layer; anti-linear qutrit conjugation
supplies the missing orientation reversal and completes (S_4).

This is finite geometry over (mathbb F_3).  “Null cone” here does **not**
mean a continuum Lorentz cone, and no spacetime metric, CPT theorem or observed
CP violation follows from this certificate.

Evidence:
- `analysis/w33_extended_clifford_hesse_null_cone.py`
- `data/w33_extended_clifford_hesse_null_cone.json`
- `tests/test_w33_extended_clifford_hesse_null_cone.py`
