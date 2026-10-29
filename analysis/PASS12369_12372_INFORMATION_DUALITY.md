# Passes 12369–12372: the duality behind c, μ₀, ε₀ and 1, rebuilt on the two-qutrit space

Claude track. Producer: `analysis/w33_pass12369_to_12372_information_duality.py`. Drivers: `analysis/search_drivers_12369/`.

**Labels used below:**

- **[E]** established literature (cited);
- **[N]** new finite computation (exact, with checks);
- **[I]** interpretation (a reading, not a theorem);
- **[C]** conjecture (with a test).

## The idea, made precise

The relation μ₀ε₀c² = 1 is not a coincidence of units.

- **[E] It is the closure relation.** In premetric electrodynamics, Maxwell's equations split into two parts (Obukhov–Hehl
  gr-qc/9904067; Gross–Rubilar; Hehl–Obukhov's book):
  - a **topological** part, dF = 0 and dG = J: conservation of flux and charge, with no metric;
  - a **constitutive** map G = κF on 2-forms (bivectors), which carries ε, μ and the impedance.
- **[E] What closure does.** If κ² = −1, κ is the Hodge star of a Lorentzian metric, so the light cone, and c with it, is derived. For an
  isotropic vacuum, κ² = −1 reads μ₀ε₀c² = 1.
- **[E] The same pattern in quantum mechanics.** Quantum state space is Kähler (Ashtekar–Schilling gr-qc/9706069):
  - a metric g ("dot": probabilities, uncertainty);
  - a symplectic form ω ("wedge": dynamics, commutators, Heisenberg);
  - a complex structure J = g⁻¹ω with J² = −1 (the quantum i).

  Any two of (g, ω, J) fix the third, which has the same shape as μ₀ε₀c² = 1.
- **[E] α is a ratio of two impedances:** α = Z₀/(2R_K), the vacuum impedance (the scalar of the electromagnetic Hodge star) over twice
  the quantum Hall resistance h/e² (the impedance of a quantum conduction channel) (CODATA 2022).
- **[E] Constitutive laws are Hodge stars** between primal and dual cells (Tonti/Bossavit "Maxwell house"). The circuit pairs
  capacitance/inductance and voltage/current are their lumped forms.

## [N] 12369: a finite closure theorem

The setting is the space of the corpus, V = F₃⁴, and its bivectors Λ²V (dimension 6) with the wedge pairing P.

- **All solutions:** every P-symmetric κ with κ² = −1 was enumerated exactly. There are **16848**.
- **All metric:** each one is ±(Hodge star) of an **elliptic** metric, and each such κ comes from exactly two metrics (g and −g).
  **No non-metric solution exists.**
- **Hyperbolic metrics** give κ² = +1 instead.

So over F₃, as over ℝ, closure alone produces the light cone.

The counts of forms (21060 hyperbolic, 16848 elliptic) are already in the corpus as weights of the quadratic code (BT5744, PASS4938).
The closure equivalence is new here.

## [N] 12370: two i's, two kinds of metric

- **The quantum i:** the metrics compatible with the W(3,3) symplectic form (J² = −1) number exactly **540 = |Sp(4,3)|/|GU(2,3)|**,
  and all are **hyperbolic**. The para-Kähler ones (J² = +1) number 1080, also all hyperbolic.
- **The electromagnetic i:** every light cone is elliptic.
- **So:** no metric on the two-qutrit space is both the quantum state metric and a light cone. This is the finite twin of the real
  statement that a Lorentzian metric is never Hermitian.
- **The duality circles coincide.** Both circles, {x + yJ} and {x + yκ} with x² + y² = 1, are the same group: the order-4 group
  {±1, ±i}, the norm-1 elements of F₉.
- **Why q = 3 behaves like ℝ:** q ≡ 3 (mod 4), so −1 is not a square and both i's must be adjoined.

## [N] 12371: electromagnetic duality acting on the 40 contexts

- **The commutation form as a field.** Read as a bivector, W(3,3)'s commutation form ω is a non-null "field": its Pfaffian ω∧ω ≠ 0 is
  the E·B analogue.
- **No duality preserves the geometry.** No light cone fixes ω (0 of 16848). Every duality turns ω into a second commutation form κω.
- **The contexts the two forms share** are fixed exactly by the second invariant P(ω, κω), the E² − B² analogue. Checked cone by cone:

  | second invariant | cones | shared contexts | shape |
  |---|---|---|---|
  | 0 ("null field", \|E\| = \|B\|) | 6480 | 16 | 4×4 grid (hyperbolic quadric) |
  | nonzero | 10368 | 10 | ovoid (elliptic quadric) |

- **Orbits:** Sp(4,3) has six orbits on the cones:
  - two null orbits of 3240 (stabilizer 16);
  - four of 2592 (stabilizer 20).
- **Joint structures:** each of the 540 quantum structures J commutes, on bivectors, with exactly **288** light cones, 96 of each
  invariant class. 96 = |GU(2,3)|.

## [I] 12372: an information dictionary

