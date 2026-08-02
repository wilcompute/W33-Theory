# Pass 2436 -- the two 6:1 fibrations over 40 are C6 and S3, and the difference IS sigma_S.
#
# Pass 1021 (mine)          : 240 E8 roots        -> 40 W(3,3) POINTS, fibre = Eisenstein units = C6
# Pass 2308 (parallel track): 240 signed dual cws -> 40 Q(4,3)  POINTS = W(3,3) LINES, fibre = S3
#
# Both order 6.  Both regular (torsors).  C6 abelian, S3 nonabelian.
# HYPOTHESIS: the antipodal map w -> -w is CENTRAL in the C6 fibre and NON-CENTRAL in the
# S3 fibre, i.e. the line-side involution INVERTS its C3 exactly as sigma_S conjugates J to -J
# (my Pass 2076).  If so the two fibrations are not exchanged by any duality, and the
# obstruction is the same one.

Print("=== Pass 2436: C6 vs S3, the two 6:1 fibrations over 40 ===\n\n");

Read(Concatenation(GAPInfo.SystemEnvironment.W33_REPO,"/analysis/_tmp_probe2308_abs.g"));;

G   := Probe2308Code.group240;;
SW  := Probe2308Code.signedWords;;
FB  := Probe2308Code.fibers6;;
QAD := Probe2308Code.quotientAdjacency;;

Print("[A] the code-side fibre group\n");
F := FB[1];;
S := Stabilizer(G, F, OnSets);;
h := ActionHomomorphism(S, F, OnPoints);;
I := Image(h);;
Print("    |G| = ", Size(G), "   fibres = ", Length(FB), "   |fibre| = ", Length(F), "\n");
Print("    setwise stabiliser |S| = ", Size(S), "   kernel = ", Size(Kernel(h)), "\n");
Print("    induced group on the fibre : ", StructureDescription(I),
      "   order ", Size(I), "   regular = ", IsRegular(I, [1..6]), "\n");

# the antipodal map INSIDE this fibre
neg := PermList(List([1..6], i -> Position(F, Position(SW, -SW[F[i]]))));;
Print("    antipodal map on the fibre : ", List([1..6], i -> i^neg),
      "   order ", Order(neg), "\n");
Print("    antipodal in the induced group ? ", neg in I, "\n");
cen := ForAll(GeneratorsOfGroup(I), g -> g*neg = neg*g);;
Print("    antipodal CENTRAL in the induced group ? ", cen, "\n");
Print("    centre of the induced group : ", StructureDescription(Centre(I)),
      "   order ", Size(Centre(I)), "\n\n");

Print("[B] the root-side fibre group, for contrast\n");
# Pass 1021: the fibre is the Eisenstein unit group <c^5> = Z6 acting by multiplication.
# A C6-torsor: build it abstractly and ask the same question.
C6 := CyclicGroup(IsPermGroup, 6);;
reg6 := Image(RegularActionHomomorphism(C6));;
z := First(Elements(reg6), g -> Order(g) = 2);;
Print("    C6 acting regularly on 6 points : ", StructureDescription(reg6),
      "   regular = ", IsRegular(reg6, [1..6]), "\n");
Print("    its unique involution (= multiplication by -1 = the antipodal map)\n");
Print("    CENTRAL in the induced group ? ",
      ForAll(GeneratorsOfGroup(reg6), g -> g*z = z*g), "\n");
Print("    centre of C6 : ", StructureDescription(Centre(reg6)),
      "   order ", Size(Centre(reg6)), "\n\n");

Print("[C] the two bases are NOT isomorphic (q odd)\n");
# W(3,3) point graph, from the symplectic form on F_3^4
raw := Filtered(Tuples([0,1,2], 4), v -> v <> [0,0,0,0]);;
pts := Filtered(raw, v -> v[PositionProperty(v, x -> x <> 0)] = 1);;
Wadj := List([1..40], i -> List([1..40], j -> i <> j and
   RemInt(pts[i][1]*pts[j][2] - pts[i][2]*pts[j][1]
        + pts[i][3]*pts[j][4] - pts[i][4]*pts[j][3], 3) = 0));;
srg := function(a)
  local k, lam, mu, i, j, c;
  k := Number([1..40], j -> a[1][j]);
  lam := 0; mu := 0;
  for j in [2..40] do
    c := Number([1..40], m -> a[1][m] and a[j][m]);
    if a[1][j] then lam := c; else mu := c; fi;
  od;
  return [40, k, lam, mu];
end;;
Print("    W(3,3)  point graph parameters : ", srg(Wadj), "\n");
Print("    Q(4,3)  quotient   parameters : ", srg(QAD), "\n");
Print("    same parameters, and Pass 2308 measured them NON-isomorphic.\n");
Print("    classical reason: W(q) = Q(4,q) iff q is EVEN.  q = 3 is odd.\n\n");

Print("[D] the ladder\n");
Print("    q odd          <=> W(q) not iso Q(4,q)      (point/line asymmetry)\n");
Print("    q odd          <=> a non-square multiplier exists  <=> sigma_S exists\n");
Print("    q = 3 mod 4    <=> mu = -1 available  <=> sigma_S is multiplication by i\n");
Print("    q = 3 mod 4    <=> PSp(4,q) has complex characters (Gow 1985)\n");
QUIT;
