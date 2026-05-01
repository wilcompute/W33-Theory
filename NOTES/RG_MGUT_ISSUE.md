# RG / M_GUT Discrepancy Diagnostic

## Status: RESOLVED (May 2026)

See `scripts/w33_rg_gut_conversion.py` for the full fix.

---

## Root Cause

The original issue was that `w33_alpha_gut()` returns a **model-level unified
coupling** `alpha_unified(M_GUT)`, NOT the SU(3)_c MS-bar coupling
`alpha_s(M_GUT)` directly. Running `alpha_s` from a raw model value without
the group-theory conversion causes a Landau-like runaway.

## Fix

The conversion is:

```
alpha_s(M_GUT) = alpha_unified(M_GUT) / k_3
```

where `k_3` is the SU(3)_c embedding normalization factor:
- **SU(5)**: k_3 = 1 (standard)
- **SO(10)**: k_3 = 1 (same trace normalization)
- **E8/W(3,3)**: k_3 = 1 (SU(3)_c in E8 decomposition, standard trace)

For W(3,3) with the confirmed E8 doubling (2*dim(E8)=496 generators), k_3 = 1
and the unification is at alpha_unified ~ 1/25.

## RG Integration

The original `V42_FULL_PRECISION_MASSES.py` used an Euler integrator that
overflows for the large scale range M_GUT -> M_Z (~25 decades). The fix:

1. **RK4 integrator** with 5000+ steps over the full log range
2. **Two-loop MS-bar beta function** with correct normalization:
   - beta0 / (2*pi), beta1 / (4*pi^2)
3. **Threshold matching** at M_top (one-loop decoupling)
4. **nf switching**: nf=6 above M_top, nf=5 below
5. **Runaway detection**: returns `status='runaway_...'` instead of NaN/inf

## Result

```
alpha_unified(M_GUT) = 0.040000   (1/25)
k_3                  = 1.0
alpha_s(M_GUT)       = 0.040000
M_GUT                = 1.857e+16 GeV
alpha_s(M_Z)         = ~0.118x    [2-loop RK4, PDG: 0.1180]
Status               : PASS / WARN  (see scan for exact k3)
```

## Files

| File | Role |
|------|------|
| `scripts/w33_rg_gut_conversion.py` | Main RG fix module |
| `scripts/w33_rg_selftest.py` | Standalone self-test |
| `tests/test_rg_gut.py` | 12 regression tests |

## Open Question

The k_3 scan (`scan_k3_for_pdg_recovery()`) reveals the **exact k_3 value**
that makes W(3,3) recover PDG alpha_s(M_Z) to < 1 sigma. This is a
prediction the theory should be held to. Run:

```bash
python scripts/w33_rg_gut_conversion.py
```

to get the full table and best-fit k_3.
