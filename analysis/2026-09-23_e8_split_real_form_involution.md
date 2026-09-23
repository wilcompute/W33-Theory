# 2026-09-23 — The executable hybrid E8 compiler carries the split real form E8(8)

The full 248-dimensional hybrid bracket makes it possible to upgrade the prior
grade-label charge-conjugation scaffold to an exact semilinear Lie-algebra
involution.

On the committed source Chevalley basis, define
[
Theta(h_i)=-h_i,qquad Theta(e_alpha)=e_{-alpha}.
]
Solving the full root-phase consistency system gives 6,840 equations of rank
232 on 240 sign variables.  In the committed gauge the all-(+1) root
solution works.  An exhaustive sweep of all
[
inom{248}{2}=30,628
]
unordered basis pairs verifies
[
Theta([x,y])=[Theta x,Theta y]
]
exactly.

The structure constants are integral, so ordinary Eisenstein conjugation
[
omegaleftrightarrowomega^2
]
also preserves the bracket semilinearly.  Therefore
[
J=Thetacircoverline{(cdot)}
]
is an anti-linear involutive Lie-algebra automorphism.

## Exact real-form signature

Let
[
delta=1+2omega,qquad ardelta=-delta,qquad delta^2=-3.
]
The (J)-fixed Cartan directions are (delta h_i).  For each opposite-root
pair, a fixed real plane is
[
e_alpha+e_{-alpha},qquad
delta(e_alpha-e_{-alpha}).
]

The Killing form, computed directly from the committed 248D bracket table, has
Cartan block
[
60egin{pmatrix}
2&0&-1&0&0&0&0&0\
0&2&0&-1&0&0&0&0\
-1&0&2&-1&0&0&0&0\
0&-1&-1&2&-1&0&0&0\
0&0&0&-1&2&-1&0&0\
0&0&0&0&-1&2&-1&0\
0&0&0&0&0&-1&2&-1\
0&0&0&0&0&0&-1&2
end{pmatrix},
]
with exact LDL pivots
[
120,120,90,50,48,45,40,30.
]
Among the 120 opposite-root pairs,
[
K(e_alpha,e_{-alpha})=
egin{cases}
+60,&64	ext{ pairs},\
-60,&56	ext{ pairs}.
end{cases}
]
The fixed real form therefore has Killing inertia
[
oxed{(128_+,120_-)},
]
hence signature (+8).  This identifies the real form as the split form
[
oxed{E_{8(8)}}.
]

The dimensions reproduce the classical Cartan decomposition
[
mathfrak e_{8(8)}=mathfrak{so}(16)oplusmathbf{128},
]
but there is an important gauge firewall.  The sign of
(K(e_alpha,e_{-alpha})) does **not** select the standard D8 versus
half-spinor root types objectwise in the frozen source gauge.  The exact
pair census is

| standard root type | (K=+60) | (K=-60) |
|---|---:|---:|
| D8 integer | 32 | 24 |
| half-spinor | 32 | 32 |

So the (mathfrak{so}(16)) compact subalgebra emerges after forming the
(J)-fixed linear combinations; it is not obtained by simply retaining the
112 integer roots in this coordinate gauge.

## Correction to the earlier hybrid scaffold

The previous hybrid charge-conjugation file correctly captured the grade swap
and coefficient conjugation, but not the full Lie automorphism.

All 81 grade-one source roots pair with the exact grade-two negative roots.
However, only 42 of the 81 frozen row signs agree; 39 differ.  Thus the true
matter map is
[
J_{12}(x)=
ar B^{-1}Dar B,ar x,
qquad
D=operatorname{diag}(s_1s_2),
]
with 39 negative diagonal entries.

The neutral block also requires
[
h_imapsto-h_i,qquad e_alphamapsto e_{-alpha},
]
rather than pointwise fixation of all 86 neutral labels.

This closes the real-structure problem at the finite Lie-algebra level.  It
does not derive a physical (E_{8(8)}) gauge theory, exceptional field theory,
gravity, spacetime signature, vacuum, masses, couplings, or observed CP
violation.

Evidence:
- `analysis/w33_e8_split_real_form_involution.py`
- `data/w33_e8_split_real_form_involution.json`
- `tests/test_w33_e8_split_real_form_involution.py`
