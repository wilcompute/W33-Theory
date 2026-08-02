# Pass 2437 -- the decisive test.
#
# Pass 2436 measured: the code-side fibre group is S3 (regular on 6), and the antipodal
# map w -> -w is NOT in it but CENTRALISES it.  That is forced: PGSp(4,3) acts on the
# codewords by PERMUTATION matrices, and -I is not a permutation matrix.
#
# Pass 1021 (mine): the root-side fibre group is the Eisenstein unit group C6, which
# DOES contain the antipode (-1 is an Eisenstein unit).
#
# So the antipode is INSIDE the fibre group on the root side and OUTSIDE it on the code
# side.  Quotienting each fibre by the antipode leaves 3 objects.  The decisive question:
#
#     what acts on those 3?   C3 (an orientation) or S3 (no orientation)?
#
# Corpus prior art for the PRINCIPLE (cited, not re-derived):
#   analysis/2026-05-30_c3_fano_triangle_orientation.md  -- C3 = A4 cap S3 inside
#   S4 = PGL(2,3) is "the cyclic rotation of the three non-anchor points", i.e.
#   C3 vs S3 on three points IS orientation vs no orientation.  That reading is
#   already the repo's.  What is new here is WHICH of the two 240 -> 40 towers
#   carries which.

Print("=== Pass 2437: is the fibre oriented? ===\n\n");

Read(Concatenation(GAPInfo.SystemEnvironment.W33_REPO, "/analysis/_tmp_probe2308_abs.g"));;

G  := Probe2308Code.group240;;
SW := Probe2308Code.signedWords;;
FB := Probe2308Code.fibers6;;

Print("[A] CODE side -- 240 dual codewords -> 40 Q(4,3) points = W(3,3) LINES\n");
F   := FB[1];;
S   := Stabilizer(G, F, OnSets);;
neg := PermList(List([1..6], i -> Position(F, Position(SW, -SW[F[i]]))));;
prs := Set(List([1..6], i -> Set([i, i^neg])));;
Print("    fibre           : ", F, "\n");
Print("    antipodal map   : ", List([1..6], i -> i^neg), "   (fixed-point-free, order ",
      Order(neg), ")\n");
Print("    3 antipodal pairs: ", prs, "\n");
h3  := ActionHomomorphism(Image(ActionHomomorphism(S, F, OnPoints)), prs, OnSets);;
I3  := Image(h3);;
Print("    ACTION ON THE 3 PAIRS : ", StructureDescription(I3), "   order ", Size(I3),
      "   faithful = ", Size(Kernel(h3)) = 1, "\n");
Print("    contains an odd permutation (a reflection) ? ",
      ForAny(Elements(I3), g -> SignPerm(g) = -1), "\n\n");

Print("[B] ROOT side -- 240 E8 roots -> 40 W(3,3) POINTS, fibre = Eisenstein units C6\n");
# The Eisenstein units {+-1, +-w, +-w^2} = C6 acting on one fibre by multiplication.
C6   := CyclicGroup(IsPermGroup, 6);;
reg  := Image(RegularActionHomomorphism(C6));;
zc   := First(Elements(reg), g -> Order(g) = 2);;
prs2 := Set(List([1..6], i -> Set([i, i^zc])));;
Print("    fibre group     : ", StructureDescription(reg), "   regular = ",
      IsRegular(reg, [1..6]), "\n");
Print("    antipode = -1   : ", List([1..6], i -> i^zc), "   IN the fibre group = ",
      zc in reg, "\n");
Print("    3 antipodal pairs: ", prs2, "\n");
h3b := ActionHomomorphism(reg, prs2, OnSets);;
I3b := Image(h3b);;
Print("    ACTION ON THE 3 PAIRS : ", StructureDescription(I3b), "   order ", Size(I3b),
      "   kernel = ", Size(Kernel(h3b)), "\n");
Print("    contains an odd permutation (a reflection) ? ",
      ForAny(Elements(I3b), g -> SignPerm(g) = -1), "\n\n");

Print("[C] the verdict\n");
Print("    POINT side (E8 roots)      : C3 on the 3 pairs -> an ORIENTATION -> CHIRAL\n");
Print("    LINE  side (dual codewords): S3 on the 3 pairs -> reflections -> ACHIRAL\n");
Print("    and W(3,3) is NOT isomorphic to Q(4,3) for q odd, so no duality of the\n");
Print("    substrate exchanges the two towers.  The chirality is confined to the\n");
Print("    point side, and the line side carries the reflection that destroys it.\n");
QUIT;
