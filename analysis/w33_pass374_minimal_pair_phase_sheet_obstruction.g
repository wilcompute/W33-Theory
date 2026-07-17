# Pass 374: construct the natural signed-chain action on all 51,840 nonzero
# minimal X/Z logical-vector pairings.  The earlier projective theorem gives one
# visible flag-quadrangle orbit of size 12,960, while BT571/BT637/BT644 own the
# four scalar lifts and their phase/deck characters.  The previously
# unclassified natural action is not a W(E6)-torsor: both PSp(4,3) and
# PGSp(4,3)=W(E6) preserve four separate sheets.

OUT374 := "data/w33_pass374_minimal_pair_phase_sheet_obstruction.json";;

Field369 := GF(3);;
Zero369 := Zero(Field369);;
One369 := One(Field369);;

Canonical369 := function(vector)
  local position;
  position := PositionProperty(vector,entry -> entry<>Zero369);
  return Inverse(vector[position])*vector;
end;;

Symplectic369 := function(left,right)
  return left[1]*right[3]-left[3]*right[1]
       + left[2]*right[4]-left[4]*right[2];
end;;

Bool369 := function(value)
  if value then return "true"; fi;
  return "false";
end;;

Assert369 := function(label,condition)
  if not condition then
    Error(Concatenation("Pass374 assertion failed: ",label));
  fi;
end;;

raw369 := Tuples([Zero369,One369,2*One369],4);;
points369 := Set(List(Filtered(raw369,vector ->
  vector<>[Zero369,Zero369,Zero369,Zero369]),Canonical369));;

edges369 := [];;
for left369 in [1..40] do
  for right369 in [left369+1..40] do
    if Symplectic369(points369[left369],points369[right369])=Zero369 then
      Add(edges369,[left369,right369]);
    fi;
  od;
od;

coefficients369 := Filtered(Tuples([Zero369,One369,2*One369],2),
  pair -> pair<>[Zero369,Zero369]);;
lines369 := [];;
for edge369 in edges369 do
  line369 := Set(List(coefficients369,pair -> Canonical369(
    pair[1]*points369[edge369[1]]+pair[2]*points369[edge369[2]])));
  AddSet(lines369,List(line369,point -> Position(points369,point)));
od;
triangles369 := Set(Concatenation(List(lines369,line ->
  Combinations(line,3))));;

# Exact CSS check matrices, used only to construct the already-owned minimal
# logical vector families over GF(3).
hx369 := List([1..40],unused -> List([1..240],unused -> Zero369));;
for position369 in [1..240] do
  hx369[edges369[position369][1]][position369] := -One369;
  hx369[edges369[position369][2]][position369] := One369;
od;
hz369 := [];;
for triangle369 in triangles369 do
  row369 := List([1..240],unused -> Zero369);
  row369[Position(edges369,[triangle369[1],triangle369[2]])] := One369;
  row369[Position(edges369,[triangle369[1],triangle369[3]])] := -One369;
  row369[Position(edges369,[triangle369[2],triangle369[3]])] := One369;
  Add(hz369,row369);
od;
hxBasis369 := BaseMat(hx369);;
hzBasis369 := BaseMat(hz369);;
hxSpace369 := VectorSpace(Field369,hxBasis369);;
hzSpace369 := VectorSpace(Field369,hzBasis369);;

xVectors369 := [];;
for line369 in lines369 do
  for center369 in line369 do
    support369 := List(Filtered(line369,point -> point<>center369),point ->
      Position(edges369,Set([center369,point])));
    for values369 in Tuples([One369,-One369],3) do
      row369 := List([1..240],unused -> Zero369);
      for position369 in [1..3] do
        row369[support369[position369]] := values369[position369];
      od;
      if ForAll(Flat(hz369*TransposedMat([row369])),IsZero) and
         not row369 in hxSpace369 then
        AddSet(xVectors369,row369);
      fi;
    od;
  od;
od;

