# Pass 1147 -- Schlaefli-Steinberg Fourier bridge.
# All coordinates use the doubled E8 normalization: roots have norm 8.

Assert1147 := function(label,condition)
  if not condition then
    Error(Concatenation("Pass1147 assertion failed: ",label));
  fi;
end;;

OUT1147 := "data/w33_pass1147_schlaefli_steinberg_fourier_bridge.json";;

BoolString1147 := function(value1147)
  if value1147 then return "true"; fi;
  return "false";
end;;

Bit1147 := function(value1147)
  if value1147 then return 1; fi;
  return 0;
end;;

# --------------------------------------------------------------------- E8
roots1147 := [];;
for i1147 in [1..8] do
  for j1147 in [i1147+1..8] do
    for si1147 in [-2,2] do
      for sj1147 in [-2,2] do
        v1147 := ListWithIdenticalEntries(8,0);;
        v1147[i1147] := si1147;;
        v1147[j1147] := sj1147;;
        Add(roots1147,v1147);
      od;
    od;
  od;
od;
for mask1147 in [0..255] do
  v1147 := List([0..7],k1147 ->
    1-2*((QuoInt(mask1147,2^k1147)) mod 2));;
  if Sum(v1147) mod 4 = 0 then Add(roots1147,v1147); fi;
od;

RootIndex1147 := x1147 -> Position(roots1147,x1147);;
ReflectionPerm1147 := function(root1147)
  return PermList(List(roots1147,x1147 ->
    RootIndex1147(x1147-((x1147*root1147)/4)*root1147)));
end;;

a2Triples1147 := [];;
for i1147 in [1..240] do
  for j1147 in [i1147+1..240] do
    k1147 := RootIndex1147(-(roots1147[i1147]+roots1147[j1147]));;
    if k1147 <> fail and k1147 > j1147 then
      Add(a2Triples1147,[i1147,j1147,k1147]);
    fi;
  od;
od;

# The same deterministic base A2 and orthogonal W(E6) as Pass 1138.
baseA2Triple1147 := a2Triples1147[1];;
baseA2Roots1147 := roots1147{baseA2Triple1147};;
Pattern1147 := i1147 -> List(baseA2Triple1147,j1147 ->
  roots1147[i1147]*roots1147[j1147]);;
e6RootIndices1147 := Filtered([1..240],i1147 ->
  Pattern1147(i1147)=[0,0,0]);;
WE61147 := Group(List(e6RootIndices1147,i1147 ->
  ReflectionPerm1147(roots1147[i1147])));;
smallGenerators1147 := SmallGeneratingSet(WE61147);;

# ------------------------------------------------------------- six shells
# The six size-27 shells have the six permutations of (-4,0,4).
allPatterns1147 := Set(List([1..240],Pattern1147));;
shellPatterns1147 := Filtered(allPatterns1147,p1147 ->
  Number([1..240],i1147 -> Pattern1147(i1147)=p1147)=27);;
shells1147 := List(shellPatterns1147,p1147 ->
  Filtered([1..240],i1147 -> Pattern1147(i1147)=p1147));;

# Negation pairs the six shells.  A color is one opposite pair, equivalently
# the common location of the zero coordinate in its two patterns.
colorPatterns1147 := List([1..3],color1147 ->
  Filtered(shellPatterns1147,p1147 -> p1147[color1147]=0));;
colorShells1147 := List(colorPatterns1147,pair1147 ->
  Filtered([1..240],i1147 -> Pattern1147(i1147) in pair1147));;

# A mixed A2 triple has a color iff it contains exactly one E6 root (pattern
# 000) and two roots in opposite 27-shells.  Its color is the zero-coordinate.
TripleColor1147 := function(triple1147)
  local patterns1147,nonzeroPatterns1147,zeroPositions1147;
  patterns1147 := List(triple1147,Pattern1147);
  if Number(patterns1147,p1147 -> p1147=[0,0,0])<>1 then
    return fail;
  fi;
  nonzeroPatterns1147 := Filtered(patterns1147,p1147 ->
    p1147<>[0,0,0]);
  if Length(nonzeroPatterns1147)<>2 or
      nonzeroPatterns1147[2]<>-nonzeroPatterns1147[1] then
    return fail;
  fi;
  zeroPositions1147 := Filtered([1..3],k1147 ->
    nonzeroPatterns1147[1][k1147]=0);
  if Length(zeroPositions1147)<>1 then return fail; fi;
  return zeroPositions1147[1];
end;;

# Choosing one shell in a color identifies the paired shell with it by
# negation.  Then a colored triple {x,y,z}, with x in S_p, y in S_-p and
# z in E6, becomes the ordered pair (x,-y); its difference (-y)-x=z is an
# E6 root.  These are exactly the directed edges of the Schlaefli graph.
orientedShells1147 := List([1..3],color1147 ->
  Filtered([1..240],i1147 ->
    Pattern1147(i1147)=colorPatterns1147[color1147][1]));;
SchlaefliAdjacent1147 := function(left1147,right1147)
  local differenceIndex1147;
  if left1147=right1147 then return false; fi;
  differenceIndex1147 := RootIndex1147(
    roots1147[right1147]-roots1147[left1147]);
  return differenceIndex1147<>fail and
    differenceIndex1147 in e6RootIndices1147;
end;;
TripleToArc1147 := function(triple1147,color1147)
  local positiveRoot1147,negativeRoot1147;
  positiveRoot1147 := First(triple1147,i1147 ->
    Pattern1147(i1147)=colorPatterns1147[color1147][1]);
  negativeRoot1147 := First(triple1147,i1147 ->
    Pattern1147(i1147)=colorPatterns1147[color1147][2]);
  if positiveRoot1147=fail or negativeRoot1147=fail then return fail; fi;
  return [positiveRoot1147,
    RootIndex1147(-roots1147[negativeRoot1147])];
end;;
SchlaefliProfile1147 := function(shell1147)
  local neighbors1147,pairs1147,adjacentPairs1147,nonadjacentPairs1147;
  neighbors1147 := List(shell1147,left1147 ->
    Filtered(shell1147,right1147 ->
      SchlaefliAdjacent1147(left1147,right1147)));
  pairs1147 := Combinations([1..27],2);
  adjacentPairs1147 := Filtered(pairs1147,pair1147 ->
    shell1147[pair1147[2]] in neighbors1147[pair1147[1]]);
  nonadjacentPairs1147 := Difference(pairs1147,adjacentPairs1147);
  return rec(
    degreeProfile := Collected(List(neighbors1147,Length)),
    edgeCount := Length(adjacentPairs1147),
    adjacentCommonProfile := Collected(List(adjacentPairs1147,pair1147 ->
      Length(Intersection(neighbors1147[pair1147[1]],
        neighbors1147[pair1147[2]])))),
    nonadjacentCommonProfile := Collected(List(nonadjacentPairs1147,pair1147 ->
      Length(Intersection(neighbors1147[pair1147[1]],
        neighbors1147[pair1147[2]]))))
  );
end;;
schlaefliProfiles1147 := List(orientedShells1147,SchlaefliProfile1147);;
schlaefliArcs1147 := List(orientedShells1147,shell1147 ->
  Set(Filtered(Cartesian(shell1147,shell1147),pair1147 ->
    SchlaefliAdjacent1147(pair1147[1],pair1147[2]))));;

# ------------------------------------------------------- W(E6) orbit census
a2ActionHom1147 := ActionHomomorphism(
  WE61147,a2Triples1147,OnSets);;
a2Orbits1147 := Orbits(Image(a2ActionHom1147),[1..2240]);;
orbits4321147 := Filtered(a2Orbits1147,o1147 -> Length(o1147)=432);;
colorFibers1147 := List([1..3],color1147 ->
  Filtered([1..2240],j1147 ->
    TripleColor1147(a2Triples1147[j1147])=color1147));;
orbitIndexInFullCensusByColor1147 := List(colorFibers1147,fiber1147 ->
  PositionProperty(a2Orbits1147,o1147 ->
    Set(o1147)=Set(fiber1147)));;

# --------------------------------------------------------- A2 Coxeter C3
# For alpha,beta the first two base roots, c=s_alpha*s_beta.  Since every E6
# root is orthogonal to alpha and beta, c centralizes every E6 reflection.
sAlpha1147 := ReflectionPerm1147(baseA2Roots1147[1]);;
sBeta1147 := ReflectionPerm1147(baseA2Roots1147[2]);;
coxeter1147 := sAlpha1147*sBeta1147;;

shellPermutation1147 := List([1..6],s1147 ->
  Position(shells1147,Set(List(shells1147[s1147],
    i1147 -> i1147^coxeter1147))));;
colorPermutation1147 := List([1..3],color1147 ->
  Position(colorShells1147,Set(List(colorShells1147[color1147],
    i1147 -> i1147^coxeter1147))));;
fiberPermutation1147 := List([1..3],color1147 ->
  Position(colorFibers1147,Set(List(colorFibers1147[color1147],
    j1147 -> Position(a2Triples1147,
      OnSets(a2Triples1147[j1147],coxeter1147))))));;

# The union of the three fibers is a free C3-torsor over any chosen fiber.
# Choosing color 1 gives an explicit product chart; changing the chosen color
# merely translates that chart.
coloredTripleIndices1147 := Set(Concatenation(colorFibers1147));;
torsorLayers1147 := List([0..2],power1147 ->
  Set(List(colorFibers1147[1],j1147 ->
    Position(a2Triples1147,
      OnSets(a2Triples1147[j1147],coxeter1147^power1147)))));;
extendedGroup1147 := Group(Concatenation(
  GeneratorsOfGroup(WE61147),[coxeter1147]));;

# ------------------------------------------------------------------ checks
checks1147 := rec();;
checks1147.base_is_A2 :=
  Sum(baseA2Roots1147)=ListWithIdenticalEntries(8,0) and
  Set(List(baseA2Roots1147,r1147 -> r1147*r1147))=[8] and
  Set(List(Combinations(baseA2Roots1147,2),pair1147 ->
    pair1147[1]*pair1147[2]))=[-4];;
checks1147.e6_is_pointwise_orthogonal_complement :=
  Length(e6RootIndices1147)=72 and Size(WE61147)=51840 and
  ForAll(GeneratorsOfGroup(WE61147),g1147 ->
    ForAll(baseA2Triple1147,i1147 -> i1147^g1147=i1147));;
checks1147.six_shell_patterns_are_permutations_of_minus4_0_4 :=
  Length(shellPatterns1147)=6 and
  ForAll(shellPatterns1147,p1147 -> SortedList(p1147)=[-4,0,4]);;
checks1147.all_six_shells_have_size_27 :=
  List(shells1147,Length)=ListWithIdenticalEntries(6,27);;
checks1147.negation_pairs_shells_into_three_colors :=
  ForAll(shellPatterns1147,p1147 -> -p1147 in shellPatterns1147) and
  List(colorPatterns1147,Length)=[2,2,2] and
  ForAll(colorPatterns1147,pair1147 ->
    pair1147[2]=-pair1147[1]) and
  List(colorShells1147,Length)=[54,54,54];;
checks1147.negation_is_object_level_between_paired_shells :=
  ForAll([1..3],color1147 ->
    Set(List(Filtered([1..240],i1147 ->
      Pattern1147(i1147)=colorPatterns1147[color1147][1]),
      i1147 -> RootIndex1147(-roots1147[i1147])))
    =
    Set(Filtered([1..240],i1147 ->
      Pattern1147(i1147)=colorPatterns1147[color1147][2])));;
checks1147.WE6_preserves_each_individual_shell :=
  ForAll(smallGenerators1147,g1147 ->
    ForAll(shells1147,shell1147 ->
      Set(List(shell1147,i1147 -> i1147^g1147))=shell1147));;
checks1147.exactly_three_432_orbits :=
  Length(orbits4321147)=3;;
