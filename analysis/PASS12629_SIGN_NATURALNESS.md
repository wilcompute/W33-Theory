# Pass 12629: two methods agree that c < 0 is mildly preferred (P(c > 0) ≈ 0.25); the published dark-axion/dark-baryon model is our c < 0 mode; natural completions need a large cyclic structure (N ≳ 20–60)

Claude track. Producer: `analysis/w33_pass12629_sign_naturalness.py`. Test: `tests/test_w33_pass12629.py`. Scripts in `analysis/toe_uv/`: `c_profile.py`, `class_monodromy_patch.py`, `mono_control.py`, `klt_check.py`, `prereg_mono.py` (frozen S6). The monodromy refits (`mono_fit.py`), the c > 0 joint shear refit and the DES-SN5YR shear-held test are running, for an addendum.

**Not a theory of everything.**

## 1. Sign of c: a profile likelihood agrees with Laplace

At each fixed c, the 7 base parameters and c′ are refitted (full Dovekie, growth likelihood):

| c | −2.0 | −1.4 | −0.9 | −0.5 | −0.2 | +0.2 | +0.5 | +0.7 | +1.0 | +1.4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| χ² | 2956.2 | 2277.4 | **2252.8** | 2257.0 | 2260.4 | 2260.0 | 2256.3 | 2255.1 | 2263.4 | 2331.1 |
| c′ | 0.147 | 0.072 | 0.054 | 0.045 | 0.041 | 0.045 | 0.050 | 0.054 | 0.062 | 0.083 |

At c = +2.0, CLASS could not find a solution (unphysical region).

- **P(c > 0) = 0.25 (PCHIP) to 0.30 (linear interpolation).** The Pass 12625 Laplace value is 0.26, so two independent methods agree: c < 0 is mildly preferred (Δχ² = 2.3).
- The two modes are separated by a barrier of 5–8 near c = 0, and |c| ≳ 1.4 is strongly excluded.
- This is a profile, not a marginal: it ignores changes in conditional width along c.

`sign_grid.py` (fixed background) stays withdrawn; see the Pass 12627 addendum.

## 2. The published model that is our c < 0 mode

Khoury, Lin and Trodden (arXiv:2503.16415, 2607.16191) propose a dark axion coupled to dark baryons. Its dark-matter mass falls between equality and recombination and rises through the BAO/SN epoch, giving an apparent phantom crossing. They find Δχ² = −14.5 against ΛCDM with CMB + DESI DR2 + DES-Dovekie.

That is the phenomenology of our c < 0 mode (turnaround at z ≈ 1.6, crossing −1 at z ≈ 0.8), with a comparable gain. **The c < 0 phenomenology is theirs, so it is cited, not claimed.** What these passes add on top is the out-of-sample, shear and sign analysis.

**Its cost, quantified (`klt_check.py`).** Their axion potential is Λ⁴ = ε m_π² f_π² ~ meV⁴, with ε a free suppression, and their coupling uses σ_N/m₀ = 0.01–0.02, taken as a free input. If the dark sector scales like QCD (σ_N ≈ 4 m_π²/m₀, f_π ≈ m₀/10), these two fix:

| m₀ | 100 eV (Tremaine–Gunn) | 1 keV | 1 MeV | 1 GeV |
|---|---:|---:|---:|---:|
| ε needed | 1×10⁻¹⁴ | 1×10⁻¹⁸ | 1×10⁻³⁰ | 1×10⁻⁴² |
| ℤ_N copies at z^N (z = 0.5 / 0.8) | 46 / 144 | 60 / 185 | 99 / 309 | 139 / 433 |

That is stronger than their ε ≲ 10⁻¹² perturbative-control bound. They suggest ℤ_N copies but leave it open. The z^N law is a rough stand-in for a ℤ_N axion potential, and QCD-like scaling is an assumption.

## 3. The monodromy-law patch, and Chat's correction (75f2a7e02), accepted

