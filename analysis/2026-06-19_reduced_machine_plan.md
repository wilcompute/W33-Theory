# Analysis: Reduced-Scale Machine Plan

**Date:** 2026-06-19  
**Covers:** 11-qubit plan, fewer-qubit fallback, qutrit compression, UTM and photonic topological QC roadmap

---

## 1. Main conclusion

The W33 / Holonet program can be reduced in a principled way. The key is to preserve the **ternary transition structure** and the **carrier-network-clock unity** rather than the full 33-qubit or 40-ray scale. [cite:40]

---

## 2. Best small-scale targets

Two near-term targets emerge:
- **11 qubits** for a compressed heptad / syndrome / control demonstrator
- **2–3 qutrits** for a more faithful native-photonic demonstrator

The 11-qubit route is best for superconducting control hardware. The qutrit route is best for fidelity to the repository’s Bell-qutrit machine architecture. [cite:40]

---

## 3. Universal-machine interpretation

A reduced machine can still support a universal-Turing-machine interpretation if it realizes a repeatable local transition law with finite control and a writable ternary symbol alphabet. In practice, this means a route-update-clock cycle implemented either by repeated circuit rounds (qubits) or a photonic delay loop (qutrits).

---

## 4. Recommended continuation

Immediate next proofs should be:
1. **BT1337** — 11-qubit compressed heptad circuit design
2. **BT1338** — 3-qutrit Bell-route-delay demonstrator
3. **BT1339** — finite-state / tape formalization of the reduced UTM
4. **BT1340** — magic-injection closure on the reduced photonic core

These four items make the reduced-machine program executable.
