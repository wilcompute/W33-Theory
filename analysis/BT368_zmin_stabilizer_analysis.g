Read("data/w33_data.gap");
G := w33_group;

find_quadrangle := function(adj)
  local i, j, k, l;
  for i in [1..40] do
    for j in [i+1..40] do
      if adj[i][j] = 1 then
        for k in [j+1..40] do
          if adj[j][k] = 1 and adj[i][k] = 0 then
            for l in [k+1..40] do
              if adj[k][l] = 1 and adj[i][l] = 1 and adj[j][l] = 0 then
                return [i, j, k, l];
              fi;
            od;
          fi;
        od;
      fi;
    od;
  od;
  return fail;
end;

q := find_quadrangle(w33_adj);

S := PerfectGroup(51840, 1);
cent := Center(S);
phi := NaturalHomomorphismByNormalSubgroup(S, cent);
z_elem := Elements(cent)[2];

iso := IsomorphismGroups(G, S/cent);
stab16 := Stabilizer(G, Set(q), OnSets);
img_stab16 := Image(iso, stab16);
stab32 := PreImage(phi, img_stab16);

Print("Stab32 order: ", Size(stab32), "\n");
cls := ConjugacyClasses(stab32);
z_idx := -1;
for i in [1..Length(cls)] do
    if z_elem in cls[i] then z_idx := i; break; fi;
od;
Print("z is in class: ", z_idx, "\n");

tbl := CharacterTable(stab32);
linear := Filtered(Irr(tbl), chi -> chi[1] = 1);
for chi in linear do
    if chi[z_idx] = -1 then
        Print("Found C2 character X.", Position(Irr(tbl), chi), " with chi(z)=-1\n");
    elif chi[z_idx] = E(4) or chi[z_idx] = -E(4) then
        Print("Found C4 character X.", Position(Irr(tbl), chi), " with chi(z)=+-i\n");
    fi;
od;
