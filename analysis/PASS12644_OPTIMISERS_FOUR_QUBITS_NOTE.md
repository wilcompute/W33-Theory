# Pass 12644: a strongly unextendible set of 9 Pauli MUBs in d = 16 (F ≥ 1999/32000, exact; min 1/16); the non-stabiliser optima are (207 − 19√57)/432 and 13/75 (numerical); Shor relaxations cannot reach 1/8

Claude track. Follows Passes 12642–12643. **Not a theory of everything.**

## 1. The exact 1/8: a negative result with its mechanism (`w33_shor_pure_state_relaxation.py`)

Pass 12643 left a gap: Lovász gives ϑ ≤ 4 + √5, while the true maximum of Σ_U ⟨P⟩² is 6. I tried the Shor relaxation of the pure-state conditions:
- write ρ = (1/d) Σ x_a P_a and impose ρ² = ρ, which is linear in the lift Z = [1 x; x X] ⪰ 0;
- add X_aa ≤ 1, ρ ⪰ 0 (the moment matrix M(x)), and X_aa + X_bb ≤ 1 for every anticommuting pair;
- maximise Σ_U X_aa.

| set | plain Shor | with ρ ⪰ 0 and anticommuting pairs | true max |
|---|---|---|---|
| two qubits, 3 | 3.000 | 3.000 | 2 |
| three qubits, 5 | 7.000 | 7.000 | 6 |

**The bound is vacuous, and the reason is structural.** The objective is a convex function being maximised, so the lifted X_aa may exceed x_a². Only the constraint Σ_a X_aa = d − 1 binds. Getting an exact 1/8 needs degree-6 (third-moment) information in ψ, which is where the numerical SOS of Pass 12642 works. **Rounding that SOS remains the route.**

## 2. The non-stabiliser optimisers (`w33_nonstabiliser_optimisers.py`, `w33_pentad_optimum_levels.py`)

| set | min F | identification | optimal profile |
|---|---|---|---|
| two-qutrit pentad | 0.1471137632635549 | **(207 − 19√57)/432**, matches to 3×10⁻¹⁶ | unique (120/120 starts). Two levels of \|⟨W_u⟩\|: 0.0531 (×24) and 0.2802 (×16). Schmidt (0.864, 0.490, 0.114). |
| d = 25 single cover (14 lines) | 0.17333333333333323 | **13/75**, matches to 10⁻¹⁶ | unique (60/60 starts). Three levels: 1/6 (×48), 0.0515 (×144), 0.1348 (×144). One Schmidt coefficient is 0.288675 ≈ 1/√12. |

**Status.**
- These are numerical identifications, not proofs.
- For the pentad, the quadratic 1944x² − 1863x + 232 has discriminant 3⁵·19³, which explains the √57.
- The individual pentad levels are known only to 10⁻⁸, and no consistent identification was found (the candidate quadratics are not in Q(√57)).

**Prior art.**
- The value 0.14711 is the corpus's own number: Pass 12637, Pass 12639, and the other track's `2026-11-09_exact_mub_sym2_blocks.md`, which also records that 1/9 is not the exact minimum.
- No closed form for it, and no 13/75, appears anywhere in the corpus (searched md/py for the values and for √57).

**Reading.** In both non-stabiliser cases the optimum is a **unique orbit with few |⟨W_u⟩| levels**, so it is an exact algebraic object, not a numerical accident.
- The pentad value involves √57 = √(3·19). Nothing in the corpus explains a 19, so no interpretation is offered.
- A clean rational 13/75 at d = 25 suggests a closed-form state.

## 3. The four-qubit rung (`w33_four_qubit_rung.py`, `data/w33_four_qubit_rung.json`)

**Setup.** W(7,2) has 2,295 Lagrangians, generated as one transvection orbit.

**Size 9 = d/2 + 1.** An integer program found maximal partial spreads of size **9**, the size of Mandayam et al.'s construction. Minimality is **not** proved: the solver hit its time limit with a dual bound of 2. Two runs returned two sets:
- the first, unsaved, had ϑ = 14.0000 = α;
- the second, saved as lines [53, 508, 753, 1027, 1092, 1602, 1876, 2024, 2095] in `data/w33_four_qubit_theta_exact.json`, is the certified one below.

**The certified set** (`w33_four_qubit_mstar.py`, `w33_four_qubit_theta_full_dual.py`):
- It is disjoint and maximal. Three Lagrangians meet C in exactly one point (m* = 1), so stabiliser states attain F = 1/16.
- The uncovered graph has 120 vertices and is 56-regular. Its spectrum is not integral (λ_min = −8), and its Hoffman bound is 15, which is useless.
- **ϑ = 13.99999997** (full SDP).
- The rounded dual has a degenerate face, so exact rounding at ϑ = 14 fails for every denominator tried, with min eigenvalue −0.0014 at D = 112.
- **ε-relaxed exact certificates** pass exact rational LDLᵀ checks: (14 + δ)I − Y ⪰ 0 for δ = 1/400, 1/1000 and **1/2000** (D = 112, 256, 512).

> **For this nine-element four-qubit Pauli MUB set and every v ∈ C¹⁶:**
> F(v) ≥ **1999/32000** · |v|⁴ ≈ 0.062469 |v|⁴, i.e. within 0.05% of the attained minimum 1/16 (exact, via de Gois et al.).

So **a strongly unextendible set of d/2 + 1 Pauli MUBs exists in d = 16**, with an exact near-tight constant. Mandayam et al. conjectured unextendible sets for n > 3. Thas (arXiv:1407.2778) solved their Conjecture 1, which concerns Pauli classes (weak unextendibility). In the sources checked I found no strong-unextendibility result in d = 16; Szántó's constructions are in d = p², p ≡ 3 (mod 4). **This is not a novelty claim**, only the outcome of the search recorded here.

**Elementary covers** (`w33_anticommuting_clique_cover.py`, `w33_four_qubit_tabucol.py`, `w33_four_qubit_fractional_cover.py`). Each pairwise-anticommuting class has Σ⟨P⟩² ≤ 1, so a k-class cover gives Σ_U ⟨P⟩² ≤ k.
- Two qubits: k = 2 exists, an elementary proof of min F = 1/4.
- Three qubits: k = 6 is proved infeasible (consistent with ϑ > 6); k = 7 exists.
- Four qubits: no 14-colouring was found (integer program timed out at 2,400 s; Tabucol, 40 × 400k iterations). The fractional cover cannot reach 14: Farley's bound gives χ_f ≥ 14.16. Column generation was stopped at LP 15.56. So the elementary route cannot give the tight value here, and the Lovász dual is needed.

## 4. Note for quantum-information readers

`analysis/NOTE_QUBIT_STRONG_UNEXTENDIBILITY.md` states:
- the single-orbit result;
- the exact constant (3 − √5)/8;
- the numerical 1/8;
- the mirror pairs and the 9/16 witness;
- priority (Mandayam et al.) and the inequality used (de Gois et al.);
- what is not claimed.

## Open

- Round the degree-6 SOS to an exact 1/8.
- Prove (207 − 19√57)/432 and 13/75, starting from the unique optimal orbits.
- Determine why √57 appears.
