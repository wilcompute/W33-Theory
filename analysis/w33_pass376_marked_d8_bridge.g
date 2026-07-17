# Pass 376: the phase-compatible D8 and the geometric D8=N_W(K)/K agree as
# marked V4:C2 extensions.  The bridge has exactly four marked choices, so it
# identifies the central C2 line but does not manufacture a canonical map of
# scalar sheets to a geometric state space.  All finite computations are GAP.

OUT376 := "data/w33_pass376_marked_d8_bridge.json";;

Assert376 := function(label, condition)
  if not condition then
    Error(Concatenation("Pass376 assertion failed: ",label));
  fi;
end;;

Bool376 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

Canonical376 := function(vector)
  local position;
  position := PositionProperty(vector, entry -> not IsZero(entry));
  return Inverse(vector[position]) * vector;
end;;

Symplectic376 := function(left, right)
  return left[1]*right[3] - left[3]*right[1]
       + left[2]*right[4] - left[4]*right[2];
end;;

TranslateLift376 := function(liftList, translation)
  return PermList(List(liftList, lift -> Position(liftList,
    [lift[1]*translation[1], lift[2]*translation[2]])));
end;;

Chi376 := function(lift)
  return lift[1] * lift[2];
end;;

TransvectionPermutation376 := function(pointList, direction)
  return PermList(List(pointList, point -> Position(pointList,
    Canonical376(point + Symplectic376(point,direction)*direction))));
end;;

OnEdgeSet376 := function(edgeSet, groupElement)
  return Set(List(edgeSet, edge ->
    Set(List(edge, point -> point^groupElement))));
end;;

OrbitSizes376 := function(group, degree)
  return SortedList(List(OrbitsDomain(group,[1..degree],OnPoints),Length));
end;;

# ---------------------------------------------------------------------------
# The phase-normalizer D8 and its marked scalar deck V4.
# ---------------------------------------------------------------------------

field376 := GF(3);;
zero376 := Zero(field376);;
one376 := One(field376);;
minusOne376 := -one376;;

lifts376 := [
  [one376,one376],
  [minusOne376,minusOne376],
  [minusOne376,one376],
  [one376,minusOne376]
];;
xFlip376 := TranslateLift376(lifts376,[minusOne376,one376]);;
zFlip376 := TranslateLift376(lifts376,[one376,minusOne376]);;
phaseDeck376 := Group(xFlip376,zFlip376);;
phasePlus376 := Filtered([1..4],position ->
  Chi376(lifts376[position])=one376);;
phaseMinus376 := Filtered([1..4],position ->
  Chi376(lifts376[position])=minusOne376);;
phasePartition376 := Set([phasePlus376,phaseMinus376]);;
phaseNormalizer376 := Stabilizer(SymmetricGroup(4),phasePartition376,
  OnSetsSets);;
phaseKernel376 := Group(xFlip376*zFlip376);;

# ---------------------------------------------------------------------------
# The visible-pair V4 and its normalizer in W(E6)=PGSp(4,3).
# ---------------------------------------------------------------------------

rawVectors376 := Tuples([zero376,one376,minusOne376],4);;
points376 := Set(List(Filtered(rawVectors376, vector ->
  vector<>[zero376,zero376,zero376,zero376]),Canonical376));;

edges376 := [];;
for left376 in [1..39] do
  for right376 in [left376+1..40] do
    if IsZero(Symplectic376(points376[left376],points376[right376])) then
      Add(edges376,[left376,right376]);
    fi;
  od;
od;

coefficients376 := Filtered(Tuples([zero376,one376,minusOne376],2),
  pair -> pair<>[zero376,zero376]);;
lines376 := [];;
for edge376 in edges376 do
  line376 := Set(List(coefficients376,pair -> Canonical376(
    pair[1]*points376[edge376[1]] + pair[2]*points376[edge376[2]])));
  AddSet(lines376,List(line376,point -> Position(points376,point)));
od;

quadrangles376 := [];;
for vertexA376 in [1..39] do
  for vertexB376 in [vertexA376+1..40] do
    if [vertexA376,vertexB376] in edges376 then
      continue;
    fi;
    common376 := Filtered([1..40],vertex ->
      Set([vertexA376,vertex]) in edges376 and
      Set([vertexB376,vertex]) in edges376);
    for opposite376 in Combinations(common376,2) do
      vertexC376 := opposite376[1];;
      vertexD376 := opposite376[2];;
      AddSet(quadrangles376,Set([
        Set([vertexA376,vertexC376]),
        Set([vertexC376,vertexB376]),
        Set([vertexB376,vertexD376]),
        Set([vertexD376,vertexA376])
      ]));
    od;
  od;
od;

pointGenerators376 := List(points376,direction ->
  TransvectionPermutation376(points376,direction));;
fullOuter376 := PermList(List(points376,point -> Position(points376,
  Canonical376([minusOne376*point[1],minusOne376*point[2],
                point[3],point[4]]))));;
