# Passes 1466-1468: name the coexact block, test the two 45s for an outer swap,
# and ask the C2/12 question representation-theoretically.
LogTo();
out := "C:/Repos/Theory of Everything/data/w33_pass1466_1468.txt";
PrintTo(out, "Passes 1466-1468: the 30+45+45 block, outer swap, and the C2\n\n");
A := function(s) AppendTo(out, s); end;
SP4  := Sp(4,3);
pts  := Orbit(SP4, NormedRowVector([1,0,0,0]*Z(3)^0), OnLines);
Gp   := Action(SP4, pts, OnLines);
form := function(u,v) return u[1]*v[4]-u[4]*v[1]+u[2]*v[3]-u[3]*v[2]; end;
zero := Zero(GF(3));
adj  := List([1..40], i -> Filtered([1..40], j -> j<>i and form(pts[i],pts[j])=zero));
edges := Filtered(Combinations([1..40],2), e -> e[2] in adj[e[1]]);
tbl := CharacterTable(Gp);
irr := Irr(tbl);
A("=== Pass 1466: degrees present in PSp(4,3) ===\n");
A(Concatenation("  all irreducible degrees: ",
   String(SortedList(List(irr, x -> x[1]))), "\n"));
d45 := Filtered([1..Length(irr)], i -> irr[i][1] = 45);
d30 := Filtered([1..Length(irr)], i -> irr[i][1] = 30);
A(Concatenation("  degree-45 irreducibles: ", String(Length(d45)),
   "   degree-30: ", String(Length(d30)), "\n"));

# ---- Pass 1467: does the OUTER automorphism swap the two 45s?
A("\n=== Pass 1467: outer automorphism on the two degree-45 irreducibles ===\n");
lines := [];
for i in [1..40] do for j in adj[i] do if j>i then
  AddSet(lines, Set(Filtered([1..40], m -> pts[m] in
    List(Filtered(Elements(VectorSpace(GF(3),[pts[i],pts[j]])),
                  v -> v <> Zero(pts[i])), NormedRowVector))));
fi; od; od;
GLin := Image(ActionHomomorphism(Gp, lines, OnSets));
Full := Normalizer(SymmetricGroup(40), GLin);
A(Concatenation("  |PSp| = ", String(Size(GLin)),
   "   |PGSp| = ", String(Size(Full)), "\n"));
tblF := CharacterTable(Full);
degF := SortedList(List(Irr(tblF), x -> x[1]));
A(Concatenation("  PGSp irreducible degrees: ", String(degF), "\n"));
A(Concatenation("  a degree-90 irreducible in PGSp? ",
   String(90 in degF), "\n"));
A("  (two PSp-45s FUSED by the outer element would appear as one 90 in PGSp;\n");
A("   two separate 45s in PGSp would mean each extends and they are NOT swapped)\n");
A(Concatenation("  number of degree-45 irreducibles in PGSp: ",
   String(Number(Irr(tblF), x -> x[1] = 45)), "\n"));

# ---- Pass 1468: the class-45 involution against the two 45s
A("\n=== Pass 1468: the cover-stabilising involution vs the degree-45 chars ===\n");
for cl in ConjugacyClasses(Gp) do
  if Order(Representative(cl)) = 2 and Size(cl) = 45 then
    A(Concatenation("  class-45 involution: chi values on it = ",
      String(List(d45, i -> irr[i][Position(ConjugacyClasses(tbl), cl)])), "\n"));
  fi;
od;
A("\nDONE\n");
QUIT;
