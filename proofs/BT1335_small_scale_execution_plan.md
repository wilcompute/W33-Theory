# BT1335 — Small-Scale Execution Plan: 11 Qubits, Fewer Qubits, and Qutrit Compression

**Date:** 2026-06-19  
**Series:** Post-HoloNet Validation  
**Predecessor:** BT1334 (Superconducting Pulse Schedule)

---

## 1. Goal

The full W33 machine uses 33 physical qubits (or a native qutrit-photonic carrier in the Holonet presentation). This BT asks a practical question:

> What is the smallest experimental system that can still demonstrate the characteristic W33 / HoloNet structure?

We give a staged answer:

1. **11 qubits** can realize a faithful *compressed witness* of the routing / syndrome / universality logic.
2. **7–9 qubits** can realize partial witnesses.
3. **Native qutrit hardware** can compress the same logic further because the theory is intrinsically ternary. [cite:40]

---

## 2. Why 11 Qubits Is Natural

W33 is ternary at its core: the substrate uses the primitive $q=3$, and the machine paper treats the carrier as a Bell qutrit with tritter + phase plate + EOM as the native gate set. [cite:40] An 11-qubit reduction is therefore not expected to preserve full distance-9 fault tolerance; instead it should preserve the **signature algebra**:

- ternary branching,
- heptad / Fano incidence,
- odd-weight syndrome witness,
- small universal gate skeleton.

The number 11 is the smallest practical register size that still allows:
- 7 data-like degrees of freedom for a heptad witness,
- 3 ancilla-like controls for syndrome or routing,
- 1 logical / clock / beacon qubit.

So 11 qubits is the right target for a **demonstrator**, not the final fault-tolerant machine.

---

## 3. 11-Qubit Architecture

### Register split

Use:
- **7 data qubits**: encode the heptad / Fano-point sector
- **3 ancilla qubits**: parity, syndrome, or route-selector register
- **1 control qubit**: logical phase beacon / clock witness

Total:
$$
7 + 3 + 1 = 11.
$$

### What this can show

This 11-qubit device can test four things:

1. **Heptad routing witness**  
   Map the 7 Fano points to 7 data qubits and implement adjacency-conditioned hopping.

2. **Odd syndrome witness**  
   Engineer a compressed stabiliser family whose single-fault signatures produce odd syndrome weights {1,3} in the compressed model, mirroring the full W33 odd-weight discriminator. [cite:40]

3. **Universal gate skeleton**  
   Implement a reduced Clifford-plus-injection demonstration: entangle, route, phase-correct, inject one non-Clifford resource.

4. **Clock / network unity**  
   Use the control qubit as a phase beacon, showing the same register acts as state, operator selector, and timing source in miniature.

---

## 4. 9-Qubit and 7-Qubit Fallbacks

### 9 qubits

A 9-qubit layout can support:
- 7 heptad data qubits
- 2 ancilla qubits

This is enough for:
- Fano-incidence routing witness
- compressed parity checks
- limited phase correction

But it is too small for a clean simultaneous demonstration of routing, syndrome, and logical beaconing.

### 7 qubits

A 7-qubit layout is the absolute minimum for a **pure heptad witness**:
- one qubit per Fano point
- edges encoded by two-qubit couplings

This can demonstrate incidence and routing motifs, but not a serious error-correction or universality story.

---

## 5. Qutrit Compression

Because the repository’s machine layer is natively ternary — Bell qutrit carrier, tritter optics, and full Clifford generation in qutrit language — a qutrit platform is more natural than a qubit-only reduction. [cite:40]

### Compression idea

Represent one ternary branch with one qutrit instead of two qubits. Then:
- **3 qutrits** encode $3^3 = 27$ branch states,
- **4 qutrits** encode $3^4 = 81$ states,
- a **Bell-qutrit pair** already carries the native substrate witness discussed in the Holonet paper. [cite:40]

So the preferred small-scale path is:

1. **2 qutrits**: carrier / Bell witness
2. **3 qutrits**: routing and operator-state duality witness
3. **4 qutrits**: compressed memory / branching demonstrator

This is conceptually closer to the claimed universal photonic topological quantum computer than any 7–11 qubit emulation.

---

## 6. Universal Turing Machine Interpretation

The README states the machine claim directly: a single self-entangled photon acts as universal computer, universal network, and clock. [cite:40] To connect the 11-qubit or qutrit demonstrator to a **universal Turing machine** interpretation, we only need three ingredients:

1. **Finite control** — the ancilla / control subsystem
2. **Tape alphabet** — ternary branch states or qutrit symbols
3. **Transition rule** — routing + phase + correction update law

### 11-qubit UTM analogue

- Data heptad = local tape window
- 3 ancilla = machine state register
- control qubit = clock / head parity / branch marker

This is not an infinite Turing tape, but it is a **universal transition gadget** that can be tiled recursively.

### Qutrit UTM analogue

A qutrit implementation is cleaner:
- one qutrit = one ternary tape cell,
- entangled qutrit pair = transition and read/write witness,
- photonic delay loop = reusable clocked tape advance.

This is much closer to a realistic substrate-level UTM.

---

## 7. Universal Photonic Topological Quantum Computer Path

The README already identifies the photonic holonet stack as:
- one Bell-qutrit carrier,
- native Clifford generation by tritter + phase plate + EOM,
- magic injection for universality,
- topological/gluing structure through the Tits-building / apartment network. [cite:40]

A practical staged roadmap is therefore:

### Stage A — 2 qutrits
Prove carrier preparation and Bell-qutrit stability.

### Stage B — 3 qutrits or 11 qubits
Demonstrate compressed routing + syndrome witness + finite-control update.

### Stage C — 4 qutrits / photonic loop
Show repeated clocked transitions with phase-coherent routing.

### Stage D — full photonic topological machine
Embed the transition gadget into the apartment / hypercube / holonet geometry claimed in the machine paper. [cite:40]

---

## 8. Recommendation

**Best near-term laboratory target:**
- If using superconducting hardware: build the **11-qubit demonstrator**.
- If using photonics: skip qubit emulation and build a **2–3 qutrit demonstrator** first.

The 11-qubit machine is best for control and syndrome engineering; the qutrit machine is best for staying faithful to the ternary W33 substrate.

---

## 9. Deliverables

Immediate deliverables for the reduced-scale program:

1. 11-qubit compressed stabiliser / routing design
2. 9-qubit and 7-qubit fallback witness circuits
3. 2-qutrit Bell-carrier experiment
4. 3-qutrit routing / operator-state duality experiment
5. Recursive transition-gadget note linking the reduced machine to a universal Turing machine model

---

**Next:** BT1336 — Reduced-machine architecture for universal photonic topological computation.
