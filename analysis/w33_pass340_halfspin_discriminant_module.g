# Pass 340: identify the 3^16 cokernel left by the integral half-spin pairing.
# Both chiral cokernels are the same faithful semisimple U4(2)-module
# 1 + 5 + 10 over F3.  The Eisenstein scalar acts trivially, and the module
# is not the genuine irreducible spin-16 of the double cover 2.U4(2).

LoadPackage("atlasrep");;

OUT340 := "data/w33_pass340_halfspin_discriminant_module.json";;

Assert340 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass340 assertion failed: ", label));
  fi;
end;;

Bool340 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

EisensteinMultiplication340 := function(value, basis)
  local coefficients, rational, omega;
  coefficients := Coefficients(basis, value);
  rational := coefficients[1];
  omega := coefficients[2];
  return [[rational, omega], [-omega, rational - omega]];
end;;

RestrictScalars340 := function(matrix, basis)
  local dimension, output, row, column, block;
  dimension := Length(matrix);
  output := NullMat(2 * dimension, 2 * dimension, Rationals);
  for row in [1..dimension] do
    for column in [1..dimension] do
      block := EisensteinMultiplication340(matrix[row][column], basis);
      output{[2*row-1,2*row]}{[2*column-1,2*column]} := block;
    od;
  od;
  return output;
end;;

DirectSum340 := function(matrices, field)
  local dimension, output, start, matrix, positions;
  dimension := Sum(List(matrices, Length));
  output := NullMat(dimension, dimension, field);
  start := 1;
  for matrix in matrices do
    positions := [start..start + Length(matrix) - 1];
    output{positions}{positions} := matrix;
    start := start + Length(matrix);
  od;
  return output;
end;;

Exterior340 := function(matrix, degree)
  if degree = 0 then return [[One(matrix[1][1])]]; fi;
  return ExteriorPower(matrix, degree);
end;;

WedgePairing340 := function(evenSubsets, oddSubsets, field)
  local output, even, odd, joined;
  output := [];
  for even in evenSubsets do
    Add(output, []);
    for odd in oddSubsets do
      if Length(Intersection(even, odd)) = 0 and
          Set(Concatenation(even, odd)) = [1..5] then
        joined := Concatenation(even, odd);
        Add(output[Length(output)], SignPerm(PermList(joined)) * One(field));
      else
        Add(output[Length(output)], Zero(field));
      fi;
    od;
  od;
  return output;
end;;

TracePairing340 := function(matrix, basis, field)
  local dimension, output, row, column, i, j;
  dimension := Length(matrix);
  output := NullMat(2*dimension, 2*dimension, Rationals);
  for row in [1..dimension] do
    for column in [1..dimension] do
      for i in [1,2] do
        for j in [1,2] do
          output[2*row-2+i][2*column-2+j] :=
            Trace(field, basis[i] * matrix[row][column] * basis[j]);
        od;
      od;
    od;
  od;
  return output;
end;;

ExtendBasis340 := function(subbasis, dimension, field)
  local current, vector;
  current := ShallowCopy(subbasis);
  for vector in IdentityMat(dimension, field) do
    if RankMat(Concatenation(current, [vector])) > Length(current) then
      Add(current, vector);
    fi;
  od;
  Assert340("basis extension", Length(current) = dimension);
  return current;
end;;

QuotientActions340 := function(subbasis, actions, field)
  local dimension, subdimension, basis, inverse, positions, conjugated;
  dimension := Length(actions[1]);
  subdimension := Length(subbasis);
  basis := ExtendBasis340(subbasis, dimension, field);
  inverse := basis^-1;
  positions := [subdimension + 1..dimension];
  conjugated := List(actions, matrix -> basis * matrix * inverse);
  Assert340("subspace invariant", ForAll(conjugated, matrix ->
    matrix{[1..subdimension]}{positions} =
      NullMat(subdimension, dimension-subdimension, field)));
  return List(conjugated, matrix -> matrix{positions}{positions});
end;;

DualActions340 := function(actions)
  return List(actions, matrix -> TransposedMat(matrix^-1));
end;;

FactorProfile340 := function(module)
  return SortedList(List(MTX.CollectedFactors(module), row ->
    [MTX.Dimension(row[1]), row[2]]));
end;;

