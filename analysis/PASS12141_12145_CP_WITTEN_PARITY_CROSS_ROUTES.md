# Passes 12141–12145: CP and S002's B-field, Witten parity protecting T115's doublet, the twisted obstruction, T115's moduli, fraction-free models with one heavy top

Claude track. Producer: `analysis/w33_pass12141_to_12145_cp_witten_parity_cross_routes.py`. Drivers and frozen outputs:
`analysis/search_drivers_12141/`.

## 12141: S002's potential is CP-even; any CP-odd B-field gives a tachyon

**Symmetry.**

- Λ(−0.1 + 0.9i) = Λ(+0.1 + 0.9i) to every printed digit.
- The tachyon levels at ±0.1 + 0.55i are identical.
- T → −T̄ is CP acting on the modulus, so the imaginary axis is the CP-invariant locus.
- Context: CP is a gauge symmetry in string theory (Dine–Leigh–MacIntire 1992; Choi–Kaplan–Nelson 1993). So the
  potential must be CP-even, and Re T_WL is a CP-odd modulus.

**The lowest Witten-sector level on the axis** is a 56-state multiplet, the same one that is tachyonic at ρ.

| point | Δ |
|---|---|
| 0.9i | +0.033 |
| 0.55i (the potential minimum) | +0.00039 |
| 0.02 + 0.55i | −0.0099 |

The slope is about −0.5 in |Re T_WL|. So S002's minimum sits on the CP-invariant line, with that multiplet within
4·10⁻⁴ of being massless. **Any spontaneous CP violation through the B-field makes it tachyonic.**

## 12142: T115's light doublet is protected by Witten parity, to all orders

- Every SM-singlet scalar of T115 lies in the θ or θ² sector: 69 + 69 components, all with mm = 0.
- The block with structural rank 5 of 6 (12138) is the βθ sector (mm = 1): 4 R̄ doublets against 3 R.
- A mass term linking βθ to θ² fermions needs an odd total mm from mm = 0 vevs. That is forbidden at **every** order.

So one vector-like lepton doublet pair is exactly massless, as long as only SM-singlet vevs are switched on. It is a
light vector-like lepton doublet protected by an exact string symmetry.

## 12143: the obstruction to a fraction-free k_Y = 5/3 is the βθ sector

Every admissible root candidate (12131) was checked: 1060 in the 104 A8 models and 44 in the five e6+a2 models. 97 of
the A8 candidates even give the SM spectrum.

- None has a fractional **untwisted** state, as the lattice argument requires.
- **Every one has a fractional state in the βθ (Witten × θ) sector**: 1104 of 1104.

The obstruction is twisted, and universal across both routes.

## 12144: T115's moduli

| point | Λ/M⁴ |
|---|---|
| (2i, 2i, 2i) | 987.6 |
| (1.75i, 2i, 2i) | 862.2 |
| (2i, 2i, 1.75i) | 863.8 |
| (1.75i, 1.75i, 1.75i) | 663.8 |
| B-field Re T = 0.2 at 1.75i | 663.907 > 663.839 |

- The three tori act almost symmetrically.
- For T115 the CP-invariant axis is a **transverse minimum**, the opposite of S002.
- All these points are tachyon-free, including Re T = 0.1.
- T115 rolls only along the radius, into its tachyon onset between 1.75i and 1.5i.

## 12145: crossing the routes — fraction-free, three generations, one heavy top

**Method.** Take the fraction-free k_Y = 17/3 hypercharges of the A8 models (12139): 218 checked, across 81 models. All
have net 3 quark doublets. Recompute the quark sector under each one: vector-like mixing plus local tree-level Yukawas.

**Results.**

- **16 models acquire a single heavy up-type quark** (light up Yukawa of rank 1).
- 13 of them also have a single heavy down-type quark.
- Every case comes from mixing with a vector-like Y = 1/6 doublet (27/27). This is the S002 mechanism inside an A8 model.

These are fraction-free, three-generation models with one heavy top at renormalisable order.

**Caveats.**

- Ranks are evaluated at random couplings, which are upper bounds.
- Extra light d^c can remain at trilinear order.
- The models' one-loop vacua are not yet computed.
