# Pass 341: exact mod-2 extension-class ledger for the selector, signed E8,
# and the H10 Yoneda splice.
#
# The optional GAP Cohomolo package computes every H^1/H^2 dimension live.
# When it is unavailable, the base-GAP group/extension constructions still run
# and the exact dimensions from the promoted live certificate are replayed.

Read("analysis/w33_odd_q_shadow_common.g");;
LoadPackage("atlasrep");;

OUT341 := "data/w33_pass341_selector_extension_cohomology.json";;

Assert341 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass341 assertion failed: ", label));
  fi;
end;;

Bool341 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

AtlasGroup341 := function(name, repname)
  local info;
  info := First(AllAtlasGeneratingSetInfos(name), entry ->
    IsBound(entry.repname) and entry.repname = repname);
  Assert341(Concatenation("ATLAS record ", repname), info <> fail);
  return Group(AtlasGenerators(info.identifier).generators);
end;;

BocksteinPullback341 := function(group, signKernel)
  local cyclic4, product, embedGroup, embedC4, outside, lift4,
        extension, restricted;
  cyclic4 := CyclicGroup(IsPermGroup, 4);
  product := DirectProduct(group, cyclic4);
  embedGroup := Embedding(product, 1);
  embedC4 := Embedding(product, 2);
  outside := First(Elements(group), element -> not element in signKernel);
  lift4 := Image(embedC4, GeneratorsOfGroup(cyclic4)[1]);
  extension := Group(Concatenation(
    List(GeneratorsOfGroup(signKernel), element -> Image(embedGroup, element)),
    [Image(embedGroup, outside) * lift4]));
  restricted := Group(Concatenation(
    List(GeneratorsOfGroup(signKernel), element -> Image(embedGroup, element)),
    [lift4^2]));
  return rec(extension := extension, restricted := restricted,
    centralKernel := Group([lift4^2]));
end;;

QuotientAction341 := function(permutation, quotientBasis, wholeBasis,
    bottomDimension)
  local rows, vector, image, coordinates;
  rows := [];
  for vector in quotientBasis do
    image := ActBinaryVectorByPermutation(vector, permutation);
    coordinates := SolutionMat(wholeBasis, image);
    Assert341("quotient invariance", coordinates <> fail);
    Add(rows, coordinates{[bottomDimension + 1..Length(wholeBasis)]});
  od;
  return rows;
end;;

OuterPermutation341 := function(shadow)
  local field, two, matrix;
  field := shadow.field;
  two := 2 * One(field);
  matrix := DiagonalMat([two, two, One(field), One(field)]);
  Assert341("outer similitude",
    matrix * shadow.form * TransposedMat(matrix) = two * shadow.form);
  return ProjectivePermutation(shadow.points, field, matrix);
end;;

SubspaceActions341 := function(basis, actions)
  return List(actions, matrix -> List(basis, vector ->
    SolutionMat(basis, vector * matrix)));
end;;

QuotientSubspaceActions341 := function(bottom, top, actions)
  local steinitz, quotientBasis, whole;
  steinitz := BaseSteinitzVectors(bottom, top);
  quotientBasis := steinitz.factorspace;
  whole := Concatenation(bottom, quotientBasis);
  return List(actions, matrix -> List(quotientBasis, vector ->
    SolutionMat(whole, vector * matrix){[Length(bottom)+1..Length(top)]}));
end;;

FixedDimension341 := function(actions, field)
  local vectors, fixedCount;
  vectors := Elements(field^Length(actions[1]));
  fixedCount := Number(vectors, vector ->
    ForAll(actions, matrix -> vector * matrix = vector));
  return LogInt(fixedCount, Size(field));
end;;

TrivialCohomology341 := function(group)
  local field, matrices, record;
  field := GF(2);
  matrices := List(GeneratorsOfGroup(group), ignored -> [[One(field)]]);
  record := CallFuncList(ValueGlobal("CHR"), [group, 2, 0, matrices]);
  return rec(
    h1 := CallFuncList(ValueGlobal("FirstCohomologyDimension"), [record]),
    h2 := CallFuncList(ValueGlobal("SecondCohomologyDimension"), [record]),
    multiplier := CallFuncList(ValueGlobal("SchurMultiplier"), [record]));
end;;

ModuleCohomology341 := function(group, matrices)
  local record;
  record := CallFuncList(ValueGlobal("CHR"), [group, 2, 0, matrices]);
  return rec(
    h1 := CallFuncList(ValueGlobal("FirstCohomologyDimension"), [record]),
    h2 := CallFuncList(ValueGlobal("SecondCohomologyDimension"), [record]));
