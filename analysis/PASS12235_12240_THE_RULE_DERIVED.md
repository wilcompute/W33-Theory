# Passes 12235–12240: the statistics rule derived

Claude track. Producer: `analysis/w33_pass12235_to_12240_the_rule_derived.py`.

## 12235: the derivation

The Witten element g = (V0, s0) acts trivially on T6. On a state of sector h = (w, n, m_a), its projection phase gives

  (P·V0 − R0) = ½(w(V0² − 1) + n·V1·V0 + Σ m_a·W_a·V0) mod 1.

With V0² = 2, this equals **w/2 exactly when every product of V0 with the shifts and Wilson lines is even.**

**Parity.** Evenness is not automatic: 65,659 of the 231,124 one-line admissible configurations have V0·W odd. There the
constant would depend on whether a fixed-point label is written 1 or −2, so the projection is ill-defined. The engine
agrees:

- every odd-parity configuration fails to load (111/111 one-line, 36/36 two-line);
- every model that loads has even parity.

**Conclusion.** On every consistent model the rule "scalar iff P·V0 ≡ w/2" is derived, not fitted.

## 12236: two lines

Three seeds of 20,000 draws each: 1,227 twisted-10 configurations and **0 scalar-type**. This is decided on the lattice
alone.

## 12237: the A8 route

Three SO(16)² Standard Models from 11095:

- the constant is w/2 in 18/18 sectors;
- R0 fixes the statistics;
- V0² = 2, and all products are even (0 or 2).

So the rule covers their Higgs doublets.

## 12238: the hidden SU(5) of SM_2496

| V0s | hidden SU(5) | scalar 10s | n_B − n_F |
|---|---|---|---|
| 9 V0 | unbroken | massless, in the unpaired θ², θ⁴ sectors; survive at large radius | 144 |
| 11 V0 | broken to A2+A1 (one A3) | none | 48 |

The second pattern is the one a 10 vev would produce. This is an observation; the condensation is not computed. The
parent keeps at most two generations at large radius.

## 12239: paper

The Section 7 boundary now states the scope of the rule:

- derived on consistent models with even products;
- on Z6-II, R0 does not fix the statistics in two Witten-twisted sectors.
