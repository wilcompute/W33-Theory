LoadPackage("ctbllib");
u := CharacterTable("U4(2)");
if u = fail then Error("CTblLib table U4(2) unavailable"); fi;
m := CharacterTable("M");
if m = fail then Error("CTblLib table M unavailable"); fi;
direct := PossibleClassFusions(u,m);
Print("DIRECT_FUSION_COUNT=",Length(direct),"\n");
maxnames := Maxes(m);
if maxnames = fail then Error("Monster maximal table list unavailable"); fi;
Print("MAXIMAL_TABLE_COUNT=",Length(maxnames),"\n");
for name in maxnames do
  h := CharacterTable(name);
  if h <> fail then
    fuh := PossibleClassFusions(u,h);
    if Length(fuh) > 0 then
      fhm := GetFusionMap(h,m);
      if fhm = fail then
        fhmall := PossibleClassFusions(h,m);
      else
        fhmall := [fhm];
      fi;
      comps := [];
      for a in fuh do
        for b in fhmall do
          Add(comps,List(a,x->b[x]));
        od;
      od;
      comps := Set(comps);
      matching := Filtered(comps,x->x in direct);
      Print("OVERGROUP=",name,";U_TO_H=",Length(fuh),
            ";H_TO_M=",Length(fhmall),";COMPOSED=",Length(comps),
            ";DIRECT_MATCH=",Length(matching),"\n");
    fi;
  fi;
od;
QUIT;
