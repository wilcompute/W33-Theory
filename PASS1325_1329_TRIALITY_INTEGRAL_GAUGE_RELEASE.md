# Passes 1325–1329 Exact Release

This release executes the five frontiers opened after Passes 1320–1324:

1. globalization across the three conjugate 432 carriers;
2. integral/Smith reduction of the six transports and all 26 Hecke units;
3. species-20 normalizer and gauge-invariant classification;
4. length-7/8 primitive-cycle transport testing;
5. an independent reconstruction and formal GAP certificate.

## Headline results

- Three-carrier commutant: `H_26 ⊗ M3(C)`, dimension **234**.
- Triality-fixed commutant: `H_26 ⊕ H_26`, dimension **52**.
- Unsymmetrized common-support linking algebra: `3 M4(C) ⊕ M10(C)`, dimension **148**.
- Triality-equivariant common-support linking algebra:
  `3(M2(C)⊕C) ⊕ M4(C) ⊕ M3(C)`, dimension **40**.
- Six-channel Smith diagonal: **1,1,1,12,12,24**.
- Primitive 26-unit Hecke Smith diagonal:
  **1,1,1,1,1,2,2,2,2,2,2,2,4,12,12,12,12,24,24,24,48,144,288,864,4320,34560**.
- Exact bad primes of the Hecke unit lattice: **2,3,5**.
- Species-20 orthogonal idempotent normalizer: `W(B3)` of order **48**; orientation-preserving subgroup order **24**.
- Three-carrier independent gauge group: `S3 wr S3`, order **1296**.
- Length-7/8 species-20 transport blocks: **−I3** and **+I3**.
- No invariant primitive-cycle operator can distinguish the three species-20 copies.

## Validation

```bash
python analysis/w33_pass1325_1329_triality_integral_gauge.py
python analysis/w33_pass1329_independent_checker.py
pytest -q tests/test_w33_pass1325_1329.py
gap -q analysis/w33_pass1329_triality_integral_check.g
```

The local Python release completed with **8/8 focused tests passing**.  The GAP
certificate is included and wired into GitHub Actions; GAP was not installed in
the local execution container, so no local GAP result is claimed.
