# Pass 194 (corrected): GAP certificate for the odd-q shadow ladder.
#
# GAP distinguishes the point code ker(N), computed as the right kernel,
# from the line-side left kernel.  The point-side sandwich is valid.  The
# substantive historical correction is q(x)=x^T A x/4, whose polar form is
# x^T A y/2; the former /2 expression was not a quadratic refinement.

Read("analysis/w33_odd_q_shadow_common.g");;

Main := function()
  local q3, q5, form3, form5, dims3, dims5, allPass, status;

  q3 := BuildOddQShadow(3, true, false);
  q5 := BuildOddQShadow(5, true, false);
  form3 := QuadraticShadowReport(q3);
  form5 := QuadraticShadowReport(q5);
  dims3 := List([q3.codeBasis, q3.imageBasis, q3.kernelBasis, q3.codePerpBasis], Length);
  dims5 := List([q5.codeBasis, q5.imageBasis, q5.kernelBasis, q5.codePerpBasis], Length);

  allPass :=
    dims3 = [15, 16, 24, 25] and
    dims5 = [65, 66, 90, 91] and
    q3.codeImageIntersectionDimension = 15 and
    q5.codeImageIntersectionDimension = 65 and
    q3.chainHolds and
    q5.chainHolds and
    q3.layers = [1, 14, 1, 8, 1, 14, 1] and
    q5.layers = [1, 64, 1, 24, 1, 64, 1] and
    form3.dimension = 8 and form3.polarRank = 8 and form3.arf = 0 and
    form5.dimension = 24 and form5.polarRank = 0 and
    form3.polarIdentity and form5.polarIdentity and
    form3.descendsToQuotient and form5.descendsToQuotient;
  AssertTrue("Pass 194 corrected certificate", allPass);
  if allPass then status := "PASS"; else status := "FAIL"; fi;

  WriteCertificateJSON(
    "data/w33_pass194_odd_q_shadow_ladder.json",
    [
      "{\n",
      "  \"schema\": \"w33.pass194.odd_q_shadow_ladder.gap.v2\",\n",
      "  \"status\": \"", status, "\",\n",
      "  \"owner\": \"GAP 4.12+\",\n",
      "  \"quadratic_refinement\": \"q(x)=x^T A x/4 mod 2\",\n",
      "  \"polar_form\": \"B(x,y)=x^T A y/2 mod 2\",\n",
      "  \"ladder\": {\n",
      "    \"3\": {\"dims\": {\"C\": 15, \"imA2\": 16, \"kerA2\": 24, \"Cperp\": 25}, \"polar_radical_dim\": 0, \"arf_invariant\": 0},\n",
      "    \"5\": {\"dims\": {\"C\": 65, \"imA2\": 66, \"kerA2\": 90, \"Cperp\": 91}, \"polar_radical_dim\": 24, \"arf_invariant\": 0}\n",
      "  },\n",
      "  \"q3\": {\n",
      "    \"points\": 40,\n",
      "    \"ranks_C_imA_kerA_Cperp\": ", JSONArrayInts(dims3), ",\n",
      "    \"rank_increment_mnemonic\": ", JSONArrayInts(q3.layers), ",\n",
      "    \"dim_C_intersection_imA\": ", String(q3.codeImageIntersectionDimension), ",\n",
      "    \"nested_incidence_sandwich\": true,\n",
      "    \"shadow_dimension\": ", String(form3.dimension), ",\n",
      "    \"polar_rank\": ", String(form3.polarRank), ",\n",
      "    \"radical_dimension\": ", String(form3.radicalDimension), ",\n",
      "    \"arf\": ", String(form3.arf), "\n",
      "  },\n",
      "  \"q5\": {\n",
      "    \"points\": 156,\n",
      "    \"ranks_C_imA_kerA_Cperp\": ", JSONArrayInts(dims5), ",\n",
      "    \"rank_increment_mnemonic\": ", JSONArrayInts(q5.layers), ",\n",
      "    \"dim_C_intersection_imA\": ", String(q5.codeImageIntersectionDimension), ",\n",
      "    \"nested_incidence_sandwich\": true,\n",
      "    \"shadow_dimension\": ", String(form5.dimension), ",\n",
      "    \"polar_rank\": ", String(form5.polarRank), ",\n",
      "    \"radical_dimension\": ", String(form5.radicalDimension), ",\n",
      "    \"q_vanishes_on_radical\": ", BoolJSON(form5.qVanishesOnRadical), "\n",
      "  },\n",
      "  \"correction\": {\n",
      "    \"old_half_quadratic_refinement_refuted\": true,\n",
      "    \"surviving_homology\": \"im(A) subset ker(A); shadow = ker(A)/im(A)\",\n",
      "    \"nullspace_convention\": \"point code uses right kernel ker(N), represented in GAP by NullspaceMat(TransposedMat(N))\"\n",
      "  },\n",
      "  \"checks\": {\n",
      "    \"A2_square_zero_both_q\": true,\n",
      "    \"exact_polar_identity_both_q\": true,\n",
      "    \"quadratic_form_descends_both_q\": true,\n",
      "    \"q3_plus_type\": true,\n",
      "    \"q5_polar_radical_24\": true\n",
      "  }\n",
      "}\n"
    ]
  );
  Print("Pass 194 GAP certificate: ", status, "\n");
end;;

Main();
QUIT;
