# Passes 4849–4856 — CLOSED

Reserved collision-free at commit `aa5439c1253feefdc6e10cb4d0b89cf31e60e336`. A post-execution namespace search found no competing canonical Pass4849–4856 reservation or result packet.

All five queued fronts and all three outside-box probes were executed and frozen.

## Frozen evidence

- Passes 4849/4852/4854/4855/4856: `data/PART_W33_PASS4849_4852_4854_4855_4856_E6_KERNEL_CODE.json`
  - `K=[360,36,20]_2 = Cut(SRG(36,20,10,12)) + <sigma_E6>`;
  - 36 minimum carriers are exactly the cubic-surface double-sixes / projective E6 root pairs;
  - nontrivial switching coset minimum 120 with 25920 Weyl-chamber minima;
  - nonsplit one-dimensional characteristic-two extension;
  - dual `[360,324,3]_2` with 1080 minimum checks;
  - full automorphism order 51840, explicitly the conjugate `W(E6) ~= PGSp(4,3)` action.
- Pass4850: `data/PART_W33_PASS4850_LEVI_MINIMUM_ORBITAL_WEDDERBURN.json`
  - PSp orbital algebra `dim=59`, center `dim=15`, complex type `C^7 x M2^4 x M3^4`, rational center `Q^9 x Q(sqrt(-3))^3`;
  - PGSp orbital algebra `dim=49`, center `dim=13`, complex type `C^6 x M2^4 x M3^3`, rational center `Q^13`;
  - K3,3 incidence Gram is `3A0+A1+A5` and is noncentral.
- Pass4851: `data/PART_W33_PASS4851_CODE399_FULL_AUTOMORPHISM.json`
  - the residual `S3^45` sheet action is a genuine full-code symmetry, not a low-shell ambiguity;
  - full coordinate automorphism structure `(S4^405 x S3^135) : (S3^45 : PGSp(4,3))`.
- Pass4853: `data/PART_W33_PASS4853_TERNARY_INCIDENCE_GOLAY_TWISTED_LIFT.json`
  - 1080 Levi cycle lines span all 64 ternary Levi-homology dimensions;
  - 360 projective K3,3 witnesses span 54, leaving codimension 10;
  - no untwisted sign gauge factors the unweighted incidence to homology;
  - the correct PGSp-equivariant lift uses the oriented K3,3 double cover, rank54/kernel306.

## Reproducibility / integration

- Producers:
  - `analysis/w33_pass4849_4852_4854_4855_4856_e6_kernel_code.py`
  - `analysis/w33_pass4850_levi_minimum_orbital_wedderburn.py`
  - `analysis/w33_pass4851_code399_full_automorphism.py`
  - `analysis/w33_pass4853_ternary_incidence_golay_twisted_lift.py`
- Cross-certificate regression: `tests/test_w33_pass4849_4856_e6_kernel_orbital_twisted.py`.
- Exact-evidence workflow: `.github/workflows/w33_pass4849_4856_e6_kernel_orbital_twisted.yml`.
- Synthesis: `analysis/PASS4849_4856_EXECUTED_OUTCOMES.md`.
- Manuscript insert: `analysis/PASS4849_4856_e6_kernel_orbital_twisted_insert.tex`.
- Shared frontier manifest includes the new insert.
- Standalone public page: `docs/e6-kernel-double-six-incidence.html`.
- Root-index card/materializer sources: `analysis/PASS4849_4856_e6_kernel_index_insert.html` and `tools/integrate_pass4849_4856_public.py`.

Evidence boundary: all promoted statements are exact finite graph/root/group/code/homology results. Rational split-versus-division status of every noncommutative Pass4850 simple block remains open. The ten-dimensional ternary homology quotient outside the canonical K3,3 span remains unidentified. No physical E6 field or hardware claim is inferred.
