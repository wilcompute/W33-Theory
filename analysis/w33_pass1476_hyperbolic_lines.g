# Passes 1476-1477: identify the degree-90 on the 90 HYPERBOLIC LINES, and
# determine which extension of the Steinberg the harmonic sector carries.
LogTo();
out := "C:/Repos/Theory of Everything/data/w33_pass1476_1477.txt";
PrintTo(out, "Passes 1476-1477: the 90, and which 81\n\n");
A := function(s) AppendTo(out, s); end;
SP4  := Sp(4,3);
pts  := Orbit(SP4, NormedRowVector([1,0,0,0]*Z(3)^0), OnLines);
Gp   := Action(SP4, pts, OnLines);
form := function(u,v) return u[1]*v[4]-u[4]*v[1]+u[2]*v[3]-u[3]*v[2]; end;
zero := Zero(GF(3));
adj  := List([1..40], i -> Filtered([1..40], j -> j<>i and form(pts[i],pts[j])=zero));
lines := [];
for i in [1..40] do for j in adj[i] do if j>i then
  AddSet(lines, Set(Filtered([1..40], m -> pts[m] in
    List(Filtered(Elements(VectorSpace(GF(3),[pts[i],pts[j]])),
                  v -> v <> Zero(pts[i])), NormedRowVector))));
fi; od; od;
GLin := Image(ActionHomomorphism(Gp, lines, OnSets));
Full := Normalizer(SymmetricGroup(40), GLin);

# A HYPERBOLIC LINE of W(3,3): a 2-space on which the form is NONdegenerate.
# Its 4 projective points are pairwise NON-collinear. So: 4-subsets of points
# that are pairwise non-adjacent AND span a 2-space.  Equivalently the 90 such
# lines are the non-totally-isotropic 2-spaces, count (40*39/2 - ...) -- build
# them as spans of two non-collinear points and keep those of size 4.
hyp := [];
for i in [1..40] do
  for j in [i+1..40] do
    if not (j in adj[i]) then
      AddSet(hyp, Set(Filtered([1..40], m -> pts[m] in
        List(Filtered(Elements(VectorSpace(GF(3),[pts[i],pts[j]])),
                      v -> v <> Zero(pts[i])), NormedRowVector))));
    fi;
  od;
od;
hyp := Filtered(hyp, L -> Length(L) = 4);
A(Concatenation("hyperbolic lines (nondegenerate 2-spaces): ",
   String(Length(hyp)), "   (expect 90)\n"));
if Length(hyp) = 90 then
  act90 := Action(Gp, hyp, OnSets);
  A(Concatenation("  transitive on the 90? ", String(IsTransitive(act90,[1..90])),
     "   |image| = ", String(Size(act90)), "\n"));
  tbl := CharacterTable(Gp); ccl := ConjugacyClasses(tbl);
  chi := List(ccl, c -> Number([1..90],
           i -> OnSets(hyp[i], Representative(c)) = hyp[i]));
  dec := MatScalarProducts(tbl, Irr(tbl), [ClassFunction(tbl, chi)])[1];
  us := Filtered([1..Length(dec)], i -> dec[i] <> 0);
  A(Concatenation("  90-point permutation character over PSp: ",
     String(List(us, i -> [Irr(tbl)[i][1], dec[i]])), "\n"));
  # and over the FULL group, where the degree-90 irreducible lives
  hypF := Action(Full, hyp, OnSets);
  tblF := CharacterTable(Full); cclF := ConjugacyClasses(tblF);
  chiF := List(cclF, c -> Number([1..90],
            i -> OnSets(hyp[i], PreImagesRepresentative(
                   ActionHomomorphism(Full, hyp, OnSets), Representative(c))) = hyp[i]));
  A("  (full-group decomposition attempted separately)\n");
fi;

# ---- Pass 1477: which extension of the Steinberg?
A("\n=== Pass 1477: the two degree-81 extensions ===\n");
tblF := CharacterTable(Full);
i81 := Filtered([1..Length(Irr(tblF))], i -> Irr(tblF)[i][1] = 81);
A(Concatenation("  degree-81 irreducibles in PGSp: ", String(Length(i81)), "\n"));
for i in i81 do
  A(Concatenation("    chi_", String(i), " on the identity = ",
    String(Irr(tblF)[i][1]),
    "; value on an OUTER class shows which extension it is\n"));
od;
A("  (identifying WHICH one the harmonic space carries needs the harmonic\n");
A("   character computed over the FULL group, i.e. the signed action extended\n");
A("   to PGSp -- stated as the next computation, not asserted here.)\n");
A("\nDONE\n");
QUIT;
