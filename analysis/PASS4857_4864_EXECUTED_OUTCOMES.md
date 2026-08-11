# Passes 4857–4864 — executed outcomes

Reserved at `e50fe1fd322c243899514e9ea44db43ac00fb880`. The namespace was rechecked after execution; no competing canonical 4857–4864 packet was found.

## 4857 — rational orbital blocks close

Pass4850 left only the split-versus-division status of the noncommutative rational simple factors open. Combining the certified `PGSp(4,3)=W(E6)` action with Benard's classical Schur-index-one theorem for exceptional Weyl groups, and then restricting the rational Weyl modules to the index-two PSp subgroup, closes every block:

- `A_Q(PGSp) = Q^6 x M2(Q)^4 x M3(Q)^3`;
- with `K=Q(sqrt(-3))`, `A_Q(PSp) = Q^3 x K^2 x M2(Q)^2 x M2(K) x M3(Q)^4`.

All noncommutative factors are split over their centers. Benard's Schur-index theorem is prior art; the repo result is the exact application/allocation to the Pass4850 orbital algebra.

## 4858 — the ten-dimensional ternary obstruction is absolutely irreducible

For `H1(Levi(GQ(4,2));F3)` the oriented K3,3 family spans 54 of 64 dimensions. The quotient has dimension ten. Exact induced PSp/PGSp matrices were built from the common GQ action. The endomorphism ring has dimension one over `F3` for both groups. Exhausting all 29,524 projective nonzero quotient vectors shows every one has cyclic span ten under PSp. Hence the quotient is absolutely irreducible, and the PGSp action extends it absolutely irreducibly.

## 4859 — exact signed-coset enumerator; covering radius remains bounded, not closed

The nontrivial E6 switching coset over the 35-dimensional cut code is completely enumerated by an exact rank-six root-sum dynamic program. It has `2^35` words on 40 even weights from 120 through 198; `A_120=25920` recovers the Weyl-chamber minimum shell.

The ordinary cut-space Ising polynomial does **not** reduce to that root-sum statistic and is not promoted as closed. Likewise the covering radius is not yet exact. A symmetric hard witness `x` with `g(x)=x+sigma_E6`, together with an exact rational LDL proof that `3 A_x + 19 I` is positive definite, yields `d(x,K)>=124`. Orthogonal-array strength two from `d(K^perp)=3` gives the universal upper bound 179. Thus

`124 <= rho(K) <= 179`.

This partial boundary is deliberate.

## 4860 — root-free E6 signing from Steiner trihedral pairs

The 36 double-sixes form `SRG(36,20,10,12)`. Its 1,200 graph triangles split exactly by triple intersection of their 12-line supports:

- 1,080 triangles have triple intersection four;
- 120 have empty triple intersection.

The latter are exactly the independently reconstructed Steiner trihedral-pair triples. The 1,200-by-360 triangle-edge parity matrix has rank 325 over `F2`; setting parity one precisely on those 120 Steiner triangles has an affine 35-dimensional solution space, exactly one switching class modulo the 35-dimensional cut space. The E6 negative-root-inner-product signing has the same triangle parities. Therefore `sigma_E6` is intrinsic to the cubic-surface double-six/Steiner incidence and no root coordinates are needed to define it.

## 4861 — minimal datum that removes the genuine sheet gauge

The intrinsic class symmetry of C399 is `S3^45 : PGSp`. A full local bijection between the three sheet-cells above a GQ point and its three incident quotient-line ports has six choices and trivial local S3 stabilizer. It is minimal among local data that kill the entire local S3. Choosing one at every point removes the sheet kernel while preserving a diagonal/cocycle copy of PGSp. Adding the previously certified global chirality bit selects the PSp index-two subgroup. Code distance/decoder guarantees are unchanged; the gain is canonical physical port compilation.

## 4862 — Steiner two-graph exact sequence

Let `delta:F2^360 -> F2^1200` send an edge signing to its triangle parities and let `p_St` be the 120-Steiner-triangle parity vector. Then

`K = delta^{-1}(<p_St>)`,

with kernel `Cut(H36)` of dimension 35. The cycle space has dimension 325. The 1,080 even-Steiner triangles span exactly 324 dimensions and are precisely the 1,080 binary Levi minimum checks, so

`K^perp = span(even Steiner triangles) = [360,324,3]_2`.

This turns the E6 switching code into a one-dimensional Steiner-parity extension of a graph cut code.

## 4863 — explicit O5 exterior-square intertwiner

In `PG(4,3)` with the standard nondegenerate five-dimensional quadratic form, the projective norm classes have sizes 40, 45, and 36. The nonorthogonality graph on the 36 norm-2 points is explicitly isomorphic to the double-six `SRG(36,20,10,12)`. The same eight PGSp generators lift to explicit 5-by-5 orthogonal matrices. Taking exterior square gives a ten-dimensional module.

Solving the simultaneous common-generator equations against the Pass4858 quotient gives a one-dimensional Hom space whose unique nonzero intertwiner has rank ten. Thus the ternary obstruction quotient is explicitly PGSp-equivariantly isomorphic to `Lambda^2(F3^5)`.

## 4864 — the homology quotient is the adjoint Lie algebra

Under the standard bivector-to-skew-endomorphism map, `Lambda^2(F3^5)=so5(F3)`. Matrix commutator gives a bracket with center zero and derived dimension ten; Jacobi is verified exactly on a basis and all common PGSp generators preserve the bracket. Transport through the rank-ten intertwiner gives the same Lie algebra structure on the homology quotient. In odd characteristic this is the classical type-B2/C2 identification `so5(F3) ~= sp4(F3)`.

This is a finite module/Lie-algebra theorem only; no continuum gauge field or particle assignment is inferred.

## Evidence paths

Producers:
- `analysis/w33_pass4857_rational_orbital_blocks.py`
- `analysis/w33_pass4858_ternary_ten_module.py`
- `analysis/w33_pass4859_switching_enumerator_radius.py`
- `analysis/w33_pass4860_intrinsic_steiner_signing.py`
- `analysis/w33_pass4861_port_matching_symmetry_break.py`
- `analysis/w33_pass4862_steiner_two_graph_code.py`
- `analysis/w33_pass4863_4864_o5_adjoint_homology.py`

Frozen certificates are the corresponding `data/PART_W33_PASS...json` files. Cross-regression: `tests/test_w33_pass4857_4864_rational_steiner_o5.py`. Exact-evidence workflow: `.github/workflows/w33_pass4857_4864_rational_steiner_o5.yml`.
