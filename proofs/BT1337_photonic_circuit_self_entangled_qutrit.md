# BT1337 — Photonic Circuit for the Self-Entangled Bell Qutrit

**Date:** 2026-06-19  
**Series:** Reduced-Scale Machine Program  
**Predecessor:** BT1336 (Reduced-Machine Architecture)  
**Source:** photonic_holonet.tex §3, §6 (carrier, build sheet)

---

## 1. Core Principle

This is a circuit built from **light, not electrons**. The self-entanglement is not between two photons — it is between the **own degrees of freedom of one photon**: its spatial path ⊗ polarization registers (the Witting carrier in $\mathbb{C}^4$) and its past ⊗ future time-bin registers (the Pauli operator carrier in $\mathbb{C}^9$). Both carry the same W(3,3) geometry.

From the Holonet paper (§3):
> *Entanglement is a relation between tensor factors; nothing requires the factors to be distinct particles. Self-entanglement is entanglement between one photon's own registers.*

The universality theorem (bt825) shows that the three optical elements — tritter $F_3$, phase plate $S$, and delay-conditioned EOM $\mathrm{CX}_{p \to f}$ — generate the **complete two-qutrit Clifford group** of order 51840, exactly.

---

## 2. Physical Components

The full build sheet from the Holonet paper §6 (all catalog optics, no cryostat):

| Component | Role | Substrate meaning |
|-----------|------|------------------|
| Heralded single-photon source | Carrier injection | L0 photon |
| **Polarizing beam splitter (PBS)** | Stage A self-entanglement | Entangles path ⊗ polarization in $\mathbb{C}^4$ |
| **Symmetric 3-port coupler (tritter)** | Qutrit Fourier gate $F_3$ | Generates Clifford frame changes |
| **Three-bin delay ladder** ($0, \tau, 2\tau$) | Defines past/future registers | Creates $\mathbb{C}^9$ time-bin space |
| **Electro-optic modulator (EOM)** | Controlled-X gate $\mathrm{CX}_{p \to f}$ | Couples past to future bin |
| Phase plate / polarization rotator | Phase gate $S$ | Single-qutrit Clifford |
| Recirculation loop at $\arccos(-2/3)$ | Boerdijk–Coxeter drive | Discrete time quasicrystal clock |
| Single-photon detectors | Measurement | Syndrome / outcome readout |

---

## 3. Stage A — Spatial Self-Entanglement (1 element)

A diagonally polarized photon meets the PBS:
$$
\frac{1}{\sqrt{2}}(|H\rangle + |V\rangle) \;\xrightarrow{\text{PBS}}\; \frac{1}{\sqrt{2}}(|H, a\rangle + |V, b\rangle)
$$
Path and polarization are now **maximally entangled within one photon**. This two-qubit $\mathbb{C}^4$ space carries the 40 Witting rays.

This is 1 optical element. No second photon is needed.

---

## 4. Stage B — Temporal Self-Entanglement (2 Clifford gates)

The photon then enters the time-bin arm:

**Step 1 — Tritter (qutrit Fourier gate):**
$$
|0\rangle_p \;\xrightarrow{F_3}\; \frac{1}{\sqrt{3}}\sum_{j=0}^{2} \omega^0|j\rangle_p
$$
where the tritter is a symmetric 3-port coupler implementing $F_3$ on the three time bins.

**Step 2 — Delay ladder defines the bins:**
Three optical paths with delays $0, \tau, 2\tau$ create the ternary past register. The future register is the output arm.

**Step 3 — EOM applies $\mathrm{CX}_{p \to f}$ conditioned on bin index:**
$$
|j\rangle_p|0\rangle_f \;\xrightarrow{\mathrm{CX}_{p \to f}}\; |j\rangle_p|j\rangle_f
$$

**Output — the temporal Bell qutrit:**
$$
|\Omega\rangle = \mathrm{CX}_{p\to f}\,(F_3 \otimes I)|0\rangle_p|0\rangle_f = \frac{1}{\sqrt{3}}\sum_{j=0}^{2}|j\rangle_p|j\rangle_f
$$

The photon is now **entangled with its own future**. This is the canonical Bell state of a qutrit system, realized in time-bin degrees of freedom of one photon.

---

## 5. The Trace-Choi Witness

Inserting any unitary $U$ in the future arm, the recombination visibility is:
$$
V(U) = \frac{|\mathrm{Tr}\,U|}{3}
$$

Key predictions (all exact, all falsifiable):
- $V(F_3) = 1/3$ (tritter itself)
- $V(X) = 0$ (qutrit shift)
- $V(Z) = 0$ (qutrit phase)
- $V(I) = 1$ (identity)

The photon implements the **Choi–Jamiołkowski isomorphism on itself**: it measures quantum channels against its own past. A single measured deviation falsifies the corresponding layer of the architecture.

Witness script: `bt820_self_entanglement_protocol.py`

