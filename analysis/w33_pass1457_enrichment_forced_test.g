LogTo();
out := "C:/Repos/Theory of Everything/data/w33_pass1457_enrichment.txt";
PrintTo(out, "Pass 1457: is the 12-of-60 enrichment forced? (corrected actions)\n\n");
A := function(s) AppendTo(out, s); end;
SP4  := Sp(4,3);
pts  := Orbit(SP4, NormedRowVector([1,0,0,0]*Z(3)^0), OnLines);
Gp   := Action(SP4, pts, OnLines);          # permutes POINTS
form := function(u,v) return u[1]*v[4]-u[4]*v[1]+u[2]*v[3]-u[3]*v[2]; end;
zero := Zero(GF(3));
adj  := List([1..40], i -> Filtered([1..40], j -> j<>i and form(pts[i],pts[j])=zero));
edges := Filtered(Combinations([1..40],2), e -> e[2] in adj[e[1]]);
lines := [];
for i in [1..40] do for j in adj[i] do if j>i then
  AddSet(lines, Set(Filtered([1..40], m -> pts[m] in
    List(Filtered(Elements(VectorSpace(GF(3),[pts[i],pts[j]])),
                  v -> v <> Zero(pts[i])), NormedRowVector))));
fi; od; od;
frames := Filtered(Combinations([1..40],2),
            p -> Intersection(lines[p[1]], lines[p[2]]) = []);
A(Concatenation("points 40  edges ", String(Length(edges)),
  "  lines ", String(Length(lines)), "  frames ", String(Length(frames)), "\n\n"));
for cl in ConjugacyClasses(Gp) do
  if Order(Representative(cl)) = 2 then
    g  := Representative(cl);                       # a POINT permutation
    fp := Number([1..40], i -> i^g = i);
    fe := Number(edges, e -> Set([e[1]^g, e[2]^g]) = e);
    gl := PermList(List(lines, L -> Position(lines, OnSets(L, g))));
    fl := Number([1..40], i -> i^gl = i);
    ff := Number(frames, f -> Set([f[1]^gl, f[2]^gl]) = f);
    A(Concatenation("class size ", String(Size(cl)), ": fixes ",
      String(fp), " points, ", String(fe), " edges, ",
      String(fl), " lines, ", String(ff), " frames\n"));
    A(Concatenation("   fixed edges divisible by 4? ", String(fe mod 4 = 0),
      "   fe/4 = ", String(fe/4), "\n"));
  fi;
od;
A("\nDONE\n");
QUIT;
