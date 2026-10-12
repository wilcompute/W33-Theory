# Pass 11930: the fixed-point-avoiding Higgs realises the theta-zero law — in the Weinberg channel, an inverted neutrino spectrum with m₃ ≈ 0

Producer: `analysis/w33_pass11930_fixed_point_avoiding_higgs.py`
Certificate: `data/w33_pass11930_fixed_point_avoiding_higgs.json`
Regression: `tests/test_w33_pass11930.py`
Track: Claude.

## Idea

**Setup.** At the Eisenstein point (Pass 11928) the 9 fixed points of T⁴/ℤ₃ form a W(3,3) line.

**What blow-ups do.** A blow-up modulus at a fixed point p gives a localised mass proportional to the coherent projector
|ψ^H(p)⟩⟨ψ^H(p)|.

**Which modes survive.** Higgs modes that **vanish at all 9 fixed points** are untouched by every blow-up, whatever the
blow-up sizes are. If the localised masses are positive (an assumption, stated), these modes are the light Higgs
directions. That is a parameter-free selection made by the orbifold geometry.

## Results

| channel | Higgs flux | modes | fixed-point rank | avoiding space | ρ charges |
|---|---|---|---|---|---|
| up, 10·10 | 2A₂ | 12 | 8 | **4** | all 2 |
| Weinberg, L·L | 2A₂′ | 12 | 8 | **4** | all 2 |
| down, 10·5̄ | 4·1 | 16 | 9 | 7 | mixed |

**1. Exactly (1, 1, 0) at the point.** In the up and Weinberg channels, **every** Higgs in the 4-dimensional avoiding
space gives the Yukawa spectrum **(1, 1, 0) exactly** at Ω = ω, checked on random combinations to 10⁻⁹. That is the
theta-zero law of Pass 11904 (massless lightest state, degenerate pair), and the strange-state class of Pass 11925.

**2. Scaling near the point.** For Ω = ω + ε(1 + (0.4 + 0.3i)J):
* the pair splits linearly, 1 − s₂/s₁ ∝ ε (slope 1);
* the lightest state rises quadratically, s₃/s₁ ∝ ε² (slope 2).

**3. Down channel.** The avoiding space is 7-dimensional, of mixed charges, with generic O(1) spectra. There is no
structure there.

## Reading

**Up quarks.** The pattern is wrong for them (top = charm), so the up Higgs cannot be this mode.

**Neutrinos.** In the Weinberg channel the pattern is an **inverted ordering**:
* a quasi-degenerate heavy pair, split linearly in ε, which is the solar splitting;
* an almost massless ν₃, with m₃/m₁ ∝ ε².

**Numbers.** Matching Δm²₂₁/|Δm²₃₂| ≈ 0.031 fixes ε ≈ 0.02–0.05 and then gives m₃/m₁ ≈ 3·10⁻⁴ – 2·10⁻³. For m₁ ≈ 0.05 eV
that is m₃ ≈ 2·10⁻⁵ – 10⁻⁴ eV. The spread comes from the unfixed direction inside the 4-dimensional space.

**How to test it.**
* **Ordering.** Inverted ordering will be decided by JUNO and DUNE. Current global fits mildly prefer normal ordering.
* **Effective mass.** The neutrinoless double-beta effective mass would be m_ββ ≈ 15–50 meV.

**Scope.** This is conditional on two things:
* that the Weinberg mediator is the blow-up-protected mode;
* that the localised masses are positive.

Neither is derived.

## Prior art

* Inverted ordering with m₃ = 0 from L_e − L_μ − L_τ-type symmetries (classic).
* Localised fixed-point couplings in orbifolds.
* New here:
  * the parameter-free fixed-point-avoiding selection;
  * its exact (1, 1, 0) law on the W(3,3) flavour qutrit;
  * the ε / ε² scaling.
* Corpus: Passes 11904, 11922, 11925, 11928 and 11929.
