# Pass 1442-1443 -- what the C2 cover involution IS, and an independent check of
# the parallel track's M20 chart.
#
# Their Pass 1505 census says 83% of exact covers lie in C2 orbits, and a
# C2-stabilised cover fixes twelve of its sixty frames.  Two questions follow,
# and the first has a candidate answer already sitting in the corpus.
#
# BT773 proves the 540 frames are in bijection with the 540 3A1 involutions of
# PSp(4,3) -- "540 cubes in W(3,3), one per 3A1 involution".  So a cover of 60
# frames IS a set of 60 involutions, and the involution STABILISING a C2 cover is
# itself an element of PSp(4,3).  The sharp question: is the stabilising
# involution one of the 540?  I.e. does a C2-stabilised cover single out a frame?
#
# Their Pass 1509 separately claims five independent three-resolution packets
# generating an H(5,3) chart of 243 covers with setwise stabiliser 2^4:A5 = M20.
# 243 = 3^5 and |2^4:A5| = 960.  The arithmetic is checkable here.

LogTo();
out := "C:/Repos/Theory of Everything/data/w33_pass1442_1443.txt";
PrintTo(out, "Passes 1442-1443: the C2 involution, and the M20 arithmetic\n\n");
A := function(s) AppendTo(out, s); end;

SP4  := Sp(4,3);
pts  := Orbit(SP4, NormedRowVector([1,0,0,0]*Z(3)^0), OnLines);
Gp   := Action(SP4, pts, OnLines);
form := function(u,v)
  return u[1]*v[4] - u[4]*v[1] + u[2]*v[3] - u[3]*v[2];
end;
zero := Zero(GF(3));
adj  := List([1..40], i -> Filtered([1..40],
          j -> j <> i and form(pts[i], pts[j]) = zero));
lines := [];
for i in [1..40] do
  for j in adj[i] do
    if j > i then
      AddSet(lines, Set(Filtered([1..40], m -> pts[m] in
        List(Filtered(Elements(VectorSpace(GF(3), [pts[i], pts[j]])),
                      v -> v <> Zero(pts[i])), NormedRowVector))));
    fi;
  od;
od;
lineAct := ActionHomomorphism(Gp, lines, OnSets);
GLin    := Image(lineAct);
frames  := Filtered(Combinations([1..40], 2),
             p -> Intersection(lines[p[1]], lines[p[2]]) = []);
A(Concatenation("frames: ", String(Length(frames)), "\n"));

frAct := ActionHomomorphism(GLin, frames, OnSets);
GF540 := Image(frAct);
A(Concatenation("|G on frames| = ", String(Size(GF540)), "\n\n"));

# ---------------------------------- BT773's bijection: frames <-> 3A1 involutions
A("=== BT773 check: are there 540 involutions matching the 540 frames? ===\n");
invs := Filtered(ConjugacyClasses(GLin),
          c -> Order(Representative(c)) = 2);
A(Concatenation("  involution classes in PSp(4,3): ",
   String(List(invs, Size)), "\n"));
c540 := Filtered(invs, c -> Size(c) = 540);
A(Concatenation("  classes of size exactly 540: ", String(Length(c540)),
   "   (BT773 predicts one)\n"));
if Length(c540) >= 1 then
  # the map: an involution <-> its fixed frame?
  t := Representative(c540[1]);
  fixedFr := Filtered([1..Length(frames)], i -> i^Image(frAct, t) = i);
  A(Concatenation("  a 540-class involution fixes ", String(Length(fixedFr)),
     " frames\n"));
fi;

# ------------------------------------- Pass 1442: the C2 cover's involution
A("\n=== Pass 1442: the involution stabilising a C2 cover ===\n");
covers := [];
inp := "C:/Repos/Theory of Everything/data/w33_pass1398_cover_sample.txt";
if IsExistingFile(inp) then Read(inp); covers := coverSamples; fi;
A(Concatenation("  cover samples: ", String(Length(covers)), "\n"));
for c in covers do
  S := Stabilizer(GF540, Set(c), OnSets);
  if Size(S) = 2 then
    g := First(Elements(S), x -> Order(x) = 2);
    cls := First([1..Length(invs)],
             k -> ForAny(Elements(invs[k]), y -> Image(frAct, y) = g));
    fixAll := Number([1..Length(frames)], i -> i^g = i);
    fixIn  := Number(c, f -> f^g = f);
    A(Concatenation("    C2 cover: its involution fixes ", String(fixAll),
      " of the 540 frames, ", String(fixIn), " of the cover's 60\n"));
    A(Concatenation("      involution class size in PSp(4,3): ",
      String(Size(invs[cls])), "\n"));
    A(Concatenation("      IS IT A 3A1 (class size 540)? ",
      String(Size(invs[cls]) = 540), "\n"));
  fi;
od;

# --------------------------------------- Pass 1443: the M20 arithmetic
A("\n=== Pass 1443: their M20 = 2^4:A5 chart, arithmetic only ===\n");
M20 := Filtered(List(ConjugacyClassesSubgroups(GLin), Representative),
         H -> Size(H) = 960);
A(Concatenation("  subgroups of order 960 in PSp(4,3) (up to conj): ",
   String(Length(M20)), "\n"));
for H in M20 do
  A(Concatenation("    ", StructureDescription(H), "  IdGroup ",
     String(IdGroup(H)), "   index ", String(Index(GLin, H)), "\n"));
  A(Concatenation("      is 2^4:A5? ", String(IdGroup(H) = [960, 11357]),
     "   |2^4:A5| = 16*60 = 960\n"));
od;
A(Concatenation("  243 = 3^5 ? ", String(3^5 = 243), "\n"));
A("  (the 243-cover H(5,3) chart itself is their computation, not reproduced)\n");

A("\nDONE\n");
QUIT;
