# Pass 205 (corrected): MTX factors for the full q=5 and q=7 groups.

Read("analysis/w33_odd_q_shadow_common.g");;

Main := function()
  local q5, q7, factors5, factors7, allPass, status;

  q5 := BuildOddQShadow(5, false, true);
  q7 := BuildOddQShadow(7, false, true);
  factors5 := CompositionFactorDimensions(q5.actionMatrices);
  factors7 := CompositionFactorDimensions(q7.actionMatrices);

  allPass :=
    q5.fullSpOrder = 9360000 and
    q7.fullSpOrder = 276595200 and
    factors5 = [24] and
    factors7 = [24, 24] and
    not (8 in factors5) and
    not (8 in factors7);
  AssertTrue("Pass 205 corrected certificate", allPass);
  if allPass then status := "PASS"; else status := "FAIL"; fi;

  WriteCertificateJSON(
    "data/w33_pass205_q7_composition_series.json",
    [
      "{\n",
      "  \"schema\": \"w33.pass205.odd_q_composition_factors.gap.v2\",\n",
      "  \"status\": \"", status, "\",\n",
      "  \"owner\": \"GAP 4.12 MTX\",\n",
      "  \"q5\": {\n",
      "    \"shadow_dimension\": 24,\n",
      "    \"full_Sp4_order\": ", String(q5.fullSpOrder), ",\n",
      "    \"composition_factors_MTX\": ", JSONArrayInts(factors5), ",\n",
      "    \"irreducible\": true\n",
      "  },\n",
      "  \"q7\": {\n",
      "    \"shadow_dimension\": 48,\n",
      "    \"full_Sp4_order\": ", String(q7.fullSpOrder), ",\n",
      "    \"composition_factors_MTX\": ", JSONArrayInts(factors7), ",\n",
      "    \"irreducible\": false,\n",
      "    \"contains_dimension_8_factor\": false\n",
      "  },\n",
      "  \"corrected_ladder_reading\": {\n",
      "    \"q3\": \"irreducible dimension 8\",\n",
      "    \"q5\": \"irreducible dimension 24\",\n",
      "    \"q7\": \"composition factors 24+24\",\n",
      "    \"E8_unique_irreducible_rung\": false,\n",
      "    \"higher_rungs_always_reducible\": false,\n",
      "    \"scope\": \"only q=3,5,7 are certified; no extrapolation beyond them\"\n",
      "  },\n",
      "  \"correction\": {\n",
      "    \"coordinate_basis_spin_search_removed\": true,\n",
      "    \"full_five_transvection_groups_used\": true,\n",
      "    \"MTX_composition_factors_used\": true\n",
      "  },\n",
      "  \"checks\": {\n",
      "    \"q5_factor_24\": true,\n",
      "    \"q7_factors_24_24\": true,\n",
      "    \"no_q7_dimension_8_factor\": true\n",
      "  }\n",
      "}\n"
    ]
  );
  Print("Pass 205 GAP certificate: ", status, "\n");
end;;

Main();
QUIT;