checks1147.each_color_fiber_has_size_432 :=
  List(colorFibers1147,Length)=[432,432,432];;
checks1147.three_432_orbits_are_exactly_the_three_color_fibers :=
  Set(List(orbits4321147,Set))=Set(List(colorFibers1147,Set));;
checks1147.colored_triples_have_one_E6_root_and_an_opposite_shell_pair :=
  ForAll(coloredTripleIndices1147,j1147 ->
    TripleColor1147(a2Triples1147[j1147]) in [1..3]);;
checks1147.no_other_A2_triple_has_a_color :=
  Number([1..2240],j1147 ->
    TripleColor1147(a2Triples1147[j1147])<>fail)=1296;;
checks1147.each_color_is_the_directed_Schlaefli_edge_carrier :=
  ForAll([1..3],color1147 ->
    Set(List(colorFibers1147[color1147],j1147 ->
      TripleToArc1147(a2Triples1147[j1147],color1147)))
    =
    schlaefliArcs1147[color1147]);;
checks1147.all_three_shell_graphs_are_SRG_27_16_10_8 :=
  ForAll(schlaefliProfiles1147,profile1147 ->
    profile1147.degreeProfile=[[16,27]] and
    profile1147.edgeCount=216 and
    profile1147.adjacentCommonProfile=[[10,216]] and
    profile1147.nonadjacentCommonProfile=[[8,135]]);;
checks1147.directed_edge_stabilizers_are_S5_of_order_120 :=
  ForAll([1..3],color1147 ->
    Size(Stabilizer(WE61147,schlaefliArcs1147[color1147][1],
      OnTuples))=120 and
    StructureDescription(Stabilizer(WE61147,
      schlaefliArcs1147[color1147][1],OnTuples))="S5");;
checks1147.base_reflections_are_involutions_and_coxeter_has_order_3 :=
  Order(sAlpha1147)=2 and Order(sBeta1147)=2 and
  Order(coxeter1147)=3;;
checks1147.coxeter_cycles_the_three_base_roots :=
  Set(List(baseA2Triple1147,i1147 -> i1147^coxeter1147))=
    Set(baseA2Triple1147) and
  List(baseA2Triple1147,i1147 -> i1147^coxeter1147)=
    [baseA2Triple1147[3],baseA2Triple1147[1],
     baseA2Triple1147[2]];;
checks1147.coxeter_centralizes_every_E6_root_reflection :=
  ForAll(GeneratorsOfGroup(WE61147),g1147 ->
    Comm(coxeter1147,g1147)=());;
checks1147.coxeter_cycles_shells_in_two_3_cycles :=
  Order(PermList(shellPermutation1147))=3 and
  Collected(List(Orbits(Group(PermList(shellPermutation1147)),
    [1..6]),Length))=[[3,2]];;
checks1147.coxeter_cycles_colors :=
  colorPermutation1147=[3,1,2] and
  Order(PermList(colorPermutation1147))=3;;
checks1147.coxeter_cycles_the_three_432_fibers :=
  fiberPermutation1147=colorPermutation1147 and
  Order(PermList(fiberPermutation1147))=3;;
checks1147.C3_action_is_free_on_all_1296_colored_triples :=
  ForAll(coloredTripleIndices1147,j1147 ->
    Position(a2Triples1147,
      OnSets(a2Triples1147[j1147],coxeter1147))<>j1147);;
checks1147.torsor_chart_has_three_disjoint_432_layers :=
  List(torsorLayers1147,Length)=[432,432,432] and
  Length(Set(Concatenation(torsorLayers1147)))=1296 and
  Set(Concatenation(torsorLayers1147))=coloredTripleIndices1147;;
checks1147.product_chart_is_WE6_equivariant :=
  ForAll(colorFibers1147[1],j1147 ->
    ForAll([0..2],power1147 ->
      ForAll(smallGenerators1147,g1147 ->
        OnSets(OnSets(a2Triples1147[j1147],g1147),
          coxeter1147^power1147)
        =
        OnSets(OnSets(a2Triples1147[j1147],
          coxeter1147^power1147),g1147))));;
checks1147.extension_is_internal_direct_product_WE6_times_C3 :=
  Size(extendedGroup1147)=3*Size(WE61147) and
  Size(Intersection(WE61147,Group(coxeter1147)))=1;;

checkNames1147 := RecNames(checks1147);;
failedChecks1147 := Filtered(checkNames1147,name1147 ->
  not checks1147.(name1147));;
Assert1147(Concatenation("all checks; failed=",String(failedChecks1147)),
  IsEmpty(failedChecks1147));;

Print("Pass1147 scratch status=PASS checks=",Length(checkNames1147),"\n");
Print("base_A2_indices=",baseA2Triple1147,
  " base_cycle=",List(baseA2Triple1147,
    i1147 -> i1147^coxeter1147),"\n");
Print("shell_patterns=",shellPatterns1147,
  " shell_sizes=",List(shells1147,Length),"\n");
Print("color_patterns=",colorPatterns1147,
  " color_sizes=",List(colorShells1147,Length),"\n");
Print("A2_orbit_sizes=",List(a2Orbits1147,Length),"\n");
Print("color_fiber_sizes=",List(colorFibers1147,Length),
  " full_orbit_indices_by_color=",orbitIndexInFullCensusByColor1147,"\n");
Print("Schlaefli_profiles=",
  List(schlaefliProfiles1147,profile1147 ->
    [profile1147.degreeProfile,profile1147.edgeCount,
     profile1147.adjacentCommonProfile,
     profile1147.nonadjacentCommonProfile]),
  " directed_arc_sizes=",List(schlaefliArcs1147,Length),"\n");
Print("coxeter_order=",Order(coxeter1147),
  " shell_permutation=",shellPermutation1147,
  " color_permutation=",colorPermutation1147,
  " fiber_permutation=",fiberPermutation1147,"\n");
Print("extended_group_order=",Size(extendedGroup1147),
  " intersection_order=",
  Size(Intersection(WE61147,Group(coxeter1147))),"\n");
Print("choice_boundary=the free color C3-torsor is intrinsic relative to the ",
  "base A2; a labeled Omega_432 x C3 chart chooses an origin color and a ",
  "generator (the inverse Coxeter element reverses the labels).\n");

# ======================================================== rank-81 bridge
# This section rebuilds the Pass-1143 intertwiner on the actual root-reflection
# W(E6), its actual 27-shell action, and the actual directed Schlaefli arcs.
baseShell1147I := orientedShells1147[1];;
baseArcs1147I := schlaefliArcs1147[1];;
baseArc1147I := baseArcs1147I[1];;
Harc1147I := Stabilizer(WE61147,baseArc1147I,OnTuples);;
hom271147I := ActionHomomorphism(
  WE61147,baseShell1147I,OnPoints);;
hom4321147I := ActionHomomorphism(
  WE61147,baseArcs1147I,OnTuples);;

# The 36 root reflections are the unique size-36 involution class (2C in the
# Pass-1143 convention).
reflectionClass1147I := Set(List(e6RootIndices1147,i1147 ->
  ReflectionPerm1147(roots1147[i1147])));;
conjugacyClass1147I := ConjugacyClass(
  WE61147,reflectionClass1147I[1]);;
size36InvolutionClasses1147I := Filtered(
  ConjugacyClasses(WE61147),class1147 ->
    Size(class1147)=36 and Order(Representative(class1147))=2);;

# Signed-pair realization of Lambda^2(C[27]).
wedgePairs1147I := [];;
wedgePairIndex1147I := List([1..27],i1147 ->
  ListWithIdenticalEntries(27,0));;
for i1147 in [1..27] do
  for j1147 in [i1147+1..27] do
    Add(wedgePairs1147I,[i1147,j1147]);;
    wedgePairIndex1147I[i1147][j1147] := Length(wedgePairs1147I);;
    wedgePairIndex1147I[j1147][i1147] := Length(wedgePairs1147I);;
  od;
od;

WedgeImage1147I := function(vector1147I,permutation1147I)
  local out1147I,k1147I,pair1147I,a1147I,b1147I,sign1147I;
  out1147I := ListWithIdenticalEntries(351,0);
  for k1147I in [1..351] do
    if vector1147I[k1147I]<>0 then
      pair1147I := wedgePairs1147I[k1147I];
      a1147I := pair1147I[1]^permutation1147I;
      b1147I := pair1147I[2]^permutation1147I;
      if a1147I<b1147I then sign1147I:=1;
      else sign1147I:=-1; fi;
      out1147I[wedgePairIndex1147I[a1147I][b1147I]] :=
        out1147I[wedgePairIndex1147I[a1147I][b1147I]]
        +sign1147I*vector1147I[k1147I];
    fi;
  od;
  return out1147I;
end;;

AddVec1147I := function(left1147I,right1147I)
  return List([1..Length(left1147I)],i1147 ->
    left1147I[i1147]+right1147I[i1147]);
end;;
SubScalar1147I := function(left1147I,right1147I,scalar1147I)
  return List([1..Length(left1147I)],i1147 ->
    left1147I[i1147]-scalar1147I*right1147I[i1147]);
end;;
Contraction1147I := function(vector1147I)
  local out1147I,k1147I,pair1147I;
  out1147I := ListWithIdenticalEntries(27,0);
  for k1147I in [1..351] do
    if vector1147I[k1147I]<>0 then
      pair1147I := wedgePairs1147I[k1147I];
      out1147I[pair1147I[1]] :=
        out1147I[pair1147I[1]]-vector1147I[k1147I];
      out1147I[pair1147I[2]] :=
        out1147I[pair1147I[2]]+vector1147I[k1147I];
    fi;
  od;
  return out1147I;
end;;

h27Elements1147I := List(Elements(Harc1147I),h1147 ->
  Image(hom271147I,h1147));;
k27Elements1147I := List(reflectionClass1147I,k1147 ->
  Image(hom271147I,k1147));;

AverageH1147I := function(seed1147I)
  local out1147I,permutation1147I;
  out1147I := ListWithIdenticalEntries(351,0);
  for permutation1147I in h27Elements1147I do
    out1147I := AddVec1147I(out1147I,
      WedgeImage1147I(seed1147I,permutation1147I));
  od;
  return out1147I;
end;;
ApplyK1147I := function(vector1147I)
  local out1147I,permutation1147I;
  out1147I := ListWithIdenticalEntries(351,0);
  for permutation1147I in k27Elements1147I do
    out1147I := AddVec1147I(out1147I,
      WedgeImage1147I(vector1147I,permutation1147I));
  od;
  return out1147I;
end;;
ApplyQ1147I := function(vector1147I)
  local out1147I,eigenvalue1147I;
  out1147I := ShallowCopy(vector1147I);
  for eigenvalue1147I in [24,18,12,9] do
    out1147I := SubScalar1147I(
      ApplyK1147I(out1147I),out1147I,eigenvalue1147I);
  od;
  return out1147I;
end;;

# Average one signed-wedge orbit under H, then project to the K-eigenvalue 4
# constituent.  The search is deterministic and normally stops at e1 wedge e2.
seenWedgePairs1147I := [];;
seedIndex1147I := fail;;
vH1147I := fail;;
vQ1147I := fail;;
for k1147I in [1..351] do
  if not k1147I in seenWedgePairs1147I then
    seed1147I := ListWithIdenticalEntries(351,0);;
    seed1147I[k1147I] := 1;;
    for permutation1147I in h27Elements1147I do
      pair1147I := wedgePairs1147I[k1147I];;
      a1147I := pair1147I[1]^permutation1147I;;
      b1147I := pair1147I[2]^permutation1147I;;
      AddSet(seenWedgePairs1147I,
        wedgePairIndex1147I[a1147I][b1147I]);;
    od;
    candidateH1147I := AverageH1147I(seed1147I);;
    if candidateH1147I<>ListWithIdenticalEntries(351,0) then
      candidateQ1147I := ApplyQ1147I(candidateH1147I);;
      if candidateQ1147I<>ListWithIdenticalEntries(351,0) then
        seedIndex1147I := k1147I;;
        vH1147I := candidateH1147I;;
        vQ1147I := candidateQ1147I;;
        break;
      fi;
    fi;
  fi;
