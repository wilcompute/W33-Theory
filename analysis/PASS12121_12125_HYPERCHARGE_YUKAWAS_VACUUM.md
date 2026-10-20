# Passes 12121–12125: hypercharge, Yukawas, vacuum energy and the gauge-group limit

Claude track. Producer: `analysis/w33_pass12121_to_12125_hypercharge_yukawas_vacuum.py`. Drivers and frozen outputs:
`analysis/search_drivers_12121/`. The field dumper `nsoq.cpp` prints, for every field of the non-SUSY engine, all
left-mover weights, right-mover weights, oscillators, the space-group element and the U(1) charges.

## Prior art (read first)

The corpus already contains a better result on the same geometry.

- **Pass 11095:** 104 tachyon-free, non-supersymmetric, three-generation Standard-Model-like models on T⁶/Z3. They use
  the W(3,3) A8 shift with SO(16)×SO(16) and have the canonical k_Y = 5/3.
- **Pass 11098:** their tree-level Yukawas. No model has a single heavy top.
- **Passes 11099 and 11106:** their one-loop vacuum energy. It is positive, and the volume runs away.
- **Literature:** SM-like tachyon-free SO(16)×SO(16) orbifolds are known in large numbers (Pérez-Martínez,
  Ramos-Sánchez, Vaudrevange, arXiv:2105.03460).

Passes 12111–12125 study a **different route**: the e6+a2 three-family shift, with the split fermion parity as the
Witten Z2. Read them as a comparison with 11095. "Three non-SUSY generations on T⁶/Z3" is not new.

## 12121: hypercharge

**Method.** An exact rational branch search over Y in span(U(1)s, SU(2)_R Cartan), with these constraints:

- (3,2) at ±1/6;
- colour triplets at the quark values;
- doublets at ±1/2.

**Result.** In each of the four left-right models of 12116 there are hypercharges (2, 29, 64 and 30 of them) under which
the net chiral spectrum is **exactly three SM generations**:

- every exotic is vector-like;
- every such Y is orthogonal to the anomalous U(1).

**Limit.** The normalisation is never canonical. The minimal k_Y = 2Y·Y is 25/3, 14/3, 13/3 and 11/3 in the four
models, against 5/3 in the A8 models of 11095. On gauge unification the A8 route is the better one.

## 12122: Yukawas

**Rules.** Gauge, Witten Z2, point group, space group, and H-momentum. The exact rule ΣR = 0 of 11098 and the weaker
mod-3 rule give identical quark results.

**No direct coupling.** The three chiral quark doublets form the untwisted three-plane triple. They have **no
gauge-invariant Q q^c H coupling** in any of the five models. This is decided by gauge invariance alone.

**Vector-like doublet.**

- Twisted U×T2×T1 Yukawas exist for the vector-like quark doublet: 15, 6, 0 and 6 in the four models.
- In S002, S033 and S053, an untwisted singlet coupling Q_chiral Q̄_vl S mixes that doublet into the light states.
- Exactly one light combination then carries all the quark Yukawas, so the **quark mass matrices have rank one** at
  renormalisable order.

**Per model.**

| model | mixed doublet couples to | consequence |
|---|---|---|
| S002 | u^c and d^c | one heavy up-type and one heavy down-type quark (top and bottom), the rest massless at this order |
| S033, S053 | d^c only | no up-type mass |
| S037 | — | no quark Yukawa |

Contrast with 11098: in the A8 models the top is degenerate with the charm, or all three are equally heavy, because
those models have no vector-like copies to mix with.

## 12123: vacuum energy

- Massless N_B − N_F < 0 in **all 75** loaded models of both scans, ranging from −454 to −186. The four left-right
  models have −390, −356, −320 and −284.
- 11099 fixed the normalisation: Λ₁₀ > 0 at N_B − N_F = −2112.
- So the large-volume term (Itoyama–Taylor, proportional to N_F − N_B) is **positive in every model**.
- There is no super-no-scale model (N_B = N_F), and the volume runs away as in 11099.

An apparent N_B = N_F = 0 model (T110, all-abelian gauge group) was a counting artefact: empty dimension strings were
skipped. It actually has −252.

## 12124 (negative): the second Wilson line in W(3,3)

- The colour A2 is an event fibre in 0/4 models; the baseline is 54/2160.
- SU(2)_L and SU(2)_R sit on collinear points (orthogonal fibres) in 3/4; the baseline is 1296/2160.
- The line is generic in W(3,3) terms.

## 12125: the gauge-group limit, and a direct SU(3)×SU(2)×U(1) model

**The limit.** Take every order-3 element λ/3 (6561 of them, λ ∈ E8 mod 3E8). On the so(10) of each of the seven base
models, it fixes one of the following:

| fixed algebra | elements |
|---|---|
| D5 | 27 |
| D4 | 270 |
| A1+A3 | 1080 |
| A1+A1+A2 | 2160 |
| A3 | 2160 |
| A4 | 864 |

This is so(10−2b)+u(b) (Kac). **A2+A1 never occurs**, so one extra Z3 line cannot give the SM group directly. The
statement is classical; here it is checked exhaustively.

**A third line.** I tried 120 candidates on the four left-right models; 56 load. One of them, **N008_F1_04_S037_T115**,
has:

- first-E8 gauge group **SU(3)×SU(2)×U(1)s**;
- net three quark doublets;
- no tachyons, and cancelled anomalies;
- 20 exact three-generation hypercharges, with k_Y ≥ 17/3.

It has **no quark Yukawa** at renormalisable order, because there is no vector-like doublet to mix with.
