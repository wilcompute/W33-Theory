# Full-byte changed revision audit after PR324

Baseline: 9e2f9b9e859ee4d7b39555c0052886653a90e3be
HEAD: 3b8f728dd45289e77e11bc3196576077d7eb4643
Complete commit messages: 43. Full versioned blobs: 190, 21938365 bytes.
Whole final changed files: 112, 4320465 bytes.
Full commit text and per-blob SHA256 hashes and Python/JSON parse checks in data/toe_20261109_postpr324_fullbyte_audit.json.
Parsed revision classes: {'Python': 58, 'Text': 5, 'Markdown': 50, 'JSON': 77}. Errors: 0.
This is a lossless structural audit, not a semantic certification of mathematical or physical results.

## Entire intervening commit list

- af2bcab7e23a | 1 blobs | Regression guard for the CLASS halofit scalar-field bug: patched class_fading_hf and class_massive_hf must match plain Lambda for LCDM-as-scf (<1e-5), unpatched must still differ (>25%, control); runs only with RUN_CLASS_TESTS=1 (WSL builds
- 25817b5f189d | 5 blobs | Merge remote-tracking branch 'origin/master' into HEAD
- 30f390f1439b | 4 blobs | Replay withdrawn S8 arithmetic from archived Halofit inputs
- 72081a475ef2 | 12 blobs | Resolve native short-face magnetic obstruction with an invariant positive completion
- a49a1e97e72f | 14 blobs | Certify the full signed cubic stabilizer and a three-copy vacuum
- 3a43e7a4ff44 | 2 blobs | Pass 12631 addendum: KLT BAO-held MCMC elpd -9.73 vs LCDM -11.47 (+1.74; between Fisher std -0.40 and double +2.75); KLT expansion total +3.7 vs fading +5.7, CPL +5.5; method spread ~1 (fading desy5 MCMC vs Fisher). GitKraken MCP unavailabl
- 84f21f0a9a17 | 28 blobs | Merge remote-tracking branch 'origin/master' into HEAD
- 320b40024e1a | 7 blobs | Transport the Albert half-turn and isolate the three-copy vacuum
- 34504b8794e1 | 3 blobs | Verify qutrit magic from compressed Albert matter parity
- 6bb87db0719b | 2 blobs | Pass 12631 addendum: KLT f-scan on patched build: f=0.35 chi2 2252.50 (-1.07 vs f=0.25), f=0.18 and 0.5 shooting failed; data do not push f down; quality side N >~ 160-200. GitKraken MCP unavailable; shell git used.
- 10ff0f6a5885 | 9 blobs | Merge remote-tracking branch 'origin/master' into HEAD
- 5d3010786370 | 8 blobs | Pass 12632 addendum 6: corrected combined out-of-sample ledger (Dovekie; BAO, SN, DES, KiDS held out): fading +4.16, CPL +3.79, KLT +1.97 over LCDM (withdrawn: fading +4.72, CPL +0.32); corrected held-out shear DES -0.69/-0.38/-0.68/-0.80,
- ce98cdbe29e0 | 3 blobs | Pass 12632: DES-SN5YR-trained held-out DES shear corrected (fading -0.74, CPL -0.62 vs LCDM; was -0.42/-2.05); totals fading +6.44, CPL +8.84: leader follows the SN sample, not shear. GitKraken MCP unavailable; shell git used.
- 75cf2141d9d0 | 2 blobs | Pass 12632 addendum 7: patched refit: LCDM-as-scf now 2238.114 = LCDM_native 2238.11 (the old 0.39 gap was the bug); full-data gains shift <= 0.4 (fading -10.79, CPL -12.27, exp -3.75). GitKraken MCP unavailable; shell git used.
- 41abb5cb935d | 0 blobs | Pass 12634 reserved: W(3,3) in the tropical moduli space of cubic surfaces (Naruki fan) (claude track)
- 991a2067160e | 5 blobs | Pass 12634: W(3,3) in the tropical moduli space of cubic surfaces (Naruki fan): reconstruction (36 roots + 40 A2^3; orthogonal sets + flags) reproduces f-vector (76,630,1620,1215) exactly; cusp rays collinear iff stars share no root -> SRG(
- c0735cec7fd6 | 3 blobs | Pass 12634 addendum: E6 pezzotopes (432 positive-geometry regions of cubic-surface moduli, arXiv:2306.13604) = S5-pentads of pairwise disjoint W(3,3) lines with unique triple roots: exactly 432 of 13824 disjoint 5-sets; all 432 induce fan f
- 9f82e8fea481 | 3 blobs | Pass 12634 addendum 2: E6 Bergman fan (750 connected flats recomputed) maps under the root/A2^3 incidence matrix into the reconstructed Naruki fan with no exceptions: A1->(a), A2->(b) = the W(3,3) line, A3->aa 2-cones (1:1, 270), A4/A5->(a)
- a4efdd37e9cd | 0 blobs | Pass 12635 reserved: tropical Burkhardt fan = W(3,3) points + 45 splits; duality with the Naruki fan (claude track)
- 8415258b8112 | 4 blobs | Pass 12635: tropical Burkhardt (= trop A2(3), corpus flavour modulus; Ren-Sam-Schrader-Sturmfels Thm 4.3) reconstructed in W(3,3) terms: (a) rays = 40 W(3,3) POINTS, (b) = 45 tensor splits; aa = 240 collinear pairs, aaa = 160 line triples,
- 57a4c02a3054 | 3 blobs | Pass 12635 addendum: explicit dictionary between the two tropical fans: via a VF2 isomorphism A2^3 -> W(3,3) lines, 36 roots <-> 36 spreads (each root's 10 A2^3 = a spread), 40 points <-> partitions of the 36 positive roots into four A2^3,
- 2075b52ee477 | 3 blobs | Pass 12634 addendum 3: every E6 pezzotope = a double-six (12 lines = the 12 Hamiltonian 5-cycles of K5, sixes = the two A5 orbits; exotic S5 in S6) whose 5 cube facets are a synthematic total; the 432 positive-geometry regions double-cover
- c55bcb85c2e6 | 3 blobs | Pass 12634 addendum 4: prior art for addendum 3 cited (P12523 totals/12+15/codewords; BT844/BT845 432 pentads in two chiral orbits; BT837 cores). New: the 432 E6 pezzotopes (positive-geometry regions of real cubic-surface moduli) = exactly
- b00a35e6efb7 | 0 blobs | Pass 12636 reserved: unextendible two-qutrit MUBs = cubic-surface geometry; chiral pezzotope pairs = codewords (claude track)
- 68c5fde40618 | 5 blobs | Pass 12636: maximal partial spreads of W(3,3) (= weakly unextendible two-qutrit Pauli MUB sets; Hilbert check: unbiased <=> disjoint on all 780 pairs) have exactly sizes 10/8/5 with counts 36/135/432 = roots / aaaa cones (orthogonal frames,
- 2fc6db548317 | 3 blobs | Pass 12636 addendum (negative): E7 rung test: maximal partial spreads of W(5,2) (3-qubit Pauli UMUBs) = 960 spreads (stab 1512) + 24192 size-5 (stab A5); no orbit 60480, so E7 pezzotopes are not 3-qubit UMUB sets; E6 identification does not
- 3776e1a0e1a1 | 1 blobs | Pass 12636: fix garbled sentence in E7 addendum. GitKraken MCP unavailable this session; shell git used.
- 76da3c2eaea6 | 3 blobs | Pass 12635 addendum: level ladder: level-2 (Segre/Igusa) tropical fans are affinely isomorphic (RSSS Thm 2.4), reconstructed: 25 rays, 105 edges (45 duad-duad = doily SRG(15,6,1,3)), 105 cones; doily point and line graphs isomorphic (self-d
- 779cc43baffa | 6 blobs | Certify integral Yoshida fibers and label the real pezzotope regions
- 771410e3bdd8 | 3 blobs | Recover the binary cusp adjacency code from real chamber transitions
- adacccd3d720 | 1 blobs | Index the Yoshida cone and pezzotope sign certificates
- 21bb7b2114be | 3 blobs | Pass 12636 addendum 2: the 135 size-8 unextendible MUB sets map 3-to-1 onto the 45 tensor splits; for every split the 24 maximally entangled stabiliser bases (P11143) are exactly the disjoint union of its three 8-sets (all 45). Cites Codex'
- f41f2d2ee539 | 3 blobs | Pass 12636 addendum 3: pezzotope amplitude: on every root (double-six) facet the residue is the 6-particle phi^3 tree amplitude with the 3 cusp facets (two-qutrit contexts) = 3-particle channels (long hexagon diagonals) and 6 orthogonal roo
- 3dd4b78cb004 | 4 blobs | Compare chiral pezzotope canonical forms and their Kummer characters
- 3984dbce4652 | 3 blobs | Replay the coarsened pezzotope face lattice and index the result
- 6bdb21f397ff | 0 blobs | Pass 12637 reserved: six particles of the double-six amplitude, hidden zeros, strong unextendibility, triality, region graph, E7 and q=5 (claude track)
- 88c504a7ae6e | 3 blobs | Certify canonical Standard Model flatness obstruction and chiral repair
- 767cdd3e2e4d | 3 blobs | Bound the mass rank for all compatible renormalizable couplings
- 9b129a727369 | 3 blobs | Lift the adjoint and anomaly spectator at the exact Standard Model vacuum
- ac5a4fd5058e | 3 blobs | Resolve the repaired vacuum into exact Standard Model multiplets
- 6b642d5dc92e | 16 blobs | Pass 12637: six particles of each double-six facet amplitude = the six lines of a six in cyclic order (4320/4320; residue zeros 1200/1200); hidden zeros do not lift (44 single-point hits all failed re-test); pentads numerically STRONGLY une
- 5a005197ff49 | 3 blobs | Merge remote-tracking branch 'origin/master' into HEAD
- 3b8f728dd452 | 0 blobs | Pass 12638 reserved: exact strong-unextendibility certificate, cube channels, triality/chirality element, E7 facets, cross-rung (claude track)

## Every final changed file

- RESULTS_INDEX.md | 2670294 bytes | 18810 lines | 0966fbc90d440305ad34 | Markdown
- TOPICAL_ALIASES.md | 360136 bytes | 1301 lines | 142e496f7345774626dc | Markdown
- analysis/2026-07-15_pass84_e6_w33_explicit_iso.md | 5282 bytes | 151 lines | 08fa85af66364fd874f6 | Markdown
- analysis/2026-11-08_exact_signed_cubic_and_three_copy_vacuum.md | 7823 bytes | 50 lines | 8d9438a9da4427bf1621 | Markdown
- analysis/2026-11-08_invariant_magnetic_cone_completion.md | 10959 bytes | 80 lines | 96a178b47e274abb44b2 | Markdown
- analysis/2026-11-08_native_halfturn_and_species_orientation.md | 6885 bytes | 31 lines | 5ca82dc9d1555fd81e8b | Markdown
- analysis/2026-11-09_canonical_sm_flatness.md | 10910 bytes | 53 lines | ada735f822330253feff | Markdown
- analysis/2026-11-09_pezzotope_canonical_reflection.md | 7328 bytes | 44 lines | 0cddd16cdccbb1b61fd2 | Markdown
- analysis/2026-11-09_yoshida_integral_fibers_and_chirality.md | 10618 bytes | 50 lines | 670baf13ad322a3ec127 | Markdown
- analysis/HANDOFF_CLAUDE_TO_CHAT_20261106.md | 9106 bytes | 62 lines | 8d5d8d50bc012efc53b1 | Markdown
- analysis/NOTE_DARK_ENERGY_EVIDENCE_20261108.md | 4601 bytes | 42 lines | a81484d0d9ca6d902c2c | Markdown
- analysis/NOTE_TWO_QUTRIT_UNEXTENDIBLE_MUBS.md | 4014 bytes | 56 lines | 2d888d69d9cf03a2e73e | Markdown
- analysis/PASS12631_KIDS_HELDOUT.md | 12429 bytes | 147 lines | 2a6c0d692b0b1a3a7d3b | Markdown
- analysis/PASS12632_HALOFIT_SCF_BUG.md | 14692 bytes | 189 lines | 4022b2c6c0c065025b89 | Markdown
- analysis/PASS12634_NARUKI_FAN.md | 13962 bytes | 128 lines | 0a0f57914ce6f1ea2ae5 | Markdown
- analysis/PASS12635_BURKHARDT_FAN.md | 7335 bytes | 85 lines | d475ab897156d9e314ef | Markdown
- analysis/PASS12636_UMUB_CUBIC_SURFACES.md | 8468 bytes | 87 lines | def8fcf075fd8bf2ab3a | Markdown
- analysis/PASS12637_SIX_PARTICLES_TRIALITY.md | 4966 bytes | 65 lines | 4296ffcb0fc84ee8d4de | Markdown
- analysis/toe_20261108_exact_signed_cubic_stabilizer.py | 10838 bytes | 230 lines | e585f163c0d630103844 | Python
- analysis/toe_20261108_invariant_magnetic_completion.py | 13598 bytes | 217 lines | faf7023044f899b2c89c | Python
- analysis/toe_20261108_invariant_magnetic_server.js | 2199 bytes | 27 lines | d8a8aa440f030b7054bb | Text
- analysis/toe_20261108_native_spin_halfturn.py | 7222 bytes | 161 lines | 3e07ac995a702fe29d4c | Python
- analysis/toe_20261108_signed_cubic_server.js | 3068 bytes | 67 lines | 522adc98bc0ee5cdc09e | Text
- analysis/toe_20261108_species_orientation_selector.py | 6294 bytes | 143 lines | 8c01099af36d822ccfbc | Python
- analysis/toe_20261108_three_copy_cubic_vacuum.py | 10541 bytes | 210 lines | 39b093ebbb644574899e | Python
- analysis/toe_20261109_canonical_sm_flatness.py | 18554 bytes | 353 lines | fb83ad0b542d0e9580fc | Python
- analysis/toe_20261109_pezzotope_canonical_partner.py | 18405 bytes | 429 lines | 4814b2c61114f9fcf6d2 | Python
- analysis/toe_20261109_real_yoshida_pezzotope_labels.py | 7701 bytes | 165 lines | d53cb9e2c75e229b8e49 | Python
- analysis/toe_20261109_yoshida_cone_census.py | 19467 bytes | 459 lines | 0ea511ed0b09aa33e5bd | Python
- analysis/toe_uv/hf_refit_dovekie.json | 3289 bytes | 135 lines | ee6edf590e8338315593 | JSON
- analysis/toe_uv/klt_fscan.json | 802 bytes | 26 lines | e52174cc3741f8e2d080 | JSON
- analysis/toe_uv/mcmc_dovekie_bao_klt25.json | 1080 bytes | 49 lines | be6fe8905de94094344f | JSON
- analysis/toe_uv/scorecard.json | 2789 bytes | 76 lines | 67b88a8832c808b69eda | JSON
- analysis/toe_uv/scorecard.py | 5252 bytes | 85 lines | fc770b47c5176b514cd6 | Python
- analysis/toe_uv/shear_ppd.json | 1290 bytes | 74 lines | 12cb36558da95cfb1f62 | JSON
- analysis/toe_uv/shear_ppd_desy5.json | 1017 bytes | 59 lines | c195e1fe30967baa380c | JSON
- analysis/toe_uv/shear_ppd_kids_dovekie.json | 1289 bytes | 74 lines | 87334fe01516a762629c | JSON
- analysis/w33_20261108_s8_hybrid_shapley_audit.py | 4772 bytes | 83 lines | ca37937a1bd73f02a371 | Python
- analysis/w33_bergman_to_naruki.py | 5410 bytes | 127 lines | b7743ecdc458f96ecfd2 | Python
- analysis/w33_e7_orbit_census.py | 2856 bytes | 51 lines | 9d54933cb01b624394b6 | Python
- analysis/w33_e7_rung_mubs.py | 3175 bytes | 68 lines | 4eb7ee4f8aebe1eb06fe | Python
- analysis/w33_e7_scalene.py | 4324 bytes | 87 lines | cda3aeeff6060c4b5e66 | Python
- analysis/w33_level2_ladder.py | 3397 bytes | 42 lines | 7fa9261778bb082fd6fd | Python
- analysis/w33_pass10950_clock_albert_lorentz_spinor.py | 23703 bytes | 528 lines | 22a29ab73d04bdb42b54 | Python
- analysis/w33_pass12634_naruki_fan.py | 10005 bytes | 195 lines | 73c3f108ddd2ce13b26e | Python
- analysis/w33_pass12635_burkhardt_fan.py | 4680 bytes | 77 lines | 6e6f3b499daa10a4063f | Python
- analysis/w33_pentad_strong_umub.py | 2894 bytes | 53 lines | 36beaed2627d0efef682 | Python
- analysis/w33_pentad_umub.py | 5744 bytes | 105 lines | 58c5930e3eda5d790396 | Python
- analysis/w33_pezzotope_amplitude.py | 3614 bytes | 58 lines | 6cc5d5e0119f338a8994 | Python
- analysis/w33_pezzotope_check.py | 4799 bytes | 92 lines | 5a14109b05738721656a | Python
- analysis/w33_pezzotope_chirality.py | 4543 bytes | 85 lines | 293e12fc08303344648c | Python
- analysis/w33_pezzotope_gosset.py | 10171 bytes | 183 lines | b1b3c30cbb56dc260f9a | Python
- analysis/w33_pezzotope_hidden_zeros.py | 10533 bytes | 199 lines | c0cc57790a9c646a113c | Python
- analysis/w33_pezzotope_reflection.py | 4276 bytes | 69 lines | 28afaa2940108911eb57 | Python
- analysis/w33_q_ladder.py | 2735 bytes | 48 lines | 6ef7cb76026eec9ad39a | Python
- analysis/w33_six_particles.py | 6782 bytes | 102 lines | 5bad6871ab815328ac7d | Python
- analysis/w33_size8_splits.py | 3423 bytes | 57 lines | 2321e70d742a2c74ad84 | Python
- analysis/w33_split_bridge.py | 6609 bytes | 109 lines | b800b2067516b7e1e4cd | Python
- analysis/w33_split_triality.py | 5055 bytes | 86 lines | 5fa689e65308946db5e7 | Python
- data/toe_20261108_exact_signed_cubic_stabilizer.json | 48356 bytes | 3561 lines | 35ae15909d9cea51e549 | JSON
- data/toe_20261108_halfturn_orientation_validation.json | 8604 bytes | 352 lines | 0eeba547b2025345ddbc | JSON
- data/toe_20261108_invariant_magnetic_completion.json | 151212 bytes | 11334 lines | 5351f1b5905063b0a018 | JSON
- data/toe_20261108_invariant_magnetic_guard_audit.json | 25337 bytes | 337 lines | 5d6bf79ef1d193a75931 | JSON
- data/toe_20261108_invariant_magnetic_intake.json | 3199 bytes | 52 lines | 9281db9eac1bfb4a964d | JSON
- data/toe_20261108_invariant_magnetic_publication_manifest.json | 130741 bytes | 2308 lines | 5377460e3351db22c2e5 | JSON
- data/toe_20261108_invariant_magnetic_server.json | 4750 bytes | 247 lines | e856f068099eb17b3f7a | JSON
- data/toe_20261108_invariant_magnetic_validation.json | 6722 bytes | 44 lines | 0fa3613b30c29c28b1da | JSON
- data/toe_20261108_native_spin_halfturn.json | 6594 bytes | 528 lines | 8aff6fadd229f9f34059 | JSON
- data/toe_20261108_signed_cubic_guard_audit.json | 32078 bytes | 363 lines | 8e2d3d271b49ae0c4940 | JSON
- data/toe_20261108_signed_cubic_intake.json | 2009 bytes | 44 lines | 4170b69034ebc15995f8 | JSON
- data/toe_20261108_signed_cubic_publication_manifest.json | 38824 bytes | 392 lines | 4c84c412e55f7c8464c7 | JSON
- data/toe_20261108_signed_cubic_server.json | 673 bytes | 38 lines | 117608e0ee5a67708cda | JSON
- data/toe_20261108_signed_cubic_validation.json | 3988 bytes | 60 lines | 6b98c307b6027a3ead2d | JSON
- data/toe_20261108_species_orientation_selector.json | 6337 bytes | 387 lines | 91939b107ee9908e0f76 | JSON
- data/toe_20261108_three_copy_cubic_vacuum.json | 3556 bytes | 164 lines | 664bf686ac3914a3a307 | JSON
- data/toe_20261109_canonical_sm_flatness.json | 12890 bytes | 657 lines | 99dae68244b3e6134080 | JSON
- data/toe_20261109_pezzotope_canonical_partner.json | 63891 bytes | 4770 lines | a1cc4b3442c7b6024ec9 | JSON
- data/toe_20261109_pezzotope_canonical_validation.json | 3436 bytes | 96 lines | 01abdaa4f3c881ae8208 | JSON
- data/toe_20261109_real_yoshida_pezzotope_labels.json | 187411 bytes | 12080 lines | 1d08a8ed3c698e5b3790 | JSON
- data/toe_20261109_yoshida_cone_census.json | 14088 bytes | 1262 lines | 72b63dfbb71242a67d31 | JSON
- data/toe_20261109_yoshida_validation.json | 14084 bytes | 983 lines | 99e3550317fa40e6432d | JSON
- data/w33_20261108_S8_hybrid_shapley_audit.json | 7707 bytes | 133 lines | 8ab752f71da7d4768563 | JSON
- data/w33_bergman_to_naruki.json | 519 bytes | 33 lines | 09dc00b2f8b57aaab718 | JSON
- data/w33_e7_orbit_census.json | 902 bytes | 124 lines | 81c4cfe7f9f1780e6601 | JSON
- data/w33_e7_rung_mubs.json | 161 bytes | 16 lines | fc503e4061b775f7d096 | JSON
- data/w33_e7_scalene.json | 687 bytes | 68 lines | 39279aa5e9a69c2dbb2f | JSON
- data/w33_level2_ladder.json | 289 bytes | 24 lines | e6220d42eef6c9c6dd3e | JSON
- data/w33_pass12632_halofit_scf.json | 7652 bytes | 344 lines | 09bfeb20fb00cbbdc096 | JSON
- data/w33_pass12634_naruki_fan.json | 1181 bytes | 67 lines | 07c923ef3e835bfcb3e5 | JSON
- data/w33_pass12635_burkhardt_fan.json | 663 bytes | 31 lines | a0b07faa5265a512cf76 | JSON
- data/w33_pentad_strong_umub.json | 336 bytes | 16 lines | 21a415d852072c03d1cb | JSON
- data/w33_pentad_umub.json | 453 bytes | 20 lines | c4dc836e1580ddf78d36 | JSON
- data/w33_pezzotope_amplitude.json | 68 bytes | 6 lines | 15792942de9f219ebbbd | JSON
- data/w33_pezzotope_check.json | 68874 bytes | 5196 lines | ce0c4adbff63f524ceb2 | JSON
- data/w33_pezzotope_chirality.json | 281 bytes | 14 lines | 139caa553d4119bd36f0 | JSON
- data/w33_pezzotope_gosset.json | 1588 bytes | 60 lines | 566fec8f5fef67cc8893 | JSON
- data/w33_pezzotope_hidden_zeros.json | 1448 bytes | 152 lines | 882a32afb187a910cc8f | JSON
- data/w33_pezzotope_reflection.json | 330 bytes | 18 lines | 9e3850a0e5b4573653b4 | JSON
- data/w33_q_ladder.json | 557 bytes | 38 lines | 3bf89310d99acc22afba | JSON
- data/w33_six_particles.json | 300 bytes | 9 lines | 31fd4e89536602d7d2c2 | JSON
- data/w33_size8_splits.json | 191 bytes | 13 lines | f3bf21a799ffe391cd72 | JSON
- data/w33_split_bridge.json | 763 bytes | 70 lines | 0ade2723d2690585059d | JSON
- data/w33_split_triality.json | 104 bytes | 8 lines | 0befd02c30b186ef8094 | JSON
- tests/test_class_scf_halofit_builds.py | 2320 bytes | 48 lines | 3fdf70b5d53eecddfb54 | Python
- tests/test_toe_20261108_halfturn_qutrit_magic.py | 1553 bytes | 38 lines | d78275b5339c6ade5bb3 | Python
- tests/test_toe_20261108_invariant_magnetic_completion.py | 4343 bytes | 90 lines | 783e3a4db53a13682165 | Python
- tests/test_toe_20261108_signed_cubic_vacuum.py | 3961 bytes | 99 lines | e17d440a03e075738396 | Python
- tests/test_toe_20261109_pezzotope_canonical_newton.py | 1591 bytes | 40 lines | 5e071721df89c57368cf | Python
- tests/test_toe_20261109_yoshida_partner_code.py | 1420 bytes | 40 lines | 6ccc49506f171f682bcb | Python
- tests/test_w33_20261108_s8_hybrid_shapley_audit.py | 2652 bytes | 46 lines | 579111e2db4998bb2288 | Python
- tests/test_w33_pass12634.py | 391 bytes | 12 lines | f719d21bc0bc049fbae5 | Python
- tests/test_w33_pass12635.py | 397 bytes | 12 lines | f2ff3ce417c0936b2974 | Python

## Structural parse failures

None
