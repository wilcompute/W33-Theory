# Pass 363: the real two-qubit Clifford group has three inequivalent
# index-two character kernels.  They are W(F4), 2O central-product 2O, and
# a third mixed kernel; radial normalization makes the middle kernel
# transitive on the 48-point F4 shell without making it a Weyl group.

OUT363 := "data/w33_pass363_real_clifford_character_diamond.json";;

Assert363 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass363 assertion failed: ", label));
  fi;
end;;

Bool363 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

OrderProfile363 := function(group)
  return Collected(List(Elements(group),Order));
end;;

Support363 := function(vector)
  return Number(vector,entry -> entry<>0);
end;;

Dot363 := function(left,right)
  return Sum([1..Length(left)],position -> left[position]*right[position]);
end;;

Reflect363 := function(vector,root)
  local coefficient;
  coefficient := 2*Dot363(vector,root)/Dot363(root,root);
  return List([1..4],position ->
    vector[position]-coefficient*root[position]);
end;;

Main363 := function()
  local sqrt2, had, identity2, pauliX, pauliZ, realGenerators,
        realClifford, realPauli, globalSign, targetC2,
        hadamardCharacter, determinantCharacter, mixedCharacter,
        characters, kernels, hadamardKernel, determinantKernel,
        mixedKernel, derived, pairIntersections, pairClosures,
        kernelProfiles, binaryOctahedral, twoFactors, embed1, embed2,
        centralInvolution, diagonalCenter, centralProduct, gl23,
        rootsF4, position1, position2, sign1, sign2, vector,
        simpleRootsF4, reflectionsF4, weylF4,
        projectiveMap, projectiveRealClifford, leftS4, rightS4,
        bipartitionBase, sideSwap, autK44, equalSignBase,
        twistedZero, oddSideSwap, twistedOne, isoK44,
        projectiveKernels, imagesK44, projectiveDerived,
        normalizedShort, normalizedLong, normalizedF4, actualF4,
        determinantOrbit, hadamardShellOrbits, determinantShellOrbits,
        supportProfile, checks, names, name, stream;

  sqrt2 := Sqrt(2);
  had := [[1/sqrt2,1/sqrt2],[1/sqrt2,-1/sqrt2]];
  identity2 := IdentityMat(2,Rationals);
  pauliX := [[0,1],[1,0]];
  pauliZ := [[1,0],[0,-1]];
  realGenerators := List([
    KroneckerProduct(had,identity2),
    KroneckerProduct(identity2,had),
    KroneckerProduct(pauliX,identity2),
    KroneckerProduct(identity2,pauliX),
    KroneckerProduct(pauliZ,identity2),
    KroneckerProduct(identity2,pauliZ),
    [[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]
  ],matrix -> ImmutableMatrix(CF(8),matrix));
  realClifford := Group(realGenerators);
  realPauli := Group(realGenerators{[3..6]});
  globalSign := Center(realClifford);
  targetC2 := Group((1,2));

  # The abelianization is C2 x C2, so these are all three nonzero
  # characters: total H parity, determinant/CNOT parity, and their sum.
  hadamardCharacter := GroupHomomorphismByImages(
    realClifford,targetC2,realGenerators,
    [(1,2),(1,2),(),(),(),(),()]);
  determinantCharacter := GroupHomomorphismByImages(
    realClifford,targetC2,realGenerators,
    [(),(),(),(),(),(),(1,2)]);
  mixedCharacter := GroupHomomorphismByImages(
    realClifford,targetC2,realGenerators,
    [(1,2),(1,2),(),(),(),(),(1,2)]);
  characters := [hadamardCharacter,determinantCharacter,mixedCharacter];
  kernels := List(characters,Kernel);
  hadamardKernel := kernels[1];
  determinantKernel := kernels[2];
  mixedKernel := kernels[3];
  derived := DerivedSeriesOfGroup(realClifford);
  pairIntersections := [
    Intersection(kernels[1],kernels[2]),
    Intersection(kernels[1],kernels[3]),
    Intersection(kernels[2],kernels[3])];
  pairClosures := [
    Group(Concatenation(GeneratorsOfGroup(kernels[1]),
      GeneratorsOfGroup(kernels[2]))),
    Group(Concatenation(GeneratorsOfGroup(kernels[1]),
      GeneratorsOfGroup(kernels[3]))),
    Group(Concatenation(GeneratorsOfGroup(kernels[2]),
      GeneratorsOfGroup(kernels[3])))];
  kernelProfiles := List(kernels,OrderProfile363);

  # Independent intrinsic models of W(F4) and 2O central-product 2O.
  rootsF4 := [];
  for position1 in [1..4] do
    for sign1 in [-1,1] do
      vector := [0,0,0,0];
      vector[position1] := 2*sign1;
      Add(rootsF4,vector);
    od;
  od;
  Append(rootsF4,Tuples([-1,1],4));
  for position1 in [1..4] do
    for position2 in [position1+1..4] do
      for sign1 in [-1,1] do
        for sign2 in [-1,1] do
          vector := [0,0,0,0];
          vector[position1] := 2*sign1;
          vector[position2] := 2*sign2;
          Add(rootsF4,vector);
        od;
      od;
    od;
  od;
  rootsF4 := Set(rootsF4);
  simpleRootsF4 := [[0,2,-2,0],[0,0,2,-2],[0,0,0,2],
    [1,-1,-1,-1]];
  reflectionsF4 := List(simpleRootsF4,root -> PermList(
    List(rootsF4,entry -> Position(rootsF4,Reflect363(entry,root)))));
  weylF4 := Group(reflectionsF4);

  binaryOctahedral := SchurCover(SymmetricGroup(4));
  twoFactors := DirectProduct(binaryOctahedral,binaryOctahedral);
  embed1 := Embedding(twoFactors,1);
  embed2 := Embedding(twoFactors,2);
  centralInvolution := First(Elements(Center(binaryOctahedral)),
    element -> element<>One(binaryOctahedral));
  diagonalCenter := Group(Image(embed1,centralInvolution)*
    Image(embed2,centralInvolution));
  centralProduct := twoFactors/diagonalCenter;

  # The projective images are three visibly different index-two subgroups
  # of Aut(K4,4)=S4 wr C2.
  projectiveMap := NaturalHomomorphismByNormalSubgroup(realClifford,
    globalSign);
  projectiveRealClifford := Image(projectiveMap);
  leftS4 := Group((1,2),(1,2,3,4));
  rightS4 := Group((5,6),(5,6,7,8));
  bipartitionBase := Group(Concatenation(GeneratorsOfGroup(leftS4),
    GeneratorsOfGroup(rightS4)));
  sideSwap := (1,5)(2,6)(3,7)(4,8);
  autK44 := Group(Concatenation(GeneratorsOfGroup(bipartitionBase),
    [sideSwap]));
  equalSignBase := Group(Filtered(Elements(bipartitionBase),permutation ->
    SignPerm(permutation)=1));
  twistedZero := Group(Concatenation(GeneratorsOfGroup(equalSignBase),
    [sideSwap]));
  oddSideSwap := (1,2)*sideSwap;
  twistedOne := Group(Concatenation(GeneratorsOfGroup(equalSignBase),
    [oddSideSwap]));
  isoK44 := IsomorphismGroups(projectiveRealClifford,autK44);
  projectiveKernels := List(kernels,kernel -> Image(projectiveMap,kernel));
  imagesK44 := List(projectiveKernels,subgroup -> Image(isoK44,subgroup));
  projectiveDerived := Image(isoK44,Image(projectiveMap,derived[2]));

  # Radially normalize the two metric F4 root lengths.  The determinant
  # kernel is transitive on the resulting shell, whereas W(F4) retains its
  # 24+24 short/long split on both the metric and normalized realizations.
  normalizedShort := [];
  for position1 in [1..4] do
    for sign1 in [-1,1] do
      vector := [0,0,0,0];
      vector[position1] := sign1;
      Add(normalizedShort,vector);
    od;
  od;
  Append(normalizedShort,Cartesian(List([1..4],unused -> [-1/2,1/2])));
  normalizedShort := Set(normalizedShort);
  normalizedLong := [];
  for position1 in [1..4] do
    for position2 in [position1+1..4] do
      for sign1 in [-1,1] do
        for sign2 in [-1,1] do
          vector := [0,0,0,0];
          vector[position1] := sign1/sqrt2;
          vector[position2] := sign2/sqrt2;
          Add(normalizedLong,vector);
        od;
      od;
    od;
  od;
  normalizedLong := Set(normalizedLong);
  normalizedF4 := Set(Concatenation(normalizedShort,normalizedLong));
  actualF4 := Set(Concatenation(normalizedShort,
    List(normalizedLong,root -> sqrt2*root)));
  determinantOrbit := Set(Orbit(determinantKernel,[1,0,0,0],OnRight));
  hadamardShellOrbits := Orbits(hadamardKernel,normalizedF4,OnRight);
  determinantShellOrbits := Orbits(determinantKernel,normalizedF4,OnRight);
  supportProfile := Collected(List(determinantOrbit,Support363));

  # GL(2,3) and the binary octahedral group share order and central
  # quotient S4, but they are not isomorphic.
  gl23 := GL(2,3);

  checks := rec();
  checks.real_clifford_has_order_2304 := Size(realClifford)=2304;
  checks.real_clifford_has_29_classes :=
    NrConjugacyClasses(realClifford)=29;
  checks.real_clifford_abelianization_is_c2_squared :=
    AbelianInvariants(realClifford/derived[2])=[2,2];
  checks.three_character_maps_are_surjective :=
    ForAll(characters,map -> Size(Image(map))=2);
  checks.three_kernels_are_distinct := Length(Set(kernels))=3;
  checks.three_kernels_have_order_1152 :=
    List(kernels,Size)=[1152,1152,1152];
  checks.three_kernels_have_center_two :=
    List(kernels,kernel -> Size(Center(kernel)))=[2,2,2];
  checks.kernel_class_counts_are_25_34_19 :=
    List(kernels,NrConjugacyClasses)=[25,34,19];
  checks.kernel_derived_orders_are_288 :=
    List(kernels,kernel -> Size(DerivedSubgroup(kernel)))=[288,288,288];
  checks.kernel_profiles_are_distinct := Length(Set(kernelProfiles))=3;
  checks.hadamard_kernel_profile_is_exact := kernelProfiles[1]=
    [[1,1],[2,139],[3,80],[4,228],[6,464],[8,144],[12,96]];
  checks.determinant_kernel_profile_is_exact := kernelProfiles[2]=
    [[1,1],[2,163],[3,80],[4,108],[6,80],[8,240],[12,288],[24,192]];
  checks.mixed_kernel_profile_is_exact := kernelProfiles[3]=
    [[1,1],[2,91],[3,80],[4,372],[6,80],[8,432],[12,96]];
  checks.kernels_are_pairwise_nonisomorphic :=
    IsomorphismGroups(kernels[1],kernels[2])=fail and
    IsomorphismGroups(kernels[1],kernels[3])=fail and
    IsomorphismGroups(kernels[2],kernels[3])=fail;
  checks.all_pair_intersections_are_commutator :=
    ForAll(pairIntersections,group -> group=derived[2]);
  checks.triple_intersection_is_commutator :=
    Intersection(Intersection(kernels[1],kernels[2]),kernels[3])=derived[2];
  checks.any_two_kernels_generate_full_group :=
    ForAll(pairClosures,group -> group=realClifford);
  checks.all_kernel_commutators_are_second_derived :=
    ForAll(kernels,kernel -> DerivedSubgroup(kernel)=derived[3]);
  checks.derived_tower_orders_are_exact :=
    List(derived,Size)=[2304,576,288,32,2,1];
  checks.derived_tower_quotients_are_exact :=
    List([1..Length(derived)-1],position1 ->
      AbelianInvariants(derived[position1]/derived[position1+1]))=
      [[2,2],[2],[3,3],[2,2,2,2],[2]];
  checks.third_derived_is_real_pauli := derived[4]=realPauli;
  checks.fourth_derived_is_global_sign := derived[5]=globalSign;

  checks.hadamard_kernel_is_weyl_f4 :=
    IsomorphismGroups(hadamardKernel,weylF4)<>fail;
  checks.binary_octahedral_has_id_48_28 := IdGroup(binaryOctahedral)=[48,28];
  checks.determinant_kernel_is_binary_octahedral_central_product :=
    IsomorphismGroups(determinantKernel,centralProduct)<>fail;
  checks.mixed_quotient_by_pauli_has_order_36 :=
    Size(mixedKernel/realPauli)=36;
  checks.mixed_quotient_has_expected_structure :=
    StructureDescription(mixedKernel/realPauli)="(C3 x C3) : C4";

  checks.projective_images_are_t0_base_t1 :=
    imagesK44=[twistedZero,bipartitionBase,twistedOne];
  checks.projective_image_class_counts_are_16_25_13 :=
    List(projectiveKernels,NrConjugacyClasses)=[16,25,13];
  checks.t0_contains_pure_side_swap := sideSwap in imagesK44[1];
  checks.t1_excludes_pure_side_swap := not sideSwap in imagesK44[3];
  checks.twisted_images_meet_base_in_equal_sign_group :=
    Intersection(imagesK44[1],bipartitionBase)=equalSignBase and
    Intersection(imagesK44[3],bipartitionBase)=equalSignBase;
  checks.projective_pair_intersections_are_common_derived :=
    ForAll([[1,2],[1,3],[2,3]],pair ->
      Intersection(imagesK44[pair[1]],imagesK44[pair[2]])=projectiveDerived);

  checks.normalized_f4_has_24_plus_24_points :=
    Length(normalizedShort)=24 and Length(normalizedLong)=24 and
    Length(normalizedF4)=48;
  checks.determinant_orbit_is_normalized_f4_shell :=
    determinantOrbit=normalizedF4;
  checks.normalized_shell_supports_are_8_24_16 :=
    supportProfile=[[1,8],[2,24],[4,16]];
  checks.weyl_f4_has_two_normalized_shell_orbits :=
    SortedList(List(hadamardShellOrbits,Length))=[24,24];
  checks.central_product_is_transitive_on_normalized_shell :=
    List(determinantShellOrbits,Length)=[48];
  checks.weyl_f4_preserves_metric_root_shell :=
    ForAll(GeneratorsOfGroup(hadamardKernel),matrix ->
      Set(List(actualF4,root -> root*matrix))=actualF4);
  checks.central_product_does_not_preserve_metric_root_shell :=
    not ForAll(GeneratorsOfGroup(determinantKernel),matrix ->
      Set(List(actualF4,root -> root*matrix))=actualF4);

  checks.gl23_has_id_48_29 := IdGroup(gl23)=[48,29];
  checks.gl23_is_not_binary_octahedral :=
    IsomorphismGroups(gl23,binaryOctahedral)=fail;
  checks.both_central_quotients_are_s4 :=
    StructureDescription(gl23/Center(gl23))="S4" and
    StructureDescription(binaryOctahedral/Center(binaryOctahedral))="S4";
  checks.gl23_has_13_involutions_but_2o_has_one :=
    Number(Elements(gl23),element -> Order(element)=2)=13 and
    Number(Elements(binaryOctahedral),element -> Order(element)=2)=1;

  names := RecNames(checks);
  Assert363("all checks",ForAll(names,name -> checks.(name)));

  stream := OutputTextFile(OUT363,false);
  SetPrintFormattingStatus(stream,false);
  WriteAll(stream,"{\n");
  WriteAll(stream,"  \"schema\": \"w33.pass363.real_clifford_character_diamond.gap.v1\",\n");
  WriteAll(stream,"  \"status\": \"PASS\",\n");
  WriteAll(stream,"  \"headline\": \"the real two-qubit Clifford group has a rigid three-kernel character diamond, and radial normalization separates the W(F4) metric action from a transitive 2O-central-product action\",\n");
  WriteAll(stream,"  \"ambient\": {\"group_order\": 2304, \"abelianization\": \"C2 x C2\", \"class_count\": 29, \"derived_orders\": [2304,576,288,32,2,1]},\n");
  WriteAll(stream,"  \"kernel_orders\": [1152,1152,1152],\n");
  WriteAll(stream,"  \"kernel_class_counts\": [25,34,19],\n");
  WriteAll(stream,"  \"kernels\": {\"hadamard\": \"W(F4)\", \"determinant\": \"(2O x 2O)/diag(C2)\", \"mixed\": \"2_+^(1+4):((C3 x C3):C4)\"},\n");
  WriteAll(stream,"  \"projective_images_in_AutK44\": [\"T0: equal-sign base plus pure side swap\", \"S4 x S4 base\", \"T1: equal-sign base plus odd-signed side swap\"],\n");
  WriteAll(stream,"  \"normalized_f4_shell\": {\"size\": 48, \"support_distribution\": {\"1\": 8, \"2\": 24, \"4\": 16}, \"W(F4)_orbits\": [24,24], \"2O_central_product_orbit\": [48]},\n");
  WriteAll(stream,"  \"correction\": {\"GL(2,3)\": \"SmallGroup(48,29), 13 involutions\", \"binary_octahedral_2O\": \"SmallGroup(48,28), 1 involution\", \"isomorphic\": false},\n");
  WriteAll(stream,"  \"boundary\": \"The formal S3 automorphism group of the C2-squared character space does not lift to this matrix group: its three kernels are pairwise nonisomorphic and hence characteristic. Radial normalization forgets the metric short/long distinction and must not be called the F4 root system itself.\",\n");
  WriteAll(stream,Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream,"  \"checks\": {\n");
  for name in names do
    WriteAll(stream,Concatenation("    \"",name,"\": ",Bool363(checks.(name))));
    if name<>names[Length(names)] then WriteAll(stream,","); fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  }\n}\n");
  CloseStream(stream);
  Print("Pass363 status=PASS checks=",Length(names)," output=",OUT363,"\n");
end;;

Main363();;
QUIT;
