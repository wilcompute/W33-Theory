# 2026-11-14 — Explicit IIB Levi dictionary and rank-two E6 gauging stabilizer

## Scope

This report connects the repository's signed 45-term cubic, all 78 E6 split-real generators, and the previously published local unipotent generalized Scherk–Schwarz (GSS) frame into a single explicit type-IIB coordinate dictionary. It proves the precise 351 embedding-tensor linear and quadratic constraints and a 52D E6 stabilizer. It does not derive a spacetime dimension, vacuum, supergravity dynamics or Theory of Everything.

Three independent Python producers and matching JSON certificates:
- analysis/toe_20261114_E6_exact_IIB_Levi_signed_tensor_intertwiner.py
- data/toe_20261114_E6_native_signed_IIB_GL5_SL2_intertwiner.json
- analysis/toe_20261114_E6_GSS_351_embedding_tensor.py
- data/toe_20261114_E6_GSS_explicit_rank2_Z_351_embedding_tensor.json
- analysis/toe_20261114_E6_GSS_351_flux_parabolic_stabilizer.py
- data/toe_20261114_E6_351_flux_52D_parabolic_stabilizer.json
- tests/test_toe_20261114_E6_IIB_Levi_351_flux_stabilizer.py

Previous parent work: local GSS/Leibniz analysis, commit ac67fdea009cf151de6007aa349c8e1e5c2ca7f8.

## A. Exact unimodular IIB 27-coordinate intertwiner

The established IIB branching is

  27 = (5,1)_4 + (5bar,2)_1 + (10,1)_-2 + (1,2)_-5 .

The explicit old-coordinate indices in canonical block order are:
V (5): 0,1,2,3,4; signs −,+,−,−,+.
W0 (5): 17,8,7,6,5; all signs +.
W1 (5): 18,12,11,10,9; all signs +.
Z_ij (10), ij in lex order 01,02,03,04,12,13,14,23,24,34:
old indices 13,14,15,16,19,20,22,21,23,24;
signs +,−,−,+,−,−,−,+,+,+.
S (2): 25,26; positive signs.

This defines an explicit integer signed permutation Q, with QQ^T=I, preserving integrality. In new coordinates, the full signed cubic is, coefficient by coefficient,

  N = sum_i V_i ( W_i0 S_1 − W_i1 S_0 )
      + sum_{i<j} Z_ij ( W_i0 W_j1 − W_i1 W_j0 )
      − sum_i sum_over_three_pairings (epsilon_ijklm V_i Z_jk Z_lm).

The latter pairings are the three perfect matchings of the remaining four indices for each i. Exact monomial counts are 10 of type VWS, 20 WWZ, 15 VZZ = all 45 terms. This is a checked polynomial identity, not a pattern inferred from dimensions.

The grading operator D acts by weights 4,1,−2,−5 on the four summands and preserves all 45 monomials. The 72 Chevalley roots have exact grades −6:5, −3:20, 0:22, +3:20, +6:5. Two zero-grade roots, indices 55 and 71, furnish SL2 raising/lowering on all five W doublets plus the S doublet. They satisfy [H,E]=2E, [H,F]=−2F and [E,F]=H.

The other 20 grade-zero roots act as the standard elementary matrix units of sl5 on V. Four commutators supply its Cartan generators. On the complete 27D space, each of the 24 sl5 basis generators is exactly intertwined to:

  A on V (5); −A^T on W0; −A^T on W1;
  exterior-square(A) on Z (10); zero on S (2).

All block entries, 576 ordered sl5 brackets, SL2 brackets and mutual commutation relations pass exact integer tests. All 28 Levi matrices are independent mod 101, proving independence over Q. This completes a concrete GL5×SL2 Levi representation intertwiner in the signed repo basis; it is not yet the full nonlinear ExFT field dictionary.

Established representation background: Hohm & Samtleben https://arxiv.org/abs/1312.0614 ; type-IIB branching https://link.springer.com/article/10.1140/epjc/s10052-024-13402-4 .

## B. Exact 351 embedding-tensor linear and quadratic constraints

For the prior local frame U(y)=I+yR, R²=0, root R=1, y=Y^3, the published generalized Lie derivative yields constant X_MN^P with 30 nonzero integer coefficients and a nonzero symmetric Dorfman part.

