# Pass 207: GAP-owned marker and companion-arithmetic audit for the Lean file.
#
# This is deliberately not a Lean parser or kernel.  It checks exact source
# markers and independently verifies the companion polynomial/parity formulas.
# A real `lake build` remains required for type-checking.

OUT := "data/w33_pass207_lean_shadow_certificate.json";;
LEAN := "formal/W33/ShadowDichotomy.lean";;
ROOTLEAN := "formal/W33.lean";;

src := StringFile(LEAN);;
rootSrc := StringFile(ROOTLEAN);;
Contains := function(text, marker)
  return PositionSublist(text, marker) <> fail;
end;;

TwoLayerD := q -> (q - 1) * (q^2 + q + 2);;
ShadowDim := q -> q^2 - 1;;
CoefficientParity := q ->
  ((q^2 - 1) / 2) mod 2 = 0 and ((q + 1) / 2) mod 2 = 0;;

checks := rec(
  imports_mathlib := Contains(src, "import Mathlib"),
  no_sorry := not Contains(src, "sorry"),
  no_axiom_declaration := not Contains(src, "axiom "),
  namespace_present := Contains(src, "namespace W33.ShadowDichotomy"),
  declares_twoLayerD := Contains(src, "def twoLayerD"),
  declares_shadowDim := Contains(src, "def shadowDim"),
  declares_twoIncidenceRank := Contains(src, "def twoIncidenceRank"),
  declares_nondegenerate := Contains(src, "def nondegenerate"),
  declares_layer_sum_eq_v := Contains(src, "theorem layer_sum_eq_v"),
  declares_nondegenerate_iff := Contains(src, "theorem nondegenerate_iff"),
  declares_two_incidence_rank_def := Contains(src, "theorem two_incidence_rank_def"),
  imported_in_project_root := Contains(rootSrc, "import W33.ShadowDichotomy"),
  layer_sum_polynomial_identity := ForAll([-50..299], q ->
    4 + TwoLayerD(q) + ShadowDim(q) = (q + 1) * (q^2 + 1)),
  coefficient_parity_exhaustive := ForAll(Filtered([3..999], q -> q mod 2 = 1),
    q -> CoefficientParity(q) = (q mod 4 = 3)),
  example_dimensions := [ShadowDim(3), ShadowDim(7), ShadowDim(11)] = [8,48,120]
);;

if not ForAll(RecNames(checks), name -> checks.(name)) then
  Error("Pass 207 marker/arithmetic audit failed");
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
  "  \"schema\": \"w33.pass207.lean_shadow_marker_arithmetic.gap.v2\",\n",
  "  \"status\": \"PASS\",\n",
  "  \"producer\": \"GAP ", GAPInfo.Version, "\",\n",
  "  \"lean_file\": \"formal/W33/ShadowDichotomy.lean\",\n",
  "  \"verification\": {\n",
  "    \"source_markers\": true,\n",
  "    \"companion_arithmetic\": true,\n",
  "    \"lean_parser\": false,\n",
  "    \"lean_kernel_run\": false,\n",
  "    \"typecheck_guaranteed\": false\n",
  "  },\n",
  "  \"honest_scope\": \"selected source markers plus independent GAP arithmetic; not a parser, kernel certificate, or substitute for lake build\",\n",
  "  \"checks\": {\n",
  "    \"imports_mathlib\": true,\n",
  "    \"no_sorry\": true,\n",
  "    \"no_axiom_declaration\": true,\n",
  "    \"namespace_present\": true,\n",
  "    \"expected_declarations_present\": true,\n",
  "    \"imported_in_project_root\": true,\n",
  "    \"layer_sum_polynomial_identity\": true,\n",
  "    \"coefficient_parity_exhaustive\": true,\n",
  "    \"example_dimensions\": true\n",
  "  }\n",
  "}\n"
);;
CloseStream(stream);;
Print("Pass 207 GAP marker/arithmetic audit: PASS\n");
