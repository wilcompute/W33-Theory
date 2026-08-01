# Passes 1887–1891 release

## Status

`PASS_WITH_WEIGHT6_AND_MIXED_ENUMERATOR_BOUNDARIES`

Aggregate certificate:

```text
4c280f57cadd9bef949b85af6c26bd4a21abbe17da8d6b0c09f0cf7575a5c4eb
```

The packet verifies **35/35** frozen assertions.

## Delivered

- **Pass 1887 — exact global fifth-order decoder.** The complementary fixed-coordinate/codeword census closes the previously open globalization problem:
  `U5 = 1,531,165,872`, with `4,747,680,912` ambiguous-minimum and `84,201,264` lower-shadowed weight-five errors. The corrected fifth-order term is `1531165872 p^5 (1-p)^235`. Weight six remains open at the singleton-component level.
- **Pass 1888 — refined separator enumerators.** The complete rank-30 fiber subcode has an exact 563-bin `(pair,phase)` enumerator over all `2^30` words. The rank-15 residual sector has 156 exact exceptional-S6 orbit records over all `2^15` assignments. The full mixed `2^45` refined contraction is not inferred from the marginals.
- **Pass 1889 — integral carrier gluing.** Each natural V9 copy has Gram Smith invariants `2,10,10,10,20,40,40,40,40`. The paired orthogonal rank-18 lattice carries an exact exceptional-S6-equivariant complex structure. Its half-integral enlargement index is `2^18`, which does not absorb the clock order's independent `2^35` maximal-order defect.
- **Pass 1890 — commutant and subgroup phases.** The exceptional-S6 commutant of `24+90` has dimension 23 and forbids a complex structure on the full carrier, while the paired V9 block admits one. Restriction to C4 gives commutant dimension 3260 and permits invariant complex structures on both sectors separately.
- **Pass 1891 — Tutte-Coxeter voltage carrier lift.** The 180 pair-transfer coordinates are exactly the nonincident syntheme-duad pairs. C4 fixes two of the 90 octagons, the 240-coordinate lift has 62 C4 orbits, and the natural V9 feeds the 36-dimensional `lambda=±2` Hashimoto channel.

## Exact decoder partition

```text
6,363,048,048
= 84,201,264 lower-shadowed
+ 1,531,165,872 globally unique minimum
+ 4,747,680,912 ambiguous minimum.
```

The prior Pass-1882 value `2,993,248,416` is superseded; it was the globalization upper bound obtained from fixed-coordinate chart singleton incidences.

## Boundaries

- The global fifth-order coefficient is exact.
- The weight-six equal-syndrome edge count is exact, but the weight-six singleton-component coefficient remains open.
- The two refined subcode enumerators are exact, but their full mixed `2^45` contraction remains open.
- Complex structures, C4 phases, voltages, and Hashimoto traces are finite representation/graph statements and do not define physical time or optical evolution.

## Primary artifacts

- `analysis/BT1887_1891_global_decoder_refined_gluing_voltage.md`
- `analysis/BT1891_global_decoder_refined_gluing_voltage_insert.tex`
- `analysis/w33_pass1887_1891_verify_frozen.py`
- `analysis/w33_pass1889_1891_algebra_voltage_verify.py`
- `analysis/cpp/w33_pass1887_weight10_degree.cpp`
- `analysis/cpp/w33_pass1887_exact_global_weight5.cpp`
- `analysis/cpp/w33_pass1888_fiber_bivariate.cpp`
- `analysis/w33_pass1888_residual_s6_refined_enumerator.py`
- `data/w33_pass1887_1891_five_frontiers.json`
- `tests/test_w33_pass1887_1891_five_frontiers.py`
- `.github/workflows/pass1887_1891_global_decoder_refined_gluing_voltage.yml`
