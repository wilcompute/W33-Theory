# 2026-09-23 — corrected Weil lift, all-q Hodge spectrum, E8 graded Hamiltonians, and FI admission

This pass both **repairs** the preceding representation-physics certificate and
executes the next five independent attacks plus three additional physics probes.

Primary executable:
- `analysis/w33_20260923_corrected_weil_hodge_e6_physics.py`

Exact GAP witness:
- `analysis/w33_20260923_corrected_weil6_e6_extension.g`

## 1. Canonical retained-phase qutrit Weil lift

The previous pass independently normalized every Clifford generator into
(SU(3)).  That operation is harmless projectively but not for a retained-phase
finite group: taking cube roots of determinant phases introduces ninth roots of
unity and changes the central extension.

A canonical finite Weil section is
[
X,quad Z,quad e^{ipi/6}F_3,quad
N=operatorname{diag}(1,omega,omega),
]
up to the physical scalar (C_3).  It generates the expected 648-element
retained-phase Clifford group.  Coefficient conjugation gives a 1296-element
completion with exact element-order census
[
1^1,2^{117},3^{98},4^{54},6^{450},8^{324},9^{144},12^{108}.
]
This matches the independently certified Pass-408 (H_{27}:GL(2,3)) census;
there are **no order-18 elements**.

The corrected 6D character is irreducible real, Frobenius--Schur (+1), and
takes only
[
{-3,-2,-1,0,1,2,3,6}.
]
For (M=A+isqrt3B), the rational realification
[
R(M)=egin{pmatrix}A&-B\3B&Aend{pmatrix}
]
preserves
[
Q_6=operatorname{diag}(3,3,3,1,1,1).
]
GAP constructs this rational matrix group exactly, verifies order 1296,
trivial center, derived subgroup 648, and an explicit abstract isomorphism to
(mathrm{TransitiveGroup}(27,294)).

The former conductor-9 cubic traces came from the bad phase section.  They are
not characters of the W33 point stabilizer.

## 2. Full (Z_3)-graded antiunitary Hamiltonian normal form

For the (86oplus81oplus81) E8 grading, impose
[
[H,C]=0,qquad HT=TH,qquad T^2=C^r,quad r=1,2.
]
After unitary basis choices,
[
oxed{H=H_0oplus H_+oplusoverline{H_+}},
]
with
[
H_0inoperatorname{Sym}_{86}(mathbb R),qquad
H_+inoperatorname{Herm}_{81}(mathbb C).
]
Hence
[
oxed{P_H(E)=P_0(E),P_+(E)^2}.
]
The generic spectrum has 86 neutral singlets and 81 forced matter doublets.
The real parameter count falls from
[
86^2+2(81^2)=20518
]
under (C) alone to
[
rac{86cdot87}{2}+81^2=oxed{10302}
]
under (C) and (T).  A full (248	imes248) seeded numerical replay closes
all semilinear identities to below (10^{-13}).

## 3. Complete circumcentric Hodge spectrum for (W(q,q))

The old (b_1=q^4) theorem is prior repo work
(`analysis/w33_ledger_allq_h2.py`).  The new result is the **weighted
circumcentric spectrum**.

Let
[
v=(q+1)(q^2+1),qquad
lambda_*=rac{2(q^2+1)}{(q+1)a^2},qquad
lambda_n=rac{2(q+1)n^2}{a^2}.
]
Then
[
L_0=0^1+lambda_*^{,q(q+1)^2/2}
+lambda_1^{,q(q^2+1)/2},
]
[
L_1=0^{q^4}+lambda_*^{,q(q+1)^2/2}
+lambda_1^{,q(q^2+1)/2}
+lambda_2^{,vinom q2},
]
and for (2le k<q),
[
L_k=lambda_k^{,vinom qk}
+lambda_{k+1}^{,vinom q{k+1}},
qquad
L_q=lambda_q^v.
]
Thus the (n^2) ladder is universal:
[
oxed{lambda_n=rac{2(q+1)}{a^2}n^2,quad 1le nle q}.
]
So q=3 is **not** selected by the square ladder.  It is simply the three-rung
member.  Direct symplectic-graph replays at q=2,3,5,7 reproduce the required
SRG spectra.  At q=3 and (a^2=5/3),
[
lambda_*=3,quad
(lambda_1,lambda_2,lambda_3)=
left(rac{24}{5},rac{96}{5},rac{216}{5}ight).
]

