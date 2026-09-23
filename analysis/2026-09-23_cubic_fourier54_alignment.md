# 2026-09-23 — Cubic image covers the full 54D Fourier-retyped quotient

The nonlinear compiler problem can now be stated and solved at the finite tangent level.

The address module has the exact K-Fourier decomposition
[
operatorname{Reg}(K)=S_1^{27}oplus S_2^{27}oplus L^{27},
]
where the (27)-dimensional (S_1) is the only operator-compatible isotypic
sector.  The minimal compiler must therefore retype the complementary
54-dimensional quotient.

For a matter background (v), let
[
D_v(x)=[v,x].
]
The relevant condition is not merely (operatorname{rank}D_vge54), but
[
operatorname{rank}(S_1+operatorname{Im}D_v)=81.
]
This is equivalent to surjectivity of
[
operatorname{Im}D_vlongrightarrow operatorname{Reg}(K)/S_1.
]

The canonical (S_1) basis was reconstructed from all 27 matrix coefficients
of the frozen qutrit Schrödinger representation (ho_omega), including the
three external (C_3) characters.  Combined ranks were then checked after
reducing (mathbb Z[omega]) at the split primes (103) and (109).
Both primes reproduce the same rank table:

| background | rank D | rank(S1+Im D) | quotient rank | dim(S1∩Im D) |
|---|---:|---:|---:|---:|
| root | 20 | 47 | 20 | 0 |
| uniform | 54 | 63 | 36 | 18 |
| linear | 54 | 72 | 45 | 9 |
| quadratic | 78 | 81 | 54 | 24 |

For the quadratic background
[
v_n=(n+1)^2,
]
the combined rank is exactly (81) modulo both split primes.  Since all entries
lie in (mathbb Z[omega]), a full-rank reduction certifies a nonzero
(81	imes81) minor over (mathbb Q(omega)).  Therefore
[
oxed{operatorname{rank}igl(operatorname{Im}D_v	o
operatorname{Reg}(K)/S_1igr)=54}.
]

This closes the finite linear-alignment obstruction: one explicit cubic
background reaches every one of the 54 Fourier directions that the minimal
compiler must retype.

The image is **not** claimed to equal the canonical (S_2oplus L) subspace.
It intersects (S_1) in dimension (24), but its projection to the chosen
54-dimensional Fourier complement is surjective.

The singular rank-54 backgrounds show why this distinction mattered:
uniform (v) only reaches 36 quotient directions and linear (v) reaches 45.
Raw Jacobian rank by itself is not the operational symmetry-changing capacity.

Evidence:
- analysis/w33_e6_cubic_fourier54_alignment.py
- data/w33_e6_cubic_fourier54_alignment.json
