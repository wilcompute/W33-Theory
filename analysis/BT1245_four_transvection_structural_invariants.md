# BT1245 -- Four-Transvection Structural Invariants

## Purpose

BT1242 proved that full-order four-transvection sets split into diameter 10, 12, and 14 word-metric regimes. BT1245 explains that split through local pair and triple closure data.

## Full-order regimes

Among the 61,560 full-order four-sets, the structural patterns are:

\[
\operatorname{diam}=10:\quad 22680\text{ sets in 3 patterns},
\]

\[
\operatorname{diam}=12:\quad 25920\text{ sets in 1 pattern},
\]

\[
\operatorname{diam}=14:\quad 12960\text{ sets in 1 pattern}.
\]

## Diagnostic rules

All full-order sets have span rank 4.

The diameter-10 regime is exactly the regime where all four triples already close to order 648.

The diameter-12 regime has pair closure pattern

\[
9^2 24^4
\]

and triple closure pattern

\[
72^1 648^3.
\]

The diameter-14 BT1228 / BT1233 regime has pair closure pattern

\[
9^3 24^3
\]

and triple closure pattern

\[
72^2 648^2.
\]

## Consequence

The diameter-14 fingerprint is the balanced local regime: three commuting/isotropic pairs and three noncommuting pairs, plus two weaker 72 triples and two 648 triples.  This explains why full order alone is not enough for tomography recovery.

## Files

- Code: `analysis/bt1245_four_transvection_structural_invariants.py`
- Result: `data/bt1245_four_transvection_structural_invariants_summary.json`