---

## 6. Full Circuit Schematic (Text)

```
[Single photon source]
        |
        v
   ┌─────────┐        Stage A
   │  PBS    │──── path a (H)
   └─────────┘──── path b (V)
        |
   spatial carrier: |H,a⟩ + |V,b⟩  (C^4, Witting rays)
        |
        v
   ┌─────────┐        Stage B — Step 1
   │ Tritter │  (symmetric 3-port coupler = F_3)
   │  F_3    │
   └─────────┘
        |
        v
   ┌─────────────┐    Stage B — Step 2
   │ Delay ladder│  bins: 0, τ, 2τ
   │ 0 | τ | 2τ  │  → past register |j⟩_p
   └─────────────┘
        |
        v
   ┌─────────┐        Stage B — Step 3
   │   EOM   │  CX_{p→f}: |j⟩_p|0⟩_f → |j⟩_p|j⟩_f
   └─────────┘
        |
        v
   ┌───────────────────────────────────────┐
   │  OUTPUT: Bell qutrit                  │
   │  |Ω⟩ = (1/√3)(|00⟩+|11⟩+|22⟩)_{pf}  │
   │  photon entangled with its own future │
   └───────────────────────────────────────┘
        |
        |── [Insert U in future arm] ──> V(U) = |Tr U|/3
        |
        v
   ┌─────────────┐    Clock / feedback
   │ BC loop     │  rotate arccos(-2/3) per pass
   │ (recirculate│  → discrete time quasicrystal
   │  at angle θ)│
   └─────────────┘
        |
        v
   ┌─────────────┐
   │  Detectors  │  single-photon detectors
   └─────────────┘
```

---

## 7. Why Light and Not Electrons

The W33 theory is native to photons for three structural reasons from the Holonet paper:

1. **The carrier is the geometry.** The 40 Witting rays live in $\mathbb{C}^4$ — exactly the path ⊗ polarization Hilbert space of one photon. Electrons would need an artificial 4-dimensional register.

2. **Qutrit arithmetic is natural in time bins.** Three time bins $\{0, \tau, 2\tau\}$ directly implement $\mathbb{F}_3$ arithmetic. The delay ladder is the ternary register.

3. **The Clifford group is generated by passive optics.** Tritter + phase plate + EOM = full 51840-element Clifford group (bt825). No cryostat, no vacuum chamber. The exotic resource is geometry, not temperature.

And the most important point from the paper:
> *Transport ≡ gate action ≡ routing. One physical process; three descriptions.*

Moving the photon through the mesh **is** applying a gate **is** routing a packet.

---

## 8. The Five Witnesses to Verify in the Lab

From the Holonet paper build sheet (§6), the five most important kill criteria for this circuit:

| Witness | Predicted value | What a failure means |
|---------|----------------|---------------------|
| $V(F_3)$ trace-Choi visibility | $1/3$ exactly | Tritter not implementing $F_3$ |
| $V(X)$, $V(Z)$ visibility | $0$ exactly | EOM phase error |
| KS classical budget | $36/40$ exactly | Contextuality not present |
| Beacon-mesh pair visibility (all 21 pairs) | $1/3$ | Bell qutrit not maximally entangled |
| BC-drive gap census at $n=30$ | exactly 2 gap lengths | Clock not quasicrystalline |

All predicted values are **exact integers or simple fractions** — no fitting parameters.

---

## 9. Connection to the Reduced-Scale Program

This circuit is the **Stage A implementation** of the photonic reduced-machine roadmap (BT1336):

- **2 qutrits**: this circuit — Bell qutrit carrier, trace-Choi witness
- **3 qutrits**: extend with routing register and operator-state duality test
- **4 qutrits + loop**: recursive transition gadget for the UTM interpretation

The 11-qubit superconducting demonstrator (BT1335) **emulates** what this circuit **is natively**.

---

## 10. Immediate Implementation Notes

### Delay choice
Choose $\tau \approx 1\,\mathrm{ns}$ (fiber delay at $c/n \approx 0.2\,\mathrm{m/ns}$, so $\sim 20\,\mathrm{cm}$ per bin). Total path: $\sim 60\,\mathrm{cm}$ of fiber delay ladder.

### EOM bandwidth
The EOM must switch in $< \tau = 1\,\mathrm{ns}$, so bandwidth $> 1\,\mathrm{GHz}$. Standard commercial EOMs meet this.

### Single-photon source
Heralded photon pairs via SPDC (Type-II BBO crystal) are sufficient. Telecom wavelength (1550 nm) is preferred for low fiber loss.

### Tritter
A fused 3×3 fiber coupler with equal splitting ratios implements $F_3$ to within fabrication tolerance. Characterized by measuring $|\langle i | F_3 | j \rangle|^2 = 1/3$ for all $i,j$.

---

**Next:** BT1338 — 3-qutrit Bell-route-delay demonstrator extending this circuit.
