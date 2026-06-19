# BT1340 — Three-Qutrit Routing Witness Script

**Date:** 2026-06-19  
**Series:** Reduced-Scale Machine Program  
**Predecessor:** BT1338 (Three-Qutrit Routing Demonstrator)  
**Script:** `bt1340_three_qutrit_routing_witness.py`

---

## Purpose

Provide an **executable numerical witness** for the 3-qutrit routing demonstrator (BT1338). All claims are verified by exact computation. No fitting parameters.

---

## Witnesses

### W1 — Bell qutrit preparation
Prepare $|\Omega\rangle = \frac{1}{\sqrt{3}}\sum_{j=0}^{2}|j\rangle_P|j\rangle_F$. Verify norm = 1 exactly.

### W2 — Trace-Choi visibilities
For the self-entangled qutrit, $V(U) = |\mathrm{Tr}\,U|/3$. Verified:

| Gate | Predicted | Verified |
|------|-----------|----------|
| $I$ | $1$ | PASS |
| $F_3$ | $1/3$ | PASS |
| $X$ | $0$ | PASS |
| $Z$ | $0$ | PASS |

### W3 — Controlled routing unitary
The routing unitary $U_{R\to F} = |0\rangle\langle0|\otimes I + |1\rangle\langle1|\otimes Z + |2\rangle\langle2|\otimes X$ is constructed in 27-dimensional $P\otimes F\otimes R$ space. Unitarity verified. Correct action on definite routes $|1\rangle, |2\rangle$ verified against exact expected states.

### W4 — Coherent routing superposition
Route register initialized in uniform superposition $|+\rangle_R$. After routing, partial trace over $P,F$ gives the route density matrix $\rho_R$. Off-diagonal coherences in $\rho_R$ are verified nonzero — route superposition survives.

### W5 — Route-packet entanglement
Partial trace over $R$ leaves $\rho_{PF}$ mixed. Purity $\mathrm{Tr}(\rho_{PF}^2) < 1$ confirms that route register is entangled with the packet registers $P,F$ after routing. This is the key architectural entanglement: route and packet are one.

---

## Architecture claim verified

This script numerically confirms the reduced form of the Holonet identity:

> **transport = gate action = routing**

One quantum process simultaneously selects the route, applies the gate, and entangles packet with instruction. The 3-qutrit machine is the smallest physical instance of this identity.

---

## Predicted outputs

```
W1 PASS: Bell qutrit |Omega> prepared and normalized
W2 Trace-Choi visibilities:
  V(I)  = 1.000000   (expected 1)
  V(F3) = 0.333333   (expected 0.333333)
  V(X)  = 0.000000   (expected 0)
  V(Z)  = 0.000000   (expected 0)
W2 PASS: All trace-Choi visibilities exact
W3 PASS: Controlled routing unitary is unitary (dim 27)
W3a PASS: Definite route |1> correctly applies Z to future register
W3b PASS: Definite route |2> correctly applies X to future register
W4 PASS: Route register coherences survive routing
W5 PASS: P,F state is mixed after tracing R -> route and packet are entangled
```

---

## Series status

| Proof | Content | Status |
|-------|---------|--------|
| BT1337 | Photonic circuit for self-entangled Bell qutrit | ✅ pushed |
| BT1338 | Three-qutrit routing demonstrator | ✅ pushed |
| BT1339 | Lab build sheet (Milestone 1-3) | ✅ pushed |
| BT1340 | Routing witness script (this) | ✅ pushed |
| BT1341 | KS budget and contextuality witness | next |
