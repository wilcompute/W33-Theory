# 2026-09-23 — Five Clifford continuations + three outside-box physics probes

This pass executes the five queued continuations after the extended-Clifford
saturation theorem and then pushes three additional physics ideas until they
either close algebraically or hit an explicit boundary.

The executable witness is:

`analysis/w33_20260923_execute_all5_plus3_wigner_clifford_physics.py`

The regression gate is:

`tests/test_w33_20260923_execute_all5_plus3_wigner_clifford_physics.py`

## 1. Reversible quantum mechanics derives the (det=pm1) boundary

The previous saturation theorem compared

[
operatorname{Aut}(Gamma_p)=H_p:GL(2,p)
]

with the retained-phase extended Clifford group

[
H_p:ESL(2,p).
]

The missing physical question was why one should privilege (ESL).

There is now a direct answer from the Weyl commutator itself.

Let

[
ZX=omega XZ.
]

A graph similitude with multiplier (m) sends the Heisenberg center by

[
omega Ilongmapsto omega^m I.
]

But conjugation by a unitary satisfies

[
U(omega I)U^{-1}=omega I,
]

while conjugation by an antiunitary complex-conjugates scalars:

[
A(omega I)A^{-1}=omega^{-1}I.
]

Therefore a reversible Hilbert-space implementation forces

[
oxed{m=pm1.}
]

So the earlier saturation condition has acquired a physical formulation:

> Every combinatorial automorphism of the Heisenberg information geometry is
> realizable as a reversible quantum symmetry.

For odd prime (p), this happens exactly when

[
mathbb F_p^	imes={pm1},
]

hence exactly at

[
oxed{p=3.}
]

This is consistent with Wigner's theorem: transition-probability-preserving ray
symmetries lift to unitary or antiunitary transformations. It is also exactly
the (det=pm1) extended-Clifford boundary used by Appleby.

## 2. The Clifford-648 / (G_{25}) identification is matrix-level

The old repo knew:

- the physical qutrit Clifford lift has order (648);
- the Shephard--Todd Hessian reflection group (G_{25}) has order (648);
- Pass 1068 has exact CHEVIE reflection matrices over (mathbb Q(omega)).

What was missing was the literal gate dictionary.

In the same three-state basis, the three (G_{25}) reflections are

[
oxed{
R_1=P=operatorname{diag}(1,1,omega),
}
]

[
oxed{
R_3=ZP=operatorname{diag}(1,omega,1),
}
]

and

[
oxed{
R_2=
F,operatorname{diag}(omega,1,1),F^{-1},
}
]

where

[
F=
rac{1}{1+2omega}
egin{pmatrix}
1&1&1\
1&omega&omega^2\
1&omega^2&omega
end{pmatrix}.
]

Since (1+2omega=isqrt3), this is only a global phase away from the usual
unitary qutrit Fourier transform.

The exact identities include

[
FXF^{-1}=Z,
qquad
PXP^{-1}=XZ.
]

Thus the CHEVIE reflection generators are not merely isomorphic to qutrit
Cliffords: they are explicit qutrit Clifford phase kicks in one Hilbert basis.

Pass 1068 independently enumerates these reflections as a group of order
(648), so the retained-phase Clifford group and (G_{25}) coincide as this
concrete matrix group.

## 3. The local determinant/spinor (C_2) reaches the exact (E_8) Lie compiler

The local anti-linear qutrit generator acts on the certified external (H_{27})
normal form by

[
Z^aX^bZ_{m FI}^c
longmapsto
Z^{-a}X^bZ_{m FI}^{-c}.
]

The same action is forced by the exact anti-linear (E_8) real structure
already certified in the repo:

[
J=	hetacirc(omegamapstoomega^2),
]

with

[
	heta(h_i)=-h_i,qquad
	heta(e_alpha)=e_{-alpha}.
]

The parent certificate verifies (J) on all (30{,}628) unordered
basis-pair Lie brackets and proves (J^2=1). The resulting fixed real form is

