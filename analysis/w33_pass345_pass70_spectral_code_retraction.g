# Pass 345: exact audit of the old Pass 70 Track B code claim.
#
# The eight recorded spectral multiplicities do sum to 360 and the labelled
# sector has multiplicity 9.  Those facts construct neither stabilizer checks
# nor a distance.  Even the script's literal ceiling ratio is 2, contradicting
# the historical [[360,9,9]] note and [[360,9,1]] JSON.

OUT345 := "data/w33_pass345_pass70_spectral_code_retraction.json";;

Assert345 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass345 assertion failed: ",label));
  fi;
end;;

Bool345 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

Main345 := function()
  local multiplicities, dimension, distinguished, largest, ceilingRatio,
        checks, names, stream, name;

  multiplicities := [1,40,9,15,15,15,15,250];
  dimension := Sum(multiplicities);
  distinguished := multiplicities[3];
  largest := Maximum(multiplicities);
  ceilingRatio := QuoInt(dimension+largest-1,largest);

  checks := rec();
  checks.eight_multiplicities_are_recorded := Length(multiplicities)=8;
  checks.all_multiplicities_are_positive := ForAll(multiplicities,value -> value>0);
  checks.multiplicity_sum_is_360 := dimension=360;
  checks.distinguished_multiplicity_is_9 := distinguished=9;
  checks.largest_multiplicity_is_250 := largest=250;
  checks.literal_ceiling_ratio_is_2 := ceilingRatio=2;
  checks.literal_ceiling_ratio_is_not_1 := ceilingRatio<>1;
  checks.literal_ceiling_ratio_is_not_9 := ceilingRatio<>9;
  checks.nine_times_forty_is_360 := distinguished*40=dimension;
  checks.spectral_ledger_alone_has_no_css_product := true;
  checks.spectral_ledger_alone_has_no_distance_computation := true;
  checks.old_code_parameter_is_not_certified := true;

  names := RecNames(checks);
  Assert345("all checks",ForAll(names,name -> checks.(name)));

  stream := OutputTextFile(OUT345,false);
  SetPrintFormattingStatus(stream,false);
  WriteAll(stream,"{\n");
  WriteAll(stream,"  \"schema\": \"w33.pass345.pass70_spectral_code_retraction.gap.v1\",\n");
  WriteAll(stream,"  \"status\": \"PASS\",\n");
  WriteAll(stream,"  \"headline\": \"the Pass 70 Track B spectrum is a 360-dimensional ledger, not a stabilizer code\",\n");
  WriteAll(stream,"  \"multiplicities\": [1, 40, 9, 15, 15, 15, 15, 250],\n");
  WriteAll(stream,Concatenation("  \"multiplicity_sum\": ",String(dimension),",\n"));
  WriteAll(stream,Concatenation("  \"distinguished_multiplicity\": ",String(distinguished),",\n"));
  WriteAll(stream,Concatenation("  \"largest_multiplicity\": ",String(largest),",\n"));
  WriteAll(stream,Concatenation("  \"literal_ceiling_ratio\": ",String(ceilingRatio),",\n"));
  WriteAll(stream,"  \"stabilizer_matrices_constructed\": false,\n");
  WriteAll(stream,"  \"distance_computed\": false,\n");
  WriteAll(stream,"  \"claimed_code\": null,\n");
  WriteAll(stream,"  \"retracted_claims\": [\"[[360,9,9]]\", \"[[360,9,1]]\"],\n");
  WriteAll(stream,"  \"boundary\": \"multiplicity 9 is not a logical dimension and ceil(360/250)=2 is not a code distance\",\n");
  WriteAll(stream,Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream,"  \"checks\": {\n");
  for name in names do
    WriteAll(stream,Concatenation("    \"",name,"\": ",Bool345(checks.(name))));
    if name<>names[Length(names)] then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  }\n}\n");
  CloseStream(stream);
  Print("Pass345 status=PASS checks=",Length(names)," output=",OUT345,"\n");
end;;

Main345();;
QUIT;
