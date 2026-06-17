# BT1242 -- Four-Transvection Word-Metric Regime Classifier

## Purpose

BT1240 showed that a swapped four-transvection set can still generate the full order \(51840\) group while failing the BT1233 word-metric fingerprint. BT1242 globalizes that observation across all four-projective-transvection sets.

## Orbit reduction

There are

\[
\binom{40}{4}=91390
\]

four-transvection sets.  By transitivity, every orbit has a representative containing a fixed projective point, reducing the scan to

\[
\binom{39}{3}=9139
\]

fixed-point representatives.  The stabilizer of the fixed point has 32 orbits on these triples, so only 32 representative closures are needed.

## Global order counts

The global order distribution is

\[
24^{90},\quad 27^{40},\quad 72^{1440},\quad 576^{1620},\quad 648^{26640},\quad 51840^{61560}.
\]

Thus 61,560 of the 91,390 four-sets generate the full group.

## Full-order word-metric regimes

The full-order sets split by diameter as

\[
51840_{\operatorname{diam}=10}^{22680},\quad
51840_{\operatorname{diam}=12}^{25920},\quad
51840_{\operatorname{diam}=14}^{12960}.
\]

The BT1228 / BT1233 fingerprint is the diameter-14 regime.  It occurs in

\[
12960
\]

four-sets, i.e.

\[
\frac{12960}{91390}=0.1418098260
\]

of all four-sets and

\[
\frac{12960}{61560}=0.2105263158
\]

of full-order four-sets.

## Consequence

Closure order alone is not a sufficient tomography invariant.  A recovered four-transvection set may generate \(Sp(4,3)\) while landing in the wrong word-metric regime.  The BT1233 sphere/ball fingerprint is therefore a real additional constraint, not decoration.

## Files

- Code: `analysis/bt1242_four_transvection_regime_classifier.py`
- Result: `data/bt1242_four_transvection_regime_classifier_summary.json`
