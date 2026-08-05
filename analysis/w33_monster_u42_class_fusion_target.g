# Passes 3694-3700: fail-closed U4(2) -> Monster class-fusion target.
# Requires GAP + CTblLib. It enumerates only maps satisfying the encoded
# 5B-containing Holmes-Wilson constraints, restricts the Monster character of
# degree 196883, and records multiplicities of all degree-81 U4(2) irreducibles.

if LoadPackage("ctbllib") <> true then Error("CTblLib is required"); fi;
s := CharacterTable("U4(2)");;
m := CharacterTable("M");;
if s = fail or m = fail then Error("required character table missing"); fi;

namesS := ClassNames(s, "Atlas");;
namesM := ClassNames(m, "Atlas");;
ordersS := OrdersClassRepresentatives(s);;

PosM := function(name)
  local p;
  p := Position(namesM, name);
  if p = fail then Error(Concatenation("Monster class missing: ", name)); fi;
  return p;
end;

init := InitFusion(s, m);;
# 5B-containing U4(2) constraints from the subgroup classification.
for i in [1..Length(ordersS)] do
  if ordersS[i] = 2 then init[i] := [PosM("2B")]; fi;
  if ordersS[i] = 3 then init[i] := [PosM("3B")]; fi;
  if ordersS[i] = 5 then init[i] := [PosM("5B")]; fi;
od;
if Position(namesS, "4B") <> fail then
  init[Position(namesS, "4B")] := [PosM("4D")];
fi;

fusions := PossibleClassFusions(s, m,
  rec(fusionmap := init, decompose := false));;
irrS := Irr(s);;
irrM := Irr(m);;
degS := List(irrS, DegreeOfCharacter);;
degM := List(irrM, DegreeOfCharacter);;
pos81 := Positions(degS, 81);;
pos196883 := Position(degM, 196883);;
if pos196883 = fail then Error("Monster degree-196883 character missing"); fi;

Print("{\n");
Print("  \"schema\": \"w33.monster_u42_class_fusion_target.v1\",\n");
Print("  \"source_class_names\": ", namesS, ",\n");
Print("  \"source_class_orders\": ", ordersS, ",\n");
Print("  \"degree_81_positions\": ", pos81, ",\n");
Print("  \"fusion_count\": ", Length(fusions), ",\n");
Print("  \"records\": [\n");
for k in [1..Length(fusions)] do
  fus := fusions[k];
  res := RestrictedClassFunction(irrM[pos196883], s, fus);
  mults := List(pos81, p -> ScalarProduct(s, irrS[p], res));
  decomp := List(irrS, chi -> ScalarProduct(s, chi, res));
  Print("    {\"fusion_index\": ", k,
        ", \"fusion_map\": ", fus,
        ", \"degree_81_multiplicities\": ", mults,
        ", \"full_decomposition\": ", decomp, "}");
  if k < Length(fusions) then Print(","); fi;
  Print("\n");
od;
Print("  ],\n");
Print("  \"status\": \"EXECUTED_CTBLIB_CLASS_FUSION_CENSUS\"\n");
Print("}\n");
QUIT;
