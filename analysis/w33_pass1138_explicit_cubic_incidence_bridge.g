# Pass 1138 -- explicit cubic-support/A2 incidence and the 2240 -> 45 -> 40
# W(E6)-equivariant bridge.
#
# GAP owns every constructed object in this certificate:
#   * the doubled-coordinate E8 roots and 2240 unordered A2 root triples;
#   * W(E6), as the reflection group of the 72 roots orthogonal to one A2;
#   * the 45 constant-sum cubic supports;
#   * the 45 x 2240 orthogonality-incidence matrix M;
#   * the 45 intrinsic W33 K4,4 octets and an equivariant support/octet
#     bijection;
#   * the composite C = N M from A2 triples to the 40 W33 points.
#
# Existing files own the previously known 45-graph and point/octet formulas:
# analysis/w33_flat_45_point_frame.py,
# analysis/bt767_k44_octet_incidence_projector.py, and
# analysis/bt769_center_quad_octet_identification.py.
# This pass constructs the missing E8 incidence map and its composite.

OUT1138 := "data/w33_pass1138_explicit_cubic_incidence_bridge.json";;

Assert1138 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass1138 assertion failed: ",label));
  fi;
end;;

Bool1138 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

Bit1138 := function(value)
  if value then return 1; fi;
  return 0;
end;;

# --------------------------------------------------------------------- E8
roots1138 := [];;
for i1138 in [1..8] do
  for j1138 in [i1138+1..8] do
    for si1138 in [-2,2] do
      for sj1138 in [-2,2] do
        v1138 := ListWithIdenticalEntries(8,0);;
        v1138[i1138] := si1138;;
        v1138[j1138] := sj1138;;
        Add(roots1138,v1138);
      od;
    od;
  od;
od;
for mask1138 in [0..255] do
  v1138 := List([0..7],k1138 ->
    1-2*((QuoInt(mask1138,2^k1138)) mod 2));;
  if Sum(v1138) mod 4 = 0 then Add(roots1138,v1138); fi;
od;

RootIndex1138 := x1138 -> Position(roots1138,x1138);;
ReflectionPerm1138 := function(root1138)
  return PermList(List(roots1138,x1138 ->
    RootIndex1138(x1138-((x1138*root1138)/4)*root1138)));
end;;

a2Triples1138 := [];;
for i1138 in [1..240] do
  for j1138 in [i1138+1..240] do
    k1138 := RootIndex1138(-(roots1138[i1138]+roots1138[j1138]));;
    if k1138 <> fail and k1138 > j1138 then
      Add(a2Triples1138,[i1138,j1138,k1138]);
    fi;
  od;
od;

baseA2Triple1138 := a2Triples1138[1];;
e6RootIndices1138 := Filtered([1..240],i1138 ->
  ForAll(baseA2Triple1138,j1138 ->
    roots1138[i1138]*roots1138[j1138]=0));;
WE61138 := Group(List(e6RootIndices1138,i1138 ->
  ReflectionPerm1138(roots1138[i1138])));;
smallGenerators1138 := SmallGeneratingSet(WE61138);;

# The pointwise A2 stabilizer has six 27-root shells.  Choose the first shell
# in lexicographic dot-pattern order, then its unique 45-element constant-sum
# family of triples.  This fixes coordinates without claiming a canonical
# global labeling.
dotPatterns1138 := Set(List([1..240],i1138 ->
  List(baseA2Triple1138,j1138 ->
    roots1138[i1138]*roots1138[j1138])));;
patterns271138 := Filtered(dotPatterns1138,pattern1138 ->
  Number([1..240],i1138 ->
    List(baseA2Triple1138,j1138 ->
      roots1138[i1138]*roots1138[j1138])=pattern1138)=27);;
shell271138 := Filtered([1..240],i1138 ->
  List(baseA2Triple1138,j1138 ->
    roots1138[i1138]*roots1138[j1138])=patterns271138[1]);;
shellTriples1138 := Combinations(shell271138,3);;
shellSums1138 := Set(List(shellTriples1138,triple1138 ->
  Sum(List(triple1138,i1138 -> roots1138[i1138]))));;
