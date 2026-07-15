# Pass 337: the dual-number epsilon is the split endpoint deck, not the
# nonsplit signed-E8 Baer class.
#
# Pass 331 found the canonical rank-one nilpotent epsilon in
# End_G(H10)=F2[epsilon]/epsilon^2.  Pass 221 independently found two central
# C2-extensions of PGSp(4,3): the split endpoint cover and the nonsplit signed
# E8-root pullback.  This GAP certificate puts those objects in one exact
# ledger.
#
# The unit 1+epsilon centralizes the full PGSp image, but adjoining it gives
# precisely C2 x PGSp.  Its derived subgroup has order 25920 and its
# abelianization is C2 x C2.  The signed-E8 Atlas group 2.U4(2).2 instead has
# derived subgroup Sp(4,3) of order 51840 and abelianization C2.  They are not
# isomorphic.  Thus epsilon realizes the trivial/split Baer class (the
# canonical endpoint deck), not the nonzero Schur-cover class required by
# signed E8 equivariance.
#
# The module extension remains genuinely nonsplit: H10 has submodule lattice
# dimensions 0,1,9,10 and epsilon is exactly top -> socle.  The distinction is
# categorical, not a contradiction: a nonsplit module/Yoneda extension does
# not become a nonsplit central group extension merely by adjoining 1+epsilon.

Read("analysis/w33_odd_q_shadow_common.g");;
LoadPackage("atlasrep");;

OUT := "data/w33_pass337_epsilon_e8_baer_separation.json";;

Assert337 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass337 assertion failed: ", label));
  fi;
end;;

BoolJSON337 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

QuotientAction337 := function(permutation, quotientBasis, wholeBasis,
    bottomDimension)
  local rows, vector, image, coordinates;
  rows := [];
  for vector in quotientBasis do
    image := ActBinaryVectorByPermutation(vector, permutation);
    coordinates := SolutionMat(wholeBasis, image);
    Assert337("quotient invariance", coordinates <> fail);
    Add(rows, coordinates{
      [bottomDimension + 1..Length(wholeBasis)]});
  od;
  return rows;
end;;

OuterPermutation337 := function(shadow)
  local field, two, matrix;
  field := shadow.field;
  two := 2 * One(field);
  matrix := DiagonalMat([two, two, One(field), One(field)]);
  Assert337("multiplier-two similitude",
    matrix * shadow.form * TransposedMat(matrix) = two * shadow.form);
  return ProjectivePermutation(shadow.points, field, matrix);
end;;

