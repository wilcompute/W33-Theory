# Passes 12351–12356: tachyon-free three-generation SO(16)×SO(16) Standard Models on Z6-II

> **Correction (Passes 12357–12362).** The radius statements below are withdrawn for large radii. The 6D theory of the
> θ²-fixed torus e5e6 has tachyons that the order-2 Wilson line W5 removes only at zero momentum. They carry half-integer e5
> momentum and return for R5 > √(3/8)·√α′. "Tachyon-free" here holds only at the orbifold point. See
> `PASS12357_12362_SUB_ORBIFOLDS_THRESHOLDS_VACUUM_PROTON.md`.

Claude track. Producer: `analysis/w33_pass12351_to_12356_tachyon_free_z6ii_standard_models.py`.

**Prior art (cited, not claimed).**

- **11095:** 104 tachyon-free three-generation SO(16)×SO(16) models on T6/Z3.
- **11100:** random draws on the other geometries found none tachyon-free and SM-like, "on this sample".
- **11096:** closed the (−1)^F-in-the-twist route; Z6-II is not in its list.
- **Parents:** the 12205 SUSY Z6-II A8 SMs, with their 12180/12281 non-SUSY V0 variants.

## 12351: hypercharge

The SUSY parents' hypercharge was fitted exactly as a 16-vector (residual 0, Y² = 5/6, so **k_Y = 5/3**) and applied to the 17
tachyon-free three-doublet parents.

- **SM_2618 (v0–v3) and SM_2913 (v6–v8): exactly three chiral Standard-Model generations**, with Tr Y = 0. The only extras are 4 pseudo-real
  (1,2)₀ doublets, which are vector-like among themselves.
- **SM_2503, SM_574, SM_1105:** chiral exotics; excluded.

## 12352: tachyons

- **At the orbifold point:** none in all seven (the engine's tachyon solver).
- **Small radii:** winding cosets reach the vacua, so winding tachyons are possible. They are closed for radii above roughly √2·√α′.
- **Large radii:** safe.

This is a necessary-condition analysis.

## 12353 / 12354: the spectrum

| | SM_2618 | **SM_2913** |
|---|---|---|
| n_F − n_B (massless) | +254 | +266 |
| Higgs scalars (1,2)_{±½} | 8 | 20 |
| fractional fermions liftable (gauge + full space-group rule) | 40/52 | **52/52** |

**Control:** with an e5 shift, 0 pairings survive. The vertex rule and the vacuum are not imposed.

**Renormalisable Yukawas (SM_2913_v6):** couplings exist in all three sectors. The structural ranks per Higgs are up 3, down 3, lepton 2,
but these are upper bounds; the hierarchy is open.

## 12355: closure statement

On Z6-II the SO(16)×SO(16) route does give **tachyon-free three-generation Standard Models with GUT-normalised hypercharge**: the SM_2913
lineage. This extends 11100's sampled negative.

**Open:**

- **Unification:** k_Y = 5/3 is not reached with the full spectrum above any common threshold (needed 0.32–1.28), the usual non-SUSY
  Weinberg-angle problem.
- the Yukawa hierarchy;
- proton operators;
- the singlet vacuum and the moduli.
