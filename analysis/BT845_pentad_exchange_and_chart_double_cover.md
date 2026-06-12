# BT845 — Chiral Pentads, Maximal Partial Spreads, and the Chart Double Cover

**Status: PROVEN (machine-verified over all 432 cores, `analysis/bt845_pentad_exchange_and_chart_double_cover.py`, data `data/bt845_pentad_exchange_chart_cover.json`)**

Full census of all 216 pentad cores across the 36 schedules. One BT844 claim
corrected, three sharp theorems found.

## Correction (heals BT844)

BT844 inferred "216 distinct pentads, each serving exactly 2 cores" from
432 slots / orbit size 216. **FALSE.** The truth: there are **432 distinct
pentads**, each serving **exactly one** core. They fall into **two chiral
PSp-orbits of 216** (each with stabilizer of order 120), and **every core
pairs one LEFT pentad with one RIGHT pentad** (verified: the pair always
straddles the orbits — necessarily, since one orbit cannot fill 432 slots).
No wormholes: the exchange graph is just the 216 left–right pairings.
BT844's MD has been annotated; the paper theorem corrected.

## T4 — Pentads are MAXIMAL partial spreads

Each pentad (5 pairwise-disjoint lines, 20 points) extends to **zero** of the
36 schedules: no spread contains a pentad. These are maximal partial spreads
of size 5 — the substrate's canonical "stuck" constellations. (A schedule's
own 5-line subsets extend by definition; the pentads are precisely
*non-completable* half-spread analogues.)

## T3 — THE CHART DOUBLE COVER (the bullseye)

Each core's two pentads interlock as K₅,₅ minus a perfect matching (BT844).
The **deleted matching** consists of 5 **skew** line pairs — 5 hypercube
**charts** (each line of P₁ is skew to exactly 1 line of P₂). Census over all
216 cores:

```
216 cores × 5 charts = 1080 = 540 × 2
every one of the 540 charts is hit EXACTLY TWICE — none missed, none thrice
```

**The pentad cores' deleted matchings form an exact double cover of the
entire hypercube-chart atlas.** The routing fabric (BT773/777's 540 charts)
is readable off the icosahedral pentad compasses: each compass needle
carries 5 charts (an F₅ register of glue), and the whole atlas is recovered
with uniform multiplicity 2.

## The emerging dictionary

| object | count | stab | covers |
|---|---|---|---|
| schedules | 36 | S₆ (720) | each context 9× |
| duad cores | 216 | (S₅) | 2·K₁₀ = 6 Petersens per schedule |
| pentad cores | 216 | (S₅) | charts 2× via matchings |
| pentads | 216 + 216 chiral | order 120 | maximal partial spreads |
| all 12 cores/schedule | 432 | — | 4·K₁₀ = 12 Petersens |
| charts (skew pairs) | 540 | D₄·(…) | in 3 schedules, 6 Petersen homes, 2 matchings |

## Open

- Are the two chiral orbits swapped by the duality (outer automorphism), or
  is the chirality absolute (cf. the BT-era absolute-chirality result for
  W(E₆) torsors)? GAP check: does Out fix each 216-orbit?
- The pentad's 20 covered points / 20 uncovered points: relation to the
  pentad core's 20-line orbit and the [20,20] point signature of BT843.
- 5 charts per core = F₅ register: lift to the Clifford/photonic layer — do
  the 5 charts of one compass needle commute as routing operations?
