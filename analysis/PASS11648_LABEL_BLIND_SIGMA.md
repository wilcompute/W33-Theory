# Pass 11648 — label-blind time II: the label-sensitive arrows are exactly the arrows on the equal-spectra locus

Producer: `analysis/w33_pass11648_label_blind_sigma.py` (stages `all` = `sigma` + `lb`, and `lattice`)
Certificate: `data/w33_pass11648_label_blind_sigma.json`
Regression: `tests/test_w33_pass11647_11654.py`

## Why label-blind arrows vanish on Σ

**What Pass 11642 found.**
* Label-blind arrows, i.e. S4-alternating functions of the four MUB outcome spectra, start at degree 9.
* The label-sensitive excess O_k − LB_k is 1, 2, 3, 4, 6, ….

**The locus.** Let Σ be the set of states on which two MUBs have equal spectra, of real codimension 2. On Σ, swapping
those two labels fixes the spectral data.
* So every alternating function of the spectra vanishes on Σ.
* Hence LB ⊆ {odd invariants vanishing on Σ}, and dim(O_k|_Σ) ≤ O_k − LB_k.

## Results

**1. Equality: the label-sensitive arrows are exactly what survives on Σ.**

| degree k | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| O_k − LB_k | 1 | 2 | 3 | 4 | 6 | 7 | 9 | 11 | 13 | 15 | 18 | 20 | 23 |
| rank of the odd module on Σ | 1 | 2 | 3 | 4 | 6 | 7 | 9 | 11 | 13 | 15 | 18 | 20 | 23 |

* **Method.** The odd module is evaluated at 400 points of Σ(Z, X), found by least squares.
* **Certification.** For k ≤ 15 the floating-point rank of the full module at generic points equals O_k, so these rows
  are certified. Rows 16–18 match but are not certified, since the generic rank there drops below O_k.
* **Reading.** **An arrow of time of a qutrit is label-blind iff it vanishes wherever two complementary measurements have
  the same outcome statistics.**

**2. Hilbert series.** These are fitted to every degree from 9 to 25, with label-blind dimensions computed mod P at 900
points (366 distinct spectral points, against a top rank of 226).

  Σ_k (O_k − LB_k) t^k = t⁶(1 + t − t³) / ((1 − t)(1 − t²)(1 − t³)),
  Σ_k LB_k t^k = (t⁹ + t¹⁰ + t¹¹ + t¹² − t¹⁵ − t¹⁶ − t¹⁷ + t¹⁹) / ((1 − t)(1 − t²)(1 − t³)(1 − t⁴)(1 − t⁶)).

The three-factor denominator of the excess is what a module supported on the 3-dimensional cone over Σ should have.

**3. A curiosity.**
* **The points.** Take every Z[ω] point ψ with entries a + bω, |a|, |b| ≤ 3: 117 648 points. Of these, 8 244 lie on
  Σ(Z, X), and 1 356 of those have the other two spectra distinct.
* **What happens there.** All 1 356 are **time-symmetric**: the whole odd module vanishes there through degree 20 (exact,
  mod P).
* **Consequence.** Small Eisenstein-integer states on Σ are never time-asymmetric. That is why the equality of result 1
  had to be tested at irrational points of Σ.

## Reading

* **Combined with Pass 11649.** The maximum of the lowest arrow h₆ is attained on Σ, at a state where three MUBs share a
  spectrum. So the arrow of time is strongest exactly where label-blind information is most degenerate.
* **Scope.**
  * The restriction law is numerical, certified for k ≤ 15.
  * The Hilbert series are fits to exact mod-P dimensions over degrees 9–25 (20 values, three numerator terms).
  * Neither is a proof for all degrees.
