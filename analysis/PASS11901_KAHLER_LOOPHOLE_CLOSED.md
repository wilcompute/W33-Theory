# Pass 11901: the Kähler escape route for m_c = m_u is closed in all 12 survivors

Producer: `analysis/w33_pass11901_kahler_loophole_closed.py`
Certificate: `data/w33_pass11901_kahler_loophole_closed.json`
Input: `data/w33_pass11103_alignments_hidden_unbroken.json` (frozen coupling data of Pass 11103)
Regression: `tests/test_w33_pass11901.py`
Track: Claude.

## Background

The 12 SO(16)×SO(16) A8 survivors (Passes 11095–11110) have m_c = m_u at tree level:
* Pass 11105 D derives it from Schur's lemma.
* Pass 11109 gets it from instanton Yukawas with diagonal moduli: m_c = m_u = m_t/2 at ρ.

Pass 11103 showed that no alignment of the SM-neutral scalar vacuum lifts it in the up sector. It left one escape
route open: "moduli-dependent Yukawa couplings".

Pass 11900 found that the off-diagonal Kähler moduli do split a light pair, at third order, but only when the
left-handed and right-handed fields sit at different points (a ≠ 0) of a Wilson-line torus.

## Result

| quantity | value |
|---|---|
| models / Higgs rows (up + down) | 12 / 72 |
| geo pattern (top, light, light) | **(0, 1, 1) in 72/72** |
| θ₍₊₁,₀,₀₎ vs θ₍₋₁,₀,₀₎ for random 3×3 Hermitian Z | relative difference ≤ 5·10⁻¹⁶ |
| control: θ₍₁,₁,₀₎ vs θ₍₂,₁,₀₎ (a ≠ 0) | relative difference 0.57–3.1 |
| top cost θ₍₀,ₐ₎/θ₍₀,₀₎ at Z = ρ, i, 2i | 0.5, 0.366 = (√3−1)/2, 0.045 |

Here geo is the number of tori on which the three fields are not at one point.

**What the geo pattern means.** On both Wilson-line tori, Q, u^c (or d^c) and H sit at the same point, so a = 0. Only
the family torus separates the light entries.

**Why the degeneracy then holds for every modulus.** The light entries are θ₍±1,0,0₎(Z) of the full T⁶/ℤ₃ Hermitian
Kähler matrix (all nine moduli). The instanton sum is even under x → −x on all three tori at once. So the two entries
are equal for every Z, and **m_c = m_u and m_s = m_d hold for every Kähler modulus**, off-diagonal ones included.
* This extends Pass 11109 (diagonal moduli) to the full Kähler sector.
* It closes the Kähler part of Pass 11103's escape route for renormalisable couplings.

**Normalisation cross-check.** This pass's Z equals Pass 11109's T. The ratios 0.366 at i, 0.045 at 2i and ½ at ρ
reproduce its table exactly.

## The price of escape

Splitting needs a ≠ 0 on some Wilson-line torus. The Wilson-line classes of Q, u^c and H are common to all three
families, so the same a enters the top coupling. The top then pays that torus's instanton factor θ₍₀,ₐ₎/θ₍₀,₀₎:
* ½ at the self-dual point;
* rapidly smaller at large area.

A light-pair split is therefore bought with a top suppression. **Scan criterion for future models:** a quark Yukawa
triangle that is not single-pointed on some Wilson-line torus, with that torus near its self-dual point.

## Not established

* **Scope.** Renormalisable twisted couplings only. Pass 11103 found a down-sector split through mixing with
  vector-like d̄ states, and that route is untouched here.
* **What remains open.** Non-perturbative effects and Higgs mixing across family-torus points (the Hesse states of
  Pass 11114) are not Kähler effects and remain open.
* **Survivors only.** The criterion has not yet been run over the wider scan.

## Prior art

* Corpus: 11102, 11103, 11105 D, 11109, 11114, 11900.
* Kobayashi–Nilles–Plöger–Raby–Ratz (hep-ph/0611020): Δ(54).
* Casas–Gómez–Muñoz (hep-th/9110060): Yukawa coset structure.
