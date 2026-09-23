# 2026-09-23 — Next five attacks + three outside-box physics probes

This pass continues directly from the qutrit extended-Clifford / Wigner-saturation
frontier.  It executes all five queued attacks, including one negative result,
and then follows three independent physics ideas far enough to produce exact
finite certificates or explicit no-go boundaries.

Executable witness:

- `analysis/w33_20260923_next5_plus3_physics.py`

Frozen certificate:

- `data/w33_20260923_next5_plus3_physics_frozen.json`

Regression gate:

- `tests/test_w33_20260923_next5_plus3_physics.py`

## 1. The formal dual completion now has an exact positive local Hodge system

The original W33 clique complex remains

[
(C_0,C_1,C_2,C_3)=(40,240,160,40),
]

with boundary ranks

[
(39,120,40)
]

and Betti vector

[
(1,81,0,0).
]

So the old obstruction remains real: the original complex has no degree-reversing
Hodge star because (C_1) and (C_2) do not even have the same dimension, and
its physical (H^1) sector has no (H^2) partner.

Adjoin the named formal dual complex (K^ee).  Then

[
C(K^ee)=(40,160,240,40),
qquad
b(K^ee)=(0,0,81,1).
]

The self-dual completion

[
widetilde K=Koplus K^ee
]

has

[
oxed{
C(widetilde K)=(80,400,400,80)
}
]

and

[
oxed{
b(widetilde K)=(1,81,81,1).
}
]

Give every primal and dual basis cell unit positive weight and pair each simplex
only with its named formal dual.  The resulting star is local in the strongest
algebraic sense: every row and column has one nonzero entry.  It obeys

[
*^2=1
]

and, writing (B_k) for the primal boundary matrices,

[
oxed{
delta_k=*^{-1}d^ee_{3-k}*=B_k=d_{k-1}^{,T}.
}
]

So the doubled carrier has an exact positive local **algebraic** Hodge system.

The firewall matters.  This is not yet a circumcentric discrete-exterior-calculus
metric obtained from an embedding.  In geometric DEC the Hodge weights are
primal/dual volume ratios.  The theorem here constructs the self-dual algebraic
carrier and its positive counting metric; deriving physical cell volumes is still
open.

## 2. The free-energy hypothesis fails — and that improves the result

The previous pass introduced the multiplier mismatch

[
E(m)=
egin{cases}
0,&m=pm1,\
2,&m
epm1,
end{cases}
]

and total defect

[
S(q)=2(q-3).
]

The obvious statistical-mechanics hypothesis was that (S(q)) might itself be
the canonical free energy after the forbidden multiplier sectors are integrated
out.

It is not.

For the literal multiplier ensemble,

[
oxed{
Z_q(eta)=2+(q-3)e^{-2eta}.
}
]

Hence

[
U_q(eta)=
rac{2(q-3)e^{-2eta}}
     {2+(q-3)e^{-2eta}}
]

and

[
F_q(eta)=
-rac1eta
log!left[2+(q-3)e^{-2eta}ight].
]

The old defect instead satisfies

[
oxed{
S(q)=(q-1)U_q(0).
}
]

So (S(q)) is the unnormalised infinite-temperature mismatch moment, **not**
the canonical equilibrium free energy.

This is recorded as a refutation, not patched into a success.  Extra forbidden
labels provide entropy, so ordinary equilibrium free-energy minimisation alone
does not select (q=3).

The replacement emerges independently in Attack 5: the log-index
(log((q-1)/2)) is simultaneously a symmetry-coset entropy, a KL divergence,
and an ideal Landauer erasure cost.

## 3. Exact 248-dimensional Floquet spectrum

The standard (G_{25}) Coxeter/qutrit Floquet element has fundamental
eigenphases

[
zeta_{12}^{,1},
qquad
zeta_{12}^{,4},
qquad
zeta_{12}^{,7}.
]

Transport this through

[
248=(78,1)+(1,8)+(27,3)+(overline{27},overline3).
]

The (81=(27,3)) matter block therefore carries exponents (1,4,7), each
with multiplicity (27); its conjugate block carries (11,8,5), again with
multiplicity (27).  The external (A_2) adjoint contributes the two Cartan
zeros and the six pairwise phase differences.