[
E_{8(8)}.
]

On the external (A_2) qutrit:

- the clock (Z) is inverted by coefficient conjugation;
- the FI center (omega I) is inverted;
- the Coxeter shift (X), being built from Weyl reflections, is unchanged by
  root sign because (s_alpha=s_{-alpha}).

Therefore the local extended-Clifford involution is the restriction of the
certified global anti-linear (E_8) involution on this (H_{27}).

This is an exact finite/Lie-algebra weld. It is not an identification with
physical CPT or observed CP violation.

## 4. A canonical Wigner-defect action

For (q=p^f), use the additive central character

[
psi(z)=
exp!left(
rac{2pi i}{p}
operatorname{Tr}_{mathbb F_q/mathbb F_p}(z)
ight).
]

For a determinant multiplier (minmathbb F_q^	imes), define its reversible
quantum mismatch by averaging over the full Heisenberg center and comparing
with the two allowed branches (psi(z)) and (psi(-z)).

Character orthogonality gives the exact result

[
E(m)=
egin{cases}
0,&m=pm1,\
2,&m
eqpm1.
end{cases}
]

Hence

[
oxed{
S(q)=
sum_{minmathbb F_q^	imes}E(m)
=
2(q-3).
}
]

So

[
oxed{S(q)=0iff q=3}
]

for every odd prime power.

This is a non-arbitrary finite action candidate: it is the mean-square failure
of a combinatorial symmetry to act as a reversible quantum symmetry on the
central commutator character.

It is still a **candidate** physical action. No continuum Hamiltonian has been
derived from it.

## 5. Prime-power closure: Frobenius does not spoil the selection

Pass 408 has the full semilinear graph symmetry

[
operatorname{Aut}(Gamma_q)
=
H_q:Gamma L(2,q).
]

The field Frobenius is physically realizable in the standard Schrödinger model.
With basis states labelled by (xinmathbb F_q),

[
U_sigma|xangle=|x^pangle
]

is literally a permutation unitary.

Trace invariance yields

[
U_sigma X_uU_sigma^{-1}=X_{u^p},
qquad
U_sigma Z_vU_sigma^{-1}=Z_{v^p}.
]

The executable witness checks all (81) clock identities explicitly in
(mathbb F_9).

Thus the semilinear physically implementable group is

[
H_q:
left(
ESL(2,q):operatorname{Gal}(mathbb F_q/mathbb F_p)
ight).
]

The Galois factor occurs on both sides, so

[
oxed{
[operatorname{Aut}(Gamma_q):
operatorname{ExtCliff}^{m semi}_q]
=
rac{q-1}{2}.
}
]

Therefore

[
oxed{
operatorname{ExtCliff}^{m semi}_q
=
operatorname{Aut}(Gamma_q)
iff q=3
}
]

among **all odd prime powers**.

For example,

[
q=9:
qquad
|operatorname{Aut}(Gamma_9)|=8{,}398{,}080,
]

while the semilinear reversible-quantum subgroup has order

[
2{,}099{,}520,
]

hence index (4).

---

# Three outside-box physics probes

## A. Primal/dual completion repairs the missing Hodge carrier

The repo's exact W33 clique complex has

[
(C_0,C_1,C_2,C_3)
=
(40,240,160,40)
]

and

[
(b_0,b_1,b_2,b_3)
=
(1,81,0,0).
]

That kills a genuine internal Hodge star.

Instead of pretending otherwise, take the formal reversed dual complex
(K^ee). It has

[
(40,160,240,40)
]

cells and reversed Betti profile

[
(0,0,81,1).
]

The canonical doubled object

[
Koplus K^ee
]

then has

[
oxed{
(C_0,C_1,C_2,C_3)
=
(80,400,400,80)
}
]

and

[
oxed{
(b_0,b_1,b_2,b_3)
=
(1,81,81,1).
}
]

