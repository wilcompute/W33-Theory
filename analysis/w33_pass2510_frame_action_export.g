# Pass 2510 -- build the 540-frame action of Sp(4,3) IN GAP, where the group and its
# invariant form already agree, and export the permutations.  Pass 2503 failed twice
# trying to do this in Python: hand-written generators gave order 192, and GAP's real
# generators preserve a different form than the hand-rolled one.
repo := GAPInfo.SystemEnvironment.W33_REPO;;
S := SP(4,3);;
V := GF(3)^4;;
form := InvariantBilinearForm(S).matrix;;
Print("|Sp(4,3)| = ", Size(S), "\n");

pts := List(Filtered(Subspaces(V,1), x -> true), b -> Basis(b)[1]);;
Print("projective points : ", Length(pts), "\n");

# totally isotropic 2-subspaces
tis := Filtered(Subspaces(V,2), U -> ForAll(Basis(U), x ->
         ForAll(Basis(U), y -> x * form * y = 0*Z(3))));;
Print("totally isotropic lines : ", Length(tis), "\n");

lines := List(tis, U -> Set(List(Filtered(Elements(U), v -> v <> Zero(V)),
                                v -> Position(pts, First(pts, p -> p in Subspace(V,[v]))))));;
lines := List(lines, Set);;
Print("line sizes : ", Set(List(lines, Length)), "\n");

frames := [];;
for i in [1..Length(lines)] do
  for j in [i+1..Length(lines)] do
    if Intersection(lines[i], lines[j]) = [] then Add(frames, [i,j]); fi;
  od;
od;
Print("frames : ", Length(frames), "\n");

fpos := NewDictionary([1,2], true);;
for k in [1..Length(frames)] do AddDictionary(fpos, frames[k], k); od;

FrameImage := function(g)
  local lmap, out, k, a, b, x, y, img;
  lmap := [];
  for a in [1..Length(lines)] do
    img := Set(List(lines[a], p -> Position(pts, First(pts,
             q -> q in Subspace(V, [pts[p] * g])))));
    lmap[a] := Position(lines, img);
  od;
  out := [];
  for k in [1..Length(frames)] do
    x := lmap[frames[k][1]]; y := lmap[frames[k][2]];
    if x > y then a := x; x := y; y := a; fi;
    out[k] := LookupDictionary(fpos, [x,y]);
  od;
  return out;
end;;

gens := List(GeneratorsOfGroup(S), FrameImage);;
P := Group(List(gens, PermList));;
Print("group order ON FRAMES : ", Size(P), "\n");
Print("transitive on 540 frames : ", IsTransitive(P, [1..540]), "\n");
Print("point stabiliser order : ", Size(Stabilizer(P, 1)), "\n");

out := Concatenation(repo, "/data/w33_pass2510_frame_action.json");;
s := OutputTextFile(out, false);;
SetPrintFormattingStatus(s, false);
WriteAll(s, "{\n  \"schema\": \"w33.pass2510.frame_action.v1\",\n");
WriteAll(s, Concatenation("  \"frames\": ", String(Length(frames)), ",\n"));
WriteAll(s, Concatenation("  \"group_order_on_frames\": ", String(Size(P)), ",\n"));
WriteAll(s, "  \"generators\": [\n");
for k in [1..Length(gens)] do
  WriteAll(s, Concatenation("    ", String(gens[k])));
  if k < Length(gens) then WriteAll(s, ","); fi;
  WriteAll(s, "\n");
od;
WriteAll(s, "  ]\n}\n");
CloseStream(s);
Print("wrote ", out, "\n");
