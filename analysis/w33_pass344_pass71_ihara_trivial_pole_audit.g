# Pass 344: exact GAP audit of the Pass 71 Track E Ihara classification.
#
# The vertex factor from the Perron eigenvalue 12 is
#   1 - 12u + 11u^2 = (1-u)(1-11u).
# Hence u=1 and u=1/11 are both trivial poles.  The remaining 78 roots
# come from lambda=2 (multiplicity 24) and lambda=-4 (multiplicity 15);
# their exact squared moduli are all 1/11.

OUT344 := "data/w33_pass344_pass71_ihara_trivial_pole_audit.json";;

Assert344 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass344 assertion failed: ", label));
  fi;
end;;

Bool344 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

Main344 := function()
  local u, bass, perronFactor, gaugeFactor, chiralFactor,
        gaugeDiscriminant, chiralDiscriminant, gaugeNormSquared,
        chiralNormSquared, spectrumMultiplicity, nontrivialRootCount,
        vertexFactorRootCount, checks, names, stream, name;

  u := Indeterminate(Rationals,"u");
  bass := 11;
  perronFactor := 1-12*u+bass*u^2;
  gaugeFactor := 1-2*u+bass*u^2;
  chiralFactor := 1+4*u+bass*u^2;

  gaugeDiscriminant := 2^2-4*bass;
  chiralDiscriminant := (-4)^2-4*bass;
  gaugeNormSquared := (1^2+10)/11^2;
  chiralNormSquared := ((-2)^2+7)/11^2;
  spectrumMultiplicity := 1+24+15;
  nontrivialRootCount := 2*(24+15);
  vertexFactorRootCount := 2*spectrumMultiplicity;

  checks := rec();
  checks.bass_parameter_is_11 := bass=11;
  checks.spectrum_multiplicities_sum_to_40 := spectrumMultiplicity=40;
  checks.perron_factorization_is_exact :=
    perronFactor=(1-u)*(1-11*u);
  checks.u_1_is_a_perron_root := Value(perronFactor,1)=0;
  checks.u_1_over_11_is_a_perron_root := Value(perronFactor,1/11)=0;
  checks.gauge_discriminant_is_minus_40 := gaugeDiscriminant=-40;
  checks.chiral_discriminant_is_minus_28 := chiralDiscriminant=-28;
  checks.nontrivial_discriminants_are_negative :=
    gaugeDiscriminant<0 and chiralDiscriminant<0;
  checks.gauge_root_norm_squared_is_1_over_11 :=
    gaugeNormSquared=1/11;
  checks.chiral_root_norm_squared_is_1_over_11 :=
    chiralNormSquared=1/11;
  checks.nontrivial_root_count_is_78 := nontrivialRootCount=78;
  checks.vertex_factor_root_count_is_80 := vertexFactorRootCount=80;
  checks.only_two_vertex_roots_are_perron_trivial :=
    vertexFactorRootCount-nontrivialRootCount=2;
  checks.graph_rh_classification_is_exact :=
    gaugeNormSquared=1/bass and chiralNormSquared=1/bass;

  names := RecNames(checks);
  Assert344("all checks",ForAll(names,name -> checks.(name)));

  stream := OutputTextFile(OUT344,false);
  SetPrintFormattingStatus(stream,false);
  WriteAll(stream,"{\n");
  WriteAll(stream,"  \"schema\": \"w33.pass344.pass71_ihara_trivial_pole_audit.gap.v1\",\n");
  WriteAll(stream,"  \"status\": \"PASS\",\n");
  WriteAll(stream,"  \"headline\": \"u=1/11 is the second Perron-trivial Ihara pole, not a Graph-RH violation\",\n");
  WriteAll(stream,"  \"perron_factor\": \"1 - 12u + 11u^2 = (1-u)(1-11u)\",\n");
  WriteAll(stream,"  \"perron_trivial_poles\": [\"1\", \"1/11\"],\n");
  WriteAll(stream,"  \"nontrivial_factors\": [\"1 - 2u + 11u^2\", \"1 + 4u + 11u^2\"],\n");
  WriteAll(stream,"  \"nontrivial_discriminants\": [-40, -28],\n");
  WriteAll(stream,"  \"nontrivial_root_forms\": [\"(1 +/- sqrt(-10))/11\", \"(-2 +/- sqrt(-7))/11\"],\n");
  WriteAll(stream,"  \"nontrivial_root_modulus_squared\": \"1/11\",\n");
  WriteAll(stream,Concatenation("  \"nontrivial_root_count\": ",String(nontrivialRootCount),",\n"));
  WriteAll(stream,Concatenation("  \"vertex_factor_root_count\": ",String(vertexFactorRootCount),",\n"));
  WriteAll(stream,"  \"graph_rh_satisfied\": true,\n");
  WriteAll(stream,"  \"correction_boundary\": \"the theorem was already correct; only the legacy Track E pole classifier was wrong\",\n");
  WriteAll(stream,Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream,"  \"checks\": {\n");
  for name in names do
    WriteAll(stream,Concatenation("    \"",name,"\": ",Bool344(checks.(name))));
    if name<>names[Length(names)] then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  }\n}\n");
  CloseStream(stream);
  Print("Pass344 status=PASS checks=",Length(names)," output=",OUT344,"\n");
end;;

Main344();;
QUIT;
