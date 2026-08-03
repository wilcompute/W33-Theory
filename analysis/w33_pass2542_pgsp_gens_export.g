repo := GAPInfo.SystemEnvironment.W33_REPO;;
S := SP(4,3);; V := GF(3)^4;;
form := InvariantBilinearForm(S).matrix;;
pts := List(Subspaces(V,1), b -> Basis(b)[1]);;
tis := Filtered(Subspaces(V,2), U -> ForAll(Basis(U), x ->
         ForAll(Basis(U), y -> x*form*y = 0*Z(3))));;
lines := List(tis, U -> Set(List(Filtered(Elements(U), v -> v <> Zero(V)),
             v -> Position(pts, First(pts, p -> p in Subspace(V,[v]))))));;
frames := [];;
for i in [1..40] do for j in [i+1..40] do
  if Intersection(lines[i], lines[j]) = [] then Add(frames,[i,j]); fi; od; od;
fpos := NewDictionary([1,2], true);;
for k in [1..540] do AddDictionary(fpos, frames[k], k); od;
FrameImage := function(g)
  local lmap,out,k,a,x,y,t,img;
  lmap := [];
  for a in [1..40] do
    img := Set(List(lines[a], p -> Position(pts,
             First(pts, q -> q in Subspace(V,[pts[p]*g])))));
    lmap[a] := Position(lines, img);
  od;
  out := [];
  for k in [1..540] do
    x := lmap[frames[k][1]]; y := lmap[frames[k][2]];
    if x > y then t:=x; x:=y; y:=t; fi;
    out[k] := LookupDictionary(fpos,[x,y]);
  od;
  return out;
end;;
G := Normalizer(GL(4,3), S);;
gens := List(GeneratorsOfGroup(G), FrameImage);;
P := Group(List(gens, PermList));;
Print("PGSp frame group order ", Size(P), "  generators ", Length(gens), "\n");
out := Concatenation(repo, "/data/w33_pass2542_pgsp_frame_gens.txt");;
s := OutputTextFile(out, false);; SetPrintFormattingStatus(s, false);
for g in gens do
  for k in [1..540] do WriteAll(s, Concatenation(String(g[k]-1), " ")); od;
  WriteAll(s, "\n");
od;
CloseStream(s);
Print("wrote ", out, "\n");