cubicSupports1138 := First(
  List(shellSums1138,sum1138 ->
    Filtered(shellTriples1138,triple1138 ->
      Sum(List(triple1138,i1138 -> roots1138[i1138]))=sum1138)),
  family1138 -> Length(family1138)=45);;
cubicSupports1138 := Set(cubicSupports1138,Set);;

# ---------------------------------------------------------------- explicit M
# M[s,t]=1 exactly when all nine E8 scalar products between the cubic support
# s and the A2 root triple t vanish.
M1138 := List(cubicSupports1138,support1138 ->
  List(a2Triples1138,triple1138 ->
    Bit1138(ForAll(support1138,i1138 ->
      ForAll(triple1138,j1138 ->
        roots1138[i1138]*roots1138[j1138]=0)))));;
rowSumsM1138 := List(M1138,Sum);;
columnSumsM1138 := List([1..2240],j1138 ->
  Sum(M1138,row1138 -> row1138[j1138]));;
liveColumns1138 := Filtered([1..2240],j1138 ->
  columnSumsM1138[j1138]<>0);;

A451138 := List([1..45],i1138 ->
  List([1..45],j1138 ->
    Bit1138(i1138<>j1138 and
      Intersection(cubicSupports1138[i1138],
                   cubicSupports1138[j1138])=[])));;
I451138 := IdentityMat(45);;
J451138 := List([1..45],i1138 -> ListWithIdenticalEntries(45,1));;
gramM1138 := M1138*TransposedMat(M1138);;
gramMExpected1138 := 24*I451138-6*A451138+8*J451138;;
gramMEigenspaces1138 := [
  [192,45-RankMat(gramM1138-192*I451138)],
  [48,45-RankMat(gramM1138-48*I451138)],
  [12,45-RankMat(gramM1138-12*I451138)]
];;
offDiagonalGramProfile1138 := Collected(
  List(Combinations([1..45],2),pair1138 ->
    gramM1138[pair1138[1]][pair1138[2]]));;

# Locate the live columns inside the complete W(E6)-orbit census.
a2ActionHom1138 := ActionHomomorphism(
  WE61138,a2Triples1138,OnSets);;
a2Action1138 := Image(a2ActionHom1138);;
a2Orbits1138 := Orbits(a2Action1138,[1..2240]);;
a2OrbitProfile1138 := SortedList(List(a2Orbits1138,Length));;
orbit2401138 := First(a2Orbits1138,orbit1138 ->
  Length(orbit1138)=240);;
orbits4321138 := Filtered(a2Orbits1138,orbit1138 ->
  Length(orbit1138)=432);;

# Exact characteristic-zero module decompositions.  GAP computes the
# permutation characters from stabilizers; labels 15a and 60a are the
# Pass-1135 character-table crosswalk, while the degree lists here are
# independently recomputed.
stabilizer2401138 := Stabilizer(
  WE61138,a2Triples1138[orbit2401138[1]],OnSets);;
stabilizer451138 := Stabilizer(
  WE61138,cubicSupports1138[1],OnSets);;
irreducibles1138 := Irr(WE61138);;
character2401138 := PermutationCharacter(WE61138,stabilizer2401138);;
character451138 := PermutationCharacter(WE61138,stabilizer451138);;
multiplicities2401138 := List(irreducibles1138,chi1138 ->
  ScalarProduct(chi1138,character2401138));;
multiplicities451138 := List(irreducibles1138,chi1138 ->
  ScalarProduct(chi1138,character451138));;
internalKernelMultiplicities1138 := List(
  [1..Length(irreducibles1138)],i1138 ->
    multiplicities2401138[i1138]-multiplicities451138[i1138]);;
decomposition2401138 := SortedList(List(
  Filtered([1..Length(irreducibles1138)],i1138 ->
    multiplicities2401138[i1138]<>0),
  i1138 -> [Degree(irreducibles1138[i1138]),
            multiplicities2401138[i1138]]));;
