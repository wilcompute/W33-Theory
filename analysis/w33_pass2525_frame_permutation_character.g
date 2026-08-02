Print("=== Pass 2525: the 540-frame permutation character ===\n\n");
repo := GAPInfo.SystemEnvironment.W33_REPO;;
S := SP(4,3);;
V := GF(3)^4;;
form := InvariantBilinearForm(S).matrix;;
pts := List(Subspaces(V,1), b -> Basis(b)[1]);;
tis := Filtered(Subspaces(V,2), U -> ForAll(Basis(U), x ->
         ForAll(Basis(U), y -> x * form * y = 0*Z(3))));;
lines := List(tis, U -> Set(List(Filtered(Elements(U), v -> v <> Zero(V)),
             v -> Position(pts, First(pts, p -> p in Subspace(V,[v]))))));;
frames := [];;
for i in [1..40] do for j in [i+1..40] do
  if Intersection(lines[i], lines[j]) = [] then Add(frames, [i,j]); fi; od; od;
Print("  frames : ", Length(frames), "\n");
fpos := NewDictionary([1,2], true);;
for k in [1..540] do AddDictionary(fpos, frames[k], k); od;
FrameImage := function(g)
  local lmap, out, k, a, x, y, t, img;
  lmap := [];
  for a in [1..40] do
    img := Set(List(lines[a], p -> Position(pts,
             First(pts, q -> q in Subspace(V, [pts[p]*g])))));
    lmap[a] := Position(lines, img);
  od;
  out := [];
  for k in [1..540] do
    x := lmap[frames[k][1]]; y := lmap[frames[k][2]];
    if x > y then t := x; x := y; y := t; fi;
    out[k] := LookupDictionary(fpos, [x,y]);
  od;
  return out;
end;;
P := Group(List(GeneratorsOfGroup(S), g -> PermList(FrameImage(g))));;
Print("  group order on frames : ", Size(P), "   stabiliser ", Size(Stabilizer(P,1)), "\n\n");
pc := PermutationCharacter(P, Stabilizer(P,1), OnPoints);;
t := CharacterTable(P);;
dec := Filtered(List(Irr(t), x -> [x[1], ScalarProduct(t, pc, x)]), y -> y[2] > 0);;
Print("  permutation character on 540 frames decomposes as:\n");
Print("    [degree, multiplicity] : ", dec, "\n");
Print("    sum of degree*mult     : ", Sum(dec, y -> y[1]*y[2]), "\n");
Print("    constituent degrees    : ", SortedList(List(dec, y -> y[1])), "\n\n");
Print("  parallel track Pass 2472 rank-9 scheme multiplicities:\n");
Print("    [1, 15, 15, 20, 162, 135, 108, 24, 60]  sum 540\n");
Print("    do the constituent DEGREES match that multiset ? ",
      SortedList(List(dec, y->y[1])) = SortedList([1,15,15,20,162,135,108,24,60]), "\n");
Print("\n=== Pass 2526: is the pentagon zero mode the same absence as the C3 orientation? ===\n");
t2 := CharacterTable("2.U4(2)");; n2 := Irr(t2);;
o2 := OrdersClassRepresentatives(t2);; s2 := SizesConjugacyClasses(t2);;
zc := First([1..Length(o2)], i -> o2[i]=2 and s2[i]=1);;
d4 := Filtered([1..Length(n2)], i -> n2[i][1]=4);;
e8 := n2[d4[1]] + n2[d4[2]];;
for ord in [3,5] do
  Print("  order-", ord, " classes and the E8 carrier's trivial multiplicity there:\n");
  for i in Filtered([1..Length(o2)], j -> o2[j]=ord) do
    Print("    class ", i, " size ", s2[i], "   chi_E8 = ", e8[i],
          "   trivial mult = ", (e8[1] + (ord-1)*e8[i])/ord, "\n");
  od;
od;
