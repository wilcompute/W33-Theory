# Passes 12223–12228: three-generation twisted-10 models, two lines, the parity character, translation-or-radius on T6/Z3

Claude track. Producer: `analysis/w33_pass12223_to_12228_twisted_tens_three_generations_and_radius.py`.
Drivers: `analysis/search_drivers_12223`–`12226`.

## 12223: generation content of the 153 twisted-10 models

| net (10, 5̄) | models |
|---|---|
| (±3, ±3) — three generations | 58 |
| (±6, ±6) | 95 |

All 153 are anomaly-free and tachyon-free and have scalar 5s. The twisted sectors contribute to the chiral 10s, so these
are three-generation models with families partly in twisted sectors. **There is still no scalar 10**, so the Wen–Witten
escape stays closed.

## 12224: two Wilson lines

**Sampling.** Naive random sampling never satisfies admissibility: one line passes only 0.65% of the time. The correct
procedure:

- draw each line from 12217's exhaustive admissible list;
- keep both lines in one of the 16 A4 classes per base;
- require 3·W1·W2 to be an integer.

**Density.** Twisted 10-type configurations make up **2.1%** of the space (63/3000; 95% CI 1.6–2.7%). That is 12× the
one-line density of 0.18%.

**Engine.** 9 of the 63 hits load, all SU(5)×U(1) and tachyon-free. Their 30 10-fields are all fermions:

| sector | fermion 10s |
|---|---|
| Witten-twisted | 14 |
| Witten-untwisted, twisted | 4 |
| untwisted | 12 |

There are **0 scalar 10s.** This is a sample, not a theorem.

## 12225: the parity character

All 4050 twisted 10-type massless momenta of the one-line class are Witten-twisted (w = 1) and have integral split-parity
character P·V0. The projection therefore sees a single left phase and selects one right-mover class. The engine reports
that class as fermionic in 153/153; the identification itself is inferred, not derived.

## 12226: translation or radius on T6/Z3

The lattice is (II(2,2) at ρ)³, checked for all 8 symmetric/asymmetric assignments:

- translations exist only on asymmetric planes;
- with the full 12×12 generalized metric (up to 18 invariant moduli, cross-plane ones included), **no translation lift
  changes length to first order**.

The reason, plane by plane: an asymmetric twist has no invariant Hom(V_L, V_R); a symmetric one has det(1 − g) = 9, which
is odd.

## 12227: cross-track

A continuity task (ticket) could not be filed, because task webhooks are a Pro feature. The question is logged as a
decision tagged cross-track, narain and codex.