Its Euler characteristic is zero, and a canonical sector swap sends primal
(C_k) to dual (C_{3-k}).

So the repo's old “missing star” obstruction may be telling us something
structural: **dynamics may require a doubled carrier**, with the missing
magnetic/dual sector living in a conjugate copy rather than inside the original
W33 clique complex.

The construction is exact, but it is only a formal Poincare completion until a
positive metric, locality law, and physical inner product are supplied.

## B. The (G_{25}) reflections form an exact (mu_{12}) Floquet clock

Take the three qutrit phase kicks above and drive them periodically:

[
U_F=R_1R_2R_3.
]

Exact (mathbb Q(omega)) arithmetic gives

[
oxed{U_F^{12}=I}
]

with no smaller positive power equal to identity.

Its characteristic polynomial is

[
oxed{
lambda^3-omegalambda^2+omega^2lambda-1,
}
]

and its eigenphases are

[
oxed{
rac1{12},quad
rac4{12},quad
rac7{12}
}
]

of a full (2pi) turn.

Thus the repo's recurring (mu_{12}) frame structure now has a literal
three-pulse qutrit Floquet representative inside the Hessian/Clifford group.

That does **not** derive physical time, but it gives a concrete internal
period-12 control clock which can be compiled optically or in a generic qutrit.

## C. A holonomy interferometer can falsify non-Wigner graph symmetries

For a Weyl pair,

[
X_uZ_vX_u^{-1}Z_v^{-1}
=
zeta_p^{operatorname{Tr}(uv)}I.
]

Take (p=5) and (operatorname{Tr}(uv)=1). A determinant-(2) graph
similitude predicts

[
zeta_5mapstozeta_5^2.
]

But a unitary can only leave the scalar phase unchanged, and an antiunitary can
only conjugate it:

[
zeta_5mapstozeta_5^{-1}=zeta_5^4.
]

Interfere that commutator loop against a reference arm. For the simplest
balanced readout,

[
P_0(phi)=rac{1+cosphi}{2}.
]

The reversible-quantum branches give

[
P_0(2pi/5)approx0.654508,
]

whereas the forbidden determinant-(2) symmetry predicts

[
P_0(4pi/5)approx0.095492.
]

The contrast is approximately

[
0.559017.
]

So the saturation principle has a direct falsification protocol in a
higher-dimensional control system. At (q=3), no forbidden determinant class
exists.

Three-mode Fourier gates and phase-controlled qutrit interferometry have
already been demonstrated experimentally; this proposal uses the same kind of
interferometric phase information as a dimension-control test rather than
claiming new laboratory data.

## Literature used in this pass

- D. M. Appleby, *Properties of the extended Clifford group with applications
  to SIC-POVMs and MUBs*, arXiv:0909.5233.
- R. Simon, N. Mukunda, S. Chaturvedi, V. Srinivasan, *Two elementary proofs
  of the Wigner theorem on symmetry in quantum mechanics*, arXiv:0808.0779.
- D. M. Appleby, I. Bengtsson, H. B. Dang, *Galois Unitaries, Mutually
  Unbiased Bases, and MUB-balanced states*, arXiv:1409.7987.
- M. Artebani, I. Dolgachev, *The Hesse pencil of plane cubic curves*,
  arXiv:math/0611590.
- S. Bravyi, M. B. Hastings, F. Verstraete, *Lieb-Robinson bounds and the
  generation of correlations and topological quantum order*,
  arXiv:quant-ph/0603121.

## Hard boundary

The strongest new statement is now:

> (q=3) is the unique odd prime-power Weyl-Heisenberg dimension in which the
> complete finite bulk automorphism group is exhausted by reversible
> unitary/antiunitary quantum symmetries, even after physically implementable
> Frobenius operations are admitted.

This is a precise finite symmetry principle. What remains open is whether a
fundamental physical axiom forces the information geometry to be maximally
reversible in exactly this sense.
