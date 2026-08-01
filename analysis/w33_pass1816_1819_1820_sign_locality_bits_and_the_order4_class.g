# Passes 1816, 1819, 1820 -- three questions about the handedness found in
# Passes 1615-1616.
#
#  1816.  Is the sign a LOCAL observable?  It is detected on the 540 frames and
#         the 36 spreads.  Restrict the two degree-81 extensions to a single
#         frame stabiliser (order 96) and a single spread stabiliser (order
#         1440).  If the restrictions differ, one frame's worth of symmetry
#         already sees the sign; if they agree, the sign is global-only.
#
#  1819.  How many handedness BITS?  Four blocks (15, 24, 30, 81) are chiral.
#         Are their signs four independent bits or one bit repeated?  The
#         difference functions delta_B = (chi_B - chi_B^eps)/2 span a space
#         whose dimension is the answer.
#
#  1820.  There are TWO conjugacy classes of size 540: one of order 2 (BT773's,
#         which carries the sign) and one of order 4 (which cancels).  Identify
#         the order-4 class geometrically and find what its square is.
#
# Run: bash scripts/run_gap.sh "C:/Repos/Theory of Everything/analysis/w33_pass1816_1819_1820_sign_locality_bits_and_the_order4_class.g"

Sp4 := Sp(4,3);;
J   := InvariantBilinearForm(Sp4).matrix;;
N   := Normalizer(GL(4,3), Sp4);;
pts := AsSortedList(Orbit(N, NormedRowVector(One(GF(3)) * [1,0,0,0]), OnLines));;
hom := ActionHomomorphism(N, pts, OnLines);;
G   := Image(hom);;  D := DerivedSubgroup(G);;
Print("|G| = ", Size(G), ", |G'| = ", Size(D), "\n");

# ---- points, lines, edges, frames
edges := [];;
for i in [1..40] do for j in [i+1..40] do
  if IsZero(pts[i] * J * pts[j]) then Add(edges, [i,j]); fi;
od; od;

lines := [];;
for e in edges do
  span := Set(Concatenation(List([[1,0],[0,1],[1,1],[1,2]], ab ->
      [Position(pts, NormedRowVector(ab[1]*pts[e[1]] + ab[2]*pts[e[2]]))])));
  AddSet(lines, span);
od;
lines := Filtered(lines, L -> Length(L) = 4);;
Print("lines = ", Length(lines), ", edges = ", Length(edges), "\n");

frames := [];;
for a in [1..Length(lines)] do
  for b in [a+1..Length(lines)] do
    if IsEmpty(Intersection(lines[a], lines[b])) then
      Add(frames, Set([lines[a], lines[b]]));
    fi;
  od;
od;
Print("frames = ", Length(frames), "\n\n");

irr := Irr(G);;
eps := First(irr, x -> x[1] = 1 and x <> TrivialCharacter(G));;
e81 := Filtered([1..Length(irr)], k -> irr[k][1] = 81);;
Print("degree-81 irreducibles : ", e81, "\n");

# ================= Pass 1816: is the sign local? =================
Print("\n=== Pass 1816: is the sign visible from ONE frame / ONE spread? ===\n");

ActFrame := function(f, g) return Set(List(f, L -> Set(List(L, p -> p^g)))); end;;
Sf := Stabilizer(G, frames[1], ActFrame);;
Print("frame stabiliser order        : ", Size(Sf),
      "   (51840/540 = ", 51840/540, ")\n");
Print("  contained in PSp?           : ", IsSubgroup(D, Sf), "\n");

TestLocal := function(H, label)
  local r1, r2, same;
  r1 := RestrictedClassFunction(irr[e81[1]], H);
  r2 := RestrictedClassFunction(irr[e81[2]], H);
  same := r1 = r2;
  Print("  ", label, ": Res(81a) = Res(81b) ? ", same, "\n");
  if same then
    Print("    -> the sign is INVISIBLE to this subgroup (global-only here)\n");
  else
    Print("    -> the sign IS visible from this subgroup alone (LOCAL)\n");
    Print("    Res(81a) decomposes with ", Length(Filtered(
      MatScalarProducts(Irr(H), [r1])[1], x -> x <> 0)), " constituents; ",
      "Res(81b) with ", Length(Filtered(
      MatScalarProducts(Irr(H), [r2])[1], x -> x <> 0)), "\n");
  fi;
  return same;
end;;
TestLocal(Sf, "frame stabiliser (order 96)");

# spread stabiliser: the size-36 outer involution class has centraliser 1440
ccl := ConjugacyClasses(G);;  reps := List(ccl, Representative);;
i36 := First([1..Length(ccl)],
             c -> Size(ccl[c]) = 36 and Order(reps[c]) = 2);;
Csp := Centralizer(G, reps[i36]);;
Print("spread-related subgroup order : ", Size(Csp), "\n");
Print("  contained in PSp?           : ", IsSubgroup(D, Csp), "\n");
TestLocal(Csp, "spread stabiliser (order 1440)");