zVectors369 := [];;
zSupports369 := [];;
for vertexA369 in [1..39] do
  for vertexB369 in [vertexA369+1..40] do
    if [vertexA369,vertexB369] in edges369 then
      continue;
    fi;
    common369 := Filtered([1..40],vertex ->
      Set([vertexA369,vertex]) in edges369 and
      Set([vertexB369,vertex]) in edges369);
    for opposite369 in Combinations(common369,2) do
      vertexC369 := opposite369[1];
      vertexD369 := opposite369[2];
      row369 := List([1..240],unused -> Zero369);
      for oriented369 in [[vertexA369,vertexC369],
                           [vertexC369,vertexB369],
                           [vertexB369,vertexD369],
                           [vertexD369,vertexA369]] do
        edge369 := Set(oriented369);
        position369 := Position(edges369,edge369);
        if oriented369=edge369 then
          row369[position369] := row369[position369]+One369;
        else
          row369[position369] := row369[position369]-One369;
        fi;
      od;
      AddSet(zSupports369,PositionsProperty(row369,entry -> entry<>Zero369));
      if ForAll(Flat(hx369*TransposedMat([row369])),IsZero) and
         not row369 in hzSpace369 then
        AddSet(zVectors369,row369);
        AddSet(zVectors369,-row369);
      fi;
    od;
  od;
od;

TransvectionPermutation369 := function(direction)
  return PermList(List(points369,point -> Position(points369,
    Canonical369(point+Symplectic369(point,direction)*direction))));
end;;

pointGenerators369 := List(points369,TransvectionPermutation369);;
innerPointGroup369 := Group(pointGenerators369);;
outerPoint369 := PermList(List(points369,point -> Position(points369,
  Canonical369([2*point[1],2*point[2],point[3],point[4]]))));;
fullPointGroup369 := Group(Concatenation(pointGenerators369,[outerPoint369]));;

ActEdgeVector369 := function(vector,groupElement)
  local image,sourcePosition,left,right,targetPosition;
  image := List([1..240],unused -> Zero369);
  for sourcePosition in PositionsProperty(vector,entry -> entry<>Zero369) do
    left := edges369[sourcePosition][1]^groupElement;
    right := edges369[sourcePosition][2]^groupElement;
    targetPosition := Position(edges369,Set([left,right]));
    if left<right then
      image[targetPosition] := image[targetPosition]+vector[sourcePosition];
    else
      image[targetPosition] := image[targetPosition]-vector[sourcePosition];
    fi;
  od;
  return image;
end;;

CombinedVectorPermutation369 := function(groupElement)
  local xMap,zMap;
  xMap := List(xVectors369,vector ->
    Position(xVectors369,ActEdgeVector369(vector,groupElement)));
  zMap := List(zVectors369,vector ->
    Position(zVectors369,ActEdgeVector369(vector,groupElement)));
  if fail in xMap or fail in zMap then
    Error("Pass374 minimal vectors are not invariant");
  fi;
  return PermList(Concatenation(xMap,
    List(zMap,position -> Length(xVectors369)+position)));
end;;

innerCombinedGenerators369 := List(pointGenerators369,
  CombinedVectorPermutation369);;
outerCombined369 := CombinedVectorPermutation369(outerPoint369);;
innerPairGroup369 := Group(innerCombinedGenerators369);;
fullPairGroup369 := Group(Concatenation(innerCombinedGenerators369,
  [outerCombined369]));;

nonzeroPairs369 := [];;
phaseOneCount369 := 0;;
phaseTwoCount369 := 0;;
seed369 := fail;;
for xIndex369 in [1..Length(xVectors369)] do
  for zIndex369 in [1..Length(zVectors369)] do
    phase369 := Sum([1..240],position ->
      xVectors369[xIndex369][position]*zVectors369[zIndex369][position]);
    if not IsZero(phase369) then
      Add(nonzeroPairs369,[xIndex369,Length(xVectors369)+zIndex369]);
      if phase369=One369 then
        phaseOneCount369 := phaseOneCount369+1;
        if seed369=fail then
          seed369 := [xIndex369,Length(xVectors369)+zIndex369];
        fi;
      else
        phaseTwoCount369 := phaseTwoCount369+1;
      fi;
    fi;
  od;
od;