decomposition451138 := SortedList(List(
  Filtered([1..Length(irreducibles1138)],i1138 ->
    multiplicities451138[i1138]<>0),
  i1138 -> [Degree(irreducibles1138[i1138]),
            multiplicities451138[i1138]]));;
internalKernelDecomposition1138 := SortedList(List(
  Filtered([1..Length(irreducibles1138)],i1138 ->
    internalKernelMultiplicities1138[i1138]<>0),
  i1138 -> [Degree(irreducibles1138[i1138]),
            internalKernelMultiplicities1138[i1138]]));;
internalKernelDimension1138 := Sum(
  [1..Length(irreducibles1138)],i1138 ->
    Degree(irreducibles1138[i1138])*
    internalKernelMultiplicities1138[i1138]);;

# Weyl generators preserve the defining orthogonality relation and both
# carriers.  This makes M an object-level equivariant map rather than a
# character-containment assertion.
weylOrthogonalityPreserved1138 := ForAll(smallGenerators1138,g1138 ->
  ForAll([1..240],i1138 ->
    ForAll([1..240],j1138 ->
      (roots1138[i1138]*roots1138[j1138]=0)=
      (roots1138[i1138^g1138]*roots1138[j1138^g1138]=0))));;
supportCarrierInvariant1138 := ForAll(smallGenerators1138,g1138 ->
  ForAll(cubicSupports1138,support1138 ->
    OnSets(support1138,g1138) in cubicSupports1138));;
a2CarrierInvariant1138 := ForAll(smallGenerators1138,g1138 ->
  ForAll(a2Triples1138,triple1138 ->
    OnSets(triple1138,g1138) in a2Triples1138));;

# --------------------------------------------------------------- W(3,3)
Canon1138 := function(vector1138)
  local normalized1138,first1138;
  normalized1138 := List(vector1138,x1138 -> x1138 mod 3);
  first1138 := First([1..4],i1138 -> normalized1138[i1138]<>0);
  if normalized1138[first1138]=2 then
    normalized1138 := List(normalized1138,x1138 -> (2*x1138) mod 3);
  fi;
  return normalized1138;
end;;

Symplectic1138 := function(x1138,y1138)
  return (x1138[1]*y1138[3]-x1138[3]*y1138[1]
    +x1138[2]*y1138[4]-x1138[4]*y1138[2]) mod 3;
end;;

points1138 := Set(Filtered(
  Cartesian([0..2],[0..2],[0..2],[0..2]),
  vector1138 -> vector1138<>[0,0,0,0]),Canon1138);;

Transvection1138 := function(vector1138)
  local images1138;
  images1138 := List(points1138,x1138 ->
    Canon1138(List([1..4],i1138 ->
      x1138[i1138]+Symplectic1138(x1138,vector1138)*
      vector1138[i1138])));
  return PermList(List(images1138,x1138 ->
    Position(points1138,x1138)));
end;;

PSp401138 := Group(List(points1138,Transvection1138));;
outer1138 := PermList(List(points1138,x1138 ->
  Position(points1138,
    Canon1138([2*x1138[1],2*x1138[2],x1138[3],x1138[4]]))));;
PGSp401138 := Group(Concatenation(
  SmallGeneratingSet(PSp401138),[outer1138]));;
A401138 := List([1..40],i1138 ->
  List([1..40],j1138 ->
    Bit1138(i1138<>j1138 and
      Symplectic1138(points1138[i1138],points1138[j1138])=0)));;
w33Lines1138 := Filtered(Combinations([1..40],4),line1138 ->
  ForAll(Combinations(line1138,2),pair1138 ->
    Symplectic1138(points1138[pair1138[1]],
                   points1138[pair1138[2]])=0));;

# Intrinsic K4,4 octets: a four-coclique together with its four common W33
# neighbors.  BT769 owns its equality with the center-quad quotient.
octets1138 := [];;
for coclique1138 in Combinations([1..40],4) do
  if ForAll(Combinations(coclique1138,2),pair1138 ->
      Symplectic1138(points1138[pair1138[1]],
                     points1138[pair1138[2]])<>0) then
    common1138 := Filtered([1..40],j1138 ->
      ForAll(coclique1138,i1138 ->
        j1138<>i1138 and
        Symplectic1138(points1138[i1138],points1138[j1138])=0));;
    if Length(common1138)=4 then
      AddSet(octets1138,Set(Concatenation(coclique1138,common1138)));
    fi;
  fi;
