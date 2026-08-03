Print("=== Pass 2540: the 540-frame permutation character under PGSp, not PSp ===\n\n");
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
# the SIMILITUDE group GSp(4,3): adjoin a similitude with non-square multiplier
G := Normalizer(GL(4,3), S);;
Print("  normaliser of SP(4,3) in GL(4,3) has order ", Size(G), "\n");
P := Group(List(GeneratorsOfGroup(G), g -> PermList(FrameImage(g))));;
Print("  group order on frames : ", Size(P), "   stabiliser ", Size(Stabilizer(P,1)), "\n");
tp := CharacterTable(P);;
cls := ConjugacyClasses(tp);;
pc := ClassFunction(tp, List(cls, c -> Number([1..540], i -> i^Representative(c) = i)));;
Print("  genuine character ? ", IsCharacter(tp, pc), "   degree ", pc[1], "\n");
Print("  rank <pc,pc>          : ", ScalarProduct(tp, pc, pc), "\n\n");
dec := Filtered(List([1..Length(Irr(tp))],
         i -> [Irr(tp)[i][1], ScalarProduct(tp, pc, Irr(tp)[i])]), y -> y[2] > 0);;
Print("  [degree, multiplicity] : ", dec, "\n");
Print("  ISOTYPIC DIMENSIONS (degree x multiplicity) : ",
      SortedList(List(dec, y -> y[1]*y[2])), "\n");
Print("  sum : ", Sum(dec, y -> y[1]*y[2]), "\n\n");
Print("  parallel track rank-9 multiplicities : [1,15,15,20,24,60,108,135,162]\n");
Print("  MATCH as a multiset ? ",
      SortedList(List(dec, y -> y[1]*y[2])) = SortedList([1,15,15,20,24,60,108,135,162]),
      "\n");