The complete exponent histogram modulo (12) is

[
oxed{
0^{80},1^{27},3^2,4^{27},5^{27},6^2,7^{27},8^{27},9^2,11^{27}.
}
]

It sums to (248), and the global action still has exact order (12).

The traces are

[
operatorname{Tr}(U^t),quad t=0,ldots,11:
]

[
oxed{
248, 51, 105, 132, 5, 51, 24, 51, 5, 132, 105, 51.
}
]

The dimensions fixed by (U^t), (t=1,ldots,12), are

[
oxed{
80, 82, 134, 86, 80, 136, 80, 86, 134, 82, 80, 248.
}
]

The (80)-dimensional fixed space of (U) itself is exactly what the branching
suggests: the (78)-dimensional (E_6) adjoint plus the two-dimensional Cartan
of the external (A_2).

Most importantly,

[
oxed{
U^4:
quad
mathfrak g_0mapsto1,quad
mathfrak g_1mapstoomega,quad
mathfrak g_2mapstoomega^2.
}
]

That is exactly the already-certified physical FI/(Q_psi) center action.

## 4. The (p=5) no-go becomes a concrete interferometric protocol

For a Weyl commutator with unit symplectic trace, the reversible quantum branches
at (p=5) carry phase

[
zeta_5^{pm1},
]

while a determinant-(2) graph similitude asks for

[
zeta_5^2.
]

A balanced reference interferometer has

[
P_0(phi)=rac{1+cosphi}{2}.
]

Thus the ideal allowed and forbidden probabilities are

[
P_{m allowed}=0.6545084972,
qquad
P_{m forbidden}=0.0954915028,
]

with ideal contrast

[
0.5590169944.
]

A conservative design budget was then imposed:

- visibility at least (0.965);
- background fraction at most (0.01);
- phase calibration error at most (1^circ);
- visibility uncertainty (0.005);
- background uncertainty (0.002).

After visibility and background the contrast is approximately (0.53406).
Subtracting the linear conservative systematic budget leaves approximately

[
oxed{0.51738}
]

contrast.

Using the worst-binomial-variance normal proxy, the minimum detected-event
count for (5sigma) separation is (94).  The proposed round number is

[
oxed{128 	ext{detected events per test setting}},
]

which gives a conservative significance proxy of roughly (5.85sigma).

This is a protocol calculation, not laboratory data.  The visibility target is
benchmarked against published integrated photonic qutrit interference; it is
not claimed as achieved for the proposed five-mode device.

## 5. Maximal reversibility is a zero-information-obstruction theorem

Let

[
G=operatorname{Aut}(Gamma_q)
]

and let (H) be the reversible unitary/antiunitary semilinear quantum subgroup.
The previous theorem gives

[
[G:H]=rac{q-1}{2}.
]

Choose a full graph symmetry uniformly and forget everything except its coset
in (G/H).  The obstruction label has entropy

[
oxed{
H_{m obs}
=
lograc{q-1}{2}
}
]

in nats.

There is an equivalent distributional statement.  Let (P_G) be uniform on
all nonzero determinant multipliers and (P_Q) uniform on the two quantum
multipliers (pm1).  Then

[
oxed{
D_{m KL}(P_QVert P_G)
=
lograc{q-1}{2}.
}
]

The total-variation distance is

[
1-rac{2}{q-1}.
]

In the ideal Landauer limit, erasing a uniformly distributed obstruction-coset
label therefore costs at least

[
oxed{
W_{min}
=
k_BTlograc{q-1}{2}.
}
]

Entropy, KL divergence, total-variation defect, and ideal erasure cost all
vanish simultaneously iff

[
oxed{q=3.}
]

This is a sharper information-theoretic form of the maximal-reversibility
principle.

# Three outside-box physics results

## A. Full similitudes can be unitarized by adding central-character sectors

The fixed-center Schrödinger representation only sees the determinant-one
symplectic group unitarily.  But the Heisenberg group has one (q)-dimensional
irreducible Schrödinger representation for each nontrivial central character.

