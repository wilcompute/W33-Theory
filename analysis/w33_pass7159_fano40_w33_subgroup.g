# Pass7159 addendum: does the 40-point complement of the 23 code-column types
# carry the same S3 wr C2 permutation action as a subgroup of Aut(W(3,3))?
#
# This is the sharp object-level test suggested by Pass1021's proved E8-root
# fibration 240 -> 40 W33 points.  A positive result identifies the two 40-point
# G-sets under a named order-72 subgroup; a negative result kills this natural
# route without saying arbitrary 40-set bijections do not exist.

repo := GAPInfo.SystemEnvironment.W33_REPO;;
out := Concatenation(repo,"/data/PART_W33_PASS7159_FANO40_W33_SUBGROUP.json");;

# ----- binary complement C = PG(5,2) \ (all wt1 + all wt2 + two triples)
T0 := [2,4,5];;  # GAP positions corresponding to zero-based {1,3,4}
T1 := [1,3,6];;
WeightBits := function(x)
  local n,k; n:=0; k:=x;
  while k>0 do if k mod 2=1 then n:=n+1; fi; k:=QuoInt(k,2); od;
  return n;
end;;
tr0 := Sum(T0,i->2^(i-1));; tr1 := 63-tr0;;
selected := Filtered([1..63],x->WeightBits(x)<=2 or x=tr0 or x=tr1);;
comp := Difference([1..63],selected);;
if Length(selected)<>23 or Length(comp)<>40 then Error("23+40 split failed"); fi;
pos := function(x) return Position(comp,x); end;;

ActMask := function(x,p)
  local y,i;
  y:=0;
  for i in [1..6] do
    if QuoInt(x,2^(i-1)) mod 2=1 then y:=y+2^(i^p-1); fi;
  od;
  return y;
end;;
MaskPerm := function(p)
  return PermList(List(comp,x->pos(ActMask(x,p))));
end;;

# S3 x S3 on the two triples, extended by the block swap.
a := (2,4,5);; b := (2,4);; c := (1,3,6);; d := (1,3);; s := (1,2)(3,4)(6,5);;
Outer6 := Group(a,b,c,d,s);;
Outer40 := Group(List(GeneratorsOfGroup(Outer6),MaskPerm));;
if Size(Outer6)<>72 or Size(Outer40)<>72 then Error("outer group order failed"); fi;
orbBin := SortedList(List(Orbits(Outer40,[1..40]),Length));;

# ----- exact W33 40-point automorphism action.
S := Sp(4,3);;
pts := NormedRowVectors(GF(3)^4);;
P := Image(ActionHomomorphism(S,pts,OnLines));;
if Size(P)<>25920 or Length(pts)<>40 then Error("PSp point action failed"); fi;

# Full graph automorphism group is PSp(4,3):2.  Build it as the automorphism
# group of the exact SRG, which avoids any convention ambiguity about GSp.
J := InvariantBilinearForm(S).matrix;;
adj := List([1..40],i->Filtered([1..40],j->j<>i and IsZero(pts[i]*J*pts[j])));;
# Encode the graph as a GRAPE-free relation and find the full normalizer in S40
# of the PSp action; the known order is 51840 and the extra coset is point-line outer.
S40 := SymmetricGroup(40);;
N := Normalizer(S40,P);;
if Size(N)<>51840 then Error(Concatenation("unexpected full normalizer order ",String(Size(N)))); fi;

classes := ConjugacyClassesSubgroups(N);;
cands := Filtered(classes,C->Size(Representative(C))=72);;
hits := [];;
for C in cands do
  H:=Representative(C);
  if IsConjugate(S40,Outer40,H) then Add(hits,H); fi;
od;

# Also record orbit-pattern matches, weaker than permutation conjugacy.
patternHits := [];;
for C in cands do
  H:=Representative(C);
  if SortedList(List(Orbits(H,[1..40]),Length))=orbBin then
    Add(patternHits,StructureDescription(H));
  fi;
od;

stream:=OutputTextFile(out,false);;
SetPrintFormattingStatus(stream,false);;
AppendTo(stream,"{\n");
AppendTo(stream,"  \"schema\": \"w33.pass7159.fano40_w33_subgroup.v1\",\n");
AppendTo(stream,"  \"status\": \"PASS\",\n");
AppendTo(stream,"  \"binary_model\": \"(PG(2,2) x PG(2,2)) minus the 3x3 basis grid, 49-9=40\",\n");
AppendTo(stream,"  \"outer_group\": \"S3 wr C2\",\n");
AppendTo(stream,"  \"outer_group_order\": 72,\n");
AppendTo(stream,"  \"binary_orbit_sizes\": [",JoinStringsWithSeparator(List(orbBin,String),","),"],\n");
AppendTo(stream,"  \"w33_full_aut_order\": ",String(Size(N)),",\n");
AppendTo(stream,"  \"order72_subgroup_classes\": ",String(Length(cands)),",\n");
AppendTo(stream,"  \"same_orbit_pattern_classes\": ",String(Length(patternHits)),",\n");
AppendTo(stream,"  \"permutation_conjugacy_hits\": ",String(Length(hits)),",\n");
AppendTo(stream,"  \"object_level_bridge\": ", (if Length(hits)>0 then "true" else "false" fi),",\n");
AppendTo(stream,"  \"boundary\": \"A positive hit identifies the binary-complement S3 wr C2 G-set with a subgroup action on the exact W33 40 points. It does not by itself identify any graph relation or the 248 code coordinates with E8 roots/adjoint basis.\"\n");
AppendTo(stream,"}\n");
CloseStream(stream);;
Print("Pass7159: binary orbits=",orbBin," order72 classes=",Length(cands)," conjugacy hits=",Length(hits),"\n");
QUIT;
