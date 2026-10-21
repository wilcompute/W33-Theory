# Passes 12156–12161: thresholds, the Fricke partner, a full-rules audit, and the Wen–Witten obstruction

Claude track. Producer: `analysis/w33_pass12156_to_12161_thresholds_fricke_audit_wenwitten.py`. Drivers and frozen
outputs: `analysis/search_drivers_12156/`.

## 12156: thresholds cannot rescue k_Y = 17/3

**The volume-growing thresholds are universal.** These are the β-sector, 10D-like thresholds.

- On every norm shell of E8, and of every SO(16) conjugacy class (0, v, s, c), the lattice sum of (p·y)² equals
  |y|²·count·N/8 exactly. That follows from Weyl irreducibility.
- So the charge-squared insertion is ∝ k_a, and the two SO(16) halves enter symmetrically.
- T⁶/Z3 has no N = 2 sectors, so there are no large moduli-dependent (Dixon–Kaplunovsky–Louis) thresholds either.

**Required non-universal threshold** at the heterotic scale, to reach the measured sin²θ_W:

| k_Y | Δ_Y − k_Y Δ_2 | fraction of the tree-level k_Y/α_U |
|---|---|---|
| 5/3 | −246 | 24% |
| 17/3 | −2636 | 77% |

The fraction-free route is closed. The canonical route needs a large, but not absurd, correction.

## 12157: the viable line is the corpus's — k_Y = 5/3 with fractional states lifted

- **Pass 11097** applied the full calibrated rules: gauge, Witten Z2, point group, space group, and H-momentum (exact at
  cubic, mod 3 at higher order). It found every fractional fermion massive in **33 of the 104** A8 models, with the
  hidden group unbroken.
- **Passes 11101/11102** narrowed these to **12 survivors** with a heavy top.
- In those survivors charm and up are degenerate, protected by an AG(3,3) reflection at all orders.
- Their vacuum (11106/11107): Λ > 0, rolling into a winding tachyon.

That is the line to push, not fraction-free hypercharges.

## 12158: the Fricke duality maps S002 to a partner with permuted degeneracies

Under T_WL → −1/(3 T_WL), the Witten-sector **level values** map exactly onto each other: all four levels below Δ = 0.3
agree to 10⁻⁹ at 0.52i and 0.641i. But two **multiplicities** are swapped: 272 ↔ 104 at Δ = 0.1519 and 0.1869.

| block | Fricke deviation at τ₂ = 2.5 |
|---|---|
| untwisted with β insertion | 6·10⁻⁸ |
| Witten-twisted | ~1% |

So the duality maps the model to a partner with the same levels and permuted degeneracies. That is why Λ is only
approximately invariant, while the lowest level, whose multiplicity is unchanged, is exactly invariant (12149, 12152).

## 12159: audit of 12121–12150 under the full rule set

| verdict | passes |
|---|---|
| valid (exact cubic H-momentum or an exact symmetry) | 12122, 12128, 12134, 12142, 12145, 12147 (\|V_tb\| = 1), 12148, 12153 |
| corrected in 12155 | 12133, 12146 (quartic lifts) |
| valid a fortiori | 12138's "protected" conclusion (extra rules only remove couplings) |
| **new correction** | 12147's "up rank 1 → 3 at quartic order" is **1 → 1** with H-momentum, in all 16 models |

Charm and up stay massless through quartic order. Compare the AG(3,3) protection of 11102.

## 12160: other geometries

Pass 11100 found only T⁶/Z3 tachyon-free with the W(3,3) shifts, on a sample. Nothing new was computed.

## 12161: Wen–Witten, and the SU(5) escape tested

**The theorem.** The 12150 congruence is an instance of **Wen and Witten (1985)**: a GUT broken by Wilson lines leaves
fractionally charged states. Schellekens (1990) generalised it. The escape is field-theoretic breaking at level 1:
flipped SU(5) broken by a 10_H, or Pati–Salam.

**The scan.** I drew second Wilson lines from the 864/6561 A4-type class (12125) on the e6+a2 bases.

- It gives 64 SU(5)×U(1) models.
- **22 have exactly three chiral generations** (net ±3 10 and 5̄). All 22 are tachyon-free and anomaly-free.
- **None has a scalar 10 (0/64).**
- The first one found, N001_F1_04_S023, has no 10_H and no 24.

So the SU(5) cannot be broken at level 1 on this route. The Wen–Witten obstruction is not sidestepped here.

## Overall position

- **Closed:** the fraction-free route (Weinberg angle), and the SU(5) escape on e6+a2 (no 10_H).
- **Open:** the corpus k_Y = 5/3 line (11097/11101: fractional states lifted, heavy top). Its open problems are the
  Weinberg-angle gap (a −246 threshold), the charm–up degeneracy, and the vacuum.
