# Pass 11642 — label-blind time: time-symmetric information is spectral, the low-order arrows of time live in the outcome labels

Producer: `analysis/w33_pass11642_label_blind_time.py`
Certificate: `data/w33_pass11642_label_blind_time.json`
Regression: `tests/test_w33_pass11641_11646.py`

## The question

**Label-blind statistics.** Measure a qutrit state in each of its four MUBs, but forget which outcome is which inside
each basis. What remains is each basis's **spectrum**: the multiset of its three probabilities. Equivalently, with
N = |ψ|²:
* e_b = Σ_{s<s′∈b} p_s p_s′ ;
* Π_b = ∏_{s∈b} p_s.

**The label-blind invariants.**
* A Clifford unitary permutes the four MUBs through A4 (Pass 11641). Complex conjugation, i.e. time reversal, swaps two
  of them.
* So the label-blind time-even invariants are the S4-symmetric polynomials in (N, e_b, Π_b).
* The label-blind time-odd invariants are the S4-alternating ones.

**Method.**
* All functions are evaluated exactly at Z[ω] points, where q_s = 3p_s is an integer, modulo P = 2³¹ − 19. Rank mod P is
  at most the rank over Q, so these dimensions are certified lower bounds.
* They are compared with Pass 11491's exact Molien dimensions E_k and O_k.

## Results

**Time-even: everything is label-blind.** For every degree k ≤ 20 the label-blind symmetric functions span all E_k
dimensions. This is an independent check of Pass 11534, whose even generators, the stabiliser moments
M_k = Σ_b Σ_{s∈b} p_s^k, are label-blind.

**Time-odd: the low-order arrows need the labels.**

| degree k | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all arrows O_k (Pass 11491) | 1 | 2 | 3 | 5 | 8 | 11 | 16 | 22 | 29 | 38 | 49 | 61 | 77 | 95 | 115 |
| label-blind arrows | **0** | **0** | **0** | 1 | 2 | 4 | 7 | 11 | 16 | 23 | 31 | 41 | 54 | 69 | 86 |
| label-sensitive excess | 1 | 2 | 3 | 4 | 6 | 7 | 9 | 11 | 13 | 15 | 18 | 20 | 23 | 26 | 29 |

* **Theorem (degree < 9).** No label-blind time arrow exists below degree 9.
  * An alternating polynomial in four points (e_b, Π_b) needs four distinct monomials in (e, Π). Their degrees are at
    least 0 + 2 + 3 + 4 = 9.
  * So the lowest arrows of Passes 11491 and 11492 (degree 6: the unique h₆; degrees 7 and 8) are **label-sensitive**.
    Detecting the direction of time with up to eight copies needs the relative alignment of outcomes across bases, not
    just the spectra.
* **The first label-blind arrow** is the degree-9 alternant det[1, e_b, Π_b, e_b²] (nonzero).
* **Pass 11641's Hesse arrow** V(Π) = ∏(Π_a − Π_b) is a label-blind arrow of degree 18.
* **Growth.**
  * The label-sensitive excess grows roughly quadratically in k, while O_k grows cubically. So label-blind arrows
    eventually dominate.
  * This is consistent with the label-sensitive part being supported on a codimension-2 locus, plausibly where two MUBs
    have identical spectra. There label-blind data cannot tell ψ from ψ̄.
  * This is an observation from the counts, not a theorem.

## The relations among the label-blind data of a pure state

* Nine functions (N, e_b, Π_b) on a cone of real dimension 5 must satisfy relations.
* The minimal relations through weighted degree 12 are listed below. Each was lifted from mod P to an **integer**
  relation and verified exactly at 300 fresh Z[ω] points.

| degree | new minimal relations | the clean ones |
|---|---|---|
| 2 | 1 | Σ_b e_b = N² (the MUB purity sum rule Σ_b P₂,b = 2N², Ivanovic / Wootters) |
| 6 | 1 | (Σ_b Π_b)² = 3 Σ_b Π_b² (Pass 11641's cone identity) |
| 8 | 1 | (104 terms) |
| 9 | 4 | (133–147 terms each) |
| 10 | 1 | (211 terms) |
| 11, 12 | 0 | — |

* A Jacobian check confirms that the four purities alone are independent (rank 3), apart from the sum rule.
* The degree-8 to degree-10 relations necessarily mix purities and triple products.

## Reading

* **Time-symmetric information about a qutrit state is spectral.** Up to degree 20, every Clifford invariant that is
  even under time reversal is a function of the four basis spectra.
* **The arrow of time is not, at low order.**
  * The first five dimensions of arrows (degrees 6–8) live entirely in the outcome labels, i.e. in phase information
    between complementary bases.
  * The label-blind arrows start at degree 9.
  * Codex's Hesse/CP arrow, through Pass 11641, sits only at degree 18.

**Scope.**
* The dimensions are exact lower bounds, certified mod P, and the degree < 9 statement is a theorem.
* The listed relations are proved over Z.
* Their completeness beyond degree 12, and the support of the label-sensitive quotient, are not proved.
