# Passes 1826, 1829, 1830 -- reading the four handedness bits.
#
#  1826.  Pass 1819 found four INDEPENDENT sign bits.  Four independent bits
#         need at least four measurements.  Find a MINIMAL set of conjugacy
#         classes whose values jointly determine all four, and say what those
#         classes are geometrically.  That is a minimal complete set of
#         observables for the substrate's handedness.
#
#  1829.  Pass 1816 showed the 81's bit is readable from one frame's order-96
#         stabiliser.  Res_H(chi) = Res_H(chi.eps) fails exactly when H meets a
#         class where delta_B is nonzero, so the SMALLEST detector of a bit is
#         cyclic, of order min{ord(g) : delta_B(g) <> 0}.  Compute that per
#         block: a hierarchy of locality across the Hodge sectors.
#
#  1830.  Identify the size-270 class -- the square of the order-4 outer
#         540-class (Pass 1820) -- geometrically.  It is currently an unnamed
#         object, which is CLAUDE.md failure mode 3.
#
# Run: bash scripts/run_gap.sh "C:/Repos/Theory of Everything/analysis/w33_pass1826_1829_1830_reading_the_bits.g"

Sp4 := Sp(4,3);;
J   := InvariantBilinearForm(Sp4).matrix;;
N   := Normalizer(GL(4,3), Sp4);;
pts := AsSortedList(Orbit(N, NormedRowVector(One(GF(3)) * [1,0,0,0]), OnLines));;
hom := ActionHomomorphism(N, pts, OnLines);;
G   := Image(hom);;  D := DerivedSubgroup(G);;

edges := [];;
for i in [1..40] do for j in [i+1..40] do
  if IsZero(pts[i] * J * pts[j]) then Add(edges, [i,j]); fi;
od; od;
lines := [];;
for e in edges do
  AddSet(lines, Set(List([[1,0],[0,1],[1,1],[1,2]], ab ->
      Position(pts, NormedRowVector(ab[1]*pts[e[1]] + ab[2]*pts[e[2]])))));
od;
lines := Filtered(lines, L -> Length(L) = 4);;
frames := [];;
for a in [1..40] do for b in [a+1..40] do
  if IsEmpty(Intersection(lines[a], lines[b])) then
    Add(frames, Set([lines[a], lines[b]])); fi;
od; od;
Print("|G| = ", Size(G), ", lines = ", Length(lines),
      ", frames = ", Length(frames), "\n");

irr  := Irr(G);;
ccl  := ConjugacyClasses(G);;
reps := List(ccl, Representative);;
eps  := First(irr, x -> x[1] = 1 and x <> TrivialCharacter(G));;
blocks := [];;
for dg in [15, 24, 30, 81] do
  Add(blocks, First([1..Length(irr)], k -> irr[k][1] = dg
                    and irr[k] <> irr[k] * eps));
od;
Print("chiral blocks (degrees) : ", List(blocks, k -> irr[k][1]), "\n");
deltas := List(blocks, k -> List([1..Length(ccl)],
                                 c -> (irr[k][c] - (irr[k]*eps)[c]) / 2));;

ActFrame := function(f, g) return Set(List(f, L -> Set(List(L, p -> p^g)))); end;;
Geom := function(c)
  local g, tag;
  g := reps[c];
  if g in D then tag := "inner"; else tag := "OUTER"; fi;
  return Concatenation("size ", String(Size(ccl[c])),
    ", order ", String(Order(g)),
    ", ", tag,
    ", fixes ", String(Number([1..40], p -> p^g = p)), " pts / ",
    String(Number(lines, L -> Set(List(L, p -> p^g)) = L)), " lines / ",
    String(Number(frames, f -> ActFrame(f, g) = f)), " frames");
end;;

# ============ Pass 1826: a minimal complete set of observables ============
Print("\n=== Pass 1826: minimal set of classes that reads all four bits ===\n");
supp := Filtered([1..Length(ccl)], c -> ForAny(deltas, d -> d[c] <> 0));;
Print("classes where ANY bit is visible : ", Length(supp), "\n");
for c in supp do
  Print("  class ", c, " [", Geom(c), "]\n       bits (15,24,30,81) = ",
        List(deltas, d -> d[c]), "\n");
od;

best := fail;;
for k in [4 .. Length(supp)] do
  for S in Combinations(supp, k) do
    if RankMat(List(deltas, d -> List(S, c -> d[c]))) = 4 then
      best := S; break; fi;
  od;
  if best <> fail then break; fi;
od;
Print("\nMINIMUM number of classes needed to read all four bits : ",
      Length(best), "\n");
for c in best do Print("   class ", c, " [", Geom(c), "]\n"); od;
nsets := Number(Combinations(supp, Length(best)),
                S -> RankMat(List(deltas, d -> List(S, c -> d[c]))) = 4);;
Print("number of such minimal observable sets : ", nsets, " of ",
      Binomial(Length(supp), Length(best)), "\n");

# ============ Pass 1829: how local is each bit? ============
Print("\n=== Pass 1829: the smallest element that reads each bit ===\n");
Print("Res_H(chi) = Res_H(chi.eps) fails iff H meets a class with delta <> 0,\n");
Print("so the smallest detector of a bit is cyclic of that element's order.\n\n");
vis := [];; ords := [];; m := 0;;      # GAP forbids 'local' inside a for body
for i in [1..4] do
  vis  := Filtered([1..Length(ccl)], c -> deltas[i][c] <> 0);
  ords := List(vis, c -> Order(reps[c]));
  m    := Minimum(ords);
  Print("  degree ", irr[blocks[i]][1], " : visible on ", Length(vis),
        " classes, element orders ", Set(ords), "\n");
  Print("      smallest detector : cyclic of order ", m, "  -> ",
        Geom(vis[Position(ords, m)]), "\n");
od;

# does one element read ALL four at once?
allf := Filtered([1..Length(ccl)], c -> ForAll(deltas, d -> d[c] <> 0));;
Print("\n  classes reading ALL FOUR bits simultaneously : ", Length(allf), "\n");
for c in allf do
  Print("      class ", c, " [", Geom(c), "]  bits = ",
        List(deltas, d -> d[c]), "\n");
od;

# ============ Pass 1830: name the 270-class ============
Print("\n=== Pass 1830: the size-270 class ===\n");
for c in Filtered([1..Length(ccl)], c -> Size(ccl[c]) = 270) do
  Print("  class ", c, " [", Geom(c), "]\n");
  Print("      centraliser order ", Size(Centralizer(G, reps[c])), "\n");
  Print("      bits (15,24,30,81) here = ", List(deltas, d -> d[c]), "\n");
  Print("      is it a square? ", ForAny([1..Length(ccl)],
        d -> (reps[d])^2 in ccl[c]), "\n");
od;

Print("\n=== done ===\n");
QUIT;
