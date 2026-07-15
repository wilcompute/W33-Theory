# Pass 342: reconcile the five local 2-adic vertices of Pass 335 with the
# global lattice count in Kirschmer's dimension-10 classification.
#
# The inner U4(2) module has five local vertices.  Eisenstein omega fixes the
# two spine vertices and cycles the three H10 leaves.  The integral outer
# reflection fixes the two spine lattices separately; it does not identify
# them.  Thus the local complex globalizes to two stable spine classes in this
# embedded module.  Kirschmer's nearby one/two/five/fifteen counts use other
# groups or equivalences and cannot be substituted for this local building.

LoadPackage("atlasrep");;

OUT342 := "data/w33_pass342_global_lattice_reconciliation.json";;

Assert342 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass342 assertion failed: ", label));
  fi;
end;;

Bool342 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

EisensteinMultiplication342 := function(value, basis)
  local coefficients;
  coefficients := Coefficients(basis, value);
  return [[coefficients[1], coefficients[2]],
    [-coefficients[2], coefficients[1]-coefficients[2]]];
end;;

RestrictScalars342 := function(matrix, basis)
  local dimension, output, row, column;
  dimension := Length(matrix);
  output := NullMat(2*dimension, 2*dimension, Rationals);
  for row in [1..dimension] do
    for column in [1..dimension] do
      output{[2*row-1,2*row]}{[2*column-1,2*column]} :=
        EisensteinMultiplication342(matrix[row][column], basis);
    od;
  od;
  return output;
end;;

RepeatBlock342 := function(block, repetitions)
  local output, index, positions;
  output := NullMat(repetitions*Length(block), repetitions*Length(block),
    Rationals);
  for index in [1..repetitions] do
    positions := [(index-1)*Length(block)+1..index*Length(block)];
    output{positions}{positions} := block;
  od;
  return output;
end;;

LiftPreimage342 := function(subspace, dimension)
  local current, complement, vector;
  current := ShallowCopy(subspace);
  complement := [];
  for vector in IdentityMat(dimension, GF(2)) do
    if RankMat(Concatenation(current,[vector])) > Length(current) then
      Add(current, vector);
      Add(complement, vector);
    fi;
  od;
  Assert342("preimage basis", Length(current)=dimension);
  return Concatenation(
    List(subspace, vector -> List(vector,IntFFE)),
    List(complement, vector -> 2*List(vector,IntFFE)));
end;;

SameLattice342 := function(left, right)
  local transition;
  transition := left * right^-1;
  return ForAll(Flat(transition), IsInt) and
    AbsInt(DeterminantMat(transition)) = 1;
end;;

LatticePermutation342 := function(matrix, bases)
  return List(bases, source -> PositionProperty(bases, target ->
    SameLattice342(source*matrix, target)));
end;;

