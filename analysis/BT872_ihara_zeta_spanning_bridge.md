# BT872 — The Ihara Zeta of W(3,3), Verified, and Its Bridge to Spanning-Tree Gravity

**Status: PROVEN (direct 480×480 Hashimoto-operator computation, `analysis/bt872_ihara_zeta_spanning_bridge.py`, data `data/bt872_ihara_zeta_spanning_bridge.json`)**

w33_paper.tex's closed-form Ihara zeta theorem was derived "via Ihara–Bass."
BT872 verifies it *directly* by building the non-backtracking operator, and
discovers it is the same analytic object as BT870's discrete gravity.

## T1 — Direct Hashimoto verification

Building the 480×480 non-backtracking operator B on the 2|E| = 480 directed
edges and computing its full spectrum:

```text
B-spectrum: 11 (×1, Perron), +1 (×201), -1 (×200), and 78 complex eigenvalues
            (1 ± i√10 ×24 from θ=2;  -2 ± i√7 ×15 from θ=-4)
            — every complex eigenvalue has |u|² = 11 = k-1
```

This reproduces the closed form ζ⁻¹(u) = (1−u²)²⁰⁰(1−u)(1−11u)(1−2u+11u²)²⁴(1+4u+11u²)¹⁵
exactly (the ±1 multiplicities 200 = |E|−|V|; the Perron 11; the two complex
sectors), and confirms the **graph Riemann Hypothesis**: all nontrivial zeros
lie on |u| = 1/√11. The discriminants are substrate-primitive: Perron 100 = Φ₄²,
gauge −40 = −v, chiral −28 = −μΦ₆.

## T3 — The bridge: the Ihara zeta IS the spanning-tree gravity

The Ihara–Bass vertex form is ζ⁻¹(u) = (1−u²)^(|E|−|V|)·det(I − Au + (k−1)u²I).
**At u = 1** the Bass matrix becomes

```text
I − A + 11I = 12I − A = L  (the Laplacian, since W33 is 12-regular)
```

so the zeta vanishes at u=1 with det L = 0, and the Matrix-Tree theorem makes
the leading coefficient the spanning-tree count:

```text
∏(nonzero Laplacian eigenvalues) = 10²⁴·16¹⁵ = 2⁸⁴·5²⁴ = v · τ(W33) = 40·(2⁸¹·5²³)
```

So **BT870's discrete-gravity partition function τ = 2⁸¹·5²³ is exactly the
u=1 behavior of the Ihara zeta.** One analytic object, two physics readings:

- the **transport spectrum** (Hashimoto eigenvalues, non-backtracking walks,
  the gauge/chiral phases arctan√10 and π−arctan(√7/2)) — the *dynamics*;
- the **discrete gravity** (Matrix-Tree spanning-tree ensemble, τ = 2⁸¹·5²³,
  the matter-sector dimension in the exponent) — the *thermodynamics*.

The Ihara zeta unifies them: its nontrivial zeros (|u|=1/√11) govern transport,
its Perron zero (u=1) governs gravity. The prime p_Ih = 11 = k−1 is the
critical norm of the transport sector; the matter dimension q⁴ = 81 is the
entropy of the gravity sector — both written into the one zeta function.

## Reading

This is the deepest unification of the late session: the substrate's
"spectral ghost" 11 (Ihara prime, the |u|²=11 of every witness row) and its
"gravitational charge" 81 = q⁴ are the two ends — critical circle and Perron
point — of a single closed-form zeta. Transport and gravity are not analogies
bolted together; they are the off-critical and critical behavior of
ζ_{W(3,3)}.

## Open

- N_n closed-walk counts: N₃ = 960 = μ|E|, N₅ = 181440 = |E|·q^q·n_even
  (the paper's Prop) — verify Tr(Bⁿ) directly and read the substrate factors.
- The complement Q's Ihara zeta and its u=1 → τ(Q) = 2⁶⁶·3³⁹·5²³ bridge
  (gauge dimension in the exponent).
