# Passes 12298–12303: a pre-registered pass, a suspect tachyon label, and two lineages closed

Claude track. Producer: `analysis/w33_pass12298_to_12303_preregistered_torsion_levels_textures.py`.

## 12298: the corrected torsion rule, pre-registered

The test uses fresh Z4 models and a different shifted line: W1, on a torus that θ² rotates. The bicharacter, fixed-point labels
included, was evaluated on every commuting pair, and the predictions were committed and pushed (e570f4b1f) **before** any engine run.

**Score: 124/124.** All 32 predicted changes changed, and all 92 predicted identical were identical.

## 12299: what the engine calls a tachyon

**The level formulas, calibrated.** Left level P²/2 + N − 1 + δc and right level R²/2 − ½ + δc. Two parsing errors were fixed first:
oscillator frequencies are printed with a sign, and the O-line N= value is already the number-operator contribution. The controls then
pass: every massless-type state sits at (0, 0), 518/518 in one parent and 13,632/13,632 over 20 parents.

**The finding.** The engine's "excited tachyon" states (types 23/24, the ones its tachyonic configuration lists) also sit at (0, 0):
16/16 in SM_810's parent and 120/120 over 20 parents. No state with the genuine tachyon label (types 21/22) occurs anywhere in the
census.

**Suspected, not confirmed:** the engine's excited-tachyonic branch yields level-matched massless states. The code reading is
inconclusive. The tachyon condition is ½(q + v)² − c < 0 with c taken from the excitation's zero-point energy, and whether that includes
the right-moving oscillator still needs a verbose run.

**Consequences:**

- "Tachyon-free" in 12281/12286/12292 is restated as **free of states the engine labels excited tachyons**.
- The left-right candidate's parent is not tachyonic at this level either, so the tachyon criterion no longer distinguishes the
  candidate.
- Earlier corpus results that rely on this engine's tachyon labels should be audited.

## 12300: the candidate's fractional fermions under point-group rules

Adding the Z6-power and Witten-label rules leaves all 48 liftable. The control shows the rules are live: unit residuals lie outside
the lattice. The fixed-point translation rule is still open.

## 12301: textures of the Z2×Z6-I lineages

Exact minimal singlet degrees, as **lower bounds** (U(1) and R rule; the probe's sector index is not a twist power, so the sector rule
is dropped). Control: all six engine cubic couplings come out at degree 0.

| model | up | down | leptons | verdict |
|---|---|---|---|---|
| SM_2579 | two up quarks massless to degree 12 | none to degree 12 | — | **excluded** |
| SM_808 | top at tree level; charm ≥ 7 | ≥ 7 | tau at tree level; others ≥ 8 | needs ε ≈ 0.5 for m_b/m_t; **fails** in practice |

## 12302: the census extended to all 1399 non-SUSY Z6-II models

The left-right scan was rerun over every completed pair: see `search_drivers_12294/lr_census_all.json` and the round report.