od;
octetsAreK441138 := ForAll(octets1138,octet1138 ->
  Length(octet1138)=8 and
  ForAll(octet1138,p1138 ->
    Number(octet1138,q1138 ->
      q1138<>p1138 and
      A401138[p1138][q1138]=1)=4));;

stabilizerOctet1138 := Stabilizer(
  PGSp401138,octets1138[1],OnSets);;
groupIsomorphism1138 := IsomorphismGroups(WE61138,PGSp401138);;
Assert1138("W(E6) to PGSp(4,3) isomorphism",
  groupIsomorphism1138<>fail);;
imageSupportStabilizer1138 := Image(
  groupIsomorphism1138,stabilizer451138);;
stabilizerConjugator1138 := RepresentativeAction(
  PGSp401138,imageSupportStabilizer1138,stabilizerOctet1138);;
Assert1138("index-45 stabilizers conjugate",
  stabilizerConjugator1138<>fail);;

supportToOctet1138 := [];;
for support1138 in cubicSupports1138 do
  transport1138 := RepresentativeAction(
    WE61138,cubicSupports1138[1],support1138,OnSets);;
  octetImage1138 := OnSets(octets1138[1],
    Image(groupIsomorphism1138,transport1138)^
      stabilizerConjugator1138);;
  Add(supportToOctet1138,Position(octets1138,octetImage1138));
od;

supportOctetEquivariance1138 := ForAll(
  [1..45],i1138 -> ForAll(smallGenerators1138,g1138 ->
    supportToOctet1138[
      Position(cubicSupports1138,
        OnSets(cubicSupports1138[i1138],g1138))]
    =
    Position(octets1138,
      OnSets(octets1138[supportToOctet1138[i1138]],
        Image(groupIsomorphism1138,g1138)^
          stabilizerConjugator1138))));;
supportOctetRelation1138 := ForAll(
  Combinations([1..45],2),pair1138 ->
    (Intersection(cubicSupports1138[pair1138[1]],
                  cubicSupports1138[pair1138[2]])=[])
    =
    (Length(Intersection(
      octets1138[supportToOctet1138[pair1138[1]]],
      octets1138[supportToOctet1138[pair1138[2]]]))=2));;

# N is the previously known point/octet incidence, transported along the
# explicit support/octet bijection.  C=N*M is the new 2240 -> 45 -> 40 map.
N1138 := List([1..40],p1138 ->
  List([1..45],i1138 ->
    Bit1138(p1138 in octets1138[supportToOctet1138[i1138]])));;
I401138 := IdentityMat(40);;
J401138 := List([1..40],i1138 -> ListWithIdenticalEntries(40,1));;
NNt1138 := N1138*TransposedMat(N1138);;
NtN1138 := TransposedMat(N1138)*N1138;;

C1138 := N1138*M1138;;
CCt1138 := C1138*TransposedMat(C1138);;
CCtExpected1138 := 96*I401138+24*A401138+336*J401138;;
rowSumsC1138 := List(C1138,Sum);;
columnSumsC1138 := List([1..2240],j1138 ->
  Sum(C1138,row1138 -> row1138[j1138]));;
compositeEigenspaces1138 := [
  [13824,40-RankMat(CCt1138-13824*I401138)],
  [144,40-RankMat(CCt1138-144*I401138)],
  [0,40-RankMat(CCt1138)]
];;

# Stronger factorization of the live 40 x 240 submatrix.  Every live column
# equals the all-ones column plus twice one W33 line-incidence column.  The 40
# lines occur six times each.
heavyLinesByColumn1138 := List(liveColumns1138,j1138 ->
  Filtered([1..40],p1138 -> C1138[p1138][j1138]=3));;
