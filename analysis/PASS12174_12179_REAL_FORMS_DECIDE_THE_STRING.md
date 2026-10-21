# Passes 12174–12179: the E8 real forms decide the string; 27 fixed points forbid Scherk–Schwarz

Claude track. Producer: `analysis/w33_pass12174_to_12179_real_forms_decide_the_string.py`. Drivers and frozen outputs:
`analysis/search_drivers_12174/` (`tenD.py`, `ss_translations.py`, `clockv0.py`, geometry files).

**Prior art.** The list of non-supersymmetric heterotic strings is classical (Kawai–Lewellen–Tye; Dixon–Harvey;
Alvarez-Gaumé–Ginsparg–Moore–Vafa). The corpus already had:

- the SO(16)² integral and its Bose–Fermi counts (11099);
- the observation that the corpus orbifolds use the split form (12084);
- Kramers squared = fermion parity (12085);
- the clock and split classes as 40×3 and 45×3 (12052).

What is new here is the classification by real form, the Scherk–Schwarz parity lemma on the W(3,3) geometries, and the
clock-Witten-shift theorem.

## 12174: real forms of the fermion parity

The parity is g = (−1)^F exp(2πi p·V), with V = (V1, V2) and each Vi in E8/2E8 = O⁺(8,2) of class 0, clock or split. The
partition function is built from its four blocks, with B11 defined as the T-image of B10.

| class | gauge | tachyons | n_B − n_F |
|---|---|---|---|
| 0 × 0 | E8×E8, supersymmetric (Z = 0) | – | 4032 − 4032 |
| split × 0 | E8×SO(16) | 16 | 3008 − 2048 |
| split × split | SO(16)² | **0** | 1984 − 4096 (= Pass 11099) |
| clock × clock | (E7×SU(2))² | 4 = (2,2) | 2240 − 3584 |
| clock × 0, clock × split | inconsistent: B10(τ+2) = −B10(τ) | | |

- The consistent cases close under T² to 10⁻¹⁵ and are S-invariant to 10⁻¹¹.
- **Consistency ⇔ Q(V1) = Q(V2).** These are the singular vectors of O⁺(16,2): 136² + 120² = 32,896 = 2¹⁵ + 2⁷ classes.
- **The only tachyon-free non-supersymmetric case is split × split:** a tensor factorisation of the two qutrits in each E8.
  A clock, the one-time event-anchored form, is consistent only paired with a second clock, and is then tachyonic.

## 12175: the tachyon is the class's minimal vector

The minimal norm over E8 + V is 0, ½ or 1 for the three classes:

- **clock:** ½, attained exactly by ±α/2, the clock's own root pair (its fibre over the event);
- **split:** 1, attained by sixteen vectors v/2.

A tachyon needs total norm 1, which only 0+split and clock+clock reach.

## 12176: Bose–Fermi counts

See the table above. Only the supersymmetric case has n_B = n_F.

## 12177: Scherk–Schwarz needs an even number of fixed points

An order-2 translation commuting with the point group is a common kernel of (M_g − 1) mod 2, computed exactly over F2.
For a cyclic twist this exists iff det(1 − θ), the number of fixed points, is even.

| W(3,3) families | det(1 − θ) | Scherk–Schwarz translation |
|---|---|---|
| Z3 | 27 | none |
| Z6-I, Z12-I | 3 | none |
| Z3×Z3, Z3×Z6, Z6×Z6, Z2×Z6-II | – | none |
| Z6-II (four lattices) | 12 | a 2-dimensional F2 space |
| Z2×Z6-I | – | a 2-dimensional F2 space |

Controls: Z4 (16 → 4), Z8-I (4 → 2), Z7 (7 → 0), Z2×Z2 (6).

**Consequence.** The T6/Z3 and Z6-I non-supersymmetric models cannot be interpolating (super-no-scale) models.
Λ4 = (V/3)Λ10 > 0 (11099) is forced.

## 12178: a clock Witten shift is tachyonic everywhere

On the A8 Kac base, 12,656 clock V0 = (α/2; β/2) are admissible, in three gauge classes:

| roots | gauge group |
|---|---|
| 78 | A5+A2 / A6 |
| 88 | A6+A1 / D5+2A1 |
| 96 | A5+A2 / D6 |

- All of them load in the engine.
- All are tachyonic at the orbifold point. The split control is tachyon-free there (A7 / A6).
- 12 representatives × 2000 random Wilson lines give **0/24,000** tachyon-free models.

**Mechanism.** The zero-winding Witten-sector state with p = V0 has p² = V0² = 1. Admissibility (V0·V1 and V0·W integral)
is exactly its invariance condition, and with no winding its mass does not depend on the moduli. So a clock Witten shift is
tachyonic on the whole moduli space of every T6/Z3 model.

## 12179: synthesis

The real form that the clock selects for time, E8(−24), cannot be the string's fermion parity without a tachyon. The
tachyon-free W(3,3) strings are forced onto the split form, and on T6/Z3 the 27 fixed points forbid interpolation to
supersymmetry.

The open lead is Scherk–Schwarz interpolation on Z6-II or Z2×Z6-I with a split Witten shift.
