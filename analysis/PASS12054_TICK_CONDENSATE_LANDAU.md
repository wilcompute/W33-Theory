# Pass 12054: does the dynamics choose the tick? A Landau map on the forty points

* **Producer:** `analysis/w33_pass12054_tick_condensate_landau.py` (6/6 checks)
* **Certificate:** `data/w33_pass12054_tick_condensate_landau.json`
* **Regression:** `tests/test_w33_pass12054.py`
* **Track:** Claude. Reservation `f3d86ed30`.
* **Continues:** 12052 (Theorem 7.3) and 12053 (the tick is central).

## Model

**Order parameter.** phi lives in R^40, one amplitude per tick centre. The permutation module splits as 1 + 24 + 15
(adjacency eigenvalues 12, 2 and -4).

**Potential.** V = -r|phi|^2 + u|phi|^4 + beta sum phi_p^4 + gamma sum_{p~q} phi_p^2 phi_q^2. In the condensing irrep the
pattern minimises cos(theta) Q1 + sin(theta) Q2 on the unit sphere, with (beta, gamma) proportional to (cos, sin).

## Results

**The localising quartic picks one event.** At theta = 180 (beta < 0), the optimum in both irreps is the single-event
pattern P e_p. Its invariants are exact: V15 (35/216, 25/108) and V24 (197/540, 77/540).

**Phase map.**

| irrep | phases in order of theta |
|---|---|
| V15 | flat +-1 (20-sets) -> hyperbolic line -> transitional -> **single event** (136-243 deg) -> **staggered factorisation** (+1 on H1, -1 on H2; an exact eigenvector; invariants (1/8, 1/4)) -> flat |
| V24 | flat -> ... -> signed hyperbolic line (11/96, 7/96) -> **single event** (105.56-221.19 deg) -> isotropic line (73/360, 59/180) -> flat |

**Exact boundaries of the event phase.** Across each one, the optimiser switches pattern as predicted.

| boundary | tan theta_c |
|---|---|
| V15: event / staggered factorisation | **2**, i.e. gamma = 2 beta (both negative) |
| V24: event / isotropic line | 7/8 |
| V24: signed hyperbolic line / event | -1081/301 |

**Size of the event phase.** It covers about 30% of quartic space in either irrep (107.9 and 115.6 deg).

## Reading

**One time, without tuning.** A tick condensate with a localising single-site quartic picks **one event**: one tick
centre, hence (by 12052-12053) one time, with the tick central in its symmetry group. It does so over a wide region,
with no tuning.

**The split form is the neighbour.** In the 15-mode, the neighbouring phase is the staggered tensor factorisation, the
anchor of the split real form. So the clock/split dichotomy of Theorem 7.3 appears dynamically as two adjacent Landau
phases, separated exactly at gamma = 2 beta.

## Scope

* **Potential:** the two simplest quartics only.
* **Irreps:** one irrep at a time.
* **Couplings:** not derived.
* **Phase scan:** numerical, apart from the exact crossings. The lower edge of the V15 event phase is numerical (about
  135.5 deg).

## What is not new

Landau theory on permutation modules, and SRG spectra.