Main340 := function()
  local field3, field, basis, info, atlas, generators5, plusField,
        minusField, plusRational, minusRational, plusLattice, minusLattice,
        plusIntegral, minusIntegral, evenSubsets, oddSubsets, wedge, trace,
        pairing, pairing3, plusActions, minusActions, plusModule, minusModule,
        plusSubmodules, minusSubmodules, plusEnd, minusEnd, atlas5, atlas10,
        atlas5Module, atlas10Module, plusMinimal, minusMinimal,
        plusFive, plusTen, minusFive, minusTen, omegaPlusField,
        omegaMinusField, omegaPlusIntegral, omegaMinusIntegral,
        omegaPlusQuotient, omegaMinusQuotient, coverInfo, coverGenerators,
        coverGroup, coverModule, coverCenter, checks, names, stream, name;

  field3 := GF(3);
  field := CF(3);
  basis := Basis(field, [One(field), E(3)]);
  info := First(AllAtlasGeneratingSetInfos("U4(2)", Dimension, 5), entry ->
    IsBound(entry.repname) and entry.repname = "U42G1-Ar5aB0");
  atlas := AtlasGenerators(info.identifier);
  generators5 := atlas.generators;

  plusField := List(generators5, matrix -> DirectSum340(
    List([0,2,4], degree -> Exterior340(matrix, degree)), field));
  minusField := List(generators5, matrix -> DirectSum340(
    List([1,3,5], degree -> Exterior340(matrix, degree)), field));
  plusRational := List(plusField, matrix -> RestrictScalars340(matrix, basis));
  minusRational := List(minusField, matrix -> RestrictScalars340(matrix, basis));
  plusLattice := InvariantLattice(Group(plusRational));
  minusLattice := InvariantLattice(Group(minusRational));
  plusIntegral := List(plusRational, matrix ->
    plusLattice * matrix * plusLattice^-1);
  minusIntegral := List(minusRational, matrix ->
    minusLattice * matrix * minusLattice^-1);

  evenSubsets := Concatenation([[]], Combinations([1..5],2),
    Combinations([1..5],4));
  oddSubsets := Concatenation(Combinations([1..5],1),
    Combinations([1..5],3), [[1..5]]);
  wedge := WedgePairing340(evenSubsets, oddSubsets, field);
  trace := TracePairing340(wedge, basis, field);
  pairing := plusLattice * trace * TransposedMat(minusLattice);
  pairing3 := pairing * One(field3);

  # Row-module convention from g_+ P g_-^T=P: the plus cokernel is the
  # quotient of the dual minus lattice by row(P), and conversely for minus.
  plusActions := QuotientActions340(BaseMat(pairing3),
    DualActions340(List(minusIntegral, matrix -> matrix * One(field3))),
    field3);
  minusActions := QuotientActions340(BaseMat(TransposedMat(pairing3)),
    DualActions340(List(plusIntegral, matrix -> matrix * One(field3))),
    field3);
  plusModule := GModuleByMats(plusActions, field3);
  minusModule := GModuleByMats(minusActions, field3);
  plusSubmodules := MTX.BasesSubmodules(plusModule);
  minusSubmodules := MTX.BasesSubmodules(minusModule);
  plusEnd := MTX.BasisModuleEndomorphisms(plusModule);
  minusEnd := MTX.BasisModuleEndomorphisms(minusModule);

  atlas5 := AtlasGenerators(First(AllAtlasGeneratingSetInfos(
    "U4(2)", Characteristic, 3, Dimension, 5)).identifier).generators;
  atlas10 := AtlasGenerators(First(AllAtlasGeneratingSetInfos(
    "U4(2)", Characteristic, 3, Dimension, 10)).identifier).generators;
  atlas5Module := GModuleByMats(atlas5, field3);
  atlas10Module := GModuleByMats(atlas10, field3);
  plusMinimal := List(MTX.BasesMinimalSubmodules(plusModule), subspace ->
    MTX.InducedActionSubmodule(plusModule, subspace));
  minusMinimal := List(MTX.BasesMinimalSubmodules(minusModule), subspace ->
    MTX.InducedActionSubmodule(minusModule, subspace));
  plusFive := First(plusMinimal, module -> MTX.Dimension(module) = 5);
  plusTen := First(plusMinimal, module -> MTX.Dimension(module) = 10);
  minusFive := First(minusMinimal, module -> MTX.Dimension(module) = 5);
  minusTen := First(minusMinimal, module -> MTX.Dimension(module) = 10);

  omegaPlusField := DirectSum340(List([0,2,4], degree ->
    E(3)^degree * IdentityMat(Binomial(5,degree), field)), field);
  omegaMinusField := DirectSum340(List([1,3,5], degree ->
    E(3)^degree * IdentityMat(Binomial(5,degree), field)), field);
  omegaPlusIntegral := plusLattice *
    RestrictScalars340(omegaPlusField, basis) * plusLattice^-1;
  omegaMinusIntegral := minusLattice *
    RestrictScalars340(omegaMinusField, basis) * minusLattice^-1;
  omegaPlusQuotient := QuotientActions340(BaseMat(pairing3),
    [TransposedMat(omegaMinusIntegral^-1) * One(field3)], field3)[1];
  omegaMinusQuotient := QuotientActions340(BaseMat(TransposedMat(pairing3)),
    [TransposedMat(omegaPlusIntegral^-1) * One(field3)], field3)[1];

  coverInfo := First(AllAtlasGeneratingSetInfos(
    "2.U4(2)", Characteristic, 3, Dimension, 16));
  coverGenerators := AtlasGenerators(coverInfo.identifier).generators;
  coverGroup := Group(coverGenerators);
  coverModule := GModuleByMats(coverGenerators, field3);
  coverCenter := Centre(coverGroup);

  checks := rec();
  checks.Smith_diagonal_is_one16_three16 :=
    ElementaryDivisorsMat(pairing) = Concatenation([1..16]*0+1,[1..16]*0+3);
  checks.pairing_rank_mod3_is_16 := RankMat(pairing3) = 16;
  checks.both_cokernels_have_dimension_16 :=
    MTX.Dimension(plusModule) = 16 and MTX.Dimension(minusModule) = 16;
  checks.both_factor_profiles_are_one_plus_five_plus_ten :=
    FactorProfile340(plusModule) = [[1,1],[5,1],[10,1]] and
    FactorProfile340(minusModule) = [[1,1],[5,1],[10,1]];
  checks.both_modules_are_completely_semisimple :=
    Length(MTX.BasisRadical(plusModule)) = 0 and
    Length(MTX.BasisSocle(plusModule)) = 16 and
    Length(MTX.BasisRadical(minusModule)) = 0 and
    Length(MTX.BasisSocle(minusModule)) = 16;
  checks.exact_eight_submodule_census :=
    SortedList(List(plusSubmodules, Length)) = [0,1,5,6,10,11,15,16] and
    SortedList(List(minusSubmodules, Length)) = [0,1,5,6,10,11,15,16];
  checks.endomorphism_algebras_are_F3_cubed :=
    Length(plusEnd) = 3 and Length(minusEnd) = 3;
  checks.chiral_cokernels_are_isomorphic :=
    MTX.IsomorphismModules(plusModule, minusModule) <> fail;
  checks.plus_is_selfdual := MTX.IsomorphismModules(plusModule,
    GModuleByMats(DualActions340(plusActions), field3)) <> fail;
  checks.minus_is_selfdual := MTX.IsomorphismModules(minusModule,
    GModuleByMats(DualActions340(minusActions), field3)) <> fail;
  checks.constituents_match_ATLAS_5_and_10 :=
    MTX.IsomorphismModules(plusFive, atlas5Module) <> fail and
    MTX.IsomorphismModules(plusTen, atlas10Module) <> fail and
    MTX.IsomorphismModules(minusFive, atlas5Module) <> fail and
    MTX.IsomorphismModules(minusTen, atlas10Module) <> fail;
  checks.actions_are_faithful_U42 :=
    Size(Group(plusActions)) = 25920 and Size(Group(minusActions)) = 25920;
  checks.Eisenstein_scalar_dies_on_both_cokernels :=
    omegaPlusQuotient = IdentityMat(16, field3) and
    omegaMinusQuotient = IdentityMat(16, field3);
  checks.no_ATLAS_U42_irreducible_16_in_characteristic_3 :=
    Length(AllAtlasGeneratingSetInfos(
      "U4(2)", Characteristic, 3, Dimension, 16)) = 0;
  checks.double_cover_spin16_is_genuine_and_irreducible :=
    Size(coverGroup) = 51840 and Size(coverCenter) = 2 and
    ForAll(GeneratorsOfGroup(coverCenter), matrix ->
      matrix = -IdentityMat(16, field3)) and
    FactorProfile340(coverModule) = [[16,1]] and
    Length(MTX.BasisModuleEndomorphisms(coverModule)) = 1;

  names := RecNames(checks);
  Assert340("all checks", ForAll(names, name -> checks.(name)));

  stream := OutputTextFile(OUT340, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass340.halfspin_discriminant_module.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"both 3^16 half-spin discriminant cokernels are the same faithful semisimple U4(2)-module 1+5+10\",\n");
  WriteAll(stream, "  \"module\": {\"field\":\"F3\",\"dimension\":16,\"decomposition\":[1,5,10],\"submodule_dimensions\":[0,1,5,6,10,11,15,16],\"endomorphism_algebra\":\"F3^3\",\"self_dual\":true,\"plus_equals_minus\":true},\n");
  WriteAll(stream, "  \"Eisenstein_action\": {\"plus\":\"identity\",\"minus\":\"identity\",\"verdict\":\"the determinant 3^16 is ramified discriminant size, not a 16-state irreducible qutrit phase carrier\"},\n");
  WriteAll(stream, "  \"spin16_separation\": {\"U4(2)_irreducible_16_exists\":false,\"double_cover\":\"2.U4(2)\",\"center_action\":\"-I16\",\"image_order\":51840},\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for name in names do
    WriteAll(stream, Concatenation("    \"", name, "\": ", Bool340(checks.(name))));
    if name <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);
  Print("Pass340 status=PASS checks=", Length(names), " output=", OUT340, "\n");
end;;

Main340();;
QUIT;
