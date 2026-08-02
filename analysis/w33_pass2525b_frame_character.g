Print("=== Pass 2525 (redone): permutation character from FIXED-POINT COUNTS ===\n\n");
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
P := Group(List(GeneratorsOfGroup(S), g -> PermList(FrameImage(g))));;
tp := CharacterTable(P);;
cls := ConjugacyClasses(tp);;
pc := ClassFunction(tp, List(cls, c -> Number([1..540],
        i -> i^Representative(c) = i)));;
Print("  is it a genuine character ? ", IsCharacter(tp, pc), "\n");
Print("  degree (must be 540)      : ", pc[1], "\n");
dec := Filtered(List([1..Length(Irr(tp))],
         i -> [Irr(tp)[i][1], ScalarProduct(tp, pc, Irr(tp)[i])]), y -> y[2] > 0);;
Print("  decomposition [degree, multiplicity] :\n    ", dec, "\n");
Print("  sum degree*mult : ", Sum(dec, y -> y[1]*y[2]), "\n");
Print("  rank (number of orbitals) = <pc,pc> : ", ScalarProduct(tp, pc, pc), "\n\n");
Print("  constituent degrees WITH multiplicity, expanded:\n    ",
      SortedList(Concatenation(List(dec, y -> List([1..y[2]], k -> y[1])))), "\n");
Print("  parallel track rank-9 multiplicities : [1,15,15,20,24,60,108,135,162]\n");
Print("  MATCH ? ", SortedList(Concatenation(List(dec, y -> List([1..y[2]], k -> y[1]))))
        = SortedList([1,15,15,20,24,60,108,135,162]), "\n");