Main337 := function()
  local field2, shadow, steinitz, hBasis, hWhole, innerActions,
        outerPermutation, outerAction, fullActions, innerGroup, fullGroup,
        innerModule, fullModule, endBasis, epsilon, identity, deckUnit,
        submodules, socle, radical, epsilonImage, epsilonKernel,
        epsilonInnerExtension, epsilonFullExtension, epsilonKernelGroup,
        epsilonQuotientMap, epsilonQuotient, signedInfo, signedAtlas,
        signedFull, signedCenter, signedQuotientMap, signedQuotient,
        signedDerived, checks, checkNames,
        allPass, status, stream, name;

  field2 := GF(2);
  shadow := BuildOddQShadow(3, true, true);
  steinitz := BaseSteinitzVectors(
    shadow.codePerpBasis, shadow.codeBasis);
  hBasis := steinitz.factorspace;
  hWhole := Concatenation(shadow.codeBasis, hBasis);
  innerActions := List(shadow.pointPermutations, permutation ->
    QuotientAction337(permutation, hBasis, hWhole,
      Length(shadow.codeBasis)));
  outerPermutation := OuterPermutation337(shadow);
  outerAction := QuotientAction337(outerPermutation, hBasis, hWhole,
    Length(shadow.codeBasis));
  fullActions := Concatenation(innerActions, [outerAction]);
  innerGroup := Group(innerActions);
  fullGroup := Group(fullActions);
  innerModule := GModuleByMats(innerActions, field2);
  fullModule := GModuleByMats(fullActions, field2);

  endBasis := MTX.BasisModuleEndomorphisms(fullModule);
  epsilon := First(endBasis, matrix -> RankMat(matrix) = 1);
  identity := IdentityMat(10, field2);
  deckUnit := identity + epsilon;
  submodules := MTX.BasesSubmodules(innerModule);
  socle := First(submodules, basis -> Length(basis) = 1);
  radical := First(submodules, basis -> Length(basis) = 9);
  epsilonImage := BaseMat(epsilon);
  epsilonKernel := NullspaceMat(epsilon);

  epsilonInnerExtension := Group(Concatenation(innerActions, [deckUnit]));
  epsilonFullExtension := Group(Concatenation(fullActions, [deckUnit]));
  epsilonKernelGroup := Group([deckUnit]);
  epsilonQuotientMap := NaturalHomomorphismByNormalSubgroup(
    epsilonFullExtension, epsilonKernelGroup);
  epsilonQuotient := Image(epsilonQuotientMap);
  signedInfo := First(AllAtlasGeneratingSetInfos("2.U4(2).2"),
    info -> IsBound(info.repname) and info.repname = "2U42d2G1-p240B0");
  signedAtlas := AtlasGenerators(signedInfo.identifier);
  signedFull := Group(signedAtlas.generators);
  signedCenter := Centre(signedFull);
  signedQuotientMap := NaturalHomomorphismByNormalSubgroup(
    signedFull, signedCenter);
  signedQuotient := Image(signedQuotientMap);
  signedDerived := DerivedSubgroup(signedFull);

  checks := rec();
  checks.H10_dimensions :=
    Length(hBasis) = 10 and Length(hWhole) = 25;
  checks.inner_and_full_image_orders :=
    Size(innerGroup) = 25920 and Size(fullGroup) = 51840;
  checks.H10_uniserial_submodule_lattice :=
    SortedList(List(submodules, Length)) = [0, 1, 9, 10];
  checks.both_short_module_extensions_are_nonsplit :=
    Number(submodules, basis -> Length(basis) = 1) = 1 and
    Number(submodules, basis -> Length(basis) = 8) = 0 and
    Number(submodules, basis -> Length(basis) = 9) = 1;
  checks.full_endomorphism_ring_is_dual_numbers :=
    Length(endBasis) = 2 and
    SortedList(List([NullMat(10, 10, field2), endBasis[1], endBasis[2],
      endBasis[1] + endBasis[2]], RankMat)) = [0, 1, 10, 10];
  checks.epsilon_is_square_zero_rank_one :=
    RankMat(epsilon) = 1 and epsilon^2 = NullMat(10, 10, field2);
  checks.epsilon_is_top_to_socle :=
    RowsContainedIn(epsilonImage, socle) and
    RowsContainedIn(socle, epsilonImage) and
    RowsContainedIn(epsilonKernel, radical) and
    RowsContainedIn(radical, epsilonKernel);
  checks.deck_unit_is_central_involution :=
    Order(deckUnit) = 2 and
    ForAll(fullActions, matrix -> matrix * deckUnit = deckUnit * matrix);
  checks.deck_unit_is_new_to_both_images :=
    not deckUnit in innerGroup and not deckUnit in fullGroup;
  checks.epsilon_inner_extension_is_split :=
    Size(epsilonInnerExtension) = 51840 and
    StructureDescription(epsilonInnerExtension) = "C2 x O(5,3)" and
    Size(DerivedSubgroup(epsilonInnerExtension)) = 25920 and
    AbelianInvariants(epsilonInnerExtension) = [2];
  checks.epsilon_full_extension_is_split_endpoint_group :=
    Size(epsilonFullExtension) = 103680 and
    StructureDescription(epsilonFullExtension) = "C2 x (O(5,3) : C2)" and
    Size(DerivedSubgroup(epsilonFullExtension)) = 25920 and
    AbelianInvariants(epsilonFullExtension) = [2, 2];
  checks.epsilon_extension_is_internal_direct_product :=
    Size(Intersection(fullGroup, epsilonKernelGroup)) = 1 and
    Size(epsilonFullExtension) =
      Size(fullGroup) * Size(epsilonKernelGroup);
  checks.epsilon_quotient_recovers_PGSp :=
    Size(Kernel(epsilonQuotientMap)) = 2 and
    Size(epsilonQuotient) = 51840 and
    Size(Image(epsilonQuotientMap, fullGroup)) = 51840;
  checks.signed_E8_Atlas_anchor :=
    signedInfo.repname = "2U42d2G1-p240B0";
  checks.signed_E8_full_extension_order_and_center :=
    Size(signedFull) = 103680 and Size(signedCenter) = 2;
  checks.signed_E8_quotient_recovers_PGSp :=
    Size(signedQuotient) = 51840 and
    StructureDescription(signedQuotient) =
      StructureDescription(fullGroup);
  checks.signed_E8_derived_core_is_Sp43 :=
    Size(signedDerived) = 51840 and
    Size(Centre(signedDerived)) = 2 and
    IsPerfectGroup(signedDerived) and
    StructureDescription(signedDerived) = "C2 . O(5,3)";
  checks.signed_E8_extension_is_nonsplit_by_derived_core :=
    Size(DerivedSubgroup(signedFull)) = 51840 and
    AbelianInvariants(signedFull) = [2];
  checks.epsilon_and_signed_extensions_are_not_isomorphic :=
    Size(DerivedSubgroup(epsilonFullExtension)) <>
      Size(DerivedSubgroup(signedFull)) and
    AbelianInvariants(epsilonFullExtension) <>
      AbelianInvariants(signedFull);
  checks.Baer_classes_are_split_versus_nonsplit :=
    StructureDescription(epsilonFullExtension) =
      "C2 x (O(5,3) : C2)" and
    StructureDescription(signedFull) = "(C2 . O(5,3)) : C2";

  checkNames := RecNames(checks);
  allPass := ForAll(checkNames, name -> checks.(name));
  Assert337("all certificate checks", allPass);
  if allPass then status := "PASS"; else status := "FAIL"; fi;

  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass337.epsilon_e8_baer_separation.gap.v1\",\n");
  WriteAll(stream, Concatenation("  \"status\": \"", status, "\",\n"));
  WriteAll(stream, "  \"headline\": \"the dual-number unit 1+epsilon realizes the split endpoint deck extension, not the nonsplit signed-E8 Schur-cover class\",\n");
  WriteAll(stream, "  \"H10_module_extension\": {\n");
  WriteAll(stream, "    \"structure\": \"1|8|1\",\n");
  WriteAll(stream, "    \"submodule_dimensions\": [0,1,9,10],\n");
  WriteAll(stream, "    \"epsilon\": \"rank one, square zero, image=socle, kernel=radical; the canonical top-to-socle map\",\n");
  WriteAll(stream, "    \"Yoneda_reading\": \"both adjacent short exact module extensions are nonsplit\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"epsilon_group_extension\": {\n");
  WriteAll(stream, Concatenation("    \"order\": ",
    String(Size(epsilonFullExtension)), ",\n"));
  WriteAll(stream, Concatenation("    \"structure\": \"",
    StructureDescription(epsilonFullExtension), "\",\n"));
  WriteAll(stream, Concatenation("    \"derived_order\": ",
    String(Size(DerivedSubgroup(epsilonFullExtension))), ",\n"));
  WriteAll(stream, Concatenation("    \"abelian_invariants\": ",
    String(AbelianInvariants(epsilonFullExtension)), ",\n"));
  WriteAll(stream, "    \"Baer_class\": \"zero/split; this is the canonical endpoint deck extension\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"signed_E8_group_extension\": {\n");
  WriteAll(stream, Concatenation("    \"Atlas_anchor\": \"",
    signedInfo.repname, "\",\n"));
  WriteAll(stream, Concatenation("    \"order\": ",
    String(Size(signedFull)), ",\n"));
  WriteAll(stream, Concatenation("    \"structure\": \"",
    StructureDescription(signedFull), "\",\n"));
  WriteAll(stream, Concatenation("    \"derived_order\": ",
    String(Size(signedDerived)), ",\n"));
  WriteAll(stream, Concatenation("    \"abelian_invariants\": ",
    String(AbelianInvariants(signedFull)), ",\n"));
  WriteAll(stream, "    \"Baer_class\": \"nonzero/nonsplit; derived core is Sp(4,3)\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"comparison\": {\n");
  WriteAll(stream, "    \"isomorphic\": false,\n");
  WriteAll(stream, "    \"verdict\": \"epsilon connects canonically to the raw 240-to-120 endpoint deck, while signed E8 equivariance requires the different nonsplit Schur cover\"\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, "  \"honest_boundary\": [\n");
  WriteAll(stream, "    \"the H10 module/Yoneda class is nonsplit\",\n");
  WriteAll(stream, "    \"the central group extension generated by 1+epsilon is nevertheless split\",\n");
  WriteAll(stream, "    \"epsilon is not the signed-E8 Bockstein or Schur multiplier class\",\n");
  WriteAll(stream, "    \"no physical identification follows from either extension\"\n");
  WriteAll(stream, "  ],\n");
  WriteAll(stream, Concatenation("  \"check_count\": ",
    String(Length(checkNames)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for name in checkNames do
    WriteAll(stream, Concatenation("    \"", name, "\": ",
      BoolJSON337(checks.(name))));
    if name <> checkNames[Length(checkNames)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n");
  WriteAll(stream, "}\n");
  CloseStream(stream);
  Print("Pass337 status=", status, " checks=", Length(checkNames),
    " output=", OUT, "\n");
end;;

Main337();;
QUIT;
