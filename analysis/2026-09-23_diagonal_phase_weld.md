# 2026-09-23 — Diagonal center/external phase weld

The cubic compiler now has a coordinate-native symmetry-changing background.

Write the frozen scheduler address as
[
K=H_{27}	imes C_3^{m ext},
qquad
h=(a,b,c)=Z^aX^bomega^c,
]
with external phase (pinmathbb F_3).

The pure central H27 direction has two lifted external slopes:
[
g_+=((0,0,1),1),qquad g_-=((0,0,1),2).
]
Define
[
	au_-=c-p,qquad 	au_+=c+ppmod 3.
]
Right multiplication by (g_+) fixes (	au_-); right multiplication by
(g_-) fixes (	au_+).  Thus each diagonal phase is constant on every
three-point coset of its corresponding lifted central cubic direction.

Use the three-level backgrounds
[
v_pm=1+	au_pmin{1,2,3}.
]
Each amplitude level occurs exactly 27 times.

The exact rational cubic-Jacobian ranks and the Fourier-quotient projection
ranks are:

| background | exact rank D | quotient rank |
|---|---:|---:|
| center only (1+c) | 54 | 36 |
| external only (1+p) | 54 | 36 |
| diagonal (1+(c+p)) | 72 | 54 |
| diagonal (1+(c-p)) | 72 | 54 |

The quotient ranks are certified at both split Eisenstein primes 103 and 109.
For either diagonal weld,
[
operatorname{rank}(S_1+operatorname{Im}D_v)=81,
]
hence
[
operatorname{rank}igl(operatorname{Im}D_v	o
operatorname{Reg}(K)/S_1igr)=54.
]

This makes the mechanism sharply interaction-like: the H27 central coordinate
alone and the external qutrit coordinate alone each miss 18 required retyped
directions, whereas correlating them diagonally covers the entire 54D quotient.

The two diagonal choices are the conjugate slope pair already present in the
lifted cubic geometry.  No physical FI orientation is inferred from this
finite statement.

Evidence:
- analysis/w33_e6_cubic_diagonal_phase_weld.py
- data/w33_e6_cubic_diagonal_phase_weld.json
