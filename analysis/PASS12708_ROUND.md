# Pass 12708: the d-wave suppression behind B's revision reproduces (Γ ∝ p⁵); a scheme-clean MS-bar top mass leaves even vacuum stability open; the M_VL threshold passes two independent checks; ATLAS's κ = √2 sin θ_L by width consistency; B′ is untested by any search; plus a ternary/simplex note

Claude track. Follows Pass 12707. **Not a theory of everything.**
- Scripts: `toe_pass12708_round.py` (≈1 min) and `ternary_radix_simplex_note.py`.
- Certificates: `data/toe_pass12708_round.json` and `data/ternary_radix_simplex_note.json`.
- Tests: `tests/test_toe_pass12708.py`, 5 tests passing.

## (1) The d-wave claim of 2610.01825, checked independently
Pass 12707's revision of B rests on a single-author preprint, so its central claim was reproduced here. Setup:
- A massive spin-1 vertex Y = (ε₁·ε₂)((p₁−p₂)·ε₃) + cyclic, with all three helicities and explicit 4-vectors.
- Its double copy for spin 2. Product polarisations span every helicity, because the amplitude is bilinear.
- Decay m₁ → m₂ + m₃ near threshold, Q = 10⁻⁷–10⁻².

| vertex | d ln\|A\|/d ln p | width ∝ |
|---|---|---|
| YM-like | 1.002 | p³ |
| spin-2 double copy | **2.003** | **p⁵** (d-wave, as claimed) |
| non-derivative s-wave contact | 0.000 | p |

**Why:** at threshold every momentum points along the rest-frame time axis and every polarisation is spatial, so each p·ε vanishes.

**Scope:** this confirms the kinematic suppression given the paper's vertex form. It does not check the paper's warped-geometry overlap integrals or its cascade simulation.

## (2) A short-distance top mass
The MS-bar mass extracted from σ_tt̄ is m̄_t(m̄_t) = 162.5 (+2.1, −1.5) GeV (PDG). Converting at four loops with α_s⁽⁶⁾(m̄_t) = 0.1086 (Marquard et al.):

| m̄_t | series terms (GeV) | pole | μ₀ |
|---|---|---|---|
| 162.5 | 7.49, 1.60, 0.49, **0.19** | 172.27 | 1.8×10¹¹ |
| 161.0 | — | 170.70 | **∞ (λ never crosses zero: stable vacuum)** |
| 164.6 | — | 174.47 | 4.8×10⁸ |

- **Today:** the scheme-clean route is too imprecise even to decide whether λ turns negative.
- **Renormalon size:** the four-loop term (0.19 GeV) is the size of the pole renormalon. This is consistent with the 0.25–0.5 GeV scheme error used in Pass 12707.
- **FCC-ee:** its threshold scan measures a short-distance mass to about 0.04 GeV with a 0.006 GeV conversion error, which removes the ambiguity.

## (3) The Pass 12707 threshold, checked
- **(a) Numeric CW potential:** fitting the exact two-state Coleman–Weinberg potential reproduces the h⁴ coefficient −(5/6)N_c y′⁴/(4·16π²) to a ratio of **1.00000**.
- **(b) Passarino–Veltman route for Z:** 2k·(k+p) = D₁ + D₂ + 2m² − p², checked numerically. Then Π′(0) ∝ −B₀(0) + 2m²B₀′(0), with 2m²B₀′(0;m,m) = **1/3**. So Z_kin(μ = M) = 1 − N_c y′²K/3, the same as Pass 12707's Feynman-parameter derivation.
- **(c) Gauge couplings:** heavy-fermion gauge thresholds vanish in MS-bar at μ = M. The +0.006 in y′ moves α_i⁻¹ by only 3.5×10⁻⁴ through two-loop Yukawa terms, so the hybrid's δ = +0.26 is unchanged.

## (4) κ vs sin θ_L (singlet T), by width consistency
Γ/M = g² s² M²/(32π m_W²) in the Goldstone limit, with Γ ≈ 2Γ_W.

| map | Γ/M at κ = 0.53, 2.3 TeV (ATLAS: inside its <50% region) | Γ/M at κ = 0.25, 1.5 TeV (ATLAS: ~5%) | |
|---|---|---|---|
| κ = sin θ | 0.97 | 0.092 | inconsistent |
| **κ = √2 sin θ** | **0.49** | **0.046** | **consistent** |

- **Coupling map settled:** this replaces the unverified assumption in Pass 12707. Roy et al. (2003.00640) do not define κ; it comes from Buchkremer et al. and Fuks–Shao.
- **Result for B:** θ_t ≤ 0.18 means κ ≤ 0.25 and Γ/M ≤ 5% at 1.5 TeV. Current single-T searches do not reach B above 1.5 TeV.
- **HL-LHC:** CMS FTR-22-002 projects a T mass exclusion of 1.75 TeV and 5σ discovery to 1.44 TeV. Neither beats B's 1.74–1.9 TeV floor.