od;
Assert1147("actual-action projected H-fixed seed exists",
  seedIndex1147I<>fail);;
contentQ1147I := Gcd(List(Filtered(vQ1147I,x1147 ->
  x1147<>0),AbsInt));;
vQPrimitive1147I := List(vQ1147I,x1147 ->
  x1147/contentQ1147I);;
zero271147I := ListWithIdenticalEntries(27,0);;

# Q has exact rank 81 on Lambda^2(Aug26).
qColumns3511147I := [];;
for k1147I in [1..351] do
  seed1147I := ListWithIdenticalEntries(351,0);;
  seed1147I[k1147I] := 1;;
  Add(qColumns3511147I,ApplyQ1147I(seed1147I));;
od;
keep3251147I := Filtered([1..351],k1147I ->
  wedgePairs1147I[k1147I][2]<>27);;
qColumns3251147I := List(qColumns3511147I,v1147 ->
  v1147{keep3251147I});;
qRank1147I := RankMat(qColumns3251147I);;

# Object-level orbit map: its columns are indexed by the actual directed
# Schlaefli edges, not by an abstract TOM coset carrier.
arcTransporters1147I := List(baseArcs1147I,arc1147 ->
  RepresentativeAction(WE61147,baseArc1147I,arc1147,OnTuples));;
columns3511147I := List(arcTransporters1147I,g1147 ->
  WedgeImage1147I(vQPrimitive1147I,Image(hom271147I,g1147)));;
columns3251147I := List(columns3511147I,v1147 ->
  v1147{keep3251147I});;
intertwinerRank1147I := RankMat(columns3251147I);;
pmod1147I := 1000003;;
onep1147I := One(GF(pmod1147I));;
intertwinerRankMod1147I := RankMat(List(columns3251147I,row1147 ->
  List(row1147,x1147 -> (x1147 mod pmod1147I)*onep1147I)));;

# The stabilizer average is not needed to define the transform.  Apply Q
# directly to the oriented Schlaefli edge wedge e_u wedge e_v.  This gives
# the same orbit map and makes orientation reversal visibly odd.
OrientedEdgeWedge1147I := function(arc1147I)
  local vector1147I,i1147I,j1147I;
  vector1147I := ListWithIdenticalEntries(351,0);
  i1147I := Position(baseShell1147I,arc1147I[1]);
  j1147I := Position(baseShell1147I,arc1147I[2]);
  if i1147I<j1147I then
    vector1147I[wedgePairIndex1147I[i1147I][j1147I]] := 1;
  else
    vector1147I[wedgePairIndex1147I[i1147I][j1147I]] := -1;
  fi;
  return vector1147I;
end;;
naturalBaseQ1147I := ApplyQ1147I(
  OrientedEdgeWedge1147I(baseArc1147I));;
naturalContent1147I := Gcd(List(Filtered(naturalBaseQ1147I,
  x1147 -> x1147<>0),AbsInt));;
naturalBasePrimitive1147I := List(naturalBaseQ1147I,
  x1147 -> x1147/naturalContent1147I);;
if naturalBasePrimitive1147I=vQPrimitive1147I then
  naturalGlobalSign1147I := 1;;
elif naturalBasePrimitive1147I=-vQPrimitive1147I then
  naturalGlobalSign1147I := -1;;
else
  Error("Pass1147 natural Q(edge) disagrees with H-fixed line");
fi;
naturalColumns3511147I := List(baseArcs1147I,arc1147 ->
  naturalGlobalSign1147I*List(
    ApplyQ1147I(OrientedEdgeWedge1147I(arc1147)),
    x1147 -> x1147/naturalContent1147I));;
arcReverse1147I := List(baseArcs1147I,arc1147 ->
  Position(baseArcs1147I,[arc1147[2],arc1147[1]]));;
arcReversePerm1147I := PermList(arcReverse1147I);;
reverseOdd1147I := ForAll([1..432],i1147 ->
  columns3511147I[i1147^arcReversePerm1147I]
    =-columns3511147I[i1147]);;

# Exact tight frame and projective three-angle quotient.
primitiveProfile1147I := Collected(vQPrimitive1147I);;
primitiveNorm21147I := vQPrimitive1147I*vQPrimitive1147I;;
gram4321147I := columns3511147I*TransposedMat(columns3511147I);;
frameScale1147I := 432*primitiveNorm21147I/81;;
offDiagonalGramProfile1147I := Collected(List(
  Combinations([1..432],2),pair1147 ->
    gram4321147I[pair1147[1]][pair1147[2]]));;
projectiveReps1147I := List(
  Orbits(Group(arcReversePerm1147I),[1..432]),Minimum);;
projectiveSignedGram1147I := gram4321147I{
  projectiveReps1147I}{projectiveReps1147I};;
projectiveAbsGram1147I := List(projectiveSignedGram1147I,row1147 ->
  List(row1147,AbsInt));;
projectiveAbsRelations1147I := List([120,40,0],value1147 ->
  List([1..216],i1147 -> List([1..216],j1147 ->
    Bit1147(i1147<>j1147 and
      projectiveAbsGram1147I[i1147][j1147]=value1147))));;
projectiveAngleDegrees1147I := List(projectiveAbsRelations1147I,
  matrix1147 -> Set(List(matrix1147,Sum)));;
projectiveAnglePairCounts1147I := List(projectiveAbsRelations1147I,
  matrix1147 -> Sum(List(matrix1147,Sum))/2);;

GeneratorEquivariant1147I := function(
    columns1147I,p271147I,p4321147I)
  local i1147I;
  for i1147I in [1..Length(columns1147I)] do
    if WedgeImage1147I(columns1147I[i1147I],p271147I)
        <>columns1147I[i1147I^p4321147I] then
      return false;
    fi;
  od;
  return true;
end;;
equivarianceChecks1147I := List(smallGenerators1147,g1147 ->
  GeneratorEquivariant1147I(columns3511147I,
    Image(hom271147I,g1147),Image(hom4321147I,g1147)));;
allReflectionEquivarianceChecks1147I := List(
  reflectionClass1147I,g1147 ->
    GeneratorEquivariant1147I(columns3511147I,
      Image(hom271147I,g1147),Image(hom4321147I,g1147)));;

checks1147I := rec();;
checks1147I.actual_arc_stabilizer_is_S5_order120 :=
  Size(Harc1147I)=120 and StructureDescription(Harc1147I)="S5";;
checks1147I.actual_27_and_432_actions_are_faithful :=
  Size(Image(hom271147I))=51840 and
  Size(Image(hom4321147I))=51840;;
checks1147I.root_reflections_are_the_size36_involution_class :=
  Length(reflectionClass1147I)=36 and
  Length(size36InvolutionClasses1147I)=1 and
  Size(conjugacyClass1147I)=36 and
  Set(Elements(conjugacyClass1147I))=reflectionClass1147I and
  ForAll(reflectionClass1147I,g1147 -> Order(g1147)=2);;
checks1147I.projected_seed_is_H_fixed :=
  ForAll(h27Elements1147I,p1147 ->
    WedgeImage1147I(vQPrimitive1147I,p1147)=vQPrimitive1147I);;
checks1147I.projected_seed_lies_in_Lambda2Aug26 :=
  Contraction1147I(vQPrimitive1147I)=zero271147I;;
checks1147I.projected_seed_has_K_eigenvalue4 :=
  ApplyK1147I(vQPrimitive1147I)=4*vQPrimitive1147I;;
checks1147I.scaled_projector_satisfies_Q2_equals11200Q_on_seed :=
  ApplyQ1147I(vQPrimitive1147I)=11200*vQPrimitive1147I;;
checks1147I.scaled_projector_has_exact_rank81 :=
  qRank1147I=81;;
checks1147I.actual_325_by_432_intertwiner_has_rank81 :=
  Length(columns3251147I)=432 and
  Set(List(columns3251147I,Length))=[325] and
  intertwinerRank1147I=81 and intertwinerRankMod1147I=81;;
checks1147I.all_actual_columns_are_in_Lambda2Aug26 :=
  ForAll(columns3511147I,v1147 ->
    Contraction1147I(v1147)=zero271147I);;
checks1147I.actual_intertwiner_is_generator_equivariant :=
  ForAll(equivarianceChecks1147I,x1147 -> x1147) and
  ForAll(allReflectionEquivarianceChecks1147I,x1147 -> x1147);;
checks1147I.natural_Q_edge_map_equals_the_orbit_intertwiner :=
  naturalColumns3511147I=columns3511147I;;
checks1147I.arc_reversal_is_odd_with_216_pairs :=
  Order(arcReversePerm1147I)=2 and
  Collected(List(Orbits(Group(arcReversePerm1147I),
    [1..432]),Length))=[[2,216]] and reverseOdd1147I;;
checks1147I.oriented_vectors_form_the_rank81_tight_frame :=
  primitiveNorm21147I=600 and frameScale1147I=3200 and
  gram4321147I^2=3200*gram4321147I;;
checks1147I.oriented_Gram_profile_is_exact :=
  offDiagonalGramProfile1147I=
    [[-600,216],[-120,7560],[-40,12960],
     [0,51840],[40,12960],[120,7560]];;
checks1147I.projective_quotient_is_a_216_line_three_angle_tight_frame :=
  Length(projectiveReps1147I)=216 and
  projectiveSignedGram1147I^2=1600*projectiveSignedGram1147I and
  projectiveAngleDegrees1147I=[[35],[60],[120]] and
  projectiveAnglePairCounts1147I=[3780,6480,12960];;

failedChecks1147I := Filtered(RecNames(checks1147I),name1147 ->
  not checks1147I.(name1147));;
Assert1147(Concatenation("actual rank81 bridge; failed=",
  String(failedChecks1147I)),IsEmpty(failedChecks1147I));;

Print("actual_rank81_bridge status=PASS checks=",
  Length(RecNames(checks1147I)),
  " H=",Size(Harc1147I),
  " seed=",wedgePairs1147I[seedIndex1147I],
  " Hsupport=",Number(vH1147I,x1147 -> x1147<>0),
  " Qsupport=",Number(vQPrimitive1147I,x1147 -> x1147<>0),
  " content=",contentQ1147I,
  " Qrank=",qRank1147I,
  " intertwiner_shape=325x432 rank=",intertwinerRank1147I,
  " rank_mod_",pmod1147I,"=",intertwinerRankMod1147I,
  " small_generator_equivariance=",equivarianceChecks1147I,
  " reflection_equivariance=",
  Number(allReflectionEquivarianceChecks1147I,x1147 -> x1147),
  "/36 natural_Q_edge=",
  naturalColumns3511147I=columns3511147I,
  " reversal_odd=",reverseOdd1147I,
  " frame_scale=",frameScale1147I,
  " projective_degrees=",projectiveAngleDegrees1147I,"\n");;

# ============================================== literal C3-colored map
# Use the c-orbit of the base shell, rather than an arbitrary lexicographic
# orientation in each color.  This makes c transport vertices, arcs, triples,
# and wedge coordinates literally.
c3Shells1147I := List([0..2],power1147 ->
  Set(List(baseShell1147I,i1147 -> i1147^
    (coxeter1147^power1147))));;
c3Arcs1147I := List([0..2],power1147 ->
  Set(List(baseArcs1147I,arc1147 ->
    OnTuples(arc1147,coxeter1147^power1147))));;
c3TripleFibers1147I := torsorLayers1147;;