heavyLines1138 := Set(heavyLinesByColumn1138);;
lineFiberMultiplicities1138 := List(heavyLines1138,line1138 ->
  Number(heavyLinesByColumn1138,x1138 -> x1138=line1138));;
linePullback1138 := List([1..40],p1138 ->
  List([1..Length(liveColumns1138)],j1138 ->
    Bit1138(p1138 in heavyLinesByColumn1138[j1138])));;
liveComposite1138 := List(C1138,row1138 ->
  row1138{liveColumns1138});;
J40x2401138 := List([1..40],i1138 ->
  ListWithIdenticalEntries(240,1));;

# -------------------------------------------------------------------- checks
checks1138 := rec();;
checks1138.e8_has_240_distinct_norm8_roots :=
  Length(roots1138)=240 and Length(Set(roots1138))=240 and
  Set(List(roots1138,x1138 -> x1138*x1138))=[8];;
checks1138.a2_carrier_has_2240_unordered_zero_sum_triples :=
  Length(a2Triples1138)=2240 and
  ForAll(a2Triples1138,triple1138 ->
    Sum(List(triple1138,i1138 -> roots1138[i1138]))=
      ListWithIdenticalEntries(8,0));;
checks1138.orthogonal_subsystem_has_72_roots_and_we6_order_51840 :=
  Length(e6RootIndices1138)=72 and Size(WE61138)=51840;;
checks1138.cubic_support_carrier_has_45_constant_sum_triples :=
  Length(cubicSupports1138)=45 and
  Length(Set(List(cubicSupports1138,support1138 ->
    Sum(List(support1138,i1138 -> roots1138[i1138])))))=1;;
checks1138.M_has_shape_45_by_2240 :=
  Length(M1138)=45 and Set(List(M1138,Length))=[2240];;
checks1138.M_has_constant_row_sum_32 :=
  Collected(rowSumsM1138)=[[32,45]];;
checks1138.M_column_sums_are_zero_2000_and_six_240 :=
  Collected(columnSumsM1138)=[[0,2000],[6,240]];;
checks1138.M_has_exact_rational_rank_45 :=
  RankMat(M1138)=45;;
checks1138.M_gram_identity_is_24I_minus_6A_plus_8J :=
  gramM1138=gramMExpected1138;;
checks1138.M_gram_off_diagonal_profile_is_2_720_and_8_270 :=
  offDiagonalGramProfile1138=[[2,720],[8,270]];;
checks1138.M_gram_spectrum_is_192_1_48_20_12_24 :=
  gramMEigenspaces1138=[[192,1],[48,20],[12,24]];;
checks1138.a2_orbit_profile_is_complete :=
  a2OrbitProfile1138=
    [1,1,27,27,27,27,27,27,240,270,270,432,432,432];;
checks1138.live_columns_are_exactly_the_unique_240_orbit :=
  Set(liveColumns1138)=Set(orbit2401138);;
checks1138.all_three_432_orbits_are_killed_basis_vector_by_basis_vector :=
  Length(orbits4321138)=3 and
  ForAll(orbits4321138,orbit1138 ->
    ForAll(orbit1138,j1138 -> columnSumsM1138[j1138]=0));;
checks1138.weyl_generators_preserve_root_orthogonality :=
  weylOrthogonalityPreserved1138;;
checks1138.weyl_generators_preserve_both_incidence_carriers :=
  supportCarrierInvariant1138 and a2CarrierInvariant1138;;
checks1138.live_240_module_is_multiplicity_free_1_15_20_24_30_60_90 :=
  decomposition2401138=
    [[1,1],[15,1],[20,1],[24,1],[30,1],[60,1],[90,1]];;
checks1138.cubic_45_module_is_1_20_24 :=
  decomposition451138=[[1,1],[20,1],[24,1]];;
checks1138.live_internal_kernel_is_15_30_60_90_of_dimension_195 :=
  internalKernelDecomposition1138=
    [[15,1],[30,1],[60,1],[90,1]] and
  internalKernelDimension1138=195;;
checks1138.full_M_kernel_dimension_is_2195 :=
  2240-RankMat(M1138)=2195;;
