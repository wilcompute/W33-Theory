# BT1716-BT1719 execution summary

Executed the three requested continuations plus the new genus-equation bridge.

## BT1716

Added `analysis/bt1716_q2025_domain_chart_extractor.py`.

The red and blue Figure-10 domains are encoded as two 24-item Pauli-code packets, using `0=I, 1=X, 2=Y, 3=Z` to avoid OCR and typography ambiguity. The verifier checks the 24/16/48 bus count and confirms that the BT1715 target is a 12-axis quotient over 16 shared cells.

Boundary: the 16 triples per color domain still have to be extracted from the figure/paper before claiming the exact Klein-Latin chart.

## BT1717

Added `analysis/bt1717_split_cayley_incidence_obstruction.py`.

The naive Fano-times-Hesse incidence cover has 63 points, 63 triples, and 189 incidences, but it splits into nine disconnected Fano components. Therefore the full split-Cayley functor needs a nontrivial Hesse/Fano monodromy twist; direct product incidence is falsified.

## BT1718

Added `analysis/bt1718_toroidal_coordinate_parser_scaffold.py`.

The parser scaffold records the invariant slots for the toroidal dual pair: Csaszar uses V=7, Szilassi uses F=7, both have 21-edge carriers, and the tetrahedral primal/dual seed has zero complete-graph genus numerator.

## BT1719

Added `analysis/bt1719.txt`.

The user's proposed link is exact arithmetically:

```text
12 = 4 + 4 + 4 axes,
16 cells * 3 axes per cell = 48,
(n-3)(n-4) at n=7 is 4*3 = 12,
(n-3)(n-4) at n=4 is 0,
(n-3)(n-4) at n=12 is 72 and C(12,2)=66.
```

Interpretation: the 12-axis bus is the denominator object, while the 3 axes per cell are the local triangular incidence. This connects the BT1715 48-bus directly to the two dual toroidal genus equations.