TripleToOrientedArc1147I := function(triple1147I,shell1147I)
  local positive1147I,negative1147I;
  positive1147I := First(triple1147I,i1147 -> i1147 in shell1147I);
  negative1147I := First(triple1147I,i1147 ->
    RootIndex1147(-roots1147[i1147]) in shell1147I);
  if positive1147I=fail or negative1147I=fail then return fail; fi;
  return [positive1147I,RootIndex1147(-roots1147[negative1147I])];
end;;

TransportWedge1147I := function(
    vector1147I,sourceShell1147I,targetShell1147I,rootPerm1147I)
  local out1147I,k1147I,pair1147I,aRoot1147I,bRoot1147I,
        a1147I,b1147I,sign1147I;
  out1147I := ListWithIdenticalEntries(351,0);
  for k1147I in [1..351] do
    if vector1147I[k1147I]<>0 then
      pair1147I := wedgePairs1147I[k1147I];
      aRoot1147I := sourceShell1147I[pair1147I[1]]^rootPerm1147I;
      bRoot1147I := sourceShell1147I[pair1147I[2]]^rootPerm1147I;
      a1147I := Position(targetShell1147I,aRoot1147I);
      b1147I := Position(targetShell1147I,bRoot1147I);
      if a1147I<b1147I then sign1147I:=1;
      else sign1147I:=-1; fi;
      out1147I[wedgePairIndex1147I[a1147I][b1147I]] :=
        out1147I[wedgePairIndex1147I[a1147I][b1147I]]
        +sign1147I*vector1147I[k1147I];
    fi;
  od;
  return out1147I;
end;;

# Transport the full orbit map, then reorder it by the target arc carrier.
c3Columns3511147I := [];;
for layer1147I in [1..3] do
  power1147I := layer1147I-1;;
  layerColumns1147I := [];;
  for arc1147I in c3Arcs1147I[layer1147I] do
    sourceArc1147I := OnTuples(
      arc1147I,coxeter1147^-power1147I);;
    sourcePosition1147I := Position(baseArcs1147I,sourceArc1147I);;
    Add(layerColumns1147I,TransportWedge1147I(
      columns3511147I[sourcePosition1147I],
      baseShell1147I,c3Shells1147I[layer1147I],
      coxeter1147^power1147I));;
  od;
  Add(c3Columns3511147I,layerColumns1147I);;
od;
c3Columns3251147I := List(c3Columns3511147I,layer1147I ->
  List(layer1147I,v1147 -> v1147{keep3251147I}));;
c3LayerRanks1147I := List(c3Columns3251147I,RankMat);;
c3Hom271147I := List(c3Shells1147I,shell1147 ->
  ActionHomomorphism(WE61147,shell1147,OnPoints));;
c3Hom4321147I := List(c3Arcs1147I,arcs1147 ->
  ActionHomomorphism(WE61147,arcs1147,OnTuples));;
c3WE6Equivariance1147I := List([1..3],layer1147 ->
  ForAll(smallGenerators1147,g1147 ->
    GeneratorEquivariant1147I(
      c3Columns3511147I[layer1147],
      Image(c3Hom271147I[layer1147],g1147),
      Image(c3Hom4321147I[layer1147],g1147))));;
c3ProjectedSeeds1147I := List([0..2],power1147 ->
  TransportWedge1147I(vQPrimitive1147I,baseShell1147I,
    c3Shells1147I[power1147+1],coxeter1147^power1147));;

ApplyClassSum1147I := function(vector1147I,permutations1147I)
  local out1147I,permutation1147I;
  out1147I := ListWithIdenticalEntries(351,0);
  for permutation1147I in permutations1147I do
    out1147I := AddVec1147I(out1147I,
      WedgeImage1147I(vector1147I,permutation1147I));
  od;
  return out1147I;
end;;
ApplyProjectorFromPerms1147I := function(
    vector1147I,permutations1147I)
  local out1147I,eigenvalue1147I;
  out1147I := ShallowCopy(vector1147I);
  for eigenvalue1147I in [24,18,12,9] do
    out1147I := SubScalar1147I(
      ApplyClassSum1147I(out1147I,permutations1147I),
      out1147I,eigenvalue1147I);
  od;
  return out1147I;
end;;
c3LayerProjectorChecks1147I := List([1..3],layer1147 ->
  ForAll(Elements(Harc1147I),h1147 ->
    WedgeImage1147I(c3ProjectedSeeds1147I[layer1147],
      Image(c3Hom271147I[layer1147],h1147))
      =c3ProjectedSeeds1147I[layer1147])
  and
  ApplyClassSum1147I(c3ProjectedSeeds1147I[layer1147],
    List(reflectionClass1147I,g1147 ->
      Image(c3Hom271147I[layer1147],g1147)))
    =4*c3ProjectedSeeds1147I[layer1147]
  and
  ApplyProjectorFromPerms1147I(c3ProjectedSeeds1147I[layer1147],
    List(reflectionClass1147I,g1147 ->
      Image(c3Hom271147I[layer1147],g1147)))
    =11200*c3ProjectedSeeds1147I[layer1147]);;

# Build the 975 x 1296 block map directly on the colored A2 triples.
combinedTripleRows1147I := [];;
for tripleIndex1147I in coloredTripleIndices1147 do
  layer1147I := PositionProperty(c3TripleFibers1147I,
    fiber1147 -> tripleIndex1147I in fiber1147);;
  arc1147I := TripleToOrientedArc1147I(
    a2Triples1147[tripleIndex1147I],c3Shells1147I[layer1147I]);;
  arcPosition1147I := Position(c3Arcs1147I[layer1147I],arc1147I);;
  targetRow1147I := ListWithIdenticalEntries(975,0);;
  targetRow1147I{
    [(layer1147I-1)*325+1..layer1147I*325]} :=
      c3Columns3251147I[layer1147I][arcPosition1147I];;
  Add(combinedTripleRows1147I,targetRow1147I);;
od;
combinedC3Rank1147I := RankMat(combinedTripleRows1147I);;
c3ShellColorIndices1147I := List(c3Shells1147I,shell1147 ->
  PositionProperty(colorShells1147,colorShell1147 ->
    ForAll(shell1147,i1147 -> i1147 in colorShell1147)));;

# Check c transport on every actual colored triple/column before dropping the
# contraction coordinates.
c3ColumnTransportChecks1147I := [];;
for layer1147I in [1..3] do
  nextLayer1147I := (layer1147I mod 3)+1;;
  layerCheck1147I := true;;
  for arcPosition1147I in [1..432] do
    arc1147I := c3Arcs1147I[layer1147I][arcPosition1147I];;
    nextArc1147I := OnTuples(arc1147I,coxeter1147);;
    nextPosition1147I := Position(
      c3Arcs1147I[nextLayer1147I],nextArc1147I);;
    transported1147I := TransportWedge1147I(
      c3Columns3511147I[layer1147I][arcPosition1147I],
      c3Shells1147I[layer1147I],
      c3Shells1147I[nextLayer1147I],coxeter1147);;
    if transported1147I<>
        c3Columns3511147I[nextLayer1147I][nextPosition1147I] then
      layerCheck1147I := false;;
      break;
    fi;
  od;
  Add(c3ColumnTransportChecks1147I,layerCheck1147I);;
od;

checks1147C3 := rec();;
checks1147C3.c3_shells_have_three_distinct_colors :=
  Set(c3ShellColorIndices1147I)=[1,2,3];;
checks1147C3.c3_arc_layers_are_432_each :=
  List(c3Arcs1147I,Length)=[432,432,432];;
checks1147C3.triple_to_arc_is_bijective_in_every_layer :=
  ForAll([1..3],layer1147 ->
    Set(List(c3TripleFibers1147I[layer1147],j1147 ->
      TripleToOrientedArc1147I(a2Triples1147[j1147],
        c3Shells1147I[layer1147])))
    =c3Arcs1147I[layer1147]);;
checks1147C3.each_transported_intertwiner_has_rank81 :=
  c3LayerRanks1147I=[81,81,81];;
checks1147C3.each_layer_is_WE6_equivariant_and_projector_certified :=
  c3WE6Equivariance1147I=[true,true,true] and
  c3LayerProjectorChecks1147I=[true,true,true];;
checks1147C3.coxeter_transports_all_three_intertwiners_literally :=
  c3ColumnTransportChecks1147I=[true,true,true];;
checks1147C3.combined_C3_colored_map_has_shape975_by1296_rank243 :=
  Length(combinedTripleRows1147I)=1296 and
  Set(List(combinedTripleRows1147I,Length))=[975] and
  combinedC3Rank1147I=243;;

failedChecks1147C3 := Filtered(RecNames(checks1147C3),name1147 ->
  not checks1147C3.(name1147));;
Assert1147(Concatenation("C3-colored rank243 bridge; failed=",
  String(failedChecks1147C3)),IsEmpty(failedChecks1147C3));;

Print("C3_colored_intertwiner status=PASS checks=",
  Length(RecNames(checks1147C3)),
  " shell_colors=",c3ShellColorIndices1147I,
  " layer_ranks=",c3LayerRanks1147I,
  " combined_shape=975x1296 rank=",combinedC3Rank1147I,
  " WE6_equivariance=",c3WE6Equivariance1147I,
  " projector_checks=",c3LayerProjectorChecks1147I,
  " c_transport=",c3ColumnTransportChecks1147I,"\n");;

# ======================================= weld to Pass-1138 cubic incidence
# Reconstruct M in the same root coordinates.  Its active columns and the
# colored Steinberg columns are disjoint, so the enhanced map has rank
# 45+3*81=288 and a genuinely explained 1952-dimensional kernel.
shellTriples1147W := Combinations(shells1147[1],3);;
shellSums1147W := Set(List(shellTriples1147W,triple1147 ->
  Sum(List(triple1147,i1147 -> roots1147[i1147]))));;
cubicSupports1147W := First(
  List(shellSums1147W,sum1147 ->
    Filtered(shellTriples1147W,triple1147 ->
      Sum(List(triple1147,i1147 -> roots1147[i1147]))=sum1147)),
  family1147 -> Length(family1147)=45);;
cubicSupports1147W := Set(cubicSupports1147W,Set);;
Bit1147W := function(value1147)
  if value1147 then return 1; fi;
  return 0;
end;;
M1147W := List(cubicSupports1147W,support1147 ->
  List(a2Triples1147,triple1147 ->
    Bit1147W(ForAll(support1147,i1147 ->
      ForAll(triple1147,j1147 ->
        roots1147[i1147]*roots1147[j1147]=0)))));;
mColumnSums1147W := List([1..2240],j1147 ->
  Sum(M1147W,row1147 -> row1147[j1147]));;
mLiveColumns1147W := Filtered([1..2240],j1147 ->
  mColumnSums1147W[j1147]<>0);;
orbit2401147W := First(a2Orbits1147,o1147 -> Length(o1147)=240);;

zero9751147W := ListWithIdenticalEntries(975,0);;
ColoredColumn1147W := function(j1147)
  if j1147 in coloredTripleIndices1147 then
    return combinedTripleRows1147I[
      Position(coloredTripleIndices1147,j1147)];
  fi;
  return zero9751147W;
end;;
fullColoredColumns1147W := List([1..2240],ColoredColumn1147W);;
coloredActiveColumns1147W := Filtered([1..2240],j1147 ->
  fullColoredColumns1147W[j1147]<>zero9751147W);;
enhancedColumns1147W := List([1..2240],j1147 ->
  Concatenation(List(M1147W,row1147 -> row1147[j1147]),
    fullColoredColumns1147W[j1147]));;
enhancedRank1147W := RankMat(enhancedColumns1147W);;
silentColumns1147W := Filtered([1..2240],j1147 ->
  mColumnSums1147W[j1147]=0 and
  fullColoredColumns1147W[j1147]=zero9751147W);;

checks1147W := rec();;
checks1147W.reconstructed_M_has_shape45_by2240_rank45 :=
  Length(M1147W)=45 and Set(List(M1147W,Length))=[2240] and
  RankMat(M1147W)=45;;
