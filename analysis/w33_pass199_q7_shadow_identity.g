# Pass 199 (corrected): full Sp(4,7) action on the q=7 shadow.

Read("analysis/w33_odd_q_shadow_common.g");;

Main := function()
  local shadow, form, factors, imageGroupOrder, preservesPolar,
        preservesQuadraticBasis, matrix, i, isotropic, allPass, status;

  shadow := BuildOddQShadow(7, false, true);
  form := QuadraticShadowReport(shadow);
  factors := CompositionFactorDimensions(shadow.actionMatrices);
  imageGroupOrder := Size(Group(shadow.actionMatrices));
  preservesPolar := ForAll(
    shadow.actionMatrices,
    matrix -> matrix * form.gram * TransposedMat(matrix) = form.gram
  );
  preservesQuadraticBasis := ForAll(
    shadow.actionMatrices,
    matrix -> ForAll([1..form.dimension], i ->
      QuadraticCoordinateValue(matrix[i], form.qValues, form.gram) =
      form.qValues[i]
    )
  );
  isotropic := 2^47 + 2^23;

  allPass :=
    shadow.fullSpOrder = 276595200 and
    shadow.pointGroupOrder = 138297600 and
    imageGroupOrder = 138297600 and
    Length(shadow.transvectionMatrices) = 5 and
    form.dimension = 48 and
    form.polarRank = 48 and
    form.arf = 0 and
    form.hyperbolicPairs = 24 and
    preservesPolar and
    preservesQuadraticBasis and
    factors = [24, 24];
  AssertTrue("Pass 199 corrected certificate", allPass);
  if allPass then status := "PASS"; else status := "FAIL"; fi;

  WriteCertificateJSON(
    "data/w33_pass199_q7_shadow_identity.json",
    [
      "{\n",
      "  \"schema\": \"w33.pass199.q7_shadow_identity.gap.v2\",\n",
      "  \"status\": \"", status, "\",\n",
      "  \"owner\": \"GAP 4.12 MTX\",\n",
      "  \"group\": {\n",
      "    \"name\": \"Sp(4,7)\",\n",
      "    \"standard_transvection_generators\": 5,\n",
      "    \"matrix_group_order\": ", String(shadow.fullSpOrder), ",\n",
      "    \"projective_point_group_order\": ", String(shadow.pointGroupOrder), ",\n",
      "    \"shadow_image_order\": ", String(imageGroupOrder), ",\n",
      "    \"shadow_action_projectively_faithful\": true\n",
      "  },\n",
      "  \"shadow\": {\n",
      "    \"dimension\": 48,\n",
      "    \"quadratic_refinement\": \"x^T A x/4 mod 2\",\n",
      "    \"type\": \"plus\",\n",
      "    \"arf\": 0,\n",
      "    \"witt_index\": 24,\n",
      "    \"isotropic_vectors\": ", String(isotropic), ",\n",
      "    \"isotropic_formula\": \"2^47+2^23\",\n",
      "    \"composition_factors_MTX\": ", JSONArrayInts(factors), ",\n",
      "    \"irreducible\": false\n",
      "  },\n",
      "  \"correction\": {\n",
      "    \"old_two_generator_SL2_subgroup_refuted\": true,\n",
      "    \"old_small_cyclic_submodule_profile_removed\": true,\n",
      "    \"actual_factor_statement\": \"24+24 under the full projective Sp(4,7) action\"\n",
      "  },\n",
      "  \"checks\": {\n",
      "    \"five_transvections_generate_full_Sp4_7\": true,\n",
      "    \"action_preserves_polar_form\": ", BoolJSON(preservesPolar), ",\n",
      "    \"action_preserves_quadratic_refinement\": ", BoolJSON(preservesQuadraticBasis), ",\n",
      "    \"MTX_factors_24_24\": true\n",
      "  }\n",
      "}\n"
    ]
  );
  Print("Pass 199 GAP certificate: ", status, "\n");
end;;

Main();
QUIT;
