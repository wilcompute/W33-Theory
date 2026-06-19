# BT1336 — Reduced-Machine Architecture for a Universal Photonic Topological Quantum Computer

**Date:** 2026-06-19  
**Series:** Reduced-Scale Machine Program  
**Predecessor:** BT1335 (Small-Scale Execution Plan)

---

## 1. Objective

This BT gives the architecture-level plan for reducing the full Photonic HoloNet into a laboratory-scale machine while preserving the defining claims:

- universal computer,
- universal network,
- clock,
- topological routing fabric,
- ternary native carrier. [cite:40]

The design principle is:

> Preserve **structure first**, scale second.

That means we do not try to preserve all 40 rays / 40 operator classes at once; instead we preserve the minimal carrier-network-clock triangle and then scale it recursively.

---

## 2. Minimal Universal Core

The README identifies the native photonic ingredients as:
- Bell qutrit carrier,
- tritter + phase plate + EOM Clifford generation,
- magic injection for universality. [cite:40]

Therefore the **minimal universal core** is:

1. **Two photonic qutrits** for the Bell carrier,
2. **One programmable tritter**,
3. **One electro-optic modulator (EOM)**,
4. **One phase plate / delay element**,
5. **One heralded magic-state injection channel**.

This is enough for a reduced but still meaningful universal photonic computation stack.

---

## 3. Topological Layer Reduction

The full machine claim uses hypercube charts glued along apartments of the Tits building, with small routing diameter and recursive scaling. [cite:40] At reduced scale, implement this as a **three-layer topological stack**:

### Layer 1 — local cell
A single Bell-qutrit processing node.

### Layer 2 — triangle or heptad patch
A small graph of 3 or 7 cells with phase-consistent couplers.

### Layer 3 — looped apartment
A recirculating photonic delay loop that revisits the same patch under different phase programs.

This simulates topological gluing without requiring the full 540-chart network physically.

---

## 4. 11-Qubit Emulation Layer

If photonic qutrit hardware is unavailable, emulate the reduced machine on 11 qubits.

### Emulation map

- 7 qubits = topological patch / heptad sector
- 3 qubits = route + syndrome controller
- 1 qubit = clock beacon

This emulation preserves:
- finite-control logic,
- route selection,
- parity witness,
- repeated clocked update.

It does **not** preserve the native qutrit geometry exactly, but it preserves the transition algebra needed for a universal-machine demonstrator.

---

## 5. UTM Reduction

To obtain a universal Turing machine interpretation, define each machine cycle as:

1. **Read** current branch symbol,
2. **Route** to the next local topological cell,
3. **Apply** phase-conditioned update,
4. **Inject** magic when non-Clifford branching is required,
5. **Advance** clock.

This 5-step cycle can be repeated by a delay loop in photonics or a repeated circuit round in superconducting hardware.

### Why this is enough

A universal Turing machine only needs:
- finite state,
- writable symbol alphabet,
- repeatable local transition.

The reduced photonic machine supplies all three, with ternary symbols rather than binary ones.

---

## 6. Qutrit Advantage

The qutrit route is preferable because the underlying theory is ternary, not binary. [cite:40] Relative to qubit emulation, qutrit hardware gives:

- more faithful alphabet size,
- cleaner routing semantics,
- simpler representation of branch phases,
- closer alignment with the Bell-carrier universality theorem in the repository. [cite:40]

### Preferred reduced stack

- **2 qutrits**: carrier and Clifford witness
- **3 qutrits**: route / operator-state duality witness
- **4 qutrits + loop**: recursive universal transition gadget

---

## 7. Experimental Program

### Program A — carrier proof
Prepare Bell qutrit, measure visibility and stability.

### Program B — route/clock proof
Use a 3-qutrit or 11-qubit patch to demonstrate deterministic branch update under clocked control.

### Program C — universality proof
Add magic-state injection and show one non-Clifford gate closes universality over the reduced core.

### Program D — topological proof
Use recirculation / delay loops to realize repeated patch traversal, interpreting the loop as a reduced apartment complex.

---

## 8. Engineering Recommendation

If resources are limited, choose one of two tracks:

### Track 1 — superconducting
Build the 11-qubit reduced machine first because control is easier and syndrome statistics are cleaner.

### Track 2 — photonic
Build the 2-qutrit Bell-carrier first because it is the shortest path to the native machine claim. Then extend to 3 qutrits with a delay loop.

Track 2 is more faithful; Track 1 is easier to debug.

---

## 9. Thesis

The universal photonic topological quantum computer does **not** need to appear fully formed at the 40-ray / full-holonet scale. A valid experimental program is:

- prove the carrier,
- prove the local transition gadget,
- prove recursive looped composition,
- then scale.

That is enough to justify a reduced but structurally faithful path from the repository’s Bell-qutrit machine claim to a laboratory universal-machine prototype. [cite:40]

---

**Next:** BT1337 — 11-qubit compressed heptad circuit design.