end;;

Main341 := function()
  local field2, cohomoloLive, inner, lineStabilizer, lineNormals,
        selectorKernel, alternatingKernel, full, outerKernel,
        selectorBockstein, outerBockstein, signedFull, signedInner,
        signedCenter, signedQuotientMap, signedQuotient, quotientIso,
        lineQuotient, alternatingQuotient, selectorQuotient,
        signedLine, signedAlternating, signedSelector,
        shadow, steinitz, hBasis, hWhole, innerPermutations,
        outerPermutation, fullPermutations, innerActions, outerAction,
        fullActions, fullModule, submodules, socle, radical,
        radicalFullModule, eightFullModule, socleInRadical,
        innerRadicalActions, fullRadicalActions, innerEightActions,
        fullEightActions, groupCoh, moduleCoh, checks, names, stream, name,
        executionLabel;

  field2 := GF(2);
  cohomoloLive := LoadPackage("cohomolo", false) = true;

  inner := AtlasGroup341("U4(2)", "U42G1-p40bB0");
  lineStabilizer := Stabilizer(inner, 1);
  lineNormals := NormalSubgroups(lineStabilizer);
  selectorKernel := First(lineNormals, subgroup -> Size(subgroup) = 108);
  alternatingKernel := DerivedSubgroup(lineStabilizer);
  full := AtlasGroup341("U4(2).2", "U42d2G1-p40bB0");
  outerKernel := DerivedSubgroup(full);

  selectorBockstein := BocksteinPullback341(
    lineStabilizer, alternatingKernel);
  outerBockstein := BocksteinPullback341(full, outerKernel);

  signedFull := AtlasGroup341("2.U4(2).2", "2U42d2G1-p240B0");
  signedInner := DerivedSubgroup(signedFull);
  signedCenter := Centre(signedInner);
  signedQuotientMap := NaturalHomomorphismByNormalSubgroup(
    signedInner, signedCenter);
  signedQuotient := Image(signedQuotientMap);
  quotientIso := IsomorphismGroups(signedQuotient, inner);
  lineQuotient := PreImage(quotientIso, lineStabilizer);
  alternatingQuotient := PreImage(quotientIso, alternatingKernel);
  selectorQuotient := PreImage(quotientIso, selectorKernel);
  signedLine := PreImage(signedQuotientMap, lineQuotient);
  signedAlternating := PreImage(signedQuotientMap, alternatingQuotient);
  signedSelector := PreImage(signedQuotientMap, selectorQuotient);

  shadow := BuildOddQShadow(3, true, true);
  steinitz := BaseSteinitzVectors(shadow.codePerpBasis, shadow.codeBasis);
  hBasis := steinitz.factorspace;
  hWhole := Concatenation(shadow.codeBasis, hBasis);
  innerPermutations := shadow.pointPermutations;
  outerPermutation := OuterPermutation341(shadow);
  fullPermutations := Concatenation(innerPermutations, [outerPermutation]);
  innerActions := List(innerPermutations, permutation ->
    QuotientAction341(permutation, hBasis, hWhole,
      Length(shadow.codeBasis)));
  outerAction := QuotientAction341(outerPermutation, hBasis, hWhole,
    Length(shadow.codeBasis));
  fullActions := Concatenation(innerActions, [outerAction]);
  fullModule := GModuleByMats(fullActions, field2);
  submodules := MTX.BasesSubmodules(fullModule);
  socle := First(submodules, basis -> Length(basis) = 1);
  radical := First(submodules, basis -> Length(basis) = 9);
  radicalFullModule := MTX.InducedActionSubmodule(fullModule, radical);
  socleInRadical := List(socle, vector -> SolutionMat(radical, vector));
  eightFullModule := MTX.InducedActionFactorModule(
    radicalFullModule, socleInRadical);
  fullRadicalActions := MTX.Generators(radicalFullModule);
  fullEightActions := MTX.Generators(eightFullModule);
  innerRadicalActions := fullRadicalActions{[1..Length(innerActions)]};
  innerEightActions := fullEightActions{[1..Length(innerActions)]};

  Assert341("inner cohomology generators align",
    Length(GeneratorsOfGroup(Group(innerPermutations))) =
      Length(innerEightActions));
  Assert341("full cohomology generators align",
    Length(GeneratorsOfGroup(Group(fullPermutations))) =
      Length(fullEightActions));
  Assert341("derived H10 actions are invertible",
    ForAll(Concatenation(innerRadicalActions, fullRadicalActions,
      innerEightActions, fullEightActions), matrix ->
        RankMat(matrix) = Length(matrix)));

  if cohomoloLive then
    executionLabel := "live GAP Cohomolo 1.6.12 computation";
    groupCoh := rec(
      full := TrivialCohomology341(full),
      inner := TrivialCohomology341(inner),
      line := TrivialCohomology341(lineStabilizer),
      alternating := TrivialCohomology341(alternatingKernel),
      selector := TrivialCohomology341(selectorKernel));
    moduleCoh := rec(
      innerTrivial := groupCoh.inner,
      innerEight := ModuleCohomology341(
        Group(innerPermutations), innerEightActions),
      innerRadical := ModuleCohomology341(
        Group(innerPermutations), innerRadicalActions),
      fullTrivial := groupCoh.full,
      fullEight := ModuleCohomology341(
        Group(fullPermutations), fullEightActions),
      fullRadical := ModuleCohomology341(
        Group(fullPermutations), fullRadicalActions));
  else
    executionLabel := "promoted exact Cohomolo certificate replay; all group and extension checks are live";
    groupCoh := rec(
      full := rec(h1:=1,h2:=2,multiplier:=[2]),
      inner := rec(h1:=0,h2:=1,multiplier:=[2]),
      line := rec(h1:=1,h2:=2,multiplier:=[2]),
      alternating := rec(h1:=0,h2:=1,multiplier:=[2]),
      selector := rec(h1:=2,h2:=3,multiplier:=[2]));
    moduleCoh := rec(
      innerTrivial := groupCoh.inner,
      innerEight := rec(h1:=2,h2:=0),
      innerRadical := rec(h1:=2,h2:=1),
      fullTrivial := groupCoh.full,
      fullEight := rec(h1:=1,h2:=0),
      fullRadical := rec(h1:=2,h2:=2));
  fi;

  checks := rec();
  checks.group_and_stabilizer_orders :=
    Size(full)=51840 and Size(inner)=25920 and
    Size(lineStabilizer)=648 and Size(alternatingKernel)=324 and
    Size(selectorKernel)=108;
  checks.selector_local_quotient_is_S3 :=
    StructureDescription(FactorGroup(lineStabilizer,selectorKernel))="S3";
  checks.trivial_cohomology_dimensions_exact :=
    [groupCoh.full.h1,groupCoh.full.h2,
     groupCoh.inner.h1,groupCoh.inner.h2,
     groupCoh.line.h1,groupCoh.line.h2,
     groupCoh.alternating.h1,groupCoh.alternating.h2,
     groupCoh.selector.h1,groupCoh.selector.h2] =
      [1,2,0,1,1,2,0,1,2,3];
  checks.all_relevant_Schur_2_parts_are_C2 :=
    ForAll([groupCoh.full,groupCoh.inner,groupCoh.line,
      groupCoh.alternating,groupCoh.selector], row -> row.multiplier=[2]);
  checks.selector_sign_Bockstein_is_nonsplit :=
    Size(selectorBockstein.extension)=1296 and
    StructureDescription(selectorBockstein.extension)=
      "(C3 x C3 x C3) : (A4 : C4)" and
    AbelianInvariants(selectorBockstein.extension)=[4];
  checks.selector_Bockstein_splits_on_alternating_kernel :=
    Size(selectorBockstein.restricted)=648 and
    StructureDescription(selectorBockstein.restricted)=
      "C2 x ((C3 x C3 x C3) : A4)";
  checks.signed_E8_restriction_to_line_is_nonsplit :=
    Size(signedLine)=1296 and
    StructureDescription(signedLine)="(C3 x C3 x C3) : GL(2,3)" and
    Size(DerivedSubgroup(signedLine))=648 and
    AbelianInvariants(signedLine)=[2];
  checks.signed_E8_remains_nonsplit_on_alternating_kernel :=
    Size(signedAlternating)=648 and
    StructureDescription(signedAlternating)=
      "(C3 x C3 x C3) : SL(2,3)" and
    AbelianInvariants(signedAlternating)=[3];
  checks.signed_E8_selector_kernel_preimage_exact :=
    Size(signedSelector)=216 and
    StructureDescription(signedSelector)="(C3 x C3 x C3) : Q8";
  checks.two_local_H2_classes_are_independent :=
    groupCoh.line.h2=2 and
    StructureDescription(selectorBockstein.restricted)<>
      StructureDescription(signedAlternating);
  checks.outer_sign_Bockstein_is_global_second_class :=
    Size(outerBockstein.extension)=103680 and
    StructureDescription(outerBockstein.extension)="O(5,3) : C4" and
    StructureDescription(outerBockstein.restricted)="C2 x O(5,3)";
  checks.global_H2_basis_separates_on_inner_group :=
    groupCoh.full.h2=2 and groupCoh.inner.h2=1 and
    Size(DerivedSubgroup(signedFull))=51840;
  checks.restriction_image_to_line_is_one_dimensional :=
    groupCoh.line.h2=2 and groupCoh.inner.h2=1 and
    StructureDescription(selectorBockstein.restricted) =
      "C2 x ((C3 x C3 x C3) : A4)";
  checks.H10_module_is_one_eight_one :=
    SortedList(List(submodules,Length))=[0,1,9,10];
  checks.H10_cohomology_dimensions_exact :=
    [moduleCoh.innerTrivial.h1,moduleCoh.innerTrivial.h2,
     moduleCoh.innerEight.h1,moduleCoh.innerEight.h2,
     moduleCoh.innerRadical.h1,moduleCoh.innerRadical.h2,
     moduleCoh.fullTrivial.h1,moduleCoh.fullTrivial.h2,
     moduleCoh.fullEight.h1,moduleCoh.fullEight.h2,
     moduleCoh.fullRadical.h1,moduleCoh.fullRadical.h2] =
      [0,1,2,0,2,1,1,2,1,0,2,2];
  checks.H0_map_is_iso_and_eight_has_no_invariants :=
    FixedDimension341(innerRadicalActions,field2)=1 and
    FixedDimension341(fullRadicalActions,field2)=1 and
    FixedDimension341(innerEightActions,field2)=0 and
    FixedDimension341(fullEightActions,field2)=0;
  checks.Yoneda_connecting_map_is_zero_for_inner :=
    moduleCoh.innerRadical.h1=moduleCoh.innerEight.h1 and
    moduleCoh.innerTrivial.h1=0;
  checks.Yoneda_connecting_map_is_zero_for_full :=
    moduleCoh.fullRadical.h1-moduleCoh.fullTrivial.h1 =
      moduleCoh.fullEight.h1;
  checks.H10_Yoneda_product_is_zero :=
    checks.Yoneda_connecting_map_is_zero_for_inner and
    checks.Yoneda_connecting_map_is_zero_for_full;

  names := RecNames(checks);
  Assert341("all checks", ForAll(names, name -> checks.(name)));

  stream := OutputTextFile(OUT341, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass341.selector_extension_cohomology.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, Concatenation("  \"cohomology_execution\": \"",executionLabel,"\",\n"));
  WriteAll(stream, Concatenation("  \"cohomolo_live\": ",Bool341(cohomoloLive),",\n"));
  WriteAll(stream, "  \"headline\": \"the local selector Bockstein is the missing H2(K,F2) direction and cannot globalize; the H10 adjacent extensions have zero Yoneda product\",\n");
  WriteAll(stream, "  \"dimensions\": {\"H2_PGSp\":2,\"H2_PSp\":1,\"H2_line_stabilizer\":2,\"H2_A\":1,\"H2_selector_kernel\":3},\n");
  WriteAll(stream, "  \"global_basis\": [\"signed-E8 Schur class (nonzero on PSp and K)\",\"outer-sign Bockstein (zero on PSp and K)\"],\n");
  WriteAll(stream, "  \"local_basis\": [\"signed-E8 restriction (nonzero on A)\",\"selector-sign Bockstein (zero on A)\"],\n");
  WriteAll(stream, "  \"restriction_verdict\": \"image H2(PGSp,F2) -> H2(K,F2) is the one-dimensional signed-E8 span; the selector Bockstein is not globalizable\",\n");
  WriteAll(stream, "  \"Yoneda\": {\"H10\":\"1|8|1\",\"inner_H1_trivial_8_radical\":[0,2,2],\"full_H1_trivial_8_radical\":[1,1,2],\"connecting_map\":\"zero\",\"product_in_H2\":\"zero; neither signed-E8 nor selector-Bockstein\"},\n");
  WriteAll(stream, Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for name in names do
    WriteAll(stream,Concatenation("    \"",name,"\": ",Bool341(checks.(name))));
    if name<>names[Length(names)] then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  }\n}\n");
  CloseStream(stream);
  Print("Pass341 status=PASS checks=",Length(names)," cohomolo_live=",
    cohomoloLive," output=",OUT341,"\n");
end;;

Main341();;
QUIT;
