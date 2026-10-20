# Passes 12106–12110: realising the clock gradings as heterotic orbifolds

Claude track. Producer: `analysis/w33_pass12106_to_12110_orbifold_realisations.py`. Drivers and frozen engine outputs:
`analysis/search_drivers_12106/` and `analysis/search_drivers_12109/`.

## 12106: the non-SUSY realisation

**Setup.** A Z2W × Z3 orbifold, using the corpus N = 0 engine (nsdump_v2):

- V0 = (σ-lift; split-lift): the split fermion parity in both E8s, as in the corpus SO(16)² route;
- V1 = a three-family e6 + a2 shift.

**Control.** The stock Z3 model reproduces SO(10) × SU(3) × SO(16) × U(1) with a net 36 left-handed 16s.

**Results.** Of 24 models, 13 loaded.

- Every loaded model with an SO(10) × SU(3) factor (6 of them, in either E8) has **3 copies of (16, 3̄), i.e. a net 9
  chiral 16s**.
- The other 7 have no 16 at all.
- So the untwisted per-plane count (N = 3) survives the full orbifold, multiplied by the 3 untwisted planes. That gives
  three copies of a family triplet, **not three generations**.
- Tachyons were not checked: the engine dump has no tachyon code.

## 12107: where the family number lives

- **Non-SUSY:** the total equals the untwisted count, so the twisted sectors are vector-like.
- **SUSY Z6-II** (12101, re-counted with representation dimensions): the totals are 0 or ±1, so there the twisted
  sectors cancel the untwisted chirality.

## 12108 (open)

The 24 rejected Z6-II models satisfy every global and local level-matching condition I tested. The separating
condition is not yet identified.

## 12109: the corpus's Standard Models are clock/split gradings

All 87 distinct corpus Z6-I A8 Standard Models share one structure:

- the order-2 part of the shift is **one clock and one split** (one E8 each);
- the order-3 Wilson line is **e6 + a2** (three-family type) in both E8s.

## 12110: the (27, 6̄) Higgs cannot be massless at level 1

| Representation | h |
|---|---|
| 27 of E6 | 2/3 |
| 6̄ of SU(3) | 5/6 |
| (27, 6̄) | **3/2 > 1** |
| (27, 3) | 1 |

So family masses need higher-dimension operators or higher-level embeddings. This is the classical level-1 rule
(Font–Ibáñez–Quevedo; Dienes).
