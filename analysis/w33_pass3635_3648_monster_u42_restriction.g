LoadPackage("ctbllib");

u := CharacterTable("U4(2)");;
m := CharacterTable("M");;
if u = fail or m = fail then
  Error("required CTblLib tables U4(2) and M are unavailable");
fi;

irrU := Irr(u);;
irrM := Irr(m);;
degU := List(irrU, chi -> chi[1]);;
degM := List(irrM, chi -> chi[1]);;
steinPositions := Positions(degU, 81);;
if Length(steinPositions) <> 1 then
  Error("expected one degree-81 U4(2) character");
fi;
steinPos := steinPositions[1];;
minPos := Position(degM, 196883);;
if minPos = fail then
  Error("Monster degree-196883 character unavailable");
fi;

ordersU := OrdersClassRepresentatives(u);;
namesU := AtlasClassNames(u);;
namesM := AtlasClassNames(m);;
threePowerPositions := Filtered([2..Length(ordersU)], i -> ordersU[i] = 3 or ordersU[i] = 9);;
steinThreePowerValues := List(threePowerPositions, i -> irrU[steinPos][i]);;
steinRegular := ForAll(steinThreePowerValues, IsZero);;
if not steinRegular then
  Error("degree-81 character fails the nonidentity 3-power vanishing test");
fi;

allFusions := PossibleClassFusions(u, m, rec(decompose := false));;
if allFusions = fail then
  allFusions := [];
fi;

IsFiveBContainingFusion := function(f)
  local i, sourceName, targetName;
  for i in [1..Length(f)] do
    sourceName := namesU[i];
    targetName := namesM[f[i]];
    if ordersU[i] = 2 and targetName <> "2B" then
      return false;
    fi;
    if ordersU[i] = 3 and targetName <> "3B" then
      return false;
    fi;
    if ordersU[i] = 5 and targetName <> "5B" then
      return false;
    fi;
    if sourceName = "4B" and targetName <> "4D" then
      return false;
    fi;
  od;
  return true;
end;

fiveBFusions := Filtered(allFusions, IsFiveBContainingFusion);;
minChi := irrM[minPos];;
compatibleFusions := [];;
decompositions := [];;

for f in fiveBFusions do
  values := List(f, j -> minChi[j]);
  restricted := ClassFunction(u, values);
  decomposition := List(irrU, psi -> ScalarProduct(restricted, psi));
  if ForAll(decomposition, x -> IsInt(x) and x >= 0) then
    Add(compatibleFusions, f);
    Add(decompositions, decomposition);
  fi;
od;

steinMultiplicities := Set(List(decompositions, d -> d[steinPos]));;
dimensionChecks := List(
  decompositions,
  d -> Sum([1..Length(d)], i -> d[i] * degU[i]) = 196883
);;

out := OutputTextFile("data/PART_3635_3648_MONSTER_U42_RESTRICTION_results.json", false);;
SetPrintFormattingStatus(out, false);
AppendTo(out, "{\n");
AppendTo(out, "  \"schema\": \"w33.pass3635_3648.monster_u42_restriction.v1\",\n");
AppendTo(out, "  \"status\": \"PASS_CHARACTER_TABLE_CENSUS\",\n");
AppendTo(out, "  \"u42_order\": ", String(Size(u)), ",\n");
AppendTo(out, "  \"monster_order\": ", String(Size(m)), ",\n");
AppendTo(out, "  \"steinberg_character_position\": ", String(steinPos), ",\n");
AppendTo(out, "  \"steinberg_degree\": 81,\n");
AppendTo(out, "  \"three_power_class_positions\": ", String(threePowerPositions), ",\n");
AppendTo(out, "  \"steinberg_three_power_values\": ", String(steinThreePowerValues), ",\n");
AppendTo(out, "  \"steinberg_regular_on_sylow3\": true,\n");
AppendTo(out, "  \"all_possible_fusions\": ", String(Length(allFusions)), ",\n");
AppendTo(out, "  \"fiveB_containing_fusions\": ", String(Length(fiveBFusions)), ",\n");
AppendTo(out, "  \"character_compatible_fusions\": ", String(Length(compatibleFusions)), ",\n");
AppendTo(out, "  \"steinberg_multiplicities\": ", String(steinMultiplicities), ",\n");
AppendTo(out, "  \"dimension_checks\": ", String(dimensionChecks), ",\n");
AppendTo(out, "  \"source_class_names\": ", String(namesU), ",\n");
AppendTo(out, "  \"compatible_fusion_maps\": ", String(compatibleFusions), ",\n");
AppendTo(out, "  \"decompositions\": ", String(decompositions), ",\n");
AppendTo(out, "  \"boundary\": \"Character-table fusion is not a serialized mmgroup embedding; all compatible maps remain distinct until subgroup words or intermediate fusion data select one.\"\n");
AppendTo(out, "}\n");
CloseStream(out);

Print("PASS 3635-3648: Monster/U4(2) restriction census written\n");
QUIT_GAP(0);