checks1147W.M_active_profile_is_unique240_orbit :=
  Collected(mColumnSums1147W)=[[0,2000],[6,240]] and
  Set(mLiveColumns1147W)=Set(orbit2401147W);;
checks1147W.colored_map_is_active_exactly_on_three432_orbits :=
  Length(coloredActiveColumns1147W)=1296 and
  Set(coloredActiveColumns1147W)=coloredTripleIndices1147;;
checks1147W.M_and_colored_Steinberg_supports_are_disjoint :=
  Intersection(mLiveColumns1147W,coloredActiveColumns1147W)=[];;
checks1147W.enhanced_map_has_exact_rank288_kernel1952 :=
  enhancedRank1147W=288 and 2240-enhancedRank1147W=1952;;
checks1147W.remaining_silent_basis_objects_number704 :=
  Length(silentColumns1147W)=704 and
  240+1296+704=2240;;

failedChecks1147W := Filtered(RecNames(checks1147W),name1147 ->
  not checks1147W.(name1147));;
Assert1147(Concatenation("rank288 weld; failed=",
  String(failedChecks1147W)),IsEmpty(failedChecks1147W));;

Print("rank288_weld status=PASS checks=",Length(RecNames(checks1147W)),
  " M_rank=",RankMat(M1147W),
  " M_active=",Length(mLiveColumns1147W),
  " colored_rank=",combinedC3Rank1147I,
  " colored_active=",Length(coloredActiveColumns1147W),
  " enhanced_shape=1020x2240 rank=",enhancedRank1147W,
  " kernel=",2240-enhancedRank1147W,
  " silent_basis=",Length(silentColumns1147W),"\n");;

irrProbe1147 := Irr(WE61147);;
edgeProbe1147 := Set(List(baseArcs1147I,Set));;
HedgeProbe1147 := Stabilizer(WE61147,edgeProbe1147[1],OnSets);;
chiDirectedProbe1147 := PermutationCharacter(WE61147,Harc1147I);;
chiUnsignedProbe1147 := PermutationCharacter(WE61147,HedgeProbe1147);;
chiOrientedProbe1147 := chiDirectedProbe1147-chiUnsignedProbe1147;;
chiDomainProbe1147 := Sum(List(a2Orbits1147,o1147 ->
  PermutationCharacter(WE61147,
    Stabilizer(WE61147,a2Triples1147[o1147[1]],OnSets))));;
chi45Probe1147 := PermutationCharacter(WE61147,
  Stabilizer(WE61147,cubicSupports1147W[1],OnSets));;
steinProbe1147 := First([1..Length(irrProbe1147)],i1147 ->
  Degree(irrProbe1147[i1147])=81 and
  ScalarProduct(chiOrientedProbe1147,irrProbe1147[i1147])=1);;

# Rows are [Irr-position, degree, domain multiplicity, cubic-image
# multiplicity, enhanced residual multiplicity, directed, unsigned, odd].
representationRows1147 := Filtered(
  List([1..Length(irrProbe1147)],i1147 ->
    [i1147,Degree(irrProbe1147[i1147]),
     ScalarProduct(chiDomainProbe1147,irrProbe1147[i1147]),
     ScalarProduct(chi45Probe1147,irrProbe1147[i1147]),
     ScalarProduct(chiDomainProbe1147,irrProbe1147[i1147])
       -ScalarProduct(chi45Probe1147,irrProbe1147[i1147])
       -3*Bit1147(i1147=steinProbe1147),
     ScalarProduct(chiDirectedProbe1147,irrProbe1147[i1147]),
     ScalarProduct(chiUnsignedProbe1147,irrProbe1147[i1147]),
     ScalarProduct(chiOrientedProbe1147,irrProbe1147[i1147])]),
  row1147 -> row1147{[3..8]}<>[0,0,0,0,0,0]);;
directedDegreeProfile1147 := List(
  Filtered(representationRows1147,row1147 -> row1147[6]<>0),
  row1147 -> [row1147[2],row1147[6]]);;
unsignedDegreeProfile1147 := List(
  Filtered(representationRows1147,row1147 -> row1147[7]<>0),
  row1147 -> [row1147[2],row1147[7]]);;
orientedDegreeProfile1147 := List(
  Filtered(representationRows1147,row1147 -> row1147[8]<>0),
  row1147 -> [row1147[2],row1147[8]]);;
residualDegreeProfile1147 := List(
  Filtered(representationRows1147,row1147 -> row1147[5]<>0),
  row1147 -> [row1147[2],row1147[5]]);;
residualDimension1147 := Sum(residualDegreeProfile1147,
  pair1147 -> pair1147[1]*pair1147[2]);;

# The old equality 1952=7*C(24,2)+20 was dimension arithmetic only.
# Exact character theory gives Lambda^2(24)=24+90+81_plus+81_minus, so seven
# copies cannot equal the residual, which has no 81 constituent at all.
characterTable1147 := CharacterTable(WE61147);;
lambda2Of24Character1147 := AntiSymmetricParts(
  characterTable1147,[irrProbe1147[14]],2)[1];;
lambda2Of24Profile1147 := Filtered(
  List([1..Length(irrProbe1147)],i1147 ->
    [i1147,Degree(irrProbe1147[i1147]),
     ScalarProduct(lambda2Of24Character1147,
       irrProbe1147[i1147])]),
  row1147 -> row1147[3]<>0);;

checks1147R := rec();;
checks1147R.directed_edge_character_decomposition_is_exact :=
  directedDegreeProfile1147=
    [[1,1],[6,2],[15,1],[15,1],[20,3],
     [30,2],[60,1],[64,2],[81,1]];;
checks1147R.unsigned_edge_character_decomposition_is_exact :=
  unsignedDegreeProfile1147=
    [[1,1],[6,1],[15,1],[20,2],[30,1],[60,1],[64,1]];;
checks1147R.reversal_odd_character_decomposition_is_exact :=
  orientedDegreeProfile1147=
    [[6,1],[15,1],[20,1],[30,1],[64,1],[81,1]];;
checks1147R.residual_representation_has_dimension1952 :=
  residualDegreeProfile1147=
    [[1,13],[6,16],[15,5],[15,4],[20,21],
     [24,2],[30,9],[60,4],[64,10],[90,1]]
  and residualDimension1147=1952;;
checks1147R.all_three_81_minus_copies_are_removed :=
  representationRows1147[
    PositionProperty(representationRows1147,row1147 ->
      row1147[1]=steinProbe1147)][3]=3
  and representationRows1147[
    PositionProperty(representationRows1147,row1147 ->
      row1147[1]=steinProbe1147)][5]=0;;
checks1147R.lambda2_24_is_24_plus90_plus81plus_plus81minus :=
  SortedList(List(lambda2Of24Profile1147,row1147 ->
    [row1147[2],row1147[3]]))=
      [[24,1],[81,1],[81,1],[90,1]];;
checks1147R.seven_lambda2_24_plus20_is_not_the_residual_module :=
  Sum(lambda2Of24Profile1147,row1147 ->
    row1147[2]*row1147[3])=276
  and 7*276+20=1952
  and Number(lambda2Of24Profile1147,row1147 ->
    row1147[2]=81)=2
  and ForAll(residualDegreeProfile1147,row1147 ->
    row1147[1]<>81);;

failedChecks1147R := Filtered(RecNames(checks1147R),name1147 ->
  not checks1147R.(name1147));;
Assert1147(Concatenation("representation subtraction; failed=",
  String(failedChecks1147R)),IsEmpty(failedChecks1147R));;

Print("representation_subtraction status=PASS directed=",
  directedDegreeProfile1147,
  " unsigned=",unsignedDegreeProfile1147,
  " odd=",orientedDegreeProfile1147,
  " residual=",residualDegreeProfile1147,
  " lambda2_24=",lambda2Of24Profile1147,"\n");;

# Complex Fourier resolution of the literal C3 color transport.  Once each
# layer is pulled back by c^k to the base 81-space, c acts by the cyclic
# 3-by-3 shift tensor the identity.  These are finite representation channels,
# not physical frequency modes without an additional encoding.
omega1147 := E(3);;
identity31147 := IdentityMat(3);;
colorShift1147 := [[0,0,1],[1,0,0],[0,1,0]];;
fourierProjectors1147 := List([0..2],r1147 ->
  (identity31147
    +omega1147^(-r1147)*colorShift1147
    +omega1147^(-2*r1147)*(colorShift1147^2))/3);;
fourierSectorRanks1147 := List(fourierProjectors1147,
  projector1147 -> 81*RankMat(projector1147));;

checks1147F := rec();;
checks1147F.color_shift_has_order3 :=
  colorShift1147^3=identity31147;;
checks1147F.fourier_projectors_are_orthogonal_idempotents :=
  ForAll(fourierProjectors1147,projector1147 ->
    projector1147^2=projector1147)
  and ForAll(Combinations([1..3],2),pair1147 ->
    fourierProjectors1147[pair1147[1]]
      *fourierProjectors1147[pair1147[2]]=0*identity31147);;
checks1147F.fourier_projectors_sum_to_identity :=
  Sum(fourierProjectors1147)=identity31147;;
checks1147F.fourier_eigenvalues_are_1_omega_omega2 :=
  ForAll([0..2],r1147 ->
    colorShift1147*fourierProjectors1147[r1147+1]
      =omega1147^r1147*fourierProjectors1147[r1147+1]);;
checks1147F.complex_color_image_splits_81_81_81 :=
  combinedC3Rank1147I=243 and
  fourierSectorRanks1147=[81,81,81];;

failedChecks1147F := Filtered(RecNames(checks1147F),name1147 ->
  not checks1147F.(name1147));;
Assert1147(Concatenation("C3 Fourier split; failed=",
  String(failedChecks1147F)),IsEmpty(failedChecks1147F));;

Print("C3_Fourier status=PASS eigenvalues=[1,E(3),E(3)^2]",
  " complex_sector_ranks=",fourierSectorRanks1147,
  " rational_sector_ranks=[81,162]\n");;

# ============================================ integral edge-to-cycle lattice
# Deleting the 26 wedge coordinates incident with vertex 27 is an integral
# coordinate chart on Lambda^2(Aug Z^27): contraction zero recovers each
# deleted coordinate as an integral sum of the retained coordinates.  The
# Smith form below therefore measures the actual image lattice of T, not a
# rationally selected minor.
Print("integral_edge_lattice computing Smith form of 432x325 matrix...\n");;
projectorScale1147Z := 11200;;
primitiveProjectorMultiplier1147Z :=
  projectorScale1147Z/naturalContent1147I;;
edgeSmithAll1147 := ElementaryDivisorsMat(columns3251147I);;
edgeSmith1147 := Filtered(List(edgeSmithAll1147,AbsInt),
  value1147 -> value1147<>0);;
edgeSmithProfile1147 := Collected(edgeSmith1147);;
edgeSmithProduct1147 := Product(edgeSmith1147);;
edgeModularPrimes1147 := [2,3,5,7,11];;
edgeRanksModPrimes1147 := List(edgeModularPrimes1147,p1147 ->
  RankMat(List(columns3251147I,row1147 ->
    List(row1147,x1147 ->
      (x1147 mod p1147)*One(GF(p1147))))));;
colorIntegralBasis1147 := [[1,1,0],[1,-1,1],[1,0,-1]];;
colorIntegralSmith1147 :=
  ElementaryDivisorsMat(colorIntegralBasis1147);;
colorIntegralIndex1147 := AbsInt(DeterminantMat(colorIntegralBasis1147));;
colorRank81SplitIndex1147 := colorIntegralIndex1147^81;;