Let T be the signed integer cubic tensor, satisfying T_iMN T_jMN =10 delta_ij, so d=T/sqrt(10). Set

  S_MN^P = X_MN^P+X_NM^P,
  Zraw_QP = sum_MN T_MNQ S_MN^P.

The exact result is:
  Zraw_25,26 = +10; Zraw_26,25=−10; all others zero.

Thus Zraw is antisymmetric rank TWO. Direct reconstruction of all 19683 entries gives 10 S_MN^P = T_MNQ Zraw_QP with ZERO residual. In the chosen d convention the normalized antisymmetric intertwiner is Z=Zraw/(2sqrt(10)), and hence X_(MN)^P=d_MNQ Z_QP. This is the 351 embedding-tensor linear constraint of 5D maximal gauged supergravity, not simply a dimension coincidence.

All 27 gauge-generator matrices preserve the exact cubic; their traces vanish, excluding a trombone trace. Exactly five of them are nonzero and independent. They multiply pairwise to zero, so the active gauged algebra is five-dimensional abelian unipotent, although the full 27D Dorfman algebra is nonantisymmetric. Every quadratic gauge closure identity [X_M,X_N]=−X_MN^P X_P holds, and both Z times gauge generators and the contragredient gauge variation of Z vanish exactly. The published local Leibniz identity also passes.

Literature: gauged maximal E6 embedding tensor 27×78=27+351+1728 and X_(MN)^P=d_MNQ Z^QP:
https://citeseerx.ist.psu.edu/document?doi=3daf582c22566670342ecdf5f3c96fde53293b35&repid=rep1&type=pdf .

## C. Exact stabilizer of this particular 351 tensor

Acting with the entire 78-dimensional E6 algebra on X, its image is rank 26 and its stabilizer dimension is EXACTLY 52. Proof: 52 independent integral stabilizer matrices are constructed and the rank of the full infinitesimal action is at least 26 mod 101. Together these fix the rational rank to 26.

All 22 grade-zero roots, all 20 grade-(−3) roots, and all five grade-(−6) roots preserve X. All 25 positive-grade roots move it. Five independent Cartans preserve X while the remaining GL1 generator acts with relative weight −10.

The stabilizer is (sl5 ⊕ sl2) semidirect n25, where n25 is a two-step nilpotent radical, with a 20-dimensional degree-(−3) part and a five-dimensional central degree-(−6) part. All 190 brackets among the negative-three root pairs reconstruct exactly inside the negative-six sector, and their span has exact rank five; all other radical brackets vanish.

Adding the broken GL1 scaling Cartan gives the associated 53-dimensional opposite parabolic preserving the DUAL IIB five-coordinate section. The nonzero rank-two 351 tensor is a relative invariant of this parabolic: a fixed nonzero flux breaks its scaling but leaves all 52 remaining directions.

This is a genuine symmetry determination for the committed E6 model, not a first classification of 351 orbits.

## D. Physical interpretation and the next falsifiers

The constructive dictionary is much stronger than counting 27 points or observing a 5+10+10+2 split. It aligns the native cubic, all Levi generators, exact local generalized GSS frame flux, the 351 linear/quadratic constraints, and an explicit opposite-parabolic symmetry on the same integral coordinate system.

But the derivative coordinate y belongs to the M and IIB shared four-section, so the gauging does not uniquely select a spacetime branch. A prior simplified flux kinetic model stabilizes shape while the Einstein-frame volume R has a strict runaway V∝R^(−26/3). No complete scalar potential, field equations, compactification/tadpole consistency, supersymmetric vacuum, or experimentally testable prediction follows.

Next: (1) insert the verified 351 tensor into the actual maximal D=5 gauged-supergravity scalar potential and solve all critical-point equations; (2) build the full nonlinear IIB generalized-metric/flux dictionary; (3) impose global E6(Z) monodromy, Bianchi identities and quantization; (4) compare uplifted IIB and M formulations on the same observables; (5) derive testable photon/quantum-information predictions that are not adjustable after measurement.

Physical reference: consistent ExFT Kaluza-Klein truncation Hohm/Samtleben https://link.springer.com/article/10.1007/JHEP01%282015%29131 .
