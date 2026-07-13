# Pass 206 correction ledger.
#
# The original Python experiment selected one representative in each of three
# filtration layers and then treated nine binary quotient directions as nine
# subsystem gauge qubits.  Neither step establishes the advertised theorem:
# layer minima require exhaustive orbit/coset minimisation, and a gauge qubit
# requires a hyperbolic X/Z Pauli pair.  GAP owns this withdrawal artifact so
# rerunning the historical Pass 206 entry point cannot restore the invalid
# [[40,1,9,4]] claim.

OUT := "data/w33_pass206_subsystem_distance_boost.json";;
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
  "  \"schema\": \"w33.pass206.subsystem_claim_withdrawal.v2\",\n",
  "  \"status\": \"WITHDRAWN\",\n",
  "  \"producer\": \"GAP withdrawal ledger\",\n",
  "  \"preserved\": {\n",
  "    \"base_css_code\": \"[[40,10,4]] sentinel CSS\",\n",
  "    \"filtration_dimensions\": \"15 < 16 < 24 < 25\"\n",
  "  },\n",
  "  \"withdrawn_claims\": {\n",
  "    \"layer_minima_12_6_4\": \"three selected cosets are not exhaustive layer minima\",\n",
  "    \"nine_gauge_qubits\": \"nine binary directions do not supply nine hyperbolic Pauli pairs\",\n",
  "    \"subsystem_parameters\": \"[[40,1,9,4]] is not established\",\n",
  "    \"bare_logical_robustness\": \"not established\"\n",
  "  },\n",
  "  \"replacement\": \"Pass 211: H is one 10-dimensional X/Z label copy and the full logical Pauli space has dimension 20\",\n",
  "  \"checks\": {\n",
  "    \"withdrawal_recorded\": true,\n",
  "    \"unsupported_subsystem_claim_present\": false\n",
  "  }\n",
  "}\n"
);;
CloseStream(stream);;
Print("Pass 206 subsystem-claim withdrawal: PASS\n");
