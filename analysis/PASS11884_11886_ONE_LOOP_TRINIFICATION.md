# Passes 11884–11886: one loop selects trinification at the W(3,3) points

Producer: `analysis/w33_pass11884_11886_one_loop_trinification.py`
Certificate: `data/w33_pass11884_11886_one_loop_trinification.json` (9/9 checks)
Regression: `tests/test_w33_pass11884_11886.py`
Track: Claude.

## Setting

Passes 11879–11883 set up SU(9) with one 84 = Λ³ℂ⁹, the ℤ₃-twisted half of E₈. Its most general renormalizable potential is

  V = −m²|x|² + λ₁|x|⁴ + λ₂‖μ(x)‖²,

where μ is the moment map. The rewrite uses tr ρ² − (tr ρ)²/9 = ‖μ‖². For λ₂ > 0 the vacua form the Kempf–Ness set
SU(9)·𝔥. There the Cartan 𝔥 is the level-3 genus-2 modulus with a marked Weierstrass point, and the tree potential is
flat along it.

The open question was which point of the flat direction the quantum theory picks.

## 11884: the one-loop function, and its global minimum

On the flat set, normalised to |x| = 1, write e₁…e₈₀ for the vector mass-squared eigenvalues.

**Fact 1: two traces are constant.** At every Cartan point Σeᵢ = 20 (Casimir) and Σeᵢ² = 8 (a quartic invariant).

**Fact 2: the heavy scalars track the vectors.** The non-Goldstone scalar mass matrix is the Hessian of λ₂‖μ‖². Its
nonzero spectrum is the vector spectrum times exactly 8/3 at every tested point (ratio spread < 10⁻⁶). This is the
moment-map identity Hess‖μ‖² = 2 dμᵀdμ, whose nonzero spectrum equals that of dμ dμᵀ = M², the same structure as a
supersymmetric D-term.

**Consequence: the selection is coupling-independent.** In every bosonic Coleman–Weinberg term along the flat direction,
the m⁴ and renormalisation-scale pieces are constant. What varies is a positive multiple of

  **F = Σᵢ eᵢ² log eᵢ,**

for all values of g, λ₁ and λ₂.

**Where F is smallest.**

| point on 𝔥 | massless vectors | spectrum | F |
|---|---|---|---|
| Witting ray (any of the 40; W(3,3) point, E₈ root ray) | 24 | 0²⁴ (1/3)⁵⁴ 1² | **−6 log 3 = −6.5917** |
| generic | 0 | continuous | ≈ −6.23 to −6.25 |
| maximum of F | 4 | | −6.2266 |

* Five randomised minimisations, each with polishing restarts, all converge to F = −6 log 3 with 24 massless vectors.
* An earlier unpolished run stopped at −6.5912. It was a convergence artefact, not a new minimum.

**Conclusion: one loop picks the 40 Witting rays, i.e. SU(9) → SU(3)³ trinification.** The massive vectors there are:
* the 54 bifundamentals (3,3̄,1) + permutations, together with their conjugates;
* the 2 U(1)s of the commutant.

The 40 rays are related by the Witting group G₃₂ = N(𝔥)/Z(𝔥) ⊂ SU(9), so they are gauge-equivalent: there is one vacuum.

## 11885: stability at the ray, and the one remaining flat direction

**Counting the 168 real fields at a ray:**
* rank dμ = 56, so ker dμ = 112;
* 56 are eaten (the orbit tangent);
* 56 are heavy (proportional to the vectors);
* 1 is radial;
* 55 are tree-flat and are neither gauge nor radial.

By the branching 84 = 3·(1,1,1) + 54 + (3,3,3) under SU(3)³, those 55 are the overall phase plus the complex (3,3,3).

**Stability.** Along every one of the 55 directions (each basis vector, both signs) and 40 random ones, F strictly
increases at finite displacement:
* t = 0.02: minimum gain 5.5·10⁻³;
* t = 0.05: minimum gain 3.3·10⁻².

The second-difference Hessian alone misses this in directions where the massless vectors gain mass only at second order
(F ∝ t⁴ log t). That is why the finite test is the certificate. So **the trinification vacuum is a strict local minimum
of the one-loop gauge potential, except along the overall phase of the 84**, which is exactly flat (|ΔF| ~ 10⁻¹⁵).

**The phase is physical.** The degree-12 Cartan invariant is nonzero at the ray (|I₁₂| = 1.3·10⁻³; degree 18 likewise).
Since e^{iφ} multiplies them by e^{12iφ} and e^{18iφ}, it is a gauge transformation only for φ ∈ 2πℤ/6. It is an
axion-like direction lifted only by the dimension-12 operator κI₁₂(x) + c.c. The phase of κ is the CP datum of
11870/11878.

**Scope of the stability statement.** It uses the gauge-loop function F, which is exact along the Kempf–Ness set. Off
it, the scalar loop is proportional to F only to leading order, so off-set stability is certified for g² ≫ λ₂. Charged
fermions coupled to the 84 would enter with the opposite sign and are not included.

## 11886: synthesis: what is now derived

The chain is now:

  **E₈ ⊃ SU(9), with matter the twisted 84**
  → renormalizable vacua = the level-3 genus-2 modulus (with a Weierstrass point), flat;
  → one loop puts the vacuum at the W(3,3) points (Witting rays), where SU(9) → **SU(3)_C × SU(3)_L × SU(3)_R**;
  → left over: a physical phase (axion-like), lifted at dimension 12 with the CP phase, and a tree-flat (3,3,3) scalar
  that gets one-loop masses.

**Why this matters for the TOE programme.**
1. The W(3,3) points stop being a passive labelling. They are where the dynamics of the E₈ twisted sector places the
   vacuum, and the unbroken group there is trinification, a standard route to the Standard Model.
2. On the Siegel side, the Witting rays are the base locus of the Maschke map, i.e. degenerate genus-2 curves (cusps).
   So the radiative vacuum is at a cusp of the modulus. Small higher-order effects displace it into the interior, which
   is where the (1, ε, ε²) hierarchy (11872/11876) and CP violation (11878) live.
3. Compared with the previous rounds, the arrow/CP datum the substrate "cannot select from inside" (Pass 346) is now
   tied to one specific operator: the phase of the first holomorphic invariant of the 84, at dimension 12.

## Not established

* No fermions in the loop. A charged fermion sector could reverse the selection.
* Not embedded in a realistic string vacuum (the hidden-E₈ placement is still open).
* No computation of the (3,3,3) one-loop masses as numbers with units.
* No derivation that SU(3)³ then breaks to the SM.
* No relation to measured couplings.

## Prior art

* Coleman–Weinberg (1973).
* Michel's conjecture on maximal isotropy subgroups in Higgs potentials.
* Kempf–Ness (1979).
* Vinberg–Elashvili (Λ³ℂ⁹, G₃₂).
* Trinification: de Rújula–Georgi–Glashow (1984).
* Corpus:
  * Passes 11879–11883 (the flat direction);
  * 11681/11699 (E₈ of two qutrits, Witting rays);
  * 11869–11878 (the Siegel modulus);
  * 11701–11703 ("two commuting clocks = trinification on one line");
  * TOE41 (parallel track): the Albert cubic in trinification coordinates.
