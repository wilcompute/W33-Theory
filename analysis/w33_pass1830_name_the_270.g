# Pass 1830 (continued) -- name the size-270 class.
#
# It is an inner involution fixing 0 points, 4 lines and 24 frames, with
# centraliser of order 192 = 2 x 96.  Four fixed lines and no fixed points is
# the signature of a configuration; find which one, and check that the
# configuration's G-orbit really has size 270 so the correspondence is a
# bijection rather than a coincidence of counts.
#
# Run: bash scripts/run_gap.sh "C:/Repos/Theory of Everything/analysis/w33_pass1830_name_the_270.g"

Sp4 := Sp(4,3);;
J   := InvariantBilinearForm(Sp4).matrix;;
N   := Normalizer(GL(4,3), Sp4);;
pts := AsSortedList(Orbit(N, NormedRowVector(One(GF(3)) * [1,0,0,0]), OnLines));;
G   := Image(ActionHomomorphism(N, pts, OnLines));;
D   := DerivedSubgroup(G);;

lines := [];;
for i in [1..40] do for j in [i+1..40] do
  if IsZero(pts[i] * J * pts[j]) then
    AddSet(lines, Set(List([[1,0],[0,1],[1,1],[1,2]], ab ->
      Position(pts, NormedRowVector(ab[1]*pts[i] + ab[2]*pts[j])))));
  fi;
od; od;
lines := Filtered(lines, L -> Length(L) = 4);;

ccl  := ConjugacyClasses(G);;
reps := List(ccl, Representative);;
c270 := First([1..Length(ccl)],
              c -> Size(ccl[c]) = 270 and Order(reps[c]) = 2);;
g := reps[c270];;
Print("the size-270 involution: inner = ", g in D,
      ", centraliser ", Size(Centralizer(G, g)), "\n");

fix := Filtered([1..40], k -> Set(List(lines[k], p -> p^g)) = lines[k]);;
Print("fixed lines : ", fix, "\n");
Print("pairwise intersection sizes : ",
      Set(Concatenation(List([1..Length(fix)], a ->
        List([a+1..Length(fix)], b ->
          Length(Intersection(lines[fix[a]], lines[fix[b]])))))), "\n");
Print("points covered by the 4 fixed lines : ",
      Length(Union(List(fix, k -> lines[k]))), "\n");

orb := Orbit(G, Set(fix), OnSets);;
Print("G-orbit of this 4-line set : size ", Length(orb),
      "   (class size is 270)\n");
Print("stabiliser of the configuration : ",
      Size(Stabilizer(G, Set(fix), OnSets)), "\n");

# is it the transversal set of a skew pair?  BT794/BT795 own that object.
skew := [];;
for a in [1..40] do for b in [a+1..40] do
  if IsEmpty(Intersection(lines[a], lines[b])) then Add(skew, [a,b]); fi;
od; od;
Print("skew pairs (frames) : ", Length(skew), "\n");
trans := function(pr)
  return Filtered([1..40], k ->
    Length(Intersection(lines[k], lines[pr[1]])) = 1 and
    Length(Intersection(lines[k], lines[pr[2]])) = 1);
end;;
tsets := Set(List(skew, pr -> Set(trans(pr))));;
Print("distinct transversal-sets over all 540 frames : ", Length(tsets), "\n");
Print("all of size 4? ", ForAll(tsets, t -> Length(t) = 4), "\n");
Print("is the fixed 4-line set one of them? ", Set(fix) in tsets, "\n");
Print("how many frames share each transversal set : ",
      Set(List(tsets, t -> Number(skew, pr -> Set(trans(pr)) = t))), "\n");

Print("\n=== done ===\n");
QUIT;
