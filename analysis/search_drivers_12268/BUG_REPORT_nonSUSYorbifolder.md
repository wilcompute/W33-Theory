# nonSUSYorbifolder 1.0: Wilson-line product conditions are never enforced

**Affected file:** `src/orbifolder/corbifoldgroup.cpp` (nonSUSYorbifolder-1.0). One additional site is in the same file.

## Summary

`COrbifoldGroup::CheckModularInvariance` computes the conditions

    gcd(N_i, N_j) (W_i · W_j) = 0 mod 2      (including i = j)

that is, Plöger–Ramos-Sánchez–Ratz–Vaudrevange, hep-th/0702176, eqs. (7e)/(7f). However, it sets `IsModularInvariant = false` only
inside a block guarded by `if (info) if (verbose)`. The local variable `verbose` is hard-coded to `false` (line 1067). As a result,
models violating these conditions are accepted silently, whatever `info` is set to.

The conditions between Wilson lines and shifts, `gcd(N, N_i) (V · W_i) = 0 mod 2`, **are** enforced. So are the shift conditions.

```cpp
if (!is_even(sp))
{
    if (info)
    if(verbose)
    {
        (*Print.out) << ... << " = 0 mod 2 failed!" << flush;
    IsModularInvariant = false;   // reached only when verbose == true
    }
}
```

`CRandomModel::Create` (around line 557) has the same pattern: an ill-defined orbifold group returns `false` only when `verbose` is
set, so the random generator can emit ill-defined models.

## Fix (minimal)

```cpp
if (!is_even(sp))
{
    if (info)
        (*Print.out) << ... << " = 0 mod 2 failed!" << flush;
    IsModularInvariant = false;
}
```

The full diff is `nonsusy_orbifolder_strict.patch` in this folder. It applies the same fix to the `CRandomModel::Create` site.

## Evidence

- **Reproducer:** a T6/(Z2^W × Z3) model with two order-3 Wilson lines on different tori and 3 W_1·W_5 = 1. The stock build loads it.
  The patched build rejects it with `3.00 W_1 x W_5 = 1.00 = 0 mod 2 failed!`. Files: `../search_drivers_12131/smwl4/N004_F1_03_S002_U219.txt`
  (rejected after the fix) and `..._U226.txt` (accepted by both builds).
- **Scale:** of 4514 T6/Z3 inputs, the stock build accepts 497 that violate (7f). The patched build rejects exactly those 497 and
  agrees with the stock build on every other input.

## Impact (measured)

**T6/Z3 with order-3 Wilson lines: spectra are unaffected in practice.** Each of the 497 inputs has a lattice-shift repair that is
consistent, and its spectrum is identical to the stock output: 983/983 repairs, comparing gauge group, U(1) directions, and every field
with its sector, fixed point, representation and charges.

**Order-2 Wilson lines (T6/Z2×Z2 tested): the stock output is not reliable.** For an order-2 input violating (7f), the stock spectrum
matches neither of two consistent repairs in 30/40 cases. The lattice representative of an order-2 line also changes the spectrum of
consistent models, in 41/80 cases; this is the mirage torsion of hep-th/0702176.

## Second, separate observation (patched orbifolder 1.2.1 used for N = 0)

A third-party N = 0 patch of orbifolder 1.2.1 drops every Witten-twisted fixed brane, because
`CFixedBrane::CreateMasslessHalfState` applies the local condition N(V_loc² − v_loc²) = 0 mod 2 there. This is not part of
nonSUSYorbifolder. It is noted because it explains disagreements between the two codes on Witten-twisted states.