ModularImage1147 := function(p1147)
  local field1147,one1147,rows1147,basisRows1147,basis1147,
        matrices1147,generator1147,pointPermutation1147,
        transportedRows1147,module1147,factors1147;
  field1147 := GF(p1147);
  one1147 := One(field1147);
  rows1147 := List(columns3511147I,vector1147 ->
    List(vector1147,x1147 -> (x1147 mod p1147)*one1147));
  basisRows1147 := BaseMat(rows1147);
  basis1147 := Basis(VectorSpace(field1147,basisRows1147),
    basisRows1147);
  matrices1147 := [];
  for generator1147 in smallGenerators1147 do
    pointPermutation1147 := Image(hom271147I,generator1147);
    transportedRows1147 := List(basisRows1147,vector1147 ->
      WedgeImage1147I(vector1147,pointPermutation1147));
    Add(matrices1147,List(transportedRows1147,vector1147 ->
      Coefficients(basis1147,vector1147)));
  od;
  module1147 := GModuleByMats(matrices1147,field1147);
  factors1147 := MTX.CompositionFactors(module1147);
  return rec(
    rank := Length(basisRows1147),
    factorDimensions := List(factors1147,factor1147 ->
      factor1147.dimension),
    factorsIrreducible := ForAll(factors1147,factor1147 ->
      factor1147.IsIrreducible)
  );
end;;
mod2Image1147 := ModularImage1147(2);;
mod5Image1147 := ModularImage1147(5);;

characterTable1147Z := CharacterTable("W(E6)");;
ordinary81Positions1147Z := Filtered(
  [1..Length(Irr(characterTable1147Z))],position1147 ->
    Degree(Irr(characterTable1147Z)[position1147])=81);;
BrauerReductionProfile1147 := function(p1147,position1147)
  local brauerTable1147,brauerIrr1147,restricted1147,
        decomposition1147;
  brauerTable1147 := BrauerTable(characterTable1147Z,p1147);
  brauerIrr1147 := Irr(brauerTable1147);
  restricted1147 := RestrictedClassFunction(
    Irr(characterTable1147Z)[position1147],brauerTable1147);
  decomposition1147 := Decomposition(
    List(brauerIrr1147,ValuesOfClassFunction),
    [ValuesOfClassFunction(restricted1147)],"nonnegative")[1];
  return Filtered(
    List([1..Length(decomposition1147)],index1147 ->
      [Degree(brauerIrr1147[index1147]),
       decomposition1147[index1147]]),
    pair1147 -> pair1147[2]<>0);
end;;
ordinary81Brauer2Profiles1147 := List(ordinary81Positions1147Z,
  position1147 -> BrauerReductionProfile1147(2,position1147));;
ordinary81Brauer5Profiles1147 := List(ordinary81Positions1147Z,
  position1147 -> BrauerReductionProfile1147(5,position1147));;

# ==================================== five-primary critical-group bridge
# The Smith calculation leaves an irreducible 23-dimensional quotient at
# p=5.  Build it literally from the W(E6) wedge action, then compare it with
# the 5-primary critical group of W(3,3), using the same W(E6) generators
# transported through W(E6) ~= PGSp(4,3).
field51147P := GF(5);;
one51147P := One(field51147P);;
zero51147P := Zero(field51147P);;

Mod5Mat1147P := function(matrix1147P)
  return List(matrix1147P,row1147P ->
    List(row1147P,value1147P ->
      (value1147P mod 5)*one51147P));
end;;

QuotientAction1147P := function(
    spaceDimension1147P,subspaceCoords1147P,ambientAction1147P)
  local steinitz1147P,fullBasis1147P,offset1147P,
        quotientBasis1147P,rows1147P,vector1147P,image1147P,
        coordinates1147P;
  steinitz1147P := BaseSteinitzVectors(
    IdentityMat(spaceDimension1147P,field51147P),
    subspaceCoords1147P);
  fullBasis1147P := Concatenation(
    steinitz1147P.subspace,steinitz1147P.factorspace);
  offset1147P := Length(steinitz1147P.subspace);
  quotientBasis1147P := steinitz1147P.factorspace;
  rows1147P := [];
  for vector1147P in quotientBasis1147P do
    image1147P := vector1147P*ambientAction1147P;
    coordinates1147P := SolutionMat(fullBasis1147P,image1147P);
    Add(rows1147P,coordinates1147P{
      [offset1147P+1..Length(fullBasis1147P)]});
  od;
  return rows1147P;
end;;

HomBasis1147P := function(leftMatrices1147P,rightMatrices1147P)
  local dimension1147P,equations1147P,left1147P,right1147P,
        i1147P,j1147P,k1147P,row1147P,index1147P;
  dimension1147P := Length(leftMatrices1147P[1]);
  equations1147P := [];
  for index1147P in [1..Length(leftMatrices1147P)] do
    left1147P := leftMatrices1147P[index1147P];
    right1147P := rightMatrices1147P[index1147P];
    for i1147P in [1..dimension1147P] do
      for j1147P in [1..dimension1147P] do
        row1147P := ListWithIdenticalEntries(
          dimension1147P^2,zero51147P);
        for k1147P in [1..dimension1147P] do
          row1147P[(k1147P-1)*dimension1147P+j1147P] :=
            row1147P[(k1147P-1)*dimension1147P+j1147P]
            +left1147P[i1147P][k1147P];
          row1147P[(i1147P-1)*dimension1147P+k1147P] :=
            row1147P[(i1147P-1)*dimension1147P+k1147P]
            -right1147P[k1147P][j1147P];
        od;
        Add(equations1147P,row1147P);
      od;
    od;
  od;
  return NullspaceMat(TransposedMat(equations1147P));
end;;

VectorToSquareMat1147P := function(vector1147P,dimension1147P)
  return List([1..dimension1147P],i1147P ->
    vector1147P{
      [(i1147P-1)*dimension1147P+1..i1147P*dimension1147P]});
end;;

InvertibleHomCount1147P := function(homBasis1147P,dimension1147P)
  local count1147P,vector1147P;
  if Length(homBasis1147P)=0 then return 0; fi;
  if Length(homBasis1147P)>5 then return -1; fi;
  count1147P := 0;
  for vector1147P in VectorSpace(field51147P,homBasis1147P) do
    if vector1147P<>Zero(vector1147P) and
        RankMat(VectorToSquareMat1147P(
          vector1147P,dimension1147P))=dimension1147P then
      count1147P := count1147P+1;
    fi;
  od;
  return count1147P;
end;;

# Integral equations for the rational 81-space give its saturated reduction
# modulo five.  The actual edge image is the invariant 58-submodule.
edgeBaseZ1147P := BaseIntMat(columns3511147I);;
edgeOrthogonalZ1147P :=
  NullspaceIntMat(TransposedMat(edgeBaseZ1147P));;
edgeSaturation51147P := NullspaceMat(TransposedMat(
  Mod5Mat1147P(edgeOrthogonalZ1147P)));;
edgeImage51147P := BaseMat(Mod5Mat1147P(columns3511147I));;
edgeImageCoords51147P := List(edgeImage51147P,row1147P ->
  SolutionMat(edgeSaturation51147P,row1147P));;

FrameQuotientMats1147P := function(generators1147P)
  local matrices1147P,generator1147P,permutation271147P,
        saturationAction1147P;
  matrices1147P := [];
  for generator1147P in generators1147P do
    permutation271147P := Image(hom271147I,generator1147P);
    saturationAction1147P := List(edgeSaturation51147P,row1147P ->
      SolutionMat(edgeSaturation51147P,
        WedgeImage1147I(row1147P,permutation271147P)));
    Add(matrices1147P,QuotientAction1147P(
      81,edgeImageCoords51147P,saturationAction1147P));
  od;
  return matrices1147P;
end;;

FrameSaturationMats1147P := function(generators1147P)
  local matrices1147P,generator1147P,permutation271147P;
  matrices1147P := [];
  for generator1147P in generators1147P do
    permutation271147P := Image(hom271147I,generator1147P);
    Add(matrices1147P,List(edgeSaturation51147P,row1147P ->
      SolutionMat(edgeSaturation51147P,
        WedgeImage1147I(row1147P,permutation271147P))));
  od;
  return matrices1147P;
end;;

# Canonical forty-point symplectic model of W(3,3).
Canon401147P := function(vector1147P)
  local position1147P,inverse1147P;
  vector1147P := List(vector1147P,value1147P -> value1147P mod 3);
  position1147P := PositionProperty(
    vector1147P,value1147P -> value1147P<>0);
  if position1147P=fail then return fail; fi;
  if vector1147P[position1147P]=1 then inverse1147P := 1;
  else inverse1147P := 2; fi;
  return List(vector1147P,value1147P ->
    (inverse1147P*value1147P) mod 3);
end;;

Symplectic401147P := function(left1147P,right1147P)
  return (left1147P[1]*right1147P[3]
    -left1147P[3]*right1147P[1]
    +left1147P[2]*right1147P[4]
    -left1147P[4]*right1147P[2]) mod 3;
end;;

points401147P := Set(Filtered(
  Cartesian([0..2],[0..2],[0..2],[0..2]),
  vector1147P -> vector1147P<>[0,0,0,0]),Canon401147P);;

Transvection401147P := function(vector1147P)
  local images1147P;
  images1147P := List(points401147P,left1147P ->
    Canon401147P(List([1..4],i1147P ->
      left1147P[i1147P]
      +Symplectic401147P(left1147P,vector1147P)
       *vector1147P[i1147P])));
  return PermList(List(images1147P,image1147P ->
    Position(points401147P,image1147P)));
end;;

PSp401147P := Group(List(points401147P,Transvection401147P));;
outer401147P := PermList(List(points401147P,vector1147P ->
  Position(points401147P,Canon401147P(
    [2*vector1147P[1],2*vector1147P[2],
     vector1147P[3],vector1147P[4]]))));;
PGSp401147P := Group(Concatenation(
  SmallGeneratingSet(PSp401147P),[outer401147P]));;
isomorphismWE6PGSp1147P :=
  IsomorphismGroups(WE61147,PGSp401147P);;

adjacency401147P := List([1..40],i1147P ->
  List([1..40],j1147P ->
    Bit1147(i1147P<>j1147P and
      Symplectic401147P(
        points401147P[i1147P],points401147P[j1147P])=0)));;
laplacian401147P := 12*IdentityMat(40)-adjacency401147P;;
reducedLaplacian401147P :=
  laplacian401147P{[1..39]}{[1..39]};;
w33Smith1147P :=
  List(ElementaryDivisorsMat(reducedLaplacian401147P),AbsInt);;
w33SmithProfile1147P := Collected(w33Smith1147P);;

# Degree-zero divisors modulo five, modulo the Laplacian image.
degreeBasis51147P := List([1..39],i1147P ->
  List([1..40],j1147P ->
    (Bit1147(i1147P=j1147P)-Bit1147(j1147P=40))*one51147P));;
laplacianCoords51147P := List(
  Mod5Mat1147P(laplacian401147P),row1147P ->
    SolutionMat(degreeBasis51147P,row1147P));;
laplacianImageCoords51147P := BaseMat(laplacianCoords51147P);;

PointImage51147P := function(vector1147P,permutation1147P)
  local out1147P,i1147P;
  out1147P := ListWithIdenticalEntries(40,zero51147P);
  for i1147P in [1..40] do
    out1147P[i1147P^permutation1147P] :=
      out1147P[i1147P^permutation1147P]+vector1147P[i1147P];
  od;
  return out1147P;
end;;

SandpileQuotientMats1147P := function(generators1147P)
  local matrices1147P,generator1147P,pointPermutation1147P,
        degreeAction1147P;
  matrices1147P := [];
  for generator1147P in generators1147P do
    pointPermutation1147P := Image(
      isomorphismWE6PGSp1147P,generator1147P);
    degreeAction1147P := List(degreeBasis51147P,row1147P ->
      SolutionMat(degreeBasis51147P,
        PointImage51147P(row1147P,pointPermutation1147P)));
    Add(matrices1147P,QuotientAction1147P(
      39,laplacianImageCoords51147P,degreeAction1147P));
  od;
  return matrices1147P;