checks1138.w33_has_40_points_40_lines_and_pgsp_order_51840 :=
  Length(points1138)=40 and Length(w33Lines1138)=40 and
  Size(PSp401138)=25920 and Size(PGSp401138)=51840;;
checks1138.intrinsic_octet_carrier_has_45_K44s :=
  Length(octets1138)=45 and octetsAreK441138;;
checks1138.support_and_octet_stabilizers_have_order_1152 :=
  Size(stabilizer451138)=1152 and
  Size(stabilizerOctet1138)=1152;;
checks1138.support_and_octet_stabilizers_are_conjugate_under_an_exact_group_isomorphism :=
  imageSupportStabilizer1138^stabilizerConjugator1138=
    stabilizerOctet1138;;
checks1138.support_to_octet_map_is_a_bijection :=
  Set(supportToOctet1138)=[1..45];;
checks1138.support_to_octet_map_is_generator_equivariant :=
  supportOctetEquivariance1138;;
checks1138.support_disjointness_equals_octet_intersection_two :=
  supportOctetRelation1138;;
checks1138.N_has_shape_40_by_45_row9_column8_and_rank25 :=
  Length(N1138)=40 and Set(List(N1138,Length))=[45] and
  Collected(List(N1138,Sum))=[[9,40]] and
  Collected(List(TransposedMat(N1138),Sum))=[[8,45]] and
  RankMat(N1138)=25;;
checks1138.NNt_reproduces_the_prior_8I_plus_J_plus_2A40_identity :=
  NNt1138=8*I401138+J401138+2*A401138;;
checks1138.NtN_reproduces_the_prior_8I_plus_2A45_identity :=
  NtN1138=8*I451138+2*A451138;;
checks1138.composite_C_has_shape_40_by_2240_and_rank25 :=
  Length(C1138)=40 and Set(List(C1138,Length))=[2240] and
  RankMat(C1138)=25;;
checks1138.composite_row_sums_are_288 :=
  Collected(rowSumsC1138)=[[288,40]];;
checks1138.composite_column_sums_are_zero_2000_and_48_240 :=
  Collected(columnSumsC1138)=[[0,2000],[48,240]];;
checks1138.composite_entry_profile_is_zero_one_three :=
  Collected(Concatenation(C1138))=
    [[0,80000],[1,8640],[3,960]];;
checks1138.composite_gram_identity_is_96I_plus_24A_plus_336J :=
  CCt1138=CCtExpected1138;;
checks1138.composite_gram_spectrum_is_13824_1_144_24_0_15 :=
  compositeEigenspaces1138=[[13824,1],[144,24],[0,15]];;
checks1138.each_live_column_has_one_on_36_points_and_three_on_a_4_point_line :=
  ForAll(liveColumns1138,j1138 ->
    Collected(List(C1138,row1138 -> row1138[j1138]))=
      [[1,36],[3,4]]) and
  ForAll(heavyLinesByColumn1138,line1138 ->
    line1138 in w33Lines1138);;
checks1138.heavy_lines_recover_all_40_W33_lines_six_times_each :=
  Set(heavyLines1138)=Set(w33Lines1138) and
  Set(lineFiberMultiplicities1138)=[6];;
checks1138.live_composite_factorizes_as_J_plus_twice_line_pullback :=
  liveComposite1138=J40x2401138+2*linePullback1138;;

checkNames1138 := RecNames(checks1138);;
failedChecks1138 := Filtered(checkNames1138,name1138 ->
  not checks1138.(name1138));;
Assert1138(Concatenation("all checks; failed=",String(failedChecks1138)),
  IsEmpty(failedChecks1138));;

# -------------------------------------------------------- deterministic JSON
stream1138 := OutputTextFile(OUT1138,false);;
SetPrintFormattingStatus(stream1138,false);;
WriteAll(stream1138,"{\n");;
WriteAll(stream1138,"  \"schema\": \"w33.pass1138.explicit_cubic_incidence_bridge.gap.v1\",\n");;
WriteAll(stream1138,"  \"status\": \"PASS\",\n");;
WriteAll(stream1138,Concatenation(
  "  \"producer\": \"GAP ",GAPInfo.Version," exact integer/rational arithmetic\",\n"));;
