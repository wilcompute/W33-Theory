# Pass 200 (corrected): the q=5 shadow under the full Sp(4,5) action.

Read("analysis/w33_odd_q_shadow_common.g");;

Main := function()
  local shadow, form, factors, imageGroupOrder, allPass, status;

  shadow := BuildOddQShadow(5, false, true);
  form := QuadraticShadowReport(shadow);
  factors := CompositionFactorDimensions(shadow.actionMatrices);
  imageGroupOrder := Size(Group(shadow.actionMatrices));

  allPass :=
    shadow.fullSpOrder = 9360000 and
    shadow.pointGroupOrder = 4680000 and
    imageGroupOrder = 4680000 and
    Length(shadow.transvectionMatrices) = 5 and
    form.dimension = 24 and
    form.polarRank = 0 and
    form.radicalDimension = 24 and
    form.qVanishesOnRadical and
    form.polarIdentity and
    form.descendsToQuotient and
    factors = [24];
  AssertTrue("Pass 200 corrected certificate", allPass);
  if allPass then status := "PASS"; else status := "FAIL"; fi;

  WriteCertificateJSON(
    "data/w33_pass200_q5_golay_leech_shadow.json",
    [
      "{\n",
      "  \"schema\": \"w33.pass200.q5_shadow.gap.v2\",\n",
      "  \"status\": \"", status, "\",\n",
      "  \"owner\": \"GAP 4.12 MTX\",\n",
      "  \"group\": {\n",
      "    \"name\": \"Sp(4,5)\",\n",
      "    \"standard_transvection_generators\": 5,\n",
      "    \"matrix_group_order\": ", String(shadow.fullSpOrder), ",\n",
      "    \"projective_point_group_order\": ", String(shadow.pointGroupOrder), ",\n",
      "    \"shadow_image_order\": ", String(imageGroupOrder), "\n",
      "  },\n",
      "  \"shadow\": {\n",
      "    \"dimension\": 24,\n",
      "    \"quadratic_refinement\": \"x^T A x/4 mod 2\",\n",
      "    \"polar_rank\": 0,\n",
      "    \"radical_dimension\": 24,\n",
      "    \"quadratic_refinement_identically_zero\": true,\n",
      "    \"composition_factors_MTX\": ", JSONArrayInts(factors), ",\n",
      "    \"irreducible_under_full_projective_group\": true\n",
      "  },\n",
      "  \"golay_leech_verdict\": {\n",
      "    \"invariant_dimension_12_submodule\": false,\n",
      "    \"golay_identification_supported\": false,\n",
      "    \"reason\": \"MTX proves the full-group 24-module is irreducible\"\n",
      "  },\n",
      "  \"correction\": {\n",
      "    \"old_two_generator_SL2_subgroup_refuted\": true,\n",
      "    \"old_14_20_cyclic_profile_removed\": true,\n",
      "    \"dimension_only_moonshine_analogy_withdrawn\": true\n",
      "  },\n",
      "  \"checks\": {\n",
      "    \"five_transvections_generate_full_Sp4_5\": true,\n",
      "    \"exact_polar_identity\": true,\n",
      "    \"MTX_irreducible_dimension_24\": true\n",
      "  }\n",
      "}\n"
    ]
  );
  Print("Pass 200 GAP certificate: ", status, "\n");
end;;

Main();
QUIT;
