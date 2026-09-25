# Pass 10952 — complete-positivity firewall for the order-eight clock

Producer: `analysis/w33_pass10952_clock_complete_positivity_firewall.py`

Certificate: `data/w33_pass10952_clock_complete_positivity_firewall.json`

Regression: `tests/test_w33_pass10952_clock_complete_positivity_firewall.py`

## Why this pass exists

Pass 10951 found a specific determinant-odd element (g\in GL(2,3)) of order eight whose fourth power is the central (-I). Older Pass 5730 already proved the general finite-qutrit rule

```text
det = +1  -> unitary Clifford,
det = -1  -> antiunitary extended Clifford.
```

The new question is operational: can **one clock tick** be a deterministic physical quantum operation on an unknown qutrit?
## Exact qutrit lift

Let (J=\mathrm{diag}(1,-1)), represented over (\mathbb F_3) by `diag(1,2)`. Since (\det g=-1),

```text
S = g J in SL(2,3).
```

The verifier constructs all 24 qutrit Clifford representatives of (SL(2,3)) from Fourier and quadratic-phase generators and obtains a unitary (U_S). The antiunitary

```text
A = U_S K
```

with (K) computational-basis complex conjugation implements the Pass-10951 phase-space action of (g) on both qutrit Weyl generators, with residual below (3\times10^{-15}).

This is objectwise: it is the particular clock tick, not merely the statement that some determinant-odd Clifford exists.
## The complete-positivity firewall

On density operators, antiunitary conjugation agrees with the complex-linear map

```text
Theta(rho) = U_S rho^T U_S^dagger.
```

Its Choi operator is unitarily equivalent to the qutrit swap operator. The executable obtains exactly the numerical spectrum

```text
-1, -1, -1, +1, +1, +1, +1, +1, +1,
```

so its inertia is

```text
(positive, negative, zero) = (6,3,0).
```

Therefore a single tick is positive and trace preserving but **not completely positive**. Acting on half of a maximally entangled qutrit pair gives eigenvalues (-1/3) three times and (+1/3) six times, so the failure is exposed by a reference system.
This is the operational meaning of the obstruction: a deterministic local quantum-operation slot must be completely positive on arbitrary reference extensions. One algebraic tick cannot occupy such a slot on the bare three-dimensional qutrit.

## Exact eight-power CP parity

The verifier checks all eight powers of the clock:

```text
n even: det(g^n)=+1, unitary Clifford, Choi inertia (1,0,8);
n odd : det(g^n)=-1, transpose-conjugated, Choi inertia (6,3,0).
```

So the (Z_8) algebraic clock carries an exact (\mathbb Z_2) **complete-positivity grading**.

The square (A^2=V=U_SU_S^*) is unitary. Its channel has projective order four, giving a physically admissible stroboscopic clock:

```text
one physical step = two algebraic ticks,
physical channel group = C4.
```
## Four ticks: same abstract -I, different representation

Pass 10951 identified

```text
g^4 = -I in GL(2,3)
```

and mapped that central element to quaternion (-1) in (2T\subset\mathrm{Spin}(3)), hence to the spin (2\pi) sign.

The qutrit Clifford representation is different. The four-tick unitary (V^2) has phase-space action (-I), but its eigenvalues are (1,-1,-1) up to numerical roundoff and

```text
|tr(V^2)| / 3 = 1/3.
```

It is therefore **not scalar**. On the qutrit it is a parity-type Clifford, not the scalar spin sign.

This repairs a possible over-reading of Pass 10951: the matter-parity weld is a statement about the central character in the Spin representation, not equality with the 3D qutrit four-tick unitary.
## Doubled conjugate-sector escape

There is a clean linearization if the carrier is enlarged. On

```text
H_3 direct-sum conjugate(H_3)
```

define

```text
D = [[0,U_S],[U_S^*,0]].
```

The verifier proves (D) is unitary to machine precision, has projective order eight, and

```text
D^2 = diag(V,V^*).
```

Thus the full odd/even (Z_8) clock can be implemented linearly only after retaining a conjugate sector. This is consistent with earlier repo realification/sector-swap results, but the new contribution is the explicit lift of the Pass-10951 clock itself.
## Process interpretation and external anchors

A process-tensor experiment permits completely positive interventions in its operation slots. Therefore Pass 10952 gives two honest architectures:

1. **bare qutrit:** coarse-grain to two algebraic ticks per physical unitary step;
2. **doubled carrier:** keep qutrit plus conjugate-qutrit sectors and realize the full order-eight clock unitarily.

Appleby's extended-Clifford construction supplies the standard unitary/antiunitary (\det=\pm1) dictionary (arXiv:0909.5233). Jiang, Wang and Wang, *Quantum* **5**, 600 (2021), emphasize that CPTP maps are the physically implementable deterministic quantum operations, while positive non-CP maps are not. Pollock et al.'s process-tensor framework supplies the intervention language already used elsewhere in this repository.

## Boundary

This is a quantum-channel and representation theorem. It does **not** prove that the algebraic clock is physical time, that antiunitarity is a thermodynamic arrow, that the doubled sector is literally past/future, or that the qutrit parity operator is the Standard-Model matter-parity operator.