WriteAll(stream1138,"  \"headline\": \"The explicit orthogonality incidence M realizes the Pass-1135 2240-to-45 quotient, and its point/octet composite factors through a sixfold W33 line fibration.\",\n");;
WriteAll(stream1138,"  \"prior_owners\": {\n");;
WriteAll(stream1138,"    \"cubic_character_decomposition\": \"analysis/w33_pass1135_cubic_kernel_decomposition.py\",\n");;
WriteAll(stream1138,"    \"45_point_graph\": \"analysis/w33_flat_45_point_frame.py\",\n");;
WriteAll(stream1138,"    \"point_octet_projector\": \"analysis/bt767_k44_octet_incidence_projector.py\",\n");;
WriteAll(stream1138,"    \"intrinsic_octet_identification\": \"analysis/bt769_center_quad_octet_identification.py\"\n");;
WriteAll(stream1138,"  },\n");;
WriteAll(stream1138,"  \"e8_a2_carrier\": {\n");;
WriteAll(stream1138,"    \"doubled_coordinate_roots\": 240,\n");;
WriteAll(stream1138,"    \"a2_zero_sum_triples\": 2240,\n");;
WriteAll(stream1138,"    \"orthogonal_e6_roots\": 72,\n");;
WriteAll(stream1138,"    \"WE6_order\": 51840,\n");;
WriteAll(stream1138,Concatenation(
  "    \"orbit_profile\": ",String(a2OrbitProfile1138),"\n"));;
WriteAll(stream1138,"  },\n");;
WriteAll(stream1138,"  \"explicit_M\": {\n");;
WriteAll(stream1138,"    \"orientation\": \"rows are 45 cubic supports; columns are 2240 unordered A2 root triples\",\n");;
WriteAll(stream1138,"    \"definition\": \"M[s,t]=1 iff every one of the nine doubled-E8 scalar products between s and t is zero\",\n");;
WriteAll(stream1138,"    \"shape\": [45,2240],\n");;
WriteAll(stream1138,"    \"rank_over_Q\": 45,\n");;
WriteAll(stream1138,"    \"row_sum_distribution\": {\"32\":45},\n");;
WriteAll(stream1138,"    \"column_sum_distribution\": {\"0\":2000,\"6\":240},\n");;
WriteAll(stream1138,"    \"live_columns\": \"exactly the unique W(E6) orbit of size 240\",\n");;
WriteAll(stream1138,"    \"killed_432_columns\": 1296,\n");;
WriteAll(stream1138,"    \"gram_identity\": \"M M^T = 24 I_45 - 6 A_45 + 8 J_45\",\n");;
WriteAll(stream1138,"    \"gram_off_diagonal_distribution\": {\"2\":720,\"8\":270},\n");;
WriteAll(stream1138,"    \"gram_spectrum\": {\"192\":1,\"48\":20,\"12\":24}\n");;
WriteAll(stream1138,"  },\n");;
WriteAll(stream1138,"  \"live_240_module\": {\n");;
WriteAll(stream1138,"    \"stabilizer_order\": 216,\n");;
WriteAll(stream1138,Concatenation(
  "    \"stabilizer_structure\": \"",
  StructureDescription(stabilizer2401138),"\",\n"));;
WriteAll(stream1138,"    \"permutation_decomposition_by_degree\": [[1,1],[15,1],[20,1],[24,1],[30,1],[60,1],[90,1]],\n");;
WriteAll(stream1138,"    \"pass1135_label_crosswalk\": \"1 + 15a + 20 + 24 + 30 + 60a + 90\",\n");;
WriteAll(stream1138,"    \"image_decomposition\": \"1 + 20 + 24\",\n");;
WriteAll(stream1138,"    \"internal_kernel_decomposition\": \"15a + 30 + 60a + 90\",\n");;
WriteAll(stream1138,"    \"internal_kernel_dimension\": 195,\n");;
WriteAll(stream1138,"    \"full_kernel_dimension\": 2195\n");;
WriteAll(stream1138,"  },\n");;
WriteAll(stream1138,"  \"support_octet_bijection\": {\n");;
WriteAll(stream1138,"    \"source\": \"45 constant-sum E8 cubic supports\",\n");;
WriteAll(stream1138,"    \"target\": \"45 intrinsic W33 K4,4 octets\",\n");;
WriteAll(stream1138,"    \"group\": \"W(E6) isomorphic to PGSp(4,3)\",\n");;
WriteAll(stream1138,"    \"stabilizer_order\": 1152,\n");;
WriteAll(stream1138,Concatenation(
  "    \"stabilizer_structure\": \"",
  StructureDescription(stabilizer451138),"\",\n"));;
