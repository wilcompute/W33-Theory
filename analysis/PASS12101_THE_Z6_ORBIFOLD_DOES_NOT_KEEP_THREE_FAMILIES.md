# Pass 12101: the full Z6-II orbifold does not keep three families (negative)

Claude track. Tests 12091 and 12096–12097 beyond untwisted counting.

## Construction

Z6-II models on G2 × SU(3) × SU(2)² (orbifolder 1.2):

- **Shift.** A Klein-clock lift plus a three-family order-3 shift.
- **Wilson lines.** Order-2 lines carrying the second Klein clock and, optionally, the split σ.
- **Second E8.** Parts chosen for modular invariance.

## Results

1. **W33SO10.** Gauge group SO(10) × SU(2)³ × U(1)⁸, with **no 16 or 16̄ at all**. σ is odd on every spinor, so fermion
   parity imposed as a gauge Wilson line projects out all 16s.
2. **W33E6** (without σ). One 16 and one 16̄: net zero.
3. **Scan.** 36 models, 12 of them accepted by the orbifolder (24 rejected: "orbifold group ill-defined", so the
   modular-invariance filter is incomplete).
   - Every accepted model has net 16s or 27s in {0, ±1}; none has 3.
   - Every accepted model with σ has no spinors at all.

## Conclusion

The three families of 12091 and 12096–12097 are an untwisted, per-plane statement only. In these actual Z6-II
realisations, twisted sectors and projections remove them. A realisation with σ paired with spacetime (−1)^F (the
corpus non-SUSY route) is open.

## Certificates

- Producer: `analysis/w33_pass12101_the_z6_orbifold_does_not_keep_three_families.py`.
- Frozen spectra, models and drivers: `analysis/search_drivers_12101/`.