fullGroup376 := Group(Concatenation(pointGenerators376,[fullOuter376]));;

seedQuadrangle376 := quadrangles376[1];;
seedEdge376 := seedQuadrangle376[1];;
seedPoint376 := seedEdge376[1];;
seedLine376 := First(lines376,line ->
  ForAll(seedEdge376,point -> point in line));;
fullFlagStabilizer376 := Stabilizer(
  Stabilizer(fullGroup376,seedPoint376,OnPoints),seedLine376,OnSets);;
fullQuadrangleStabilizer376 := Stabilizer(
  fullGroup376,seedQuadrangle376,OnEdgeSet376);;
visiblePairStabilizer376 := Intersection(fullFlagStabilizer376,
  fullQuadrangleStabilizer376);;
geometricNormalizer376 := Normalizer(fullGroup376,visiblePairStabilizer376);;
geometricQuotientMap376 := NaturalHomomorphismByNormalSubgroup(
  geometricNormalizer376,visiblePairStabilizer376);;
geometricD8376 := Image(geometricQuotientMap376);;

# C_N(K)/K is a canonical V4 inside N_W(K)/K.  It is the geometric analogue
# of the phase deck, not an asserted action on the four scalar sheet labels.
centralizerOfK376 := Centralizer(geometricNormalizer376,
  visiblePairStabilizer376);;
geometricDeck376 := Image(geometricQuotientMap376,centralizerOfK376);;

# ---------------------------------------------------------------------------
# Compare marked extensions and construct every allowed ambiguity.
# ---------------------------------------------------------------------------

phaseDeckElements376 := Elements(phaseDeck376);;
phaseConjugationGenerators376 := List(GeneratorsOfGroup(phaseNormalizer376),
  groupElement -> PermList(List(phaseDeckElements376, deckElement ->
    Position(phaseDeckElements376,deckElement^groupElement))));;
phaseConjugation376 := Group(phaseConjugationGenerators376);;

geometricDeckElements376 := Elements(geometricDeck376);;
geometricConjugationGenerators376 := List(GeneratorsOfGroup(geometricD8376),
  groupElement -> PermList(List(geometricDeckElements376, deckElement ->
    Position(geometricDeckElements376,deckElement^groupElement))));;
geometricConjugation376 := Group(geometricConjugationGenerators376);;

rawIsomorphism376 := IsomorphismGroups(phaseNormalizer376,geometricD8376);;
phaseAutomorphisms376 := AutomorphismGroup(phaseNormalizer376);;
markedAutomorphismGroup376 := Stabilizer(phaseAutomorphisms376,phaseDeck376,
  function(subgroup,automorphism)
    return Image(automorphism,subgroup);
  end);;
markedAutomorphisms376 := Filtered(Elements(phaseAutomorphisms376),
  automorphism -> Image(rawIsomorphism376,
    Image(automorphism,phaseDeck376))=geometricDeck376);;
markedAlpha376 := markedAutomorphisms376[1];;
markedIsomorphism376 := GroupHomomorphismByImages(phaseNormalizer376,
  geometricD8376,GeneratorsOfGroup(phaseNormalizer376),
  List(GeneratorsOfGroup(phaseNormalizer376),groupElement ->
    Image(rawIsomorphism376,Image(markedAlpha376,groupElement))));;

checks376 := rec();;
checks376.phase_lifts_are_four_distinct_scalar_pairs :=
  Length(lifts376)=4 and Length(Set(lifts376))=4;
checks376.phase_character_partition_is_two_plus_two :=
  phasePlus376=[1,2] and phaseMinus376=[3,4];
checks376.phase_deck_is_regular_v4 :=
  Size(phaseDeck376)=4 and
  StructureDescription(phaseDeck376)="C2 x C2" and
  IsTransitive(phaseDeck376,[1..4]) and
  Size(Stabilizer(phaseDeck376,1))=1;
checks376.phase_normalizer_is_d8 :=
  Size(phaseNormalizer376)=8 and
  StructureDescription(phaseNormalizer376)="D8";
checks376.phase_kernel_is_the_d8_center :=
  phaseKernel376=Center(phaseNormalizer376) and Size(phaseKernel376)=2;
checks376.phase_marked_extension_is_v4_by_c2 :=
  IsNormal(phaseNormalizer376,phaseDeck376) and
  Size(FactorGroup(phaseNormalizer376,phaseDeck376))=2;
checks376.w33_counts_are_40_240_40_1620 :=
  [Length(points376),Length(edges376),Length(lines376),Length(quadrangles376)]
  =[40,240,40,1620];
checks376.full_group_is_weyl_e6_order_51840 := Size(fullGroup376)=51840;
checks376.visible_pair_stabilizer_is_v4 :=
  Size(visiblePairStabilizer376)=4 and
  StructureDescription(visiblePairStabilizer376)="C2 x C2";
checks376.geometric_normalizer_has_order_32 :=
  Size(geometricNormalizer376)=32;
