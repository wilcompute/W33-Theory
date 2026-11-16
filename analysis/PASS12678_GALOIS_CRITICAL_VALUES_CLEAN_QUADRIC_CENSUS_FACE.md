# Pass 12678: Galois conjugates of the torus levels are critical values; the clean E₈/2E₈ quadric is generic for high-weight types; corrections to the E₆/E₈ framing; facial reduction at c₈

Claude track. Follows Pass 12677. **Not a theory of everything.**

## 0. Corrections of emphasis to Passes 12675 and 12677 (over-read guard)

Over F₂ there is exactly one isometry class of nondegenerate elliptic quadratic space in dimension 6 (≅ E₆/2E₆) and exactly one hyperbolic class in dimension 8 (≅ E₈/2E₈). So:
- "the T code space is E₆/2E₆" is **automatic** once an elliptic form is preserved;
- "the type-C code space is E₈/2E₈" is automatic once a clean hyperbolic form exists.

The non-automatic content of Pass 12675 is unchanged:
- the torus symmetry σ **preserves** exactly one form, which is elliptic, so σ ∈ O⁻(6,2) = W(E₆) is of type E₆(a₁);
- the nine bases are **one σ-orbit of tritangent planes**;
- the weights are incidence counts.

For Pass 12677, §2 below shows the clean hyperbolic form is generic for any order-4 group with a coset of weight ≥ 3, so "type C is special" was an over-read. The corpus already notes that W33's own 8-dimensional plus-type module has the E₈/2E₈ type, *without* a canonical identification (`2026-10-29_W33_even_line_resolution.md`, `2026-07-10_levi_closure.md`). Nothing here supplies one.

## 1. Galois conjugates of torus levels are critical values (`w33_torus_critical_values_galois.py`)

At q = 8 the conjugates of c₈ are values of other torus eigenstates (eigenspaces of dimension 1). At q ≥ 16 the conjugates of τ_q do not occur as eigenspace minima (checked against the stored eigenspace minima for 2 + 2 classes). Solving ∇F = 0 inside each torus eigenspace (least squares, many starts) gives:
- **q = 4 (control):** both conjugates, 1.2111456180 and 4.7888543820, are critical values in **all 8 eigenspaces**.
- **q = 16: inconclusive.** With 8 least-squares starts per eigenspace (32 eigenspaces of dimension 8), the solver converged to 40 distinct critical values, all random saddles between 7.47 and about 12. It found neither τ₁₆ (a known critical point) nor any conjugate, so the search is too sparse to test the claim. The decisive test would Galois-conjugate an exact q = 16 minimiser, as Pass 12672 did at q = 8; that needs an exact minimiser over Q(cos 2π/17, …) and was not done.

By symmetric criticality these are critical points of F on C^{q²}. At q = 4 this supports the following reading of the "smallest conjugate" law of Pass 12677: the torus construction's critical points come in Galois orbits, as Pass 12672 proved exactly at q = 8, and the reported level τ_q is the lowest member of its orbit.

## 2. Clean-quadric census (`w33_f8_clean_quadric_census.py`)

Over 300 random uncovered order-4 groups at q = 8, nine coset-weight types occur (B 109, C 16, A 1, and six others). A form is "clean" if every covered coset is singular.

| type (weights) | groups | clean forms |
|---|---|---|
| C {1: 54, 2: 27, 3: 9} | 16 | one hyperbolic (E₈/2E₈ type), every time |
| {1: 72, 2: 21, 3: 7} | 23 | one hyperbolic, every time |
| {1: 55, 2: 36, 4: 2} | 8 | one hyperbolic, every time |
| A, B and four other types (weights 1, 2 only) | 253 | none |

> A clean form exists exactly for the types with a coset of weight ≥ 3. It is then unique and hyperbolic, and no clean elliptic form ever occurs. The type-C cleanliness of Pass 12677 is an instance of this, not a special E₈ feature of the F₈ minimum.

## 3. Facial reduction at c₈ (`w33_f8_facial_reduction.py`)

1. **Minimisers.** 1,500 random starts on the effective three-qubit objective give **exactly 128 distinct minimisers up to phase** (113 after 300 starts, saturating at 128 after 1,200). Each was polished by Newton with an analytic gradient to |∇| ≤ 6×10⁻¹⁵. A first run without polishing inflated the numerical kernel rank (2,324) because state errors of ~10⁻⁶ exceeded the rank tolerance; it was discarded.
2. **The face.** In each Fourier block (χ, ξ) the minimisers give kernel vectors y_O = F_{O,ξ}(ψ*)/|stab_O|, which follows from Σ m̄Gm = N⁻¹ Σ_ξ F̃ᴴ M F̃. Their spans total **383 complex dimensions, histogram {2: 191, 1: 1}**. This is identical, block for block, to the near-zero eigenvalues of the independent rational certificate at 2.498508646 (Pass 12676: {4 real: 191, 2 real: 1}). The face is exactly the span of the 128 minimisers' monomial vectors.
3. **The SDP at C = c₈ exactly**, with M·y = 0 imposed (10,272 kernel equations) and margin s on the complement (M − s·P⊥ ⪰ 0): SCS solves with **margin s = 0.649**, about eight orders of magnitude above solver noise.

> **Result (numerical, strong).** The degree-8 SOS certificate at C = c₈ exists and is strictly feasible on the face spanned by the 128 minimisers. That is the standard condition under which exact facial reduction followed by rounding yields an exact certificate. So c₈ = (47 − 32cos 2π/9)/9 is the degree-8 SOS value on the T code space, not just a limit of it. Completing the exact proof needs only the face in exact arithmetic: the 128 eigenstates are known algebraically over Q(ζ₇₂) (Pass 12673), and the remaining Gram entries would be rounded within Q(cos 2π/9). Not done here.

## 4. The E₇ rung (`w33_f8_E7_rung.py`)

On the effective three-qubit space, Sp(6,2) ≅ W(E₇)/{±1} (the full three-qubit Clifford group modulo Paulis) acts on the 64 quadratic forms polarising the symplectic form: 28 odd, the bitangents of a plane quartic, and 36 even.
- σ fixes **exactly one bitangent**, the elliptic form of Pass 12675: 28 = 1 + 9 + 9 + 9. The 36 even forms fall into four orbits of 9.
- Each of the nine bases has exactly 8 even forms and no odd form vanishing on it.
- **The full Sp(6,2) stabiliser of the nine-basis configuration has order 18**, found by exhaustive backtracking over all symplectic maps, not only those in W(E₆). It equals the W(E₆) stabiliser D₉ of Pass 12676.

> The configuration lives a priori in the E₇ (three-qubit Clifford) geometry, but it canonically selects one bitangent. Its entire symplectic symmetry lies in that bitangent's stabiliser W(E₆) = O⁻(6,2): E₇ (three qubits) → one bitangent → E₆ (cubic surface) → E₆(a₁) torus → c₈. Like the rest of this note, this is a statement of finite geometry, with no physical claim.
