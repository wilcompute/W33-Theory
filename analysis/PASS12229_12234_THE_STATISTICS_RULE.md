# Passes 12229–12234: the statistics rule of the twisted sectors

Claude track. Producer: `analysis/w33_pass12229_to_12234_the_statistics_rule.py`. Drivers:

- `analysis/search_drivers_12229/` (`vet58.py`, `z6ii_tens.py`)
- `analysis/search_drivers_12230/` (`selection.py` and the nsoq dumps)
- `analysis/search_drivers_12224/twoline3.py`

## 12230: the rule

In every sector the projection fixes **(P·V0 − R0) mod 1 = w/2**:

- P is the left momentum and V0 the Witten shift;
- R0 is the spacetime component of the right-mover;
- w is the Witten label.

It holds in all 30 sectors of five T6/Z3 models, both one-line and two-line, and R0 fixes the statistics in all 30.
Therefore **a state is a scalar exactly when P·V0 ≡ w/2.**

Every observed 10 obeys the rule:

| 10s | w | P·V0 | statistics |
|---|---|---|---|
| untwisted | 0 | ½ | fermion |
| twisted, one line | 1 | integer | fermion |
| twisted, two lines, Witten-untwisted | 0 | ½ | fermion |

With 12225 (all 4050 one-line twisted 10-type momenta have w = 1 and integral P·V0), **"no scalar 10 in any sector" is
a lattice theorem on the one-line admissible space.**

## 12231: two lines

Twenty thousand draws: 401 twisted-10 configurations (2.0%, 95% CI 1.8–2.2%) and **0 scalar-type**. This is a large
sample, decided on the lattice alone.

## 12229: the 58 three-generation models

They carry only scalar SU(5) singlets (11,952) and 5s (840). No representation can break SU(5) to the Standard Model.
This population closes.

## 12233: Z6-II

There are 134 non-free split-parity models with an A4 factor. Their 10s:

| kind | count |
|---|---|
| untwisted fermions | 106 |
| Witten-twisted fermions | 12 |
| **scalar 10s** | **54** |

**All 54 scalars belong to the hidden SU(5)** of one parent, SM_2496. Its SUSY gauge group is SU(5)×SU(3)×SU(2), with
quark doublets in (1, 3, 2). These scalars obey the rule (w = 0, P·V0 integral, R0 = 0). There is no visible scalar 10 on
Z6-II.

**Scope.** On Z6-II the constant phase holds in 12/12 sectors, but two Witten-twisted sectors carry bosons with R0 = ½.
There the statistics has to be read from the engine, not from R0.

## 12232

The main checkout was fast-forwarded. All ten blocking files were byte-identical to origin, or semantically identical
(formatting only), and they were backed up first.