Induce the Heisenberg--Weil representation from

[
H_q:SL(2,q)
]

to

[
H_q:GL(2,q).
]

The resulting unitary carrier has dimension

[
oxed{q(q-1)}
]

and, when restricted back to (H_q), contains all (q-1) nontrivial central
characters once.  Determinant similitudes now act by permuting these character
sectors.

That exposes a striking qutrit speciality.  An ordinary charge-conjugate
matter/antimatter pair contains only the two sectors

[
chi,chi^{-1},
]

so its dimension is (2q).  This already equals the full similitude carrier
exactly when

[
q(q-1)=2q,
]

i.e.

[
oxed{q=3.}
]

So the qutrit is uniquely the odd field dimension where **ordinary conjugate
doubling already supplies every nontrivial central-character sector needed to
unitarize the full similitude symmetry**.

## B. Kramers (T^2=-1) is impossible on 81 but natural on (81+81)

Suppose an antiunitary (T=UK) obeys

[
T^2=-I
]

on complex dimension (n).  Then

[
Uoverline U=-I.
]

Taking determinants gives

[
|det U|^2=(-1)^n.
]

For odd (n) this is impossible.  Therefore neither a single qutrit
((n=3)) nor the single (81)-dimensional matter grade can carry a Kramers
structure with (T^2=-1).

But on the doubled matter/antimatter carrier

[
mathbb C^{81}oplusoverline{mathbb C^{81}},
]

define

[
oxed{
T(v,w)=(-overline w,overline v).
}
]

Its linear part is

[
S=
egin{pmatrix}
0&-I\
I&0
end{pmatrix},
]

which is unitary and satisfies

[
S^2=-I.
]

Hence the antiunitary (T) satisfies

[
oxed{T^2=-I}
]

on dimension (162).

This gives a canonical quaternionic/Kramers structure only after the
matter/antimatter doubling.  It is **not** being identified with the repo's
existing (E_8) real involution (J), which has (J^2=+1), nor with observed
physical time reversal.  If a future Hamiltonian commuted with this new (T),
Kramers pairing would then follow.

## C. Four Floquet ticks equal one physical FI-center step

The order-(12) qutrit Floquet clock has fundamental phase exponents

[
(1,4,7)pmod{12}.
]

Multiply by four:

[
(4,16,28)equiv(4,4,4)pmod{12}.
]

Therefore

[
oxed{
U_F^4=omega I_3.
}
]

But the physical FI theorem already identifies (omega I_3) with the
(H_{27}) center and (Q_psimod3) grading element.

On all of (E_8),

[
oxed{
U_F^4:
quad
1^{86}oplusomega^{81}oplus(omega^2)^{81},
}
]

exactly reproducing the certified physical FI spectrum.

So the (mu_{12}) clock does not merely coexist numerically with the physical
(Z_3) center:

[
oxed{
	ext{four Floquet ticks}=	ext{one FI-center step},
qquad
	ext{twelve ticks}=1.
}
]

This is an exact finite internal-control identity, not a claim that the
Floquet clock is physical time.

# Literature interfaces

The external literature was used only to locate the correct mathematical or
experimental interfaces:

- discrete exterior calculus: circumcentric primal/dual complexes and Hodge
  weights as dual/primal volume ratios;
- finite Heisenberg/Stone--von Neumann theory: uniqueness of the Schrödinger
  irrep for a chosen nontrivial center character;
- Kramers theorem: antiunitary (T^2=-1) forces orthogonal pairing;
- group/information correspondences: uniform coset partitions have entropy
  given by logarithmic subgroup indices;
- integrated photonic qutrit experiments: high-visibility multidimensional
  interference is an established platform primitive.

None of those references supplies the W33-specific conclusions above; those
come from the explicit repo certificates and the new finite calculations.

# Hard evidence boundary

The pass closes algebraic and finite information-theoretic objects.  It does
not yet supply an embedded geometric DEC metric, a physical thermal ensemble
whose equilibrium chooses (q=3), a measured five-level experiment, or a
Hamiltonian realizing the proposed Kramers symmetry.  Those are now sharply
defined next problems rather than hidden assumptions.