| physics | information reading | finite object here |
|---|---|---|
| dF = 0, dG = J (metric-free) | bookkeeping: conserved counts (flux, charge) | wedge pairing P (no metric) |
| constitutive κ (ε, μ, Z₀) | rate/cost of transfer between dual cells | the 16848 light cones |
| closure κ² = −1 ⇔ μ₀ε₀c² = 1 | a transfer rule that is its own inverse up to sign defines causality | finite closure theorem |
| ω (commutator, wedge) | "state vs update" incompatibility (Heisenberg) | W(3,3), 40 contexts |
| g (Born metric, dot) | distinguishability of states | 540 Kähler metrics |
| J = g⁻¹ω, J² = −1 | the quantum i: converts update into state change | GU(2,3) structures |
| α = Z₀/(2R_K) | mismatch between free-space and quantum-channel impedance | — (no finite analogue claimed) |

These pairings are your duals, made precise:

| your pair | which side is which |
|---|---|
| E / B, D / H, ε / μ, C / L, V / I | ends of one Hodge star (constitutive) |
| position / momentum, state / update | ends of one symplectic pairing |
| dot / wedge | metric / symplectic sides of one Kähler triple |
| "size" / "efficiency of transfer" | topological count / constitutive rate |

## [C] Conjectures with tests

1. **q ≡ 3 (mod 4).** For q ≡ 3 (mod 4), the closure theorem holds and the quantum and light-cone metric types are disjoint.
   - Test: q = 7, by the same enumeration with symmetry reduction.
   - Expected failure for q ≡ 1 (mod 4): there κ² = −1 has eigenvalues in F_q, so self-dual 2-forms become rational.
2. **Null cones and stabilizer codes.** The 16 shared contexts of the null cones form a 4×4 grid. Test: identify it with the
   commuting-context grids (reguli) the corpus uses for two-qutrit stabilizer codes.
3. **A finite α?** No finite analogue of α is claimed. Any "finite α" must be a ratio of the two impedance scales: the light-cone
   (Hodge) scale over the quantum (Kähler) scale. On F₃ both scales are ±1, so α is not visible at this level.

## 12372b: what energy, mass and c are, in this split (labelled claim by claim)

**Thesis [I], backed piece by piece below.** Every fundamental law has two parts:

- **a counting part:** topological, metric-free and exactly conserved. This is the information.
- **a constitutive part:** a Hodge star. It sets how fast and at what cost the counted things move.

Each fundamental constant is an exchange rate between the two parts.

| law | counting part (information) | transfer part (Hodge / constitutive) | exchange rate |
|---|---|---|---|
| Maxwell [E] | dF = 0, dG = J: flux and charge counts | G = κF | Z₀; the closure κ² = −1 is μ₀ε₀c² = 1, which gives c |
| Kirchhoff [E] | KVL = cycle space, KCL = cut space; they are orthogonal ("dot" duals) | Ohm's law, C and L: a Hodge star on edges | R, C, L; effective resistance = random-walk commute time / (2\|E\|) (Chandra et al., 1989) |
| Quantum [E] | symplectic ω: commutators, phase-space cells | Kähler metric g: Born rule | ħ (action per state); i = J = g⁻¹ω |
| Relativity / Dirac QCA [E + computed] | causal graph, 1 cell per step (exact cone) | mixing angle m between chiralities | c = cells per step; mass = mixing per step |
| Gravity [E] (Jacobson gr-qc/9504004) | horizon area counts entropy | δQ = T dS gives Einstein's equation as an equation of state | G (area per bit) |
| Thermodynamics [E] (Landauer) | bits erased | heat k_B T ln 2 per bit | k_B |

### What each quantity is

- **Energy [E]:** the maximal rate of distinguishable (orthogonal) state changes is 2E/(πħ) (Margolus–Levitin). Energy is the update
  rate; ħ converts.
- **Mass [E, computed]:** in the Dirac automaton, mass is the rotation between left- and right-movers per step.
  - The rest frequency is exactly arcsin m (12372b, checked to 10⁻¹⁶).
  - A massive particle is a clock. Compton clocks realise this experimentally (Lan et al., Science 2013).
- **c [E, N]:** the maximal propagation of updates. It is exact in the automaton (zero amplitude outside the cone).
  - μ₀ε₀c² = 1 is the closure condition κ² = −1.
  - Over F₃, closure alone forces Lorentzian light cones (12369).
- **E = mc² [I, computed]:** a localised system's update budget splits between translating (n) and internal turning (m), on the circle
  n² + m² = 1.
  - Massive particles move slower than light because part of the budget is spent turning.
  - E = mc² is the small-angle limit of ω₀ = arcsin m. At m = 1, propagation stops.
- **One circle [N, finite]:** over F₃, three circles are the same norm-1 group of F₉, of order 4:
  - the update-budget circle;
  - the electromagnetic-duality circle;
  - the quantum-phase circle.

### What this does not do

It does not derive the value of α, any particle mass, or G. It reorganises the laws so that each constant is visibly a ratio of a
counting scale to a transfer scale. A derivation of a value would have to compute such a ratio from a single structure. The corpus's
W(3,3) cell has no macroscopic light cone on its own (in-corpus toe54); a growing tessellation is needed first.
