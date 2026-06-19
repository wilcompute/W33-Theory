# BT1338 — Three-Qutrit Routing Demonstrator

**Date:** 2026-06-19  
**Series:** Reduced-Scale Machine Program  
**Predecessor:** BT1337 (Photonic self-entangled Bell qutrit)  

---

## 1. Objective

Extend the BT1337 single-photon Bell-qutrit carrier into a **3-qutrit routing demonstrator** that realizes the first nontrivial identity of the Holonet thesis:

> **transport = gate action = routing**

The 3 qutrits are:

- **P** = past register
- **F** = future register
- **R** = route register

The first two are the Bell pair already constructed in BT1337:
\[
|\Omega\rangle_{PF} = \frac{1}{\sqrt{3}}\sum_{j=0}^2 |j\rangle_P |j\rangle_F
\]

The third register $R$ selects which local routing move is enacted. In the reduced demonstrator, it does not yet realize the full 540-chart atlas; instead it realizes the **minimal ternary route alphabet** that is the seed of the atlas grammar.

---

## 2. Minimal Routing Alphabet

A full chart in the Holonet has local XOR moves in a cube $Q_3$, but the reduced 3-qutrit machine compresses this to the ternary alphabet:

\[
R \in \{0,1,2\}
\]

with interpretation:

- **0** = hold / identity route
- **1** = phase route $Z$
- **2** = shift route $X$

So the controlled routing unitary is:
\[
U_{R\to F} = |0\rangle\langle0|_R \otimes I_F
+ |1\rangle\langle1|_R \otimes Z_F
+ |2\rangle\langle2|_R \otimes X_F
\]

This is the smallest nontrivial qutrit router: one qutrit chooses which Clifford action is applied to the future arm.

---

## 3. Physical Realization

### Registers

- **Past register P**: time-bin qutrit from delay ladder A
- **Future register F**: time-bin qutrit from delay ladder B
- **Route register R**: second path-encoded or polarization-multiplexed qutrit selector

### Optical implementation

1. Prepare BT1337 Bell qutrit on $(P,F)$ using tritter + delay ladder + EOM.
2. Prepare route qutrit $R$ using a second tritter:
   \[
   |r\rangle = \alpha|0\rangle + \beta|1\rangle + \gamma|2\rangle
   \]
3. Implement controlled routing with three conditional arms:
   - route 0 arm: apply $I$
   - route 1 arm: apply qutrit phase plate $Z$
   - route 2 arm: apply qutrit shift element $X$
4. Recombine coherently and measure joint output on $(P,F,R)$.

This realizes a qutrit-controlled qutrit Clifford router.

---

## 4. Output State

Given a general route superposition,
\[
|r\rangle_R = \alpha|0\rangle + \beta|1\rangle + \gamma|2\rangle
\]
and Bell state $|\Omega\rangle_{PF}$, the routed state is:
\[
|\Psi\rangle_{RPF} = \frac{1}{\sqrt{3}}\sum_{k=0}^{2}
\big(
\alpha |0\rangle_R |k\rangle_P |k\rangle_F
+ \beta |1\rangle_R |k\rangle_P Z|k\rangle_F
+ \gamma |2\rangle_R |k\rangle_P X|k\rangle_F
\big)
\]

This is the first true **routing superposition**: one photon coherently exploring multiple route instructions.

---

## 5. Why This Matters

BT1337 proved: one photon can self-entangle into a Bell qutrit.  
BT1338 adds the missing third register: **instruction / route selection**.

This is the minimal point at which the Holonet identity becomes experimentally visible:

- If $R=0$, the packet is held.
- If $R=1$, the packet acquires a phase route.
- If $R=2$, the packet is shifted.
- In superposition, the route itself is coherent.

That is the seed of:

- packet routing,
- gate application,
- instruction decoding.

All three are now one photonic process.

---

## 6. Experimental Witnesses

### Witness A — Branch visibility
Measure coherence between the three route branches. If routing is coherent, off-diagonal terms in $R$ survive recombination.

### Witness B — Conditional trace-Choi
For each route branch, the future-arm visibility obeys:
- $V(I)=1$
- $V(Z)=0$
- $V(X)=0$

### Witness C — Controlled-routing tomography
Reconstruct the process matrix of $U_{R\to F}$. It should equal:
\[
|0\rangle\langle0|\otimes I + |1\rangle\langle1|\otimes Z + |2\rangle\langle2|\otimes X
\]

### Witness D — Route-packet entanglement
Verify that tracing out $R$ decoheres the future branch statistics, proving route and packet are entangled.

---

## 7. Lab Build Sheet

### Additional components beyond BT1337

| Component | Role |
|-----------|------|
| Second tritter | Prepare route qutrit |
| Conditional phase arm | Implements $Z$ branch |
| Conditional shift arm | Implements $X$ branch |
| 3-arm coherent recombiner | Restores route superposition |
| Additional detectors | Joint tomography on $(R,P,F)$ |

### Total reduced demonstrator stack

- 1 heralded photon source
- 1 PBS
- 2 tritters
- 2 delay ladders
- 1 EOM for $\mathrm{CX}_{P\to F}$
- 1 route-controlled arm network
- single-photon detectors

---

## 8. Architecture Meaning

This 3-qutrit machine is the smallest reduced device that contains all three architectural nouns:

- **state** ($P,F$ Bell carrier)
- **operator** ($X,Z$ branch action)
- **route** ($R$ branch selector)

It therefore realizes, in reduced form, the operator-operand duality of the Holonet paper.

The full 40-point W(3,3) substrate is not yet built physically here, but the reduced machine already demonstrates the architectural law that the full geometry globalizes.

---

## 9. Next Step

**BT1339** should build the **lab paper / engineering build sheet** for BT1337+BT1338 as a single experimental proposal suitable for a photonics lab.