end;;

literalWE6Generators1147P := smallGenerators1147;;
derivedWE61147P := DerivedSubgroup(WE61147);;
derivedGenerators1147P := SmallGeneratingSet(derivedWE61147P);;
literalGeneratorOrders1147P :=
  List(literalWE6Generators1147P,Order);;
outerSignValues1147P := List(literalWE6Generators1147P,
  generator1147P ->
    2*Bit1147(generator1147P in derivedWE61147P)-1);;

frameFullMats1147P :=
  FrameQuotientMats1147P(literalWE6Generators1147P);;
sandpileFullMats1147P :=
  SandpileQuotientMats1147P(literalWE6Generators1147P);;
frameDerivedMats1147P :=
  FrameQuotientMats1147P(derivedGenerators1147P);;
sandpileDerivedMats1147P :=
  SandpileQuotientMats1147P(derivedGenerators1147P);;
frameSaturationFullMats1147P :=
  FrameSaturationMats1147P(literalWE6Generators1147P);;
frameSaturationDerivedMats1147P :=
  FrameSaturationMats1147P(derivedGenerators1147P);;
frameSignTwistedMats1147P := List(
  [1..Length(frameFullMats1147P)],i1147P ->
    outerSignValues1147P[i1147P]*frameFullMats1147P[i1147P]);;

frameQuotientModule1147P :=
  GModuleByMats(frameFullMats1147P,field51147P);;
sandpileQuotientModule1147P :=
  GModuleByMats(sandpileFullMats1147P,field51147P);;
frameSaturationModule1147P :=
  GModuleByMats(frameSaturationFullMats1147P,field51147P);;
frameDerivedQuotientModule1147P :=
  GModuleByMats(frameDerivedMats1147P,field51147P);;
frameDerivedSaturationModule1147P :=
  GModuleByMats(frameSaturationDerivedMats1147P,field51147P);;
frameQuotientFactors1147P :=
  MTX.CompositionFactors(frameQuotientModule1147P);;
sandpileQuotientFactors1147P :=
  MTX.CompositionFactors(sandpileQuotientModule1147P);;
homUntwisted1147P :=
  HomBasis1147P(frameFullMats1147P,sandpileFullMats1147P);;
homSignTwisted1147P :=
  HomBasis1147P(frameSignTwistedMats1147P,sandpileFullMats1147P);;
homDerived1147P :=
  HomBasis1147P(frameDerivedMats1147P,sandpileDerivedMats1147P);;
invertibleUntwisted1147P :=
  InvertibleHomCount1147P(homUntwisted1147P,23);;
invertibleSignTwisted1147P :=
  InvertibleHomCount1147P(homSignTwisted1147P,23);;
invertibleDerived1147P :=
  InvertibleHomCount1147P(homDerived1147P,23);;
splitHomFull1147P := MTX.BasisModuleHomomorphisms(
  frameQuotientModule1147P,frameSaturationModule1147P);;
splitHomDerived1147P := MTX.BasisModuleHomomorphisms(
  frameDerivedQuotientModule1147P,
  frameDerivedSaturationModule1147P);;
frameSaturationSubmoduleProfile1147P := Collected(List(
  MTX.BasesSubmodules(frameSaturationModule1147P),Length));;
frameDerivedSaturationSubmoduleProfile1147P := Collected(List(
  MTX.BasesSubmodules(frameDerivedSaturationModule1147P),Length));;
edgeImageInvariant1147P := ForAll(
  frameSaturationFullMats1147P,matrix1147P ->
    ForAll(edgeImageCoords51147P,row1147P ->
      SolutionMat(edgeImageCoords51147P,row1147P*matrix1147P)<>fail));;

checks1147Z := rec();;
checks1147Z.edge_lattice_smith_profile_is_exact :=
  edgeSmithProfile1147=
    [[1,15],[2,6],[4,8],[8,29],[40,23]];;
checks1147Z.edge_lattice_saturation_index_is_2pow178_5pow23 :=
  edgeSmithProduct1147=2^178*5^23;;
checks1147Z.primitive_transform_is_40_times_the_rational_projector :=
  naturalContent1147I=280 and
  projectorScale1147Z=11200 and
  primitiveProjectorMultiplier1147Z=40 and
  naturalBaseQ1147I=
    naturalContent1147I*naturalBasePrimitive1147I and
  ApplyQ1147I(naturalBasePrimitive1147I)=
    projectorScale1147Z*naturalBasePrimitive1147I;;
checks1147Z.all_Smith_invariants_divide_the_projector_multiplier :=
  ForAll(edgeSmith1147,invariant1147 ->
    primitiveProjectorMultiplier1147Z mod invariant1147=0);;
checks1147Z.prime7_cancels_in_the_primitive_normalization :=
  Valuation(projectorScale1147Z,7)=1 and
  Valuation(naturalContent1147I,7)=1 and
  Valuation(primitiveProjectorMultiplier1147Z,7)=0 and
  edgeRanksModPrimes1147[Position(edgeModularPrimes1147,7)]=81 and
  edgeSmithProduct1147 mod 7<>0;;
checks1147Z.edge_lattice_bad_primes_are_exactly_2_and_5 :=
  edgeRanksModPrimes1147=[15,81,58,81,81];;
checks1147Z.integral_color_split_has_smith_1_1_3 :=
  DeterminantMat(colorIntegralBasis1147)=3 and
  colorIntegralSmith1147=[1,1,3];;
checks1147Z.rank81_color_split_has_index_3pow81 :=
  colorRank81SplitIndex1147=3^81;;
checks1147Z.mod2_image_is_the_1_plus14_layer :=
  mod2Image1147.rank=15 and
  SortedList(mod2Image1147.factorDimensions)=[1,14] and
  mod2Image1147.factorsIrreducible;;
checks1147Z.mod5_image_is_irreducible_dimension58 :=
  mod5Image1147.rank=58 and
  mod5Image1147.factorDimensions=[58] and
  mod5Image1147.factorsIrreducible;;
checks1147Z.ordinary_81_mod2_has_1_8_3x6_14_40_factors :=
  Length(ordinary81Positions1147Z)=2 and
  ForAll(ordinary81Brauer2Profiles1147,profile1147 ->
    SortedList(profile1147)=
      [[1,1],[6,3],[8,1],[14,1],[40,1]]);;
checks1147Z.ordinary_81_mod5_has_23_plus58_factors :=
  ForAll(ordinary81Brauer5Profiles1147,profile1147 ->
    SortedList(profile1147)=[[23,1],[58,1]]);;
checks1147Z.W33_reduced_laplacian_smith_profile_is_exact :=
  w33SmithProfile1147P=[[1,16],[10,8],[40,1],[160,14]];;
checks1147Z.five_primary_modules_are_both_irreducible_23 :=
  Length(edgeOrthogonalZ1147P)=270 and
  Length(edgeSaturation51147P)=81 and
  Length(edgeImage51147P)=58 and
  Length(laplacianImageCoords51147P)=16 and
  List(frameQuotientFactors1147P,
    factor1147P -> factor1147P.dimension)=[23] and
  List(sandpileQuotientFactors1147P,
    factor1147P -> factor1147P.dimension)=[23] and
  ForAll(Concatenation(
      frameQuotientFactors1147P,sandpileQuotientFactors1147P),
    factor1147P -> factor1147P.IsIrreducible);;
checks1147Z.literal_WE6_generators_act_on_both_23_modules :=
  Size(WE61147)=51840 and
  Size(PGSp401147P)=51840 and
  Size(derivedWE61147P)=25920 and
  Size(PSp401147P)=25920 and
  isomorphismWE6PGSp1147P<>fail and
  Image(isomorphismWE6PGSp1147P,derivedWE61147P)=PSp401147P and
  ForAll(Concatenation(
      frameFullMats1147P,sandpileFullMats1147P),
    matrix1147P ->
      Length(matrix1147P)=23 and RankMat(matrix1147P)=23);;
checks1147Z.five_primary_Hom_dimensions_are_0_1_1 :=
  Length(homUntwisted1147P)=0 and
  Length(homSignTwisted1147P)=1 and
  Length(homDerived1147P)=1;;
checks1147Z.every_nonzero_scalar_intertwiner_is_invertible :=
  invertibleUntwisted1147P=0 and
  invertibleSignTwisted1147P=4 and
  invertibleDerived1147P=4;;
checks1147Z.five_primary_saturation_sequence_is_nonsplit :=
  edgeImageInvariant1147P and
  Length(splitHomFull1147P)=0 and
  Length(splitHomDerived1147P)=0 and
  frameSaturationSubmoduleProfile1147P=[[0,1],[58,1],[81,1]] and
  frameDerivedSaturationSubmoduleProfile1147P=
    [[0,1],[58,1],[81,1]];;

failedChecks1147Z := Filtered(RecNames(checks1147Z),name1147 ->
  not checks1147Z.(name1147));;
Assert1147(Concatenation("integral edge/color lattice; failed=",
  String(failedChecks1147Z)),IsEmpty(failedChecks1147Z));;
Print("integral_edge_lattice Smith_profile=",edgeSmithProfile1147,
  " nonzero=",Length(edgeSmith1147),
  " product=",edgeSmithProduct1147,
  " primes=",edgeModularPrimes1147,
  " ranks=",edgeRanksModPrimes1147,
  " color_smith=",colorIntegralSmith1147,
  " rank81_color_index=",colorRank81SplitIndex1147,
  " mod2_factors=",mod2Image1147.factorDimensions,
  " mod5_factors=",mod5Image1147.factorDimensions,"\n");;
Print("five_primary_critical_group_bridge W33_Smith=",
  w33SmithProfile1147P,
  " quotient_dimensions=[23,23]",
  " Hom_dimensions=[",Length(homUntwisted1147P),",",
  Length(homSignTwisted1147P),",",Length(homDerived1147P),"]",
  " invertible_nonzero=[",invertibleUntwisted1147P,",",
  invertibleSignTwisted1147P,",",invertibleDerived1147P,"]\n");;
Print("five_primary_saturated_extension split_Hom_dimensions=[",
  Length(splitHomFull1147P),",",Length(splitHomDerived1147P),"]",
  " submodule_profiles=[",frameSaturationSubmoduleProfile1147P,",",
  frameDerivedSaturationSubmoduleProfile1147P,"]\n");;

# =========================================== deterministic JSON certificate
allCheckCount1147 :=
  Length(RecNames(checks1147))
  +Length(RecNames(checks1147I))
  +Length(RecNames(checks1147C3))
  +Length(RecNames(checks1147W))
  +Length(RecNames(checks1147R))
  +Length(RecNames(checks1147F))
  +Length(RecNames(checks1147Z));;
allFailedChecks1147 := Concatenation(
  failedChecks1147,
  failedChecks1147I,
  failedChecks1147C3,
  failedChecks1147W,
  failedChecks1147R,
  failedChecks1147F,
  failedChecks1147Z);;

stream1147 := OutputTextFile(OUT1147,false);;
SetPrintFormattingStatus(stream1147,false);;
Emit1147 := function(arg)
  local item1147;
  for item1147 in arg do
    WriteAll(stream1147,String(item1147));
  od;
end;;

Emit1147("{\n");
Emit1147("  \"schema\":\"w33.pass1147.schlaefli_steinberg_fourier_bridge.gap.v1\",\n");
Emit1147("  \"status\":\"PASS\",\n");
Emit1147("  \"producer\":{\"system\":\"GAP\",\"version\":\"",
  GAPInfo.Version,"\",\"check_count\":",allCheckCount1147,
  ",\"failed_checks\":",String(allFailedChecks1147),"},\n");