- **The patch** (`class_monodromy_patch.py`) implements m² ∝ cos(θ₀ + φ/F) with 1/F in scf_parameters[3]. **Control:** at 1/F = 0 it reproduces the fading binary to Δχ² = 2×10⁻⁵ (relative 10⁻⁸; d4c3be9c7 said "to all digits", which overstated four printed decimals).
- **Minimal running.** dc′/dφ = 1/(2F²) + 2c′² ≥ 2c′² for every F, so this law never reduces to constant c′. At fixed other parameters, even F = 100 M_P costs Δχ² = +4.3 (CMB). Refits are running (`mono_fit.py`).
- **Chat's correction:** a *single* mixed cosine Λ⁴[1 − cos(a/f + φ/F)] has a rank-one Hessian, so along the relaxed trough the heavy mass does not depend on the light field. My "b = (M_P/2F) tan θ" mapping (Pass 12627 addendum) came from a coordinate derivative, not a physical mode: **it is an over-read and is withdrawn.** A physical realisation needs multi-cosine potentials (D'Amico, Hamill and Kaloper's three-term form) or another mechanism. Frozen S6 (`prereg_mono.json`) therefore tests only the phenomenological law. Its premise is not a derived property of axion monodromy, and the frozen file stays unedited.
- **A protected mechanism that works (Chat, citing Delaunay, Lee, Yin and Yu, arXiv:2610.30253):** cyclic Dirac partners m_k = M√(1 + ε² + 2ε cos(θ + 2πk/N)) suppress the vacuum harmonic as ε^N. At 16 keV, N ≥ 21 puts the loop curvature below H₀², and populations frozen at decoupling give an effective b up to 0.05. Chat finds W(3,3)'s groups have maximal element order 18 (< 21), while three-qutrit Sp(6,3) holds a ℤ₂₄.

**Convergence.** Both natural routes I can find need a large cyclic copy structure: **N ≳ 21** (cyclic partners, 16 keV) and **N ≳ 46–60** (KLT under QCD-like scaling, keV dark baryons). That matches the generic 0.02 eV one-loop cap of Pass 12627: an unprotected field-dependent mass is unnatural, and protection costs a ℤ_N with N of order tens.

## 4. Two quick negatives

- **Wave dark matter cannot lower S8.** For axion dark matter allowed by Lyman-α (m ≳ 2×10⁻²⁰ eV), the half-mode scale is about 47 Mpc⁻¹ or more (formula recalled), far above the k ≈ 0.1–1 h/Mpc that S8 probes.
- **Swampland cost.** Shiu, Tonioni and Tran (arXiv:2604.09141) combine the axion weak gravity conjecture with DESI and SN and find axion dark energy needs m ≳ 100 H₀. Our fitted dark-energy field has m ≈ √V″ ≈ 1 H₀, so an axion reading of it needs the WGC evaded (by monodromy or similar). This is a stated tension, not a calculation.

## Sources

arXiv:2503.16415, 2607.16191 (Khoury, Lin and Trodden); 2610.30253 (cyclic partners, via Chat); 1605.00996 (DHK); 2604.09141 (Shiu, Tonioni and Tran); 2507.16970 (monodromic dark energy); 2511.23463 (axion–dilaton); Chat's `analysis/2026-11-08_physical_axion_modes_and_cyclic_protection.md`.

## Addendum: shear joint refit of c > 0, and which qutrit symplectic group holds N ≥ 21

**c > 0 joint refit including DES Y3 shear (`des_joint_cpos.py`):**
- Total χ² 2457.70 (c = 0.68, c′ = 0.053, S8 = 0.820), against 2456.22 for c < 0.
- With shear in, c < 0 leads by **1.5**, down from 2.0–2.3 without shear. After refitting, shear itself prefers c > 0 by 0.8 (202.54 against 203.34).
- The corresponding odds give P(c > 0) ≈ 0.3. **The sign remains undetermined.**

**Element orders of Sp(2n, 3)** (`sp_orders.py`, random products of symplectic transvections, symplecticity asserted):

| group | orders found | max found |
|---|---|---:|
| Sp(4,3) (two qutrits, W(3,3)) | 1–6, 8, 9, 10, 12, 18 | **18** (control: matches the repo and Chat 75f2a7e02) |
| Sp(6,3) (three qutrits) | … 20, 24, 26, 28, 30, **36** | **36** |

- Three qutrits host cyclic elements of order 24, 26 (= 3³ − 1), 28 (= 3³ + 1), 30 and 36, all at or above the N ≥ 21 cyclic-partner threshold at 16 keV.
- Sampling shows these orders exist; it does not prove that 36 is the maximum.
- Whether a qutrit Clifford symmetry should act as the partner-protecting ℤ_N is a separate, unbuilt hypothesis. This is a group-theory fact relevant to it, nothing more.
- It extends Chat's ℤ₂₄ construction, which it cites.
