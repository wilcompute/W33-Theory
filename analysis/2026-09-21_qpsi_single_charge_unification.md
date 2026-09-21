# One integer charge unifies the E8 Z2, Z3, Z4, Z6 and Z12 layers

## Exact result

The source-locked E8 root-channel (Q_psi) histogram is

[
Q_psi:quad
(-4)^3,;(-3)^{16},;(-2)^{30},;(-1)^{48},;
0^{54},;1^{48},;2^{30},;3^{16},;4^3,
]

where the eight Cartan generators are included in the (Q_psi=0) count.

Reducing this one integer charge gives every discrete grading that had
previously been certified in separate steps:

[
egin{array}{c|c}
	ext{reduction}&	ext{adjoint sector dimensions}\ hline
Q_psimod2&(120,128)\
Q_psimod3&(86,81,81)\
Q_psimod4&(60,64,60,64)\
Q_psimod6&(54,48,33,32,33,48)\
Q_psimod12&(54,48,30,16,3,0,0,0,3,16,30,48).
end{array}
]

The mod-3 statement is objectwise at the certified channel level:

- (g_0(E_6)) has charges (0,pm3), hence grade 0;
- (g_0(A_2)) has charge 0, hence grade 0;
- (g_1) has charges (1,-2,4), all congruent to 1 mod 3;
- (g_2) has charges (-1,2,-4), all congruent to 2 mod 3.

Therefore the canonical CE2 (E_6+A_2) (Z_3) grading is precisely
(Q_psimod3).  The measured heterotic FI projection was already proved
Weyl-equivalent to that canonical (Z_3).  Matter parity is
(Q_psimod2), and the Kummer grading was already frozen as
(Q_psimod4).  The Chinese-remainder refinements are thus not independent
labels:

[
oxed{
Z_6=Q_psimod6,qquad
Z_{12}=Q_psimod12.
}
]

Equivalently, the structural order-six generator is

[
oxed{g_6=exp(2pi iQ_psi/6)}
]

and the order-twelve grading generator is

[
oxed{g_{12}=exp(2pi iQ_psi/12)}.
]

## Literature cross-check

This is the standard (E_8	o SO(10)	imes SU(3)	imes U(1)) charge
decomposition.  For example, the published branching in
*Family unification via quasi-Nambu--Goldstone fermions in string theory*
(PTEP 2013, 053B01) contains
((16,3)_{-1}), ((10,3)_2), ((1,3)_{-4}), their conjugates,
((16,1)_{pm3}), and the neutral (SO(10)	imes SU(3)	imes U(1))
adjoint pieces.  Those dimensions reproduce the exact histogram above.

## Why this matters for the current TOE architecture

The recent FI, matter-parity, Kummer and common-refinement theorems are not four
unrelated coincidences.  They are reductions of one integral lattice charge.
This is stronger than an equality of group orders and stronger than a match of
sector dimensions: the mod-3 congruence is already visible channel by channel,
while mod-2 and mod-4 were separately certified in the existing pipeline.

The new affine-Kac classification then becomes natural: the FI x parity
order-six class is the Kac normal form of the (Q_psimod6) action.

## Evidence

- `analysis/w33_qpsi_mod12_unification.py`
- `data/w33_qpsi_mod12_unification.json`
- `tests/test_w33_qpsi_mod12_unification.py`
- `analysis/w33_e8_order6_kac_classification.py`

## Firewalls

This does **not** identify the (E_8) (Z_{12}) grading with the independent
photonic (mu_{12}) scalar phase group; an explicit character/intertwiner is
still required there.

It also does not prove that the heterotic vacuum preserves matter parity.
Holotrade has correctly withdrawn the old fixed-support 0/24 result as exact
(Z_2) evidence: that calculation imposed full (U(1)) neutrality rather
than even (3(B-L)).  The class-wide parity-preserving D/F-flat vacuum remains
open pending the missing exact rational charge ledgers.
