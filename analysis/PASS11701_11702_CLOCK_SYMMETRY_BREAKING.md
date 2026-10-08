# Passes 11701–11702 — which two-qutrit clocks leave exactly Standard-Model-shaped symmetry: one third-level clock never, two commuting clocks yes, and the GUT ladder in between

Producer: `analysis/w33_pass11701_11702_clock_symmetry_breaking.py` (`--pairs` adds the 8-minute pair census)
Certificate: `data/w33_pass11701_11702_clock_symmetry_breaking.json`
Regression: `tests/test_w33_pass11697_11703.py`

**Question.** Pass 11692 found SM-shaped unbroken symmetry su(3) ⊕ su(2) ⊕ u(1)⁵ in about 0.1% of random magic ticks and in no Clifford tick. Pass 11693 asked for a *natural* tick with exactly that centraliser, and for Codex's Spin(10) route inside the two-qutrit E₈.

## 11701 — a Kac bound, and the third-level census

**Kac bound (an elementary consequence of Kac's theorem; enumerated exhaustively for orders m ≤ 30).**
* An E₈ element of order m has centraliser given by its Kac coordinates: Σ aᵢsᵢ = m with gcd 1, and the zero nodes give the semisimple part.
* **SM-shaped centralisers first occur at order 16**, and then at every order ≥ 16.
* As a check of the enumerator, the regular (Cartan-only) case first occurs at m = 30, the Coxeter number.
* Prior art: the repository's own Kac classification at order 6 is `analysis/2026-09-21_e8_order6_kac_classification.md`.

**Third-level diagonal clocks.** These are ζ₉^{f(x,y)} with f = c₁x³ + c₂y³ + 3q(x,y) and deg q ≤ 3, giving 19,683 gates × 3 lifts. Examples: T = ζ₉^{x³}, Z = ζ₉^{3x}, CZ = ζ₉^{3xy}.
* Every one has E₈ order 1, 3 or 9 (counts 1 / 6,560 / 52,488). Since 9 < 16, **none is SM-shaped**. The Kac bound *explains* the Clifford-tick zero of Pass 11692.
* Their centralisers form exactly a GUT ladder:

| centraliser | share | simplest clock |
|---|---|---|
| A1+A1+A4 | 26.3% | ζ₉^{y³+6x²y} |
| A1+A4 = SU(5)×SU(2) | 17.6% | ζ₉^{y³+3x²y} |
| A1+D4 | 11.0% | |
| A1+A2³ | 9.8% | I⊗T |
| A1+A2+A4, A1+A5 | 8.8% each | |
| A2+E6 | 3.8% | ω^{xy²} |
| D7 | 3.7% | ω^{xy²} (other lift) |
| A1+D5 | 3.3% | |
| A8 | 3.3% | identity (non-trivial lift) |
| D5 = Spin(10) | 2.2% | |
| A2+D5, E7, A1+E6, E8 | rest | |

Nothing smaller than SU(5) or Spin(10) occurs.

**Fourth-level clocks (ζ₂₇ phases).** SM-shaped in 9.5% of random diagonal clocks. Even unentangled product clocks diag(1, ζ₂₇ᵃ, ζ₂₇ᵇ) ⊗ diag(1, ζ₂₇ᶜ, ζ₂₇ᵉ) reach it: 50,544 of 1,594,323 (exhaustive). **A single tick with exactly SM symmetry needs the fourth level of the qutrit Clifford hierarchy.**

## 11702 — commuting clocks: the GUT chain inside the two-qutrit E₈

Commuting clocks break to the intersection of their centralisers (a finite "Wilson-line" mechanism).

* **Pairs.** Among pairs of the 9,605 distinct third-level centraliser patterns with 8 joint roots, **5,037,660 are SM-shaped** and 1,309,284 are A1⁴.
* **Two clocks suffice.** **Z⊗I** (centraliser E₆ × SU(3)) together with **(I⊗T)·CZ** = ζ₉^{y³+3xy} leaves exactly su(3) ⊕ su(2) ⊕ u(1)⁵.
* **Codex's Spin(10) route, realised by commuting clocks:**
  * E₈ → E₆ × SU(3) [Z⊗I] → **Spin(10) × SU(2)** [ω^{xy²}] → SM shape [ζ₉^{y³+3xy+3x²y}];
  * E₈ → E₆ × SU(3) → **SU(5) × SU(2) × SU(2)** [ω^{xy²}, other lift] → SM shape [ω^{x²y}];
  * also via D5 alone, A2 + D5 and SU(5) × SU(2). 264–1,200 third clocks complete each chain.
* **Matter.** Under every SM-shaped joint centraliser, the 232 broken roots form 12 sextets ((3,2) or (3̄,2)), 30 triplets, 20 doublets and 30 singlets. This is the standard E₈ ⊃ SU(3) × SU(2) branching. Only multiplet sizes were computed; the split into (3,2) versus (3̄,2) and the assignment to families were not.

**Caveat on lifts.** "Lift k" is the principal branch of det^{−1/9} times ζ₉ᵏ. It is a label, not a canonical choice: the E₈ element of a gate is defined only up to the central grading element (Pass 11700).

## Reading

* **The clock picture of symmetry breaking is now explicit.** Stabiliser gates keep E₈ large. One magic gate (third level) reaches the GUT groups, and never further. A second commuting clock, or one fourth-level clock, reaches the SM shape.
* **Answer to the Pass 11693 question.** There *is* a natural SM-shaped tick: Z⊗I followed by (I⊗T)·CZ. It is a two-clock structure, not a single gate.

## Scope

These are symmetry-breaking **patterns** realised by explicit commuting qutrit gates.

Not derived:
* why a dynamics would choose them;
* the hypercharge embedding among the five u(1)s;
* chirality (see Pass 11698);
* couplings.
