# Pass 338: the regular S3 refinement of the W(3,3) selector is a
# principal 240-cover over the p40b line action.  It is not the signed-E8
# 240-action, whose forty hexads lie over the nonconjugate p40a action.

LoadPackage("atlasrep");;

OUT338 := "data/w33_pass338_selector_frame_240.json";;

Assert338 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass338 assertion failed: ", label));
  fi;
end;;

Bool338 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

AtlasGroup338 := function(name, repname)
  local info;
  info := First(AllAtlasGeneratingSetInfos(name), entry ->
    IsBound(entry.repname) and entry.repname = repname);
  Assert338(Concatenation("ATLAS record ", repname), info <> fail);
  return Group(AtlasGenerators(info.identifier).generators);
end;;

Subdegrees338 := function(group)
  return SortedList(List(Orbits(Stabilizer(group, 1),
    [1..LargestMovedPoint(group)]), Length));
end;;

Main338 := function()
  local p40a, p40b, symmetric40, inner, lineStabilizer, normals, kernel,
        cosets, action, frame, innerFrame, blocks, normalizer, deck,
        subdegrees, innerSubdegrees, quotientRows, block, system, hom,
        quotient, innerQuotient, naturalSix, flip, twistedSix,
        signed, signedBlocks, hexad, hexads, hexadHom, hexadQuotient,
        signedSubdegrees, checks, names, stream, name;

  p40a := AtlasGroup338("U4(2).2", "U42d2G1-p40aB0");
  p40b := AtlasGroup338("U4(2).2", "U42d2G1-p40bB0");
  symmetric40 := SymmetricGroup(40);
  inner := DerivedSubgroup(p40b);
  lineStabilizer := Stabilizer(p40b, 1);
  normals := Filtered(NormalSubgroups(lineStabilizer), subgroup ->
    Index(lineStabilizer, subgroup) = 6 and
    StructureDescription(FactorGroup(lineStabilizer, subgroup)) = "S3");
  Assert338("unique regular fibre kernel", Length(normals) = 1);
  kernel := normals[1];
  cosets := RightCosets(p40b, kernel);
  action := ActionHomomorphism(p40b, cosets, OnRight);
  frame := Image(action);
  innerFrame := Image(action, inner);
  blocks := AllBlocks(frame);
  normalizer := Normalizer(p40b, kernel);
  deck := FactorGroup(normalizer, kernel);
  subdegrees := Subdegrees338(frame);
  innerSubdegrees := Subdegrees338(innerFrame);

  quotientRows := [];
  for block in blocks do
    system := Blocks(frame, [1..240], block);
    hom := ActionHomomorphism(frame, system, OnSets);
    quotient := Image(hom);
    innerQuotient := Image(hom, innerFrame);
    Add(quotientRows, [Length(block), Length(system),
      ScalarProduct(NaturalCharacter(quotient), NaturalCharacter(quotient)),
      Subdegrees338(quotient),
      ScalarProduct(NaturalCharacter(innerQuotient),
        NaturalCharacter(innerQuotient)),
      Subdegrees338(innerQuotient)]);
  od;

  # The integral outer S3 of Pass 333 acts naturally on two copies of its
  # three-leaf set.  The canonical simultaneous refinement flip centralizes
  # it.  Twisting odd elements by that flip changes 3+3 into the regular S3.
  naturalSix := Group((1,2,3)(4,5,6), (2,3)(5,6));
  flip := (1,4)(2,5)(3,6);
  twistedSix := Group((1,2,3)(4,5,6), flip * (2,3)(5,6));

  signed := AtlasGroup338("2.U4(2).2", "2U42d2G1-p240B0");
  signedBlocks := AllBlocks(signed);
  hexad := First(signedBlocks, candidate -> Length(candidate) = 6);
  hexads := Blocks(signed, [1..240], hexad);
  hexadHom := ActionHomomorphism(signed, hexads, OnSets);
  hexadQuotient := Image(hexadHom);
  signedSubdegrees := Subdegrees338(signed);

  checks := rec();
  checks.p40a_and_p40b_are_nonconjugate :=
    not IsConjugate(symmetric40, p40a, p40b);
  checks.selector_line_stabilizer_exact :=
    Size(lineStabilizer) = 1296 and
    StructureDescription(lineStabilizer) =
      "(C3 x C3 x C3) : (C2 x S4)";
  checks.unique_kernel_and_regular_deck :=
    Size(kernel) = 216 and StructureDescription(kernel) = "S3 x S3 x S3" and
    normalizer = lineStabilizer and StructureDescription(deck) = "S3";
  checks.principal_240_cover_is_faithful_and_transitive :=
    Length(cosets) = 240 and Size(frame) = 51840 and
    Size(Kernel(action)) = 1 and IsTransitive(frame, [1..240]);
  checks.inner_group_is_also_transitive :=
    Size(innerFrame) = 25920 and IsTransitive(innerFrame, [1..240]);
  checks.full_rank_and_subdegrees :=
    ScalarProduct(NaturalCharacter(frame), NaturalCharacter(frame)) = 13 and
    subdegrees = [1,1,1,1,1,1,27,27,27,27,27,27,72];
  checks.inner_rank_and_subdegrees :=
    ScalarProduct(NaturalCharacter(innerFrame),
      NaturalCharacter(innerFrame)) = 14 and
    innerSubdegrees = [1,1,1,1,1,1,27,27,27,27,27,27,36,36];
  checks.block_ledger_is_S3_subgroup_lattice :=
    Collected(SortedList(List(blocks, Length))) = [[2,3],[3,1],[6,1]];
  checks.intermediate_quotients_exact :=
    Collected(SortedList(quotientRows)) = [
      [[2,120,5,[1,2,27,36,54],5,[1,2,27,36,54]],3],
      [[3,80,5,[1,1,24,27,27],6,[1,1,12,12,27,27]],1],
      [[6,40,3,[1,12,27],3,[1,12,27]],1]
    ];
  checks.three_120_quotients_recover_selector_action :=
    Number(quotientRows, row -> row[1] = 2 and row[2] = 120 and
      row[4] = [1,2,27,36,54]) = 3;
  checks.new_80_parity_quotient_exact :=
    Number(quotientRows, row -> row[1] = 3 and row[2] = 80 and
      row[4] = [1,1,24,27,27] and
      row[6] = [1,1,12,12,27,27]) = 1;
  checks.integral_refinement_action_is_three_plus_three :=
    Size(naturalSix) = 6 and
    SortedList(List(Orbits(naturalSix, [1..6]), Length)) = [3,3];
  checks.refinement_flip_is_central :=
    ForAll(GeneratorsOfGroup(naturalSix), generator ->
      Comm(generator, flip) = ());
  checks.sign_twist_is_regular_S3 :=
    Size(twistedSix) = 6 and IsTransitive(twistedSix, [1..6]) and
    Size(Stabilizer(twistedSix, 1)) = 1;
  checks.signed_E8_action_exact :=
    Size(signed) = 103680 and
    Collected(SortedList(List(signedBlocks, Length))) = [[2,1],[6,1]] and
    signedSubdegrees = [1,1,4,54,72,108];
  checks.signed_hexad_base_is_p40a :=
    Length(hexads) = 40 and Size(Kernel(hexadHom)) = 2 and
    IsConjugate(symmetric40, hexadQuotient, p40a) and
    not IsConjugate(symmetric40, hexadQuotient, p40b);
  checks.selector_frame_is_not_signed_E8 :=
    Size(frame) <> Size(signed) and subdegrees <> signedSubdegrees;

  names := RecNames(checks);
  Assert338("all checks", ForAll(names, name -> checks.(name)));

  stream := OutputTextFile(OUT338, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass338.selector_frame_240.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"the W(3,3) selector has a faithful principal S3 frame cover of degree 240 over p40b; signed E8 lies over nonconjugate p40a\",\n");
  WriteAll(stream, "  \"selector_frame\": {\n");
  WriteAll(stream, "    \"orders_G_K_N\": [51840,1296,216],\n");
  WriteAll(stream, "    \"deck\": \"S3\",\n");
  WriteAll(stream, Concatenation("    \"subdegrees\": ", String(subdegrees), ",\n"));
  WriteAll(stream, Concatenation("    \"inner_subdegrees\": ", String(innerSubdegrees), ",\n"));
  WriteAll(stream, "    \"block_sizes\": {\"2\":3,\"3\":1,\"6\":1},\n");
  WriteAll(stream, "    \"quotients\": \"three degree-120 selector quotients, one degree-80 refinement-parity quotient, and the degree-40 W(3,3) base\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"signed_E8_comparison\": {\n");
  WriteAll(stream, "    \"order\": 103680,\n");
  WriteAll(stream, "    \"subdegrees\": [1,1,4,54,72,108],\n");
  WriteAll(stream, "    \"forty_hexad_base\": \"p40a, not p40b\",\n");
  WriteAll(stream, "    \"equivalent_to_selector_frame\": false\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"refinement_twist\": {\"integral_orbits\":[3,3],\"sign_twisted_orbit\":[6],\"interpretation\":\"the central refinement flip converts the natural two-copy S3 action into the regular fibre action\"},\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for name in names do
    WriteAll(stream, Concatenation("    \"", name, "\": ", Bool338(checks.(name))));
    if name <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);
  Print("Pass338 status=PASS checks=", Length(names), " output=", OUT338, "\n");
end;;

Main338();;
QUIT;
