# 2026-11-14 — A local E6 generalized Scherk–Schwarz flux with an explicit type-IIB wedge dictionary

## Scope

This is a reproducible local generalized-frame experiment using the repository's independently certified signed 45-term E6 cubic and 78 Lie generators. It strengthens the previous 42-scalar no-selection and flux-volume-runaway results with a NONZERO, CONSTANT generalized ExFT frame algebra. It does NOT produce a complete consistent reduction, solve higher-dimensional field equations, select physical spacetime, or establish a Theory of Everything.

Two producers:
- analysis/toe_20261114_E6_unipotent_GSS_local_parallelization.py
- analysis/toe_20261114_E6_GSS_nilpotent_flux_monodromy_sections.py

Matching JSON certificates in data/ and independent regression test in tests/.

### 1. Constructive twist and exact generalized gauge flux

Take root generator R indexed 1 among the 72 non-diagonal cubic-preserving E6 generators. Its six signed entries in row-column conventions are:
(0,15,-1), (1,20,+1), (2,21,+1), (4,24,+1), (6,25,+1), (10,26,+1).
Exactly R²=0, so U(y)=I+yR and U(y)^(-1)=I-yR. By the infinitesimal cubic identity and nilpotent exponential, U(y) preserves the signed cubic for every y. The producer also tests integer cubic values of transformed random vectors at y=1,-2,3 as independent controls.

Choose a derivative along original coordinate j=3. The vector and covector at index 3 are annihilated by R, and the original signed cubic has C_jjk=0. A field depending only on Y^3 satisfies the strong E6 section constraint. The coordinate Y^3 lies in both explicit maximal coordinate sections
IIB5=(0,1,2,3,4) and M6=(0,1,2,3,5,9).

For the weight-1/3 generalized Lie derivative in the standard E6 ExFT convention, define generalized frame E_A^M(y)=U_A^M(y) and Y-tensor Y^{Mj}{}_{NL}=sum_r C^{Mjr}C_{NLr}. The exact coefficient tensor X_AB^C(y) follows by expanding

L_{E_A} E_B^M = E_A^j R_B^M - E_B^j R_A^M
                 + Y^{Mj}{}_{NL} R_A^L E_B^N,

then expressing the output in the moving frame via U(y)^(-1).

The complete tensor is integer-valued with 30 nonzero coefficients, unchanged across y=0,1,2,3,-1. Because the construction is polynomial in y with bounded degree, these samples prove X is constant for all y. The full 27^4 component generalized Leibniz identity vanishes EXACTLY. The generalized trace sum_B X_AB^B is zero for every A. This meets local necessary conditions for a generalized Scherk–Schwarz twist, not the complete reduction consistency requirements.

### 2. Crucial distinction: non-Lie Leibniz algebra and tensor-hierarchy ideal

The exact X is NOT antisymmetric: the symmetric product S_AB^C=X_AB^C+X_BA^C has 20 nonzero entries. Its rational image is exactly the two-dimensional span of basis indices (25,26). Both-sided multiplication by the entire 2D symmetric ideal vanishes; it is a two-sided annihilator. The entire algebra is two-step nilpotent as a generalized Leibniz algebra:
(X_AB^C) X_CD^E =0 identically.

Rational ranks are:
- full product image dimension 12;
- symmetric/trivial ideal dimension 2;
- left annihilator dimension 22;
- right annihilator dimension 12.

Quotienting by the symmetric ideal yields a 25-dimensional ordinary Lie algebra with derived-algebra dimension 10, center dimension 20, and exact antisymmetric Jacobi identity. Only the five original generators indexed (0,1,2,3,4) act nontrivially. Their ten pairwise brackets are each a signed single independent basis vector. Consequently the quotient is

  free_2step_Lie(5) direct_sum R^10,

where free_2step_Lie(5) has dimension 5+10=15. This explicit result is much stronger than observing a numerical 27 decomposition, but it does NOT automatically produce a supergravity field dictionary.

### 3. Explicit 5+10+10+2 partition and IIB generalized-tangent analogy

The certificate constructs all ten signed pair-to-coordinate brackets, proving an isomorphism from Lambda^2 R^5 onto the 10-dimensional derived subspace. The native coordinate blocks are:

- five generators (0,1,2,3,4);
- ten independent central spectator candidates (5,6,7,8,9,10,11,12,17,18);
- ten derived wedge coordinates (13,14,15,16,19,20,21,22,23,24);
- two top symmetric-ideal coordinates (25,26).

These match the DIMENSIONS of the known type-IIB E6 generalized tangent decomposition

  T_5 [5] + (T_5* tensor SL2) [10]
      + Lambda^3 T_5* [10] + (Lambda^5 T_5* tensor SL2) [2].

The wedge-bracket map is explicitly verified, and Lambda^2 T_5 can map to Lambda^3 T_5* upon choosing an orientation/volume form. But identification of the central spectator ten as the SL2 doublet of covectors and identification of the final two as the SL2 doublet of top forms require the FULL GL5 x SL2 equivariant intertwiner, still unproved. This is a concrete candidate bridge, not a proven field-theory identification.

Published IIB generalized parameterization and self-duality dictionary: Baguet, Hohm and Samtleben, E6(6) Exceptional Field Theory Review and Embedding of Type IIB, arXiv:1506.01065, https://arxiv.org/abs/1506.01065 .

### 4. Integral unipotent monodromy does not itself select a section

Since U(y+1)=(I+R) U(y), with U(1)=I+R and U(1)^(-1)=I-R, an internal periodic y would have an INTEGRAL, infinite-order cubic-preserving monodromy. This suggests an arithmetic duality-twist or U-fold candidate, subject to a global physical section, consistent lattice and boundary-field identifications that we have not constructed.

Among all 216 maximal coordinate five-sections and 72 maximal six-sections, the MONODROMY fixes exactly 141 and 51, respectively, when acting on the primal coordinate subspaces; the dual action fixes the same numbers. Of these, 27 stable fivers and 12 stable sixers contain the chosen base coordinate j=3. Both explicit representative sections above are stable simultaneously under primal monodromy.

Therefore a nontrivial generalized gauge flux need not break the M/IIB section ambiguity. A dynamical selector would still require a consistent source/flux background and a comparative action calculation, not a count of fixed sections.

### 5. Physics firewall and next falsifiers

Hohm and Samtleben, Consistent Kaluza-Klein truncations via exceptional field theory, JHEP01(2015)131, https://doi.org/10.1007/JHEP01(2015)131 , establish the generalized Scherk–Schwarz framework and embedding-tensor consistency equations.

This local calculation has not:
- projected X into the complete E6(6) embedding-tensor 351 or proved every linear constraint and density/trombone requirement;
- constructed the full fermionic/tensor-hierarchy ansatz or solved its Einstein and scalar equations;
- established global compactness, boundary/monodromy consistency, a quantized physical flux, a positive/negative mode spectrum or quantum stability;
- selected the five- or six-coordinate section, or demonstrated observed physics.

Independent next tests are an explicit IIB GL5 x SL2 intertwiner and proper tensor-hierarchy ideal, embedding tensor linear/quadratic constraints under the published convention, global U-fold compactification, scalar-potential evaluation for the twisted generalized metric, and a physical source/boundary mechanism that can distinguish duality-related vacua without double-counting frames.