checks376.geometric_quotient_is_d8 :=
  Size(geometricD8376)=8 and StructureDescription(geometricD8376)="D8";
checks376.geometric_deck_is_canonical_centralizer_quotient_v4 :=
  Size(centralizerOfK376)=16 and Size(geometricDeck376)=4 and
  StructureDescription(geometricDeck376)="C2 x C2";
checks376.geometric_marked_extension_is_v4_by_c2 :=
  IsNormal(geometricD8376,geometricDeck376) and
  Size(FactorGroup(geometricD8376,geometricDeck376))=2;
checks376.geometric_center_is_in_the_geometric_deck :=
  Size(Center(geometricD8376))=2 and
  IsSubgroup(geometricDeck376,Center(geometricD8376));
checks376.phase_deck_conjugation_has_one_one_two_profile :=
  Size(phaseConjugation376)=2 and
  OrbitSizes376(phaseConjugation376,Length(phaseDeckElements376))=[1,1,2];
checks376.geometric_deck_conjugation_has_one_one_two_profile :=
  Size(geometricConjugation376)=2 and
  OrbitSizes376(geometricConjugation376,Length(geometricDeckElements376))=
  [1,1,2];
checks376.marked_isomorphism_maps_deck_to_deck :=
  Image(markedIsomorphism376,phaseDeck376)=geometricDeck376;
checks376.marked_isomorphism_maps_center_to_center :=
  Image(markedIsomorphism376,Center(phaseNormalizer376))=
  Center(geometricD8376);
checks376.exactly_four_marked_isomorphism_choices :=
  Length(markedAutomorphisms376)=4;
checks376.residual_marked_ambiguity_is_v4 :=
  Size(markedAutomorphismGroup376)=4 and
  StructureDescription(markedAutomorphismGroup376)="C2 x C2";

checkNames376 := RecNames(checks376);;
failedCheckNames376 := Filtered(checkNames376,name -> not checks376.(name));;
Assert376(Concatenation("all checks; failed=",String(failedCheckNames376)),
  IsEmpty(failedCheckNames376));;

stream376 := OutputTextFile(OUT376,false);;
SetPrintFormattingStatus(stream376,false);;
WriteAll(stream376,"{\n");;
WriteAll(stream376,"  \"schema\": \"w33.pass376.marked_d8_bridge.gap.v1\",\n");;
WriteAll(stream376,"  \"status\": \"PASS\",\n");;
WriteAll(stream376,"  \"theorem\": \"Marked D8 Bridge and Fourfold Ambiguity Theorem\",\n");;
WriteAll(stream376,"  \"prior_boundary\": \"Pass 375 proved that the phase D8 and N_W(E6)(K)/K are isomorphic outputs on different objects and claimed no intertwiner. Pass 376 compares the marked group extensions only; it does not identify scalar sheets with geometric states.\",\n");;
WriteAll(stream376,"  \"phase_side\": {\"group\":\"D8\",\"deck\":\"V4=(F3*)^2\",\"phase_kernel\":\"ker chi = Z(D8)\",\"quotient\":\"C2\",\"deck_conjugation_orbits\":[1,1,2]},\n");;
WriteAll(stream376,"  \"geometric_side\": {\"group\":\"N_W(E6)(K)/K\",\"group_order\":8,\"deck\":\"C_N(K)/K\",\"deck_order\":4,\"normalizer_order\":32,\"quotient\":\"C2\",\"deck_conjugation_orbits\":[1,1,2]},\n");;
WriteAll(stream376,"  \"marked_bridge\": {\"exists\":true,\"maps_phase_deck_to_geometric_deck\":true,\"maps_center_to_center\":true,\"marked_isomorphism_count\":4,\"ambiguity_group\":\"C2 x C2\"},\n");;
WriteAll(stream376,"  \"search_signature\": \"32/8/4/2/1/1/2/4\",\n");;
WriteAll(stream376,"  \"scope\": \"The common marked V4:C2 extension and its central C2 line are exact. Four marked group isomorphisms remain, so this certificate supplies no preferred scalar-sheet-to-state map, no physical phase identification, and no regular W(E6) action.\",\n");;
WriteAll(stream376,Concatenation("  \"check_count\":",String(Length(checkNames376)),",\n"));;
WriteAll(stream376,"  \"checks\": {\n");;
for checkPosition376 in [1..Length(checkNames376)] do
  checkName376 := checkNames376[checkPosition376];;
  WriteAll(stream376,Concatenation("    \"",checkName376,"\": ",
    Bool376(checks376.(checkName376))));
  if checkPosition376<Length(checkNames376) then WriteAll(stream376,","); fi;
  WriteAll(stream376,"\n");;
od;
WriteAll(stream376,"  }\n");;
WriteAll(stream376,"}\n");;
CloseStream(stream376);;

Print("Pass376 status=PASS checks=",Length(checkNames376),
  " marked_D8_bridge=4 ambiguity=C2xC2 output=",OUT376,"\n");;
QUIT;
