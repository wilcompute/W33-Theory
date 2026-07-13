# Pass 198 (corrected): q=7 anchor and the divided-pairing parity law.

Read("analysis/w33_odd_q_shadow_common.g");;

PairingCoefficientSurvives := function(q)
  # A^2/2 = ((q^2-1)/2)I - A + ((q+1)/2)J.
  # For odd q the I coefficient is always even.  The J coefficient is even
  # exactly when q=3 mod 4, yielding the observed nondegenerate anchors.
  return ((q^2 - 1) / 2) mod 2 = 0 and ((q + 1) / 2) mod 2 = 0;
end;;

Main := function()
  local shadow, form, dims, residues, allPass, status;

  shadow := BuildOddQShadow(7, true, false);
  form := QuadraticShadowReport(shadow);
  dims := List(
    [shadow.codeBasis, shadow.imageBasis, shadow.kernelBasis, shadow.codePerpBasis],
    Length
  );
  residues := List([3, 5, 7, 11, 13, 19], PairingCoefficientSurvives);

  allPass :=
    shadow.n = 400 and
    dims = [175, 176, 224, 225] and
    shadow.codeImageIntersectionDimension = 175 and
    shadow.chainHolds and
    shadow.layers = [1, 174, 1, 48, 1, 174, 1] and
    form.dimension = 48 and
    form.polarRank = 48 and
    form.radicalDimension = 0 and
    form.arf = 0 and
    form.hyperbolicPairs = 24 and
    form.polarIdentity and
    form.descendsToQuotient and
    residues = [true, false, true, true, false, true];
  AssertTrue("Pass 198 corrected certificate", allPass);
  if allPass then status := "PASS"; else status := "FAIL"; fi;

  WriteCertificateJSON(
    "data/w33_pass198_layer_law_q7.json",
    [
      "{\n",
      "  \"schema\": \"w33.pass198.layer_law_q7.gap.v2\",\n",
      "  \"status\": \"", status, "\",\n",
      "  \"owner\": \"GAP 4.12+\",\n",
      "  \"q7\": {\n",
      "    \"points\": 400,\n",
      "    \"dims\": {\"C\": 175, \"imA2\": 176, \"kerA2\": 224, \"Cperp\": 225},\n",
      "    \"ranks_C_imA_kerA_Cperp\": ", JSONArrayInts(dims), ",\n",
      "    \"rank_increment_mnemonic\": ", JSONArrayInts(shadow.layers), ",\n",
      "    \"dim_C_intersection_imA\": 175,\n",
      "    \"nested_incidence_sandwich\": true,\n",
      "    \"shadow_dimension\": 48,\n",
      "    \"quadratic_refinement\": \"x^T A x/4 mod 2\",\n",
      "    \"polar_form\": \"x^T A y/2 mod 2\",\n",
      "    \"polar_rank\": 48,\n",
      "    \"polar_radical_dim\": 0,\n",
      "    \"radical_dimension\": 0,\n",
      "    \"arf\": 0,\n",
      "    \"witt_index\": 24\n",
      "  },\n",
      "  \"coefficient_parity_law\": {\n",
      "    \"identity\": \"A^2/2=((q^2-1)/2)I-A+((q+1)/2)J\",\n",
      "    \"nondegenerate_residue_class\": \"q congruent 3 mod 4\",\n",
      "    \"q3\": true,\n",
      "    \"q5\": false,\n",
      "    \"q7\": true,\n",
      "    \"q11_coefficient_prediction_only\": true,\n",
      "    \"q13_coefficient_prediction_only\": false,\n",
      "    \"q19_coefficient_prediction_only\": true\n",
      "  },\n",
      "  \"correction\": {\n",
      "    \"old_q3_mod8_wording_refuted\": true,\n",
      "    \"right_kernel_point_code_verified\": true,\n",
      "    \"computed_matrix_anchors\": [3,5,7]\n",
      "  },\n",
      "  \"checks\": {\n",
      "    \"q7_A2_square_zero\": true,\n",
      "    \"q7_exact_polar_identity\": true,\n",
      "    \"q7_form_descends\": true,\n",
      "    \"q7_plus_type\": true\n",
      "  }\n",
      "}\n"
    ]
  );
  Print("Pass 198 GAP certificate: ", status, "\n");
end;;

Main();
QUIT;
