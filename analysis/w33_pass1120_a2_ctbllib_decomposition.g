# Pass 1120: complete CTblLib decomposition of the 2240-point A2-root-triple carrier.
t := CharacterTable("U4(2).2");;
irr := Irr(t);;
vals := [2240,32,160,26,242,8,32,12,20,2,32,2,10,2,2,672,40,8,80,42,6,4,8,2,8];;
perm := Character(t, vals);;
mults := List(irr, chi -> ScalarProduct(perm, chi));;
if ForAny(mults, x -> not IsInt(x) or x < 0) then
  Error("Pass1120: non-integral or negative multiplicity");
fi;
if Sum([1..Length(irr)], i -> mults[i] * irr[i][1]) <> 2240 then
  Error("Pass1120: degree reconstruction failed");
fi;
Print("{\"schema\":\"w33.pass1120.a2_ctbllib_decomposition.observed.v1\",");
Print("\"status\":\"PASS\",\"table\":\"U4(2).2\",\"degree\":2240,");
Print("\"irreducible_count\":",Length(irr),",\"nonzero\":[");
first := true;;
for i in [1..Length(irr)] do
  if mults[i] <> 0 then
    if not first then Print(","); fi;
    first := false;
    Print("{\"row\":",i,",\"degree\":",irr[i][1],",\"multiplicity\":",mults[i],",\"values\":[");
    for j in [1..Length(irr[i])] do
      if j > 1 then Print(","); fi;
      Print(irr[i][j]);
    od;
    Print("]}");
  fi;
od;
Print("],\"degree_reconstruction\":",Sum([1..Length(irr)], i -> mults[i] * irr[i][1]),"}\n");