## 4. Fail-closed FI reference-arm Monte Carlo

The new calibration model includes Poisson plus/minus counts, 10-ns dark gates,
a 10-s dark reference, (0.3^circ) EOM jitter, binomial efficiency/loss
calibration, and three-sigma confidence gates.

Admission requires
[
V-3sigma_Vge0.98093363146,quad
|delta|+3sigma_deltale2.5^circ,
]
plus efficiency (>0.90), loss (<0.05), and dark rate (<100) Hz.

With 80,000 detected signal events per analyzer quadrature and 20,000 trials
per case:
- good device ((V=.99,delta=.5^circ,eta=.95,L=.02,D=20,Hz)):
  **0.9969 accepted**;
- all five deliberately bad devices: **0 accepted**;
- five near-boundary bad devices: acceptance between **0 and 0.00045**.

At nominal good efficiency/loss the four-quadrature packet needs 343,720 launch
opportunities.  With 4,320 candidate opportunities per supercycle,
[
oxed{80	ext{ supercycles}}
]
is the conservative schedule.  The old two-supercycle number was only a
phase-Fisher lower bound and did not certify the full admission gate.

## 5. Phase-field audit

The corrected finite Clifford section lives in the already-established
(mathbb Q(zeta_{12})) framework and its real 6D character descends to
(mathbb Q).  Independent SU-normalization instead produces 216 order-18
elements and the spurious conductor-9 cubic trace field.  The repository's
older (zeta_9) Galois phase-cycle remains valid as a separate construction;
it is not selected by this point-stabilizer representation.

## Three additional physics probes

### A. Exact local-to-global (E_6) extension and Weil-phase triality

[
W(E_6)cong U_4(2).2
]
has a 40-point action whose stabilizer is the extraspecial
(3_+^{1+2}:GL(2,3)) group.  GAP verifies that
(mathrm{TransitiveGroup}(27,294)) is isomorphic to this stabilizer, while
the second 40-point action has the nonisomorphic (3^3:(C_2	imes S_4))
stabilizer.

The stabilizer automorphism group has order 3888.  Since its center is trivial,
[
oxed{operatorname{Out}(G)cong C_3}.
]
This actual outer (C_3) cycles all three rational 6D irreducible characters.
The restrictions of both 6D (W(E_6)) characters lie in that orbit.
Consequently every corrected qutrit 6D carrier becomes the restriction of a
global (W(E_6)) 6D representation after precomposition by an actual outer
automorphism of the local point stabilizer.

This is an exact representation bridge, but it does not canonically choose one
of the three phase frames.

### B. All-q finite McKean--Singer identity

Every positive (lambda_*) or (lambda_n) band occurs in adjacent cochain
degrees with equal multiplicity and opposite parity. Therefore
[
oxed{operatorname{Str}(e^{-tL})=1-q^4}
]
for every (t).  The q=3 value is (-80).

### C. Symmetry-protected (1+2) crossings

A (C)-preserving perturbation cannot mix a neutral grade-0 state with the
paired matter grades.  When one neutral eigenvalue meets one matter-doublet
eigenvalue, the crossing is therefore a protected
[
oxed{1+2	ext{ triple crossing}}
]
as long as the grading and antiunitary symmetry remain exact.

## Evidence boundary

These are finite algebra, finite DEC, and simulation results.  They do not by
themselves derive a continuum action, physical masses, observed particle
multiplets, or laboratory performance.
