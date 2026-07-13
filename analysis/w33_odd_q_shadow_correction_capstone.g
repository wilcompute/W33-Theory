# Odd-q shadow correction capstone.
#
# One GAP-owned artifact correcting the quadratic-refinement and subgroup
# claims spread across historical Passes 194, 198, 199, 200, and 205.

Read("analysis/w33_odd_q_shadow_common.g");;

Main := function()
  local q3, q5, q7, form3, form5, form7, factors3, factors5, factors7,
        allPass, status;

  q3 := BuildOddQShadow(3, true, true);
  q5 := BuildOddQShadow(5, true, true);
  q7 := BuildOddQShadow(7, true, true);
  form3 := QuadraticShadowReport(q3);
  form5 := QuadraticShadowReport(q5);
  form7 := QuadraticShadowReport(q7);
  factors3 := CompositionFactorDimensions(q3.actionMatrices);
  factors5 := CompositionFactorDimensions(q5.actionMatrices);
  factors7 := CompositionFactorDimensions(q7.actionMatrices);

  allPass :=
    List([q3, q5, q7], shadow -> shadow.codeImageIntersectionDimension) = [15, 65, 175] and
    ForAll([q3, q5, q7], shadow -> shadow.chainHolds) and
    List([form3, form5, form7], form -> form.dimension) = [8, 24, 48] and
    List([form3, form5, form7], form -> form.polarRank) = [8, 0, 48] and
    List([form3, form5, form7], form -> form.arf) = [0, 0, 0] and
    factors3 = [8] and factors5 = [24] and factors7 = [24, 24] and
    List([q3, q5, q7], shadow -> shadow.fullSpOrder) =
      [51840, 9360000, 276595200] and
    ForAll([form3, form5, form7], form ->
      form.polarIdentity and form.descendsToQuotient
    );
  AssertTrue("odd-q correction capstone", allPass);
  if allPass then status := "PASS"; else status := "FAIL"; fi;

  WriteCertificateJSON(
    "data/w33_odd_q_shadow_correction_capstone.json",
    [
      "{\n",
      "  \"schema\": \"w33.odd_q_shadow_correction_capstone.gap.v1\",\n",
      "  \"status\": \"", status, "\",\n",
      "  \"owner\": \"GAP 4.12 MTX\",\n",
      "  \"supersedes_claims_in\": [194,198,199,200,205],\n",
      "  \"uniform_construction\": {\n",
      "    \"group_generators\": \"five standard symplectic transvections e1,e2,f1,f2,e1+e2\",\n",
      "    \"quadratic_refinement\": \"q(x)=x^T A x/4 mod 2\",\n",
      "    \"polar_form\": \"B(x,y)=x^T A y/2 mod 2\",\n",
      "    \"shadow\": \"H_A=ker(A mod 2)/im(A mod 2)\"\n",
      "  },\n",
      "  \"anchor_table\": [\n",
      "    {\"q\":3, \"points\":40, \"Sp4_order\":51840, \"projective_order\":25920, \"C_inter_imA\":15, \"shadow_dim\":8, \"polar_rank\":8, \"arf\":0, \"MTX_factors\":[8]},\n",
      "    {\"q\":5, \"points\":156, \"Sp4_order\":9360000, \"projective_order\":4680000, \"C_inter_imA\":65, \"shadow_dim\":24, \"polar_rank\":0, \"arf\":0, \"MTX_factors\":[24]},\n",
      "    {\"q\":7, \"points\":400, \"Sp4_order\":276595200, \"projective_order\":138297600, \"C_inter_imA\":175, \"shadow_dim\":48, \"polar_rank\":48, \"arf\":0, \"MTX_factors\":[24,24]}\n",
      "  ],\n",
      "  \"refutations\": {\n",
      "    \"half_quadratic_refinement\": false,\n",
      "    \"two_transvections_generate_Sp4_q\": false,\n",
      "    \"q5_has_14_20_submodule_profile\": false,\n",
      "    \"E8_is_unique_irreducible_rung\": false\n",
      "  },\n",
      "  \"surviving_theorems\": {\n",
      "    \"A2_square_zero_for_odd_q\": true,\n",
      "    \"point_code_C_subset_imA\": true,\n",
      "    \"valid_A_homology_shadow\": true,\n",
      "    \"q3_plus_8\": true,\n",
      "    \"q5_zero_form_irreducible_24\": true,\n",
      "    \"q7_plus_48_with_factors_24_24\": true,\n",
      "    \"computed_scope_only_q3_q5_q7\": true\n",
      "  }\n",
      "}\n"
    ]
  );
  Print("Odd-q shadow correction capstone: ", status, "\n");
end;;

Main();
QUIT;