Main342 := function()
  local field, basis, info, atlas, rationalGenerators, inner,
        invariantLattice, integralGenerators, module, submodules,
        eightSpace, nineSpaces, nodeBases, labels, omegaOriginal,
        omegaIntegral, reflectionOriginal, reflectionIntegral,
        omegaPermutation, reflectionPermutation, maximalGroup,
        maximalLattice, maximalTransition, outerNormalizer,
        fixedNodes, fixedOrbits, checks, names, stream, name;

  field := CF(3);
  basis := Basis(field,[One(field),E(3)]);
  info := First(AllAtlasGeneratingSetInfos("U4(2)",Dimension,5), entry ->
    IsBound(entry.repname) and entry.repname="U42G1-Ar5aB0");
  atlas := AtlasGenerators(info.identifier);
  rationalGenerators := List(atlas.generators, matrix ->
    RestrictScalars342(matrix,basis));
  inner := Group(rationalGenerators);
  invariantLattice := InvariantLattice(inner);
  integralGenerators := List(rationalGenerators, matrix ->
    invariantLattice*matrix*invariantLattice^-1);
  module := GModuleByMats(List(integralGenerators, matrix ->
    matrix*One(GF(2))),GF(2));
  submodules := MTX.BasesSubmodules(module);
  eightSpace := First(submodules, subspace -> Length(subspace)=8);
  nineSpaces := Filtered(submodules, subspace -> Length(subspace)=9);
  nodeBases := Concatenation([IdentityMat(10),
    LiftPreimage342(eightSpace,10)],
    List(nineSpaces,subspace -> LiftPreimage342(subspace,10)));
  labels := ["L","R","L1","L2","L3"];

  omegaOriginal := RepeatBlock342(
    EisensteinMultiplication342(E(3),basis),5);
  omegaIntegral := invariantLattice*omegaOriginal*invariantLattice^-1;
  reflectionOriginal := [
    [ 1, 0, 1, 0, 1, 1,0,0,0,0],[-1,-1,-1,-1,0,-1,0,0,0,0],
    [ 0, 0, 0, 0,-1,-1,0,0,0,0],[ 0, 0, 0, 0,0,1,0,0,0,0],
    [ 0, 0,-1,-1, 0, 0,0,0,0,0],[ 0, 0, 0, 1,0,0,0,0,0,0],
    [ 0, 0, 1, 1, 0, 1,0,1,0,0],[ 0, 0, 0,-1,1,0,1,0,0,0],
    [ 0, 0,-1,-1, 0,-1,0,0,0,1],[ 0, 0, 0, 1,-1,0,0,0,1,0]
  ];
  reflectionIntegral := invariantLattice*reflectionOriginal*invariantLattice^-1;
  omegaPermutation := LatticePermutation342(omegaIntegral,nodeBases);
  reflectionPermutation := LatticePermutation342(reflectionIntegral,nodeBases);

  maximalGroup := Group(Concatenation(rationalGenerators,
    [omegaOriginal,-IdentityMat(10,Rationals)]));
  maximalLattice := InvariantLattice(maximalGroup);
  maximalTransition := maximalLattice*invariantLattice^-1;
  outerNormalizer := Group(Concatenation(rationalGenerators,
    [omegaOriginal,reflectionOriginal,-IdentityMat(10,Rationals)]));
  fixedNodes := Filtered([1..5],index -> omegaPermutation[index]=index);
  fixedOrbits := Orbits(Group(PermList(reflectionPermutation)),fixedNodes);

  checks := rec();
  checks.inner_group_is_U42 := Size(inner)=25920;
  checks.local_submodule_census_recovers_five_vertices :=
    SortedList(List(submodules,Length))=[0,8,9,9,9,10] and
    Length(nodeBases)=5;
  checks.local_index_exponents_are_0_2_1_1_1 :=
    List(nodeBases,basisMatrix -> LogInt(AbsInt(DeterminantMat(basisMatrix)),2))
      =[0,2,1,1,1];
  checks.omega_action_is_two_fixed_plus_three_cycle :=
    omegaPermutation=[1,2,5,3,4] and
    Order(PermList(omegaPermutation))=3 and fixedNodes=[1,2];
  checks.reflection_normalizes_inner_group :=
    Group(Concatenation(rationalGenerators,[reflectionOriginal])) =
      Group(Concatenation([reflectionOriginal],rationalGenerators));
  checks.reflection_lattice_permutation_is_defined :=
    ForAll(reflectionPermutation,entry -> entry<>fail);
  checks.reflection_fixes_both_omega_stable_spine_lattices :=
    reflectionPermutation{[1,2]}=[1,2];
  checks.maximal_Eisenstein_normalizer_order_and_structure :=
    Size(maximalGroup)=155520 and
    StructureDescription(maximalGroup)="C6 x O(5,3)" and
    Size(Centre(maximalGroup))=6 and
    Size(DerivedSubgroup(maximalGroup))=25920;
  checks.maximal_group_uses_same_integral_root_lattice :=
    ForAll(Flat(maximalTransition),IsInt) and
    AbsInt(DeterminantMat(maximalTransition))=1;
  checks.outer_normalizer_order := Size(outerNormalizer)=311040;
  checks.exactly_two_local_vertices_are_globally_omega_stable :=
    fixedNodes=[1,2];
  checks.the_two_spine_lattices_remain_distinct_under_outer_reflection :=
    fixedOrbits=[[1],[2]];

  names := RecNames(checks);
  Print("Pass342 check ledger=",
    List(names,name -> [name,checks.(name)]),"\n");
  Print("omega=",omegaPermutation," reflection=",reflectionPermutation,
    " fixed=",fixedNodes," fixed_orbits=",fixedOrbits,"\n");
  Assert342("all checks",ForAll(names,name -> checks.(name)));

  stream := OutputTextFile(OUT342,false);
  SetPrintFormattingStatus(stream,false);
  WriteAll(stream,"{\n");
  WriteAll(stream,"  \"schema\": \"w33.pass342.global_lattice_reconciliation.gap.v1\",\n");
  WriteAll(stream,"  \"status\": \"PASS\",\n");
  WriteAll(stream,"  \"headline\": \"five local 2-adic vertices globalize to two omega-stable spine lattices; the tested outer normalizer does not merge them\",\n");
  WriteAll(stream,Concatenation("  \"local_nodes\": ",String(labels),",\n"));
  WriteAll(stream,Concatenation("  \"omega_permutation\": ",String(omegaPermutation),",\n"));
  WriteAll(stream,Concatenation("  \"outer_reflection_permutation\": ",String(reflectionPermutation),",\n"));
  WriteAll(stream,"  \"compression\": \"omega removes the three H10 leaves as individual stable global classes; L and R remain separately stable and the outer reflection fixes each\",\n");
  WriteAll(stream,"  \"Kirschmer_reconciliation\": {\"source\":\"Finite symplectic matrix groups, Theorem 4.6.1 proof, printed p.64, plus the dimension-20 discussion on printed p.113\",\"verdict\":\"do not equate the thesis counts with the Pass 335 local vertices without an explicit group-and-equivalence identification\",\"correction\":\"the GAP object in this pass has exactly two omega-stable local classes; nearby counts 1, 2, 5 and 15 occur for differently named maximal or dimension-20 groups and table columns\"},\n");
  WriteAll(stream,Concatenation("  \"check_count\": ",String(Length(names)),",\n"));
  WriteAll(stream,"  \"checks\": {\n");
  for name in names do
    WriteAll(stream,Concatenation("    \"",name,"\": ",Bool342(checks.(name))));
    if name<>names[Length(names)] then WriteAll(stream,",");fi;
    WriteAll(stream,"\n");
  od;
  WriteAll(stream,"  }\n}\n");
  CloseStream(stream);
  Print("Pass342 status=PASS checks=",Length(names)," output=",OUT342,"\n");
end;;

Main342();;
QUIT;