Emit1147("  \"spectral_guard\":\"{shifted-adjacency:corrected} The degree multiplicities below are W(E6) character data, not the retracted shifted-adjacency packet.\",\n");
Emit1147("  \"directed_schlaefli\":{\n");
Emit1147("    \"object\":\"three colored copies of the directed-edge carrier of SRG(27,16,10,8)\",\n");
Emit1147("    \"shell_patterns\":",String(shellPatterns1147),",\n");
Emit1147("    \"shell_sizes\":",String(List(shells1147,Length)),",\n");
Emit1147("    \"color_fiber_sizes\":",String(List(colorFibers1147,Length)),",\n");
Emit1147("    \"a2_orbit_sizes\":",String(List(a2Orbits1147,Length)),",\n");
Emit1147("    \"srg_parameters\":[27,16,10,8],\n");
Emit1147("    \"directed_edge_count\":",Length(baseArcs1147I),",\n");
Emit1147("    \"directed_edge_stabilizer\":{\"order\":",
  Size(Harc1147I),",\"structure\":\"",
  StructureDescription(Harc1147I),"\"},\n");
Emit1147("    \"objectwise_bijection_verified\":true\n");
Emit1147("  },\n");
Emit1147("  \"steinberg_transform\":{\n");
Emit1147("    \"domain\":\"directed Schlaefli edges\",\n");
Emit1147("    \"codomain\":\"Lambda^2(Aug(Q^27))\",\n");
Emit1147("    \"reflection_class_size\":",Length(reflectionClass1147I),",\n");
Emit1147("    \"class_sum_projector\":\"(K-24)(K-18)(K-12)(K-9)\",\n");
Emit1147("    \"selected_K_eigenvalue\":4,\n");
Emit1147("    \"projector_scale\":11200,\n");
Emit1147("    \"matrix_shape\":[325,432],\n");
Emit1147("    \"rank\":",intertwinerRank1147I,",\n");
Emit1147("    \"rank_mod_1000003\":",intertwinerRankMod1147I,",\n");
Emit1147("    \"reversal_odd\":",BoolString1147(reverseOdd1147I),",\n");
Emit1147("    \"vector_norm_squared\":",primitiveNorm21147I,",\n");
Emit1147("    \"gram_identity\":\"G^2=3200G\",\n");
Emit1147("    \"oriented_off_diagonal_profile\":",
  String(offDiagonalGramProfile1147I),",\n");
Emit1147("    \"projective_lines\":216,\n");
Emit1147("    \"projective_dimension\":81,\n");
Emit1147("    \"absolute_normalized_inner_products\":[\"0\",\"1/15\",\"1/5\"],\n");
Emit1147("    \"projective_valencies\":[120,60,35],\n");
Emit1147("    \"absolute_angle_relations_form_association_scheme\":false\n");
Emit1147("  },\n");
Emit1147("  \"a2_color_torsor\":{\n");
Emit1147("    \"colors\":3,\n");
Emit1147("    \"coxeter_order\":",Order(coxeter1147),",\n");
Emit1147("    \"color_permutation\":",String(colorPermutation1147),",\n");
Emit1147("    \"extended_group_order\":",Size(extendedGroup1147),",\n");
Emit1147("    \"structure\":\"W(E6) x C3\",\n");
Emit1147("    \"combined_matrix_shape\":[975,1296],\n");
Emit1147("    \"combined_rank\":",combinedC3Rank1147I,",\n");
Emit1147("    \"rational_sector_ranks\":[81,162],\n");
Emit1147("    \"complex_sector_ranks\":",String(fourierSectorRanks1147),",\n");
Emit1147("    \"choice_boundary\":\"the unbased C3 torsor is intrinsic; labeling Fourier modes chooses an origin and generator\"\n");
Emit1147("  },\n");
Emit1147("  \"enhanced_map\":{\n");
Emit1147("    \"source_dimension\":2240,\n");
Emit1147("    \"target_dimension\":1020,\n");
Emit1147("    \"matrix_shape\":[1020,2240],\n");
Emit1147("    \"cubic_rank\":45,\n");
Emit1147("    \"three_color_rank\":",combinedC3Rank1147I,",\n");
Emit1147("    \"rank\":",enhancedRank1147W,",\n");
Emit1147("    \"kernel_dimension\":",2240-enhancedRank1147W,",\n");
Emit1147("    \"active_source_profile\":{\"cubic\":",
  Length(mLiveColumns1147W),",\"schlaefli\":",
  Length(coloredActiveColumns1147W),",\"silent\":",
  Length(silentColumns1147W),"},\n");
Emit1147("    \"supports_disjoint\":true\n");
Emit1147("  },\n");
Emit1147("  \"residual_representation\":{\n");
Emit1147("    \"dimension\":",residualDimension1147,",\n");
Emit1147("    \"degree_multiplicities\":",
  String(residualDegreeProfile1147),",\n");
Emit1147("    \"directed_edge_degree_multiplicities\":",
  String(directedDegreeProfile1147),",\n");
Emit1147("    \"unsigned_edge_degree_multiplicities\":",
  String(unsignedDegreeProfile1147),",\n");
Emit1147("    \"reversal_odd_degree_multiplicities\":",
  String(orientedDegreeProfile1147),",\n");
Emit1147("    \"lambda2_of_24_degree_multiplicities\":",
  String(List(lambda2Of24Profile1147,row1147 ->
    [row1147[2],row1147[3]])),",\n");
Emit1147("    \"removed_constituents\":\"three copies of 81_minus\",\n");
Emit1147("    \"supersedes\":\"1952=7*dim(Lambda^2(24))+20 dimension mnemonic\"\n");
Emit1147("  },\n");
Emit1147("  \"integral_edge_lattice\":{\n");
Emit1147("    \"matrix_shape\":[432,325],\n");
Emit1147("    \"rational_rank\":81,\n");
Emit1147("    \"integral_chart\":\"delete the 26 vertex-27 wedge coordinates and recover them integrally from contraction zero\",\n");
Emit1147("    \"structural_normalization\":{\"natural_Q_edge_content\":",
  naturalContent1147I,",\"projector_scale\":",projectorScale1147Z,
  ",\"primitive_projector_multiplier\":",
  primitiveProjectorMultiplier1147Z,
  ",\"identity\":\"T=Q/280=40*P_4\",\"all_smith_invariants_divide_40\":true,\"prime7_cancellation\":\"7 divides both Q's eigenvalue scale 11200 and every Schlaefli-edge Q-image content 280; it is absent from the primitive multiplier 40, the Smith product, and the rank drop\"},\n");
Emit1147("    \"smith_diagonal_profile\":{\"1\":15,\"2\":6,\"4\":8,\"8\":29,\"40\":23},\n");
Emit1147("    \"saturation_quotient\":\"(Z/2)^6 + (Z/4)^8 + (Z/8)^29 + (Z/40)^23\",\n");
Emit1147("    \"primary_quotient\":{\"2\":\"(Z/2)^6 + (Z/4)^8 + (Z/8)^52\",\"5\":\"(Z/5)^23\"},\n");
Emit1147("    \"saturation_index_factorization\":{\"2\":178,\"5\":23},\n");
Emit1147("    \"saturation_index_decimal\":\"",
  String(edgeSmithProduct1147),"\",\n");
Emit1147("    \"rank_mod_prime\":{\"2\":15,\"3\":81,\"5\":58,\"7\":81,\"11\":81},\n");
Emit1147("    \"bad_primes\":[2,5],\n");
Emit1147("    \"modular_image_composition\":{\n");
Emit1147("      \"2\":{\"rank\":15,\"irreducible_factor_dimensions\":[1,14],\"ambient_81_Brauer_profile\":{\"1\":1,\"6\":3,\"8\":1,\"14\":1,\"40\":1}},\n");
Emit1147("      \"5\":{\"rank\":58,\"irreducible_factor_dimensions\":[58],\"ambient_81_Brauer_profile\":{\"23\":1,\"58\":1}}\n");
Emit1147("    },\n");
Emit1147("    \"integral_color_fourier_split\":{\n");
Emit1147("      \"basis_matrix\":",String(colorIntegralBasis1147),",\n");
Emit1147("      \"smith_diagonal\":",String(colorIntegralSmith1147),",\n");
Emit1147("      \"one_color_index\":3,\n");
Emit1147("      \"rank81_index_factorization\":{\"3\":81},\n");
Emit1147("      \"rank81_index_decimal\":\"",
  String(colorRank81SplitIndex1147),"\"\n");
Emit1147("    },\n");
Emit1147("    \"five_primary_critical_group_bridge\":{\n");
Emit1147("      \"W33_reduced_laplacian_smith_profile\":{\"1\":16,\"10\":8,\"40\":1,\"160\":14},\n");
Emit1147("      \"literal_action\":{\"group\":\"W(E6)=PGSp(4,3)\",\"order\":51840,\"derived_group\":\"PSp(4,3)\",\"derived_order\":25920,\"generator_orders\":",
  String(literalGeneratorOrders1147P),",\"outer_sign_values\":",
  String(outerSignValues1147P),"},\n");
Emit1147("      \"frame_saturation_quotient\":{\"prime\":5,\"dimension\":23,\"module\":\"irreducible 23-dimensional F5 W(E6)-module\"},\n");
Emit1147("      \"W33_sandpile_primary\":{\"prime\":5,\"group\":\"(Z/5)^23\",\"dimension\":23,\"module\":\"irreducible 23-dimensional F5 W(E6)-module\"},\n");
Emit1147("      \"Hom_dimensions\":{\"untwisted_W(E6)\":",
  Length(homUntwisted1147P),",\"outer_sign_twisted_W(E6)\":",
  Length(homSignTwisted1147P),",\"restricted_PSp(4,3)\":",
  Length(homDerived1147P),"},\n");
Emit1147("      \"nonzero_scalar_intertwiners\":{\"untwisted\":",
  invertibleUntwisted1147P,",\"outer_sign_twisted\":",
  invertibleSignTwisted1147P,",\"restricted_PSp(4,3)\":",
  invertibleDerived1147P,"},\n");
Emit1147("      \"all_nonzero_scalar_intertwiners_invertible\":true,\n");
Emit1147("      \"module_isomorphism\":\"(saturation quotient at 5) tensor outer_sign ~= K(W33)_5\",\n");
Emit1147("      \"saturated_frame_exact_sequence\":{\"sequence\":\"0 -> irreducible_58 -> saturated_frame_mod5_81 -> K(W33)_5 tensor outer_sign -> 0\",\"splits_over_W(E6)\":false,\"splits_over_PSp(4,3)\":false,\"Hom_quotient_to_saturation\":{\"W(E6)\":",
  Length(splitHomFull1147P),",\"PSp(4,3)\":",
  Length(splitHomDerived1147P),
  "},\"submodule_dimension_profiles\":{\"W(E6)\":{\"0\":1,\"58\":1,\"81\":1},\"PSp(4,3)\":{\"0\":1,\"58\":1,\"81\":1}},\"structure\":\"the image 58 is the unique proper nonzero submodule; the saturated reduction is a nonsplit length-two module\",\"extension_scope\":\"this certifies that the displayed extension class is nonzero; it does not compute the dimension of the full Ext^1 space\"},\n");
Emit1147("      \"uniqueness\":\"unique up to F5^x; exactly four nonzero scalar isomorphisms\",\n");
Emit1147("      \"scope\":\"module isomorphism class is intrinsic; a displayed matrix depends on the chosen W(E6)~=PGSp(4,3) isomorphism and quotient bases; no canonical integral lift or physical channel is asserted\"\n");
Emit1147("    },\n");
Emit1147("    \"arithmetic_factorization\":\"the within-color Schlaefli-Steinberg lattice has bad primes 2 and 5; integral separation into trivial and augmentation color sectors contributes prime 3, yielding the full set 2,3,5\"\n");
Emit1147("  },\n");
Emit1147("  \"scope\":\"exact finite E8/W(E6) geometry and representation theory; no identification with generations, masses, Yukawa couplings, polarizations, or measured hardware channels\"\n");
Emit1147("}\n");
CloseStream(stream1147);;

QUIT;