WriteAll(stream1138,"    \"equivariant\": true,\n");;
WriteAll(stream1138,"    \"relation_transport\": \"disjoint E8 supports iff the corresponding W33 octets intersect in two points\",\n");;
WriteAll(stream1138,"    \"choice_boundary\": \"the verifier constructs an equivariant bijection after choosing a group isomorphism and a stabilizer conjugator; no preferred global labeling is claimed\"\n");;
WriteAll(stream1138,"  },\n");;
WriteAll(stream1138,"  \"composite_C_equals_NM\": {\n");;
WriteAll(stream1138,"    \"shape\": [40,2240],\n");;
WriteAll(stream1138,"    \"rank_over_Q\": 25,\n");;
WriteAll(stream1138,"    \"image\": \"the W33 point-carrier 1+24 sector\",\n");;
WriteAll(stream1138,"    \"intermediate_kernel\": \"the 20-dimensional octet-only sector\",\n");;
WriteAll(stream1138,"    \"row_sum_distribution\": {\"288\":40},\n");;
WriteAll(stream1138,"    \"column_sum_distribution\": {\"0\":2000,\"48\":240},\n");;
WriteAll(stream1138,"    \"entry_distribution\": {\"0\":80000,\"1\":8640,\"3\":960},\n");;
WriteAll(stream1138,"    \"gram_identity\": \"C C^T = 96 I_40 + 24 A_W33 + 336 J_40\",\n");;
WriteAll(stream1138,"    \"gram_spectrum\": {\"13824\":1,\"144\":24,\"0\":15},\n");;
WriteAll(stream1138,"    \"live_factorization\": \"C_live = J_(40x240) + 2 R, where R pulls back W33 point-line incidence\",\n");;
WriteAll(stream1138,"    \"line_fibration\": {\"live_a2_triples\":240,\"W33_lines\":40,\"fiber_size\":6,\"column_profile\":{\"1\":36,\"3\":4}}\n");;
WriteAll(stream1138,"  },\n");;
WriteAll(stream1138,"  \"search_signature\": \"45x2240/32x45/0^2000+6^240/24I-6A+8J/240-to-40x6/CCt=96I+24A+336J\",\n");;
WriteAll(stream1138,"  \"scope\": \"Exact finite E8 root incidence, finite permutation representations, and W33 incidence. The sixfold line fibration is not identified with qutrit phase sheets, a physical bundle, a mass spectrum, or a continuum operator.\",\n");;
WriteAll(stream1138,Concatenation(
  "  \"check_count\": ",String(Length(checkNames1138)),",\n"));;
WriteAll(stream1138,"  \"checks\": {\n");;
for checkPosition1138 in [1..Length(checkNames1138)] do
  checkName1138 := checkNames1138[checkPosition1138];;
  WriteAll(stream1138,Concatenation(
    "    \"",checkName1138,"\": ",
    Bool1138(checks1138.(checkName1138))));;
  if checkPosition1138<Length(checkNames1138) then
    WriteAll(stream1138,",");
  fi;
  WriteAll(stream1138,"\n");;
od;
WriteAll(stream1138,"  }\n");;
WriteAll(stream1138,"}\n");;
CloseStream(stream1138);;

Print("Pass1138 status=PASS checks=",Length(checkNames1138),
  " M=45x2240 rank=45 live=240 composite_rank=25 line_fibers=40x6 output=",
  OUT1138,"\n");;
QUIT;