xIndex369 := seed369[1];;
zIndex369 := seed369[2]-Length(xVectors369);;
negativeXIndex369 := Position(xVectors369,-xVectors369[xIndex369]);;
negativeZIndex369 := Position(zVectors369,-zVectors369[zIndex369]);;
fourSeeds369 := [
  [xIndex369,Length(xVectors369)+zIndex369],
  [negativeXIndex369,Length(xVectors369)+negativeZIndex369],
  [negativeXIndex369,Length(xVectors369)+zIndex369],
  [xIndex369,Length(xVectors369)+negativeZIndex369]
];;

innerOrbits369 := OrbitsDomain(innerPairGroup369,nonzeroPairs369,OnTuples);;
fullOrbits369 := OrbitsDomain(fullPairGroup369,nonzeroPairs369,OnTuples);;
innerSeedOrbits369 := List(fourSeeds369,seed ->
  Orbit(innerPairGroup369,seed,OnTuples));;
fullSeedOrbits369 := List(fourSeeds369,seed ->
  Orbit(fullPairGroup369,seed,OnTuples));;
innerStabilizers369 := List(fourSeeds369,seed ->
  Stabilizer(innerPairGroup369,seed,OnTuples));;
fullStabilizers369 := List(fourSeeds369,seed ->
  Stabilizer(fullPairGroup369,seed,OnTuples));;

checks369 := rec();;
checks369.w33_counts_are_40_240_40_160 :=
  [Length(points369),Length(edges369),Length(lines369),Length(triangles369)]
  =[40,240,40,160];;
checks369.css_check_ranks_are_39_120 :=
  [Length(hxBasis369),Length(hzBasis369)]=[39,120];;
checks369.css_checks_commute_over_gf3 :=
  ForAll(Flat(hx369*TransposedMat(hz369)),IsZero);;
checks369.minimal_vector_counts_are_320_1620_3240 :=
  [Length(xVectors369),Length(zSupports369),Length(zVectors369)]
  =[320,1620,3240];;
checks369.connected_group_is_psp4_3_order_25920 :=
  Size(innerPointGroup369)=25920;
checks369.full_group_is_pgsp4_3_order_51840 :=
  Size(fullPointGroup369)=51840;
checks369.signed_chain_actions_are_faithful :=
  Size(innerPairGroup369)=25920 and Size(fullPairGroup369)=51840;
checks369.nonzero_vector_pair_count_is_51840 :=
  Length(nonzeroPairs369)=51840;
checks369.phases_split_evenly_25920_25920 :=
  [phaseOneCount369,phaseTwoCount369]=[25920,25920];
checks369.inner_action_has_four_orbits := Length(innerOrbits369)=4;
checks369.inner_orbits_all_have_size_12960 :=
  Set(List(innerOrbits369,Length))=[12960];
checks369.full_action_has_four_orbits := Length(fullOrbits369)=4;
checks369.full_orbits_all_have_size_12960 :=
  Set(List(fullOrbits369,Length))=[12960];
checks369.four_inner_seed_orbits_partition_the_pair_set :=
  Length(Set(Concatenation(innerSeedOrbits369)))=51840;
checks369.four_full_seed_orbits_partition_the_pair_set :=
  Length(Set(Concatenation(fullSeedOrbits369)))=51840;
checks369.connected_stabilizers_are_c2 :=
  ForAll(innerStabilizers369,stabilizer ->
    Size(stabilizer)=2 and StructureDescription(stabilizer)="C2");
checks369.full_stabilizers_are_klein_four :=
  ForAll(fullStabilizers369,stabilizer ->
    Size(stabilizer)=4 and StructureDescription(stabilizer)="C2 x C2");
checks369.simultaneous_negation_separates_equal_phase_sheets :=
  not fourSeeds369[2] in fullSeedOrbits369[1];
checks369.single_negation_separates_opposite_phase_sheets :=
  not fourSeeds369[3] in fullSeedOrbits369[1] and
  not fourSeeds369[4] in fullSeedOrbits369[1];
checks369.outer_similitude_preserves_all_four_sheets :=
  ForAll([1..4],position ->
    OnTuples(fourSeeds369[position],outerCombined369)
      in fullSeedOrbits369[position]);
checks369.deck_sign_group_is_c2_squared :=
  negativeXIndex369<>xIndex369 and negativeZIndex369<>zIndex369 and
  fourSeeds369[1]<>fourSeeds369[2] and
  fourSeeds369[3]<>fourSeeds369[4];