# and a control: a subgroup INSIDE PSp cannot see the sign, by construction
Sfi := Intersection(Sf, D);;
Print("control, Sf cap PSp order     : ", Size(Sfi), "\n");
TestLocal(Sfi, "frame stabiliser INSIDE PSp");

# ================= Pass 1819: how many handedness bits =================
Print("\n=== Pass 1819: how many independent handedness bits? ===\n");
blocks := [6, 14, 15, 24];;      # the four chiral constituents of V
Print("chiral blocks (degrees) : ", List(blocks, k -> irr[k][1]), "\n");
deltas := List(blocks, k -> List([1..Length(ccl)],
                                 c -> (irr[k][c] - (irr[k]*eps)[c]) / 2));;
Print("delta_B supports (number of classes where B's sign shows):\n");
for i in [1..Length(blocks)] do
  Print("  degree ", irr[blocks[i]][1], " : ",
        Number(deltas[i], x -> x <> 0), " classes\n");
od;
Print("rank of the 4 x ", Length(ccl), " matrix of sign-differences : ",
      RankMat(deltas), "\n");
if RankMat(deltas) = 1 then
  Print("  -> ONE bit: all four blocks flip together.\n");
else
  Print("  -> ", RankMat(deltas), " INDEPENDENT bits: the blocks can be ",
        "signed separately,\n     so V's handedness is not a single scalar.\n");
fi;
Print("pairwise equal? ");
for i in [1..4] do for j in [i+1..4] do
  if deltas[i] = deltas[j] then
    Print("(", irr[blocks[i]][1], "=", irr[blocks[j]][1], ") "); fi;
od; od;
Print("\n");

# ================= Pass 1820: the order-4 class of size 540 =================
Print("\n=== Pass 1820: the two size-540 classes ===\n");
f540 := Filtered([1..Length(ccl)], c -> Size(ccl[c]) = 540);;
for c in f540 do
  g := reps[c];
  Print("class ", c, "  order ", Order(g), "  inner: ", g in D, "\n");
  Print("    fixed points : ", Number([1..40], p -> p^g = p), "\n");
  Print("    fixed lines  : ", Number(lines, L -> Set(List(L, p -> p^g)) = L),
        "\n");
  Print("    fixed frames : ", Number(frames, f -> ActFrame(f, g) = f), "\n");
  Print("    centraliser  : ", Size(Centralizer(G, g)), "\n");
  if Order(g) = 4 then
    Print("    g^2 lies in class ", First([1..Length(ccl)],
          d -> g^2 in ccl[d]), " of size ",
          Size(ccl[First([1..Length(ccl)], d -> g^2 in ccl[d])]),
          " and order ", Order(g^2), "\n");
  fi;
od;

# ================= certificate =================
JF := "C:/Repos/Theory of Everything/data/w33_pass1816_1819_1820_sign_locality.json";;
fh := OutputTextFile(JF, false);;
SetPrintFormattingStatus(fh, false);   # else GAP wraps with a backslash and the
                                       # JSON is unparseable
Pr := function(s) AppendTo(fh, s); end;;
Res81 := function(H) return RestrictedClassFunction(irr[e81[1]], H)
                          = RestrictedClassFunction(irr[e81[2]], H); end;;
Pr("{\n");
Pr(Concatenation("  \"group_order\": ", String(Size(G)), ",\n"));
Pr(Concatenation("  \"frame_stab_order\": ", String(Size(Sf)),
   ", \"frame_stab_sees_sign\": ", String(not Res81(Sf)), ",\n"));
Pr(Concatenation("  \"spread_stab_order\": ", String(Size(Csp)),
   ", \"spread_stab_sees_sign\": ", String(not Res81(Csp)), ",\n"));
Pr(Concatenation("  \"control_frame_stab_in_PSp_order\": ", String(Size(Sfi)),
   ", \"control_sees_sign\": ", String(not Res81(Sfi)), ",\n"));
Pr(Concatenation("  \"chiral_block_degrees\": ",
   String(List(blocks, k -> irr[k][1])), ",\n"));
Pr(Concatenation("  \"handedness_bits\": ", String(RankMat(deltas)), ",\n"));
Pr("  \"size540_classes\": [");
Pr(JoinStringsWithSeparator(List(f540, c -> Concatenation(
   "{\"class\": ", String(c),
   ", \"order\": ", String(Order(reps[c])),
   ", \"inner\": ", String(reps[c] in D),
   ", \"fixed_points\": ", String(Number([1..40], p -> p^(reps[c]) = p)),
   ", \"fixed_lines\": ", String(Number(lines,
        L -> Set(List(L, p -> p^(reps[c]))) = L)),
   ", \"fixed_frames\": ", String(Number(frames,
        f -> ActFrame(f, reps[c]) = f)),
   ", \"centraliser\": ", String(Size(Centralizer(G, reps[c]))),
   ", \"square_class_size\": ", String(Size(ccl[First([1..Length(ccl)],
        d -> (reps[c])^2 in ccl[d])])), "}")), ", "));
Pr("]\n}\n");
CloseStream(fh);
Print("\nwrote data/w33_pass1816_1819_1820_sign_locality.json\n");

Print("\n=== done ===\n");
QUIT;
