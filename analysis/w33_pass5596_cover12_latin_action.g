# Pass5596 addendum -- action-level test for the 13-cover's moving 12-orbit.
# Reuse the exact committed Pass5417 construction of the P-block graph, selected
# 13-cover, setwise stabilizer, and induced order-576 S13 action.
Read("analysis/w33_pass5417_cover_orbits.g");;

mov := First(orbs, o -> Length(o) = 12);;
h12 := ActionHomomorphism(act, mov, OnPoints);;
cover12 := Image(h12);;

# Independent Klein-V4 Latin 12-symbol action.  Points 1..4,5..8,9..12 are
# the three labelled V4 copies in x+y+z=0.  t0/t1 are the two independent
# translations; glswap/gl3 generate GL(2,2); pswap/p3 generate S3 on parts.
t0 := (1,2)(3,4)(9,10)(11,12);;
t1 := (5,6)(7,8)(9,10)(11,12);;
glswap := (2,3)(6,7)(10,11);;
gl3 := (2,3,4)(6,7,8)(10,11,12);;
pswap := (1,5)(2,6)(3,7)(4,8);;
p3 := (1,5,9)(2,6,10)(3,7,11)(4,8,12);;
latin12 := Group([t0,t1,glswap,gl3,pswap,p3]);;

sym12 := SymmetricGroup(12);;
conj := IsConjugate(sym12, cover12, latin12);;
stabC := Stabilizer(cover12, 1);;
stabL := Stabilizer(latin12, 1);;
orbC := SortedList(List(Orbits(stabC, [1..12]), Length));;
orbL := SortedList(List(Orbits(stabL, [1..12]), Length));;

repo2 := GAPInfo.SystemEnvironment.W33_REPO;;
f2 := OutputTextFile(Concatenation(repo2,
  "/data/PART_W33_PASS5596_COVER12_LATIN_ACTION.json"), false);;
SetPrintFormattingStatus(f2, false);;
AppendTo(f2, "{\n");
AppendTo(f2, "  \"pass\": 5596,\n");
AppendTo(f2, "  \"status\": \"ACTION_CONJUGACY_TEST\",\n");
AppendTo(f2, "  \"cover12_order\": ", Size(cover12), ",\n");
AppendTo(f2, "  \"latin12_order\": ", Size(latin12), ",\n");
AppendTo(f2, "  \"cover12_point_stabilizer_order\": ", Size(stabC), ",\n");
AppendTo(f2, "  \"latin12_point_stabilizer_order\": ", Size(stabL), ",\n");
AppendTo(f2, "  \"cover12_point_stabilizer_structure\": \"", StructureDescription(stabC), "\",\n");
AppendTo(f2, "  \"latin12_point_stabilizer_structure\": \"", StructureDescription(stabL), "\",\n");
AppendTo(f2, "  \"cover12_suborbit_sizes\": ", orbC, ",\n");
AppendTo(f2, "  \"latin12_suborbit_sizes\": ", orbL, ",\n");
AppendTo(f2, "  \"conjugate_in_S12\": ", conj, ",\n");
AppendTo(f2, "  \"boundary\": \"The cover action is rebuilt from the exact committed Pass5417 P-block graph and selected 13-cover; the Latin action is constructed independently from V4 affine translations, GL(2,2), and S3 parastrophes. Conjugacy in S12 is an action-level test, stronger than abstract group isomorphism.\"\n");
AppendTo(f2, "}\n");
CloseStream(f2);;

Print("cover12 order=", Size(cover12), " latin12 order=", Size(latin12),
      " suborbits=", orbC, "/", orbL, " conjugate=", conj, "\n");