checks369.weyl_torsor_is_refuted :=
  Length(fullOrbits369)=4 and
  ForAll(fullStabilizers369,stabilizer -> Size(stabilizer)=4);

names369 := RecNames(checks369);;
Assert369("all checks",ForAll(names369,name -> checks369.(name)));;

stream369 := OutputTextFile(OUT374,false);;
SetPrintFormattingStatus(stream369,false);;
WriteAll(stream369,"{\n");;
WriteAll(stream369,"  \"schema\": \"w33.pass374.minimal_pair_phase_sheet_obstruction.gap.v1\",\n");;
WriteAll(stream369,"  \"status\": \"PASS\",\n");;
WriteAll(stream369,"  \"pairing_space\": {\"X_min_vectors\":320,\"Z_min_vectors\":3240,\"nonzero_pairs\":51840,\"phase_counts\":{\"1\":25920,\"2\":25920}},\n");;
WriteAll(stream369,"  \"projective_owner\": {\"file\":\"analysis/w33_visible_pair_orbit_weyl_torsor.py\",\"visible_ray_pairs\":12960,\"connected_stabilizer_order\":2},\n");;
WriteAll(stream369,"  \"phase_cover_owners\": {\"files\":[\"analysis/bt571_phase_double_cover_algebra.py\",\"analysis/bt637_phase_deck_ij_scalar_lift.py\",\"analysis/bt644_phase_character_commutative_diagram.py\"],\"owned_result\":\"four F3-star x F3-star lifts over each of 12960 projective incidences, split 25920+25920 with scalar sign deck involutions\",\"new_gap\":\"the orbit and stabilizer classification of the natural signed-chain PSp(4,3) and PGSp(4,3) actions\"},\n");;
WriteAll(stream369,"  \"group_identification_owner\": {\"file\":\"w33_pass125_two_we6_embeddings.py\",\"result\":\"the multiplier-2 projective similitude extends PSp(4,3) to PGSp(4,3) isomorphic to W(E6)\",\"boundary\":\"Pass 374 reuses this constructed identification; it does not infer an isomorphism from order 51840 alone.\"},\n");;
WriteAll(stream369,"  \"connected_action\": {\"group\":\"PSp(4,3)\",\"order\":25920,\"orbit_profile\":[12960,12960,12960,12960],\"stabilizer\":\"C2\"},\n");;
WriteAll(stream369,"  \"full_action\": {\"group\":\"PGSp(4,3)=PSp(4,3):2=W(E6)\",\"order\":51840,\"orbit_profile\":[12960,12960,12960,12960],\"stabilizer\":\"C2 x C2\",\"coset_model\":\"four disjoint copies of W(E6)/(C2 x C2)\"},\n");;
WriteAll(stream369,"  \"deck_group\": {\"group\":\"C2_X x C2_Z\",\"generators\":[\"x -> -x\",\"z -> -z\"],\"reading\":\"two pairing phases, each split into two simultaneous-sign sheets\"},\n");;
WriteAll(stream369,"  \"correction\": \"The equality 51840=|W(E6)| is a cardinality identity for the nonzero vector-pair set, not a torsor theorem for the natural signed-chain action. The previously known fourfold scalar cover has four invariant 12960-sheets under that action.\",\n");;
WriteAll(stream369,"  \"boundary\": \"This classifies the natural finite collineation action. A regular 51840-state action would require additional non-geometric phase transport, which is not supplied here.\",\n");;
WriteAll(stream369,Concatenation("  \"check_count\": ",String(Length(names369)),",\n"));;
WriteAll(stream369,"  \"checks\": {\n");;
for name369 in names369 do
  WriteAll(stream369,Concatenation("    \"",name369,"\": ",Bool369(checks369.(name369))));;
  if name369<>names369[Length(names369)] then WriteAll(stream369,","); fi;
  WriteAll(stream369,"\n");;
od;
WriteAll(stream369,"  }\n}\n");;
CloseStream(stream369);;

Print("Pass374 status=PASS checks=",Length(names369),
      " pair_orbits=4x12960 stabilizers=C2/C2xC2 output=",OUT374,"\n");;
QUIT;