## (5) B′ = dark dimension + top partner + B-mesogenesis
- **Requirement:** B-mesogenesis needs BR(B → ψ + baryon + X) ≳ 10⁻⁴ (2101.02706).
- **No dedicated search exists (2026-11).** The ALEPH recast gives BR ≲ 10⁻⁴–10⁻². BaBar's B⁻ → Λ̄p̄νν̄ < 3×10⁻⁵ is a related mode, not the ψ channel.
- **B′ is therefore untested.** Dedicated Belle II and LHCb searches at the 10⁻⁵–10⁻⁴ level would decide it.

## Ternary computing and the triangle idea (requested note)

**Radix economy (computed).**
- The cost r × (digits needed) ∝ r/ln r is minimised at r = e.
- Base 3 gives 2.7307 against 2.8854 for base 2, so base 3 is **5.4% cheaper**; base 10 gives 4.34.
- This is the real content of "3 is the integer closest to e". It assumes the cost of a digit grows in proportion to its number of states. Hardware breaks that assumption: a binary transistor is either fully on or fully off, so its noise margin is large, while three voltage levels squeeze it.

**Balanced ternary {−, 0, +}.**
- Example: 2026 = `+0-+000+`.
- Negation flips every trit, so no sign bit is needed and rounding is truncation.
- Setun (Moscow State University, 1958) used it.

**Ternary hardware and AI today (2025–26).**
- In March 2026 a 24-trit balanced-ternary RISC CPU ran on an FPGA at 20 MHz. It encodes each trit with binary gates.
- Carbon-nanotube (CNTFET) ternary cells and EDA tools are research-stage.
- Reports of a Huawei "ternary logic chip" cite no primary source.
- The strongest practical use is **ternary neural-network weights {−1, 0, +1}** (for example BitNet b1.58), which carry log₂3 = 1.585 bits each and replace multiplications with additions.
- In quantum computing the ternary unit is the **qutrit**.

**Triangles → any shape (computed).**
- **Circle from triangles:** a fan of n triangles converges to the circle's perimeter and area, with error ∝ 1/n². At 10 000 triangles both agree with 2π and π to seven figures.
- **Where curvature lives:** on a triangulated surface, curvature sits at the vertices as *deficit angles*. For the icosahedron and three levels of geodesic refinement, the total deficit is **exactly 4π every time**, the discrete Gauss–Bonnet theorem: χ = 2 for the sphere. The largest single deficit shrinks from 1.05 to 0.02 rad, as the smooth limit requires.
- **This is Regge calculus.** Causal dynamical triangulations (CDT) build quantum spacetime from 4-simplices and is an active quantum-gravity programme.

**Corrections to the idea as stated.**
- **2D triangles build surfaces, not volumes.** Three dimensions need tetrahedra (3-simplices), and d dimensions need d-simplices. The triangle is the second member of that family, not a universal brick.
- **Not every shape can be triangulated.** Smooth manifolds always can (Cairns–Whitehead), but the 4D E₈ manifold cannot. Manolescu (2013) proved non-triangulable manifolds exist in every dimension ≥ 5.
- **Two different threes.** The "3" of base 3 (states per digit) and the "3" of a triangle (vertices) are not the same quantity; this is the repo's "same kind of quantity" check. They meet only through geometry over the field GF(3).

**Where they do meet in this repository (computed; results owned elsewhere).**
- W33 is the symplectic polar space W(3,3) over **GF(3)**, the ternary field.
- Its 40 points and 40 lines form a complex in which each line is a solid tetrahedron (a 4-clique). The f-vector is (40, 240, 160, 40) and χ = −80.
- Its homology is computed here as **Betti numbers (1, 81, 0, 0) over Q, GF(3) and GF(2)**: torsion-free, a wedge of **81 = 3⁴** loops.
- This is homotopy-equivalent to the 80-vertex Levi graph by the nerve lemma. That graph's first Betti number 81 and its Steinberg / apartment interpretation are **owned by Passes BT545–BT551 and BT744**, and are not claimed here.
- So gluing tetrahedra over the ternary field yields exactly 3⁴ independent loops, which is the repo's own version of "triangles make loops".

## Status
- **A:** unchanged.
- **B:** y′ = 0.488–0.505 (Pass 12707). The d-wave basis of that revision is confirmed kinematically. B′ awaits a B → ψ + baryon search.
- **Hybrid:** y′ = 0.470. Its unification is unaffected by the threshold.
- **The Higgs quartic's zero itself:** today, at ±1σ in a short-distance top mass, it may not exist (stable vacuum) or may sit anywhere from 5×10⁸ GeV up. FCC-ee decides.
