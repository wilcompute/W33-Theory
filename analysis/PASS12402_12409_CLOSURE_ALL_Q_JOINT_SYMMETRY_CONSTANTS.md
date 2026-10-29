# Passes 12402–12409: closure for every odd q, the joint symmetry of the two i's, and constants as exchange rates

> **Correction (Pass 12410).** The statement below holds as written only for q ≡ 3 (mod 4). For q ≡ 1 (mod 4), i lies in F_q,
> and closure solutions whose eigenspaces have unequal dimensions also exist; κ = i·I is one, and none of them is a Hodge star. The
> exact counts are 2,834,952 solutions at q = 5, of which 71% are hyperbolic Hodge stars. There, κ is a Hodge star iff tr κ = 0.
> The q = 5 and 13 sampling drew only 3-dimensional eigenspaces, so it was conditional on that. See
> `PASS12410_12417_CLOSURE_PROOF_ALPHA_ENTANGLEMENT_CEILING_TPRIME.md`.


Claude track. Producer: `analysis/w33_pass12402_to_12409_closure_all_q_joint_symmetry_constants.py`. Drivers:
`analysis/search_drivers_12402`–`12406`.

**Labels used below:**

- **[E]** established (cited);
- **[N]** new, computed here;
- **[I]** interpretation.

In-corpus prior art: P11831 (SL(2,9) as the finite Lorentz group of two qutrits) and 12369–12372 (the closure theorem at q = 3).

## [N] 12404–12405: closure always makes a metric, and −1 decides which kind

On the bivectors of F_q⁴ (wedge pairing P), every P-symmetric κ with κ² = −1 is the Hodge star of a metric.

The kind of metric depends on whether −1 is a square:

| q | −1 is | closure metrics | evidence |
|---|---|---|---|
| 3 | non-square | elliptic (Lorentzian-type) | all 16848, exact enumeration |
| 7 | non-square | elliptic | 200/200 sampled |
| 11 | non-square | elliptic | sampled (see certificate) |
| 5 | square | hyperbolic | 400/400 sampled |
| 13 | square | hyperbolic | 200/200 sampled |

**Sampling method:**

- Closure solutions are drawn uniformly:
  - as nondegenerate 3-spaces when q ≡ 1 (mod 4);
  - as nondegenerate generators of the Hermitian polar space H(5, q²) when q ≡ 3 (mod 4).
- A finite Urbantke formula reconstructs the metric from the self-dual bivectors. It returns the inverse-metric density; a first version
  forgot to invert it, and its control caught that.
- **Control:** random metrics of the right type are recovered exactly.

**Counting.** By group orders, the number of closure solutions equals the number of metric Hodge stars of that kind for every
q = 3 … 13. For example, q = 7 gives 39,414,816 both ways.

The reason is a pair of exceptional isomorphisms:

- the Klein correspondence O⁺(6, q) ~ SL(4, q);
- O⁻(4, q) ~ PSL(2, q²) ~ O(3, q²), the finite form of SO(3,1) ≅ SO(3, ℂ) ("the Lorentz group is the rotation group with an i").

**Statement:** closure always produces a light cone, and it is Lorentzian exactly when −1 has no square root in the field, as in ℝ.

## [N] 12403: the symmetry of the quantum i, and what a light cone leaves

**The quantum i.** In Sp(4,3), the stabilizer of a quantum structure J of W(3,3) has three layers:

- **the whole group:** order 96 = |GU(2,3)|, the finite U(2);
- **its centre:** Z₄, the phase circle {±1, ±i};
- **its derived subgroup:** order 24 with element orders 1, 2, 3 (×8), 4 (×6), 6 (×8), which is SL(2,3), the binary tetrahedral group
  (the finite SU(2)).

**Adding a light cone** that commutes with J:

- for every non-null cone (192 of 288), only the centre Z₄ survives;
- for the 96 null cones, an abelian group of order 8 survives.

**[I]** U(2) ≅ (SU(2) × U(1))/Z₂ is the electroweak group. Here a generic light cone breaks it down to the phase circle. That circle is
the hypercharge-like centre, not U(1)_em, so the analogy is structural only.

## 12402: the twin obstruction across all 59 candidates

All 59 candidates were checked, 65 SU(3)×SU(2) pairings in all.

- **The checked claim holds everywhere:** a Standard-Model hypercharge with a hypercharge-neutral hidden sector is infeasible in all 65
  pairings.
- **Every pairing** also carries chiral (3,2)-type matter in the second SU(3)×SU(2) pair (net 1 in 53 pairings, net 3 in 12).

The failure has two mechanisms:

| mechanism | pairings | what happens |
|---|---|---|
| twin | 28 | the colour conditions alone are feasible; the neutral hidden sector kills them |
| colour-blocked | 37 | the colour conditions alone are already infeasible (for example SM_574_c2183) |

## [E + numerically re-derived] 12406–12408: constants as exchange rates between counting and transfer

| constant / law | counted thing | transferred thing | exact form (checked) |
|---|---|---|---|
| ħ (Margolus–Levitin) | orthogonal updates | energy × time | max rate 2E/(πħ): 6.04×10³³ /s per joule |
| k_B (Landauer) | bits erased | heat | k_B T ln 2 per bit |
| Shannon, wideband limit | bits sent | signal energy | E_b/N₀ → ln 2 (to 10⁻⁷), the same as Landauer with N₀ = k_B T |
| G with ħ and c | bits | horizon area | a black hole saturates the Bekenstein bound: 2πk R E/(ħc) = k A/(4ℓ_P²) (to 10⁻¹⁶); area per bit = 4 ln 2 ℓ_P² |
| Smarr | bits | mass-energy | Mc² = 2 × (bits) × k T_H ln 2 (to 10⁻¹⁶): a black hole's energy is twice the erasure cost of its memory at its own temperature |
| e²/h, π²k²T/(3h) | channels | charge or heat current | Landauer and Pendry per-channel quanta; Pendry's entropy constant = 2 g₀/T |
| c | lattice cells | time steps | Lieb–Robinson / QCA cone; μ₀ε₀c² = 1 (to 10⁻¹²) is closure |
| m (Compton) | clock cycles | rest energy | ν = mc²/h: 1.2356×10²⁰ Hz for the electron |
| α | — | two impedances | α = Z₀/(2R_K) (to 6×10⁻¹³): free-space EM duality over a quantum-Hall channel |
| Unruh | horizon bits | acceleration | T = ħa/(2πck) |

**[I] Principle.** Dimensional constants convert a count into a transfer. A dimensionless constant compares two transfer laws acting on
the same count: α compares the impedance of the electromagnetic Hodge star with that of a quantum channel.

**Consequence for a theory of everything:** deriving α means building both dualities on one structure, the Lorentzian Hodge star on
2-forms and the Kähler/Landauer channel on states, and computing the ratio of their scales.

**Where this leaves the finite model.** On F_q both scales are ±1, so α cannot show up at the finite level (12370). That is precisely
what a continuum or tessellation limit would have to supply.

## 12409: synthesis

- The light cone (closure), the quantum i (Kähler) and the phase circle shared by both are now theorems on every odd-q two-qutrit space.
- What remains is a scale: the ratio between the two i's, which is where α lives.
