# Pass 202 correction: GAP-owned arithmetic companion for ShadowDichotomy.lean.
#
# This certificate proves only polynomial identities and a coefficient-parity
# predicate.  It neither constructs W(3,q) nor proves that a quadratic shadow
# exists or is nondegenerate.  In particular, it never writes the Lean source.

OUT := "data/w33_pass202_shadow_dichotomy_arithmetic.json";;

LayerD := q -> (q - 1) * (q^2 + q + 2) / 2;;
ShadowDim := q -> q^2 - 1;;
IncidenceRank := q -> (q * (q + 1)^2 + 2) / 2;;
CoefficientParity := q ->
  ((q^2 - 1) / 2) mod 2 = 0 and ((q + 1) / 2) mod 2 = 0;;
LayerSum := q -> 1 + LayerD(q) + 1 + ShadowDim(q) + 1 + LayerD(q) + 1;;

oddQ := Filtered([3..59], q -> q mod 2 = 1);;
checks := rec(
  layer_d_integral := ForAll(oddQ,
    q -> ((q - 1) * (q^2 + q + 2)) mod 2 = 0),
  incidence_rank_integral := ForAll(oddQ,
    q -> (q * (q + 1)^2 + 2) mod 2 = 0),
  layer_sum_is_v := ForAll(oddQ,
    q -> LayerSum(q) = (q + 1) * (q^2 + 1)),
  coefficient_parity_iff_mod4_3 := ForAll(oddQ,
    q -> CoefficientParity(q) = (q mod 4 = 3)),
  anchor_dimensions := [ShadowDim(3), ShadowDim(5), ShadowDim(7)] = [8,24,48]
);;

if not ForAll(RecNames(checks), name -> checks.(name)) then
  Error("Pass 202 arithmetic correction failed");
fi;

stream := OutputTextFile(OUT, false);;
SetPrintFormattingStatus(stream, false);;
Emit := function(arg)
  local out, i;
  out := "";
  for i in [2..Length(arg)] do
    out := Concatenation(out, String(arg[i]));
  od;
  WriteAll(arg[1], out);
end;;
Emit(stream,
  "{\n",
  "  \"schema\": \"w33.pass202.shadow_dichotomy_arithmetic.gap.v2\",\n",
  "  \"status\": \"PASS\",\n",
  "  \"producer\": \"GAP ", GAPInfo.Version, "\",\n",
  "  \"closed_forms\": {\n",
  "    \"layer_d\": \"(q-1)(q^2+q+2)/2\",\n",
  "    \"shadow_dim\": \"q^2-1\",\n",
  "    \"incidence_rank\": \"(q(q+1)^2+2)/2 [Sastry-Sin]\",\n",
  "    \"coefficient_parity\": \"equivalent to q = 3 (mod 4) for odd q >= 3\"\n",
  "  },\n",
  "  \"certified_scope\": {\n",
  "    \"arithmetic_only\": true,\n",
  "    \"constructs_W3q\": false,\n",
  "    \"proves_quadratic_shadow_nondegenerate\": false,\n",
  "    \"higher_q_module_structure\": \"prediction only\"\n",
  "  },\n",
  "  \"sample_table\": {\n",
  "    \"3\": {\"d\": 14, \"shadow_dim\": 8, \"incidence_rank\": 25, \"coefficient_parity\": true},\n",
  "    \"5\": {\"d\": 64, \"shadow_dim\": 24, \"incidence_rank\": 91, \"coefficient_parity\": false},\n",
  "    \"7\": {\"d\": 174, \"shadow_dim\": 48, \"incidence_rank\": 225, \"coefficient_parity\": true}\n",
  "  },\n",
  "  \"lean_source\": \"formal/W33/ShadowDichotomy.lean\",\n",
  "  \"lean_source_written\": false,\n",
  "  \"lean_toolchain_run\": false,\n",
  "  \"checks\": {\n",
  "    \"layer_d_integral\": true,\n",
  "    \"incidence_rank_integral\": true,\n",
  "    \"layer_sum_is_v\": true,\n",
  "    \"coefficient_parity_iff_mod4_3\": true,\n",
  "    \"anchor_dimensions\": true\n",
  "  }\n",
  "}\n"
);;
CloseStream(stream);;
Print("Pass 202 GAP arithmetic correction: PASS\n");
