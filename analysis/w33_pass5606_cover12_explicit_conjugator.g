# Pass5606 -- extract an explicit cover12 -> Latin12 conjugator, not only yes/no.
# This deliberately rebuilds the exact Pass5417 325-vertex substrate and selected
# 13-cover. It then compares the moving 12-orbit to the independently constructed
# Klein-V4 Latin action.  Pass5623 repaired the output contract so downstream
# consumers receive original cover vertices, the fixed vertex, and a zero-based
# cover12->Latin permutation in addition to the legacy one-based witness.
Read("analysis/w33_pass5417_cover_orbits.g");;
mov := First(orbs, o -> Length(o)=12);;
fixedPos := First([1..13], i -> not (i in mov));;
movingVertices := List(mov, i -> cover[i]);;
fixedVertex := cover[fixedPos];;
h12 := ActionHomomorphism(act,mov,OnPoints);;
cover12 := Image(h12);;

t0 := (1,2)(3,4)(9,10)(11,12);;
t1 := (5,6)(7,8)(9,10)(11,12);;
glswap := (2,3)(6,7)(10,11);;
gl3 := (2,3,4)(6,7,8)(10,11,12);;
pswap := (1,5)(2,6)(3,7)(4,8);;
p3 := (1,5,9)(2,6,10)(3,7,11)(4,8,12);;
latin12 := Group([t0,t1,glswap,gl3,pswap,p3]);;
sym12 := SymmetricGroup(12);;
conj := IsConjugate(sym12,cover12,latin12);;
rep := fail;;
if conj then
  rep := RepresentativeAction(sym12,cover12,latin12,OnPoints);;
  if rep=fail then Error("IsConjugate true but no RepresentativeAction witness"); fi;
  if not cover12^rep=latin12 then Error("representative does not conjugate cover12 to latin12"); fi;
fi;

stabC := Stabilizer(cover12,1);;
orbC := SortedList(List(Orbits(stabC,[1..12]),Length));;
repo := GAPInfo.SystemEnvironment.W33_REPO;;
f := OutputTextFile(Concatenation(repo,"/data/PART_W33_PASS5606_COVER12_EXPLICIT_CONJUGATOR.json"),false);;
SetPrintFormattingStatus(f,false);;
AppendTo(f,"{\n");
AppendTo(f,"  \"pass\": 5606,\n");
AppendTo(f,"  \"cover13_moving_orbit_original_positions\": ",mov,",\n");
AppendTo(f,"  \"moving_cover_vertices\": ",movingVertices,",\n");
AppendTo(f,"  \"fixed_cover_position_one_based\": ",fixedPos,",\n");
AppendTo(f,"  \"fixed_cover_vertex\": ",fixedVertex,",\n");
AppendTo(f,"  \"cover12_order\": ",Size(cover12),",\n");
AppendTo(f,"  \"latin12_order\": ",Size(latin12),",\n");
AppendTo(f,"  \"cover12_suborbit_sizes\": ",orbC,",\n");
AppendTo(f,"  \"conjugate_in_S12\": ",conj,",\n");
if conj then
  AppendTo(f,"  \"conjugator_cover12_to_latin12_one_based\": ",List([1..12],i->i^rep),",\n");
  AppendTo(f,"  \"cover12_to_latin\": ",List([1..12],i->(i^rep)-1),",\n");
else
  AppendTo(f,"  \"conjugator_cover12_to_latin12_one_based\": null,\n");
  AppendTo(f,"  \"cover12_to_latin\": null,\n");
fi;
AppendTo(f,"  \"boundary\": \"This is a direct action-level conjugacy witness from the exact selected 13-cover. No group-order inference is substituted.\"\n");
AppendTo(f,"}\n");
CloseStream(f);;
Print("Pass5606 cover12 order=",Size(cover12)," suborbits=",orbC," conjugate=",conj," fixedVertex=",fixedVertex,"\n");
if conj then Print("conjugator images=",List([1..12],i->i^rep),"\n"); fi;
