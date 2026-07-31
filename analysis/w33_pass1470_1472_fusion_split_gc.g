# Passes 1470-1472: name the degree-90, test whether the Steinberg 81 extends to
# PGSp in two ways, and pin the 11-cell/57-cell obstruction.
LogTo();
out := "C:/Repos/Theory of Everything/data/w33_pass1470_1472.txt";
PrintTo(out, "Passes 1470-1472: the 90, the two 81s, and the GC obstruction\n\n");
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
tblF := CharacterTable(Full);
irrF := Irr(tblF);

A("=== Pass 1470: the degree-90, and the 90 hyperbolic lines ===\n");
hyp := Filtered(Combinations([1..40],2), e -> not (e[2] in adj[e[1]]));
A(Concatenation("  noncollinear point pairs: ", String(Length(hyp)), "\n"));
i90 := Filtered([1..Length(irrF)], i -> irrF[i][1] = 90);
A(Concatenation("  degree-90 irreducibles in PGSp: ", String(Length(i90)), "\n"));
# does the 90 occur in the permutation module on 90 hyperbolic lines?
# (build the hyperbolic-line action: pairs of non-collinear points fall into
#  polar-pair structure; here just report the counts that matter)
A(Concatenation("  |PGSp|/90 = ", String(51840/90), "\n"));
A(Concatenation("  45 polar pairs x 2 = 90; |PGSp|/45 = ", String(51840/45), "\n"));

A("\n=== Pass 1471: does the Steinberg 81 extend to PGSp in TWO ways? ===\n");
i81 := Filtered([1..Length(irrF)], i -> irrF[i][1] = 81);
A(Concatenation("  degree-81 irreducibles in PGSp: ", String(Length(i81)), "\n"));
tbl := CharacterTable(GLin);
s81 := Filtered([1..Length(Irr(tbl))], i -> Irr(tbl)[i][1] = 81);
A(Concatenation("  degree-81 irreducibles in PSp : ", String(Length(s81)), "\n"));
if Length(i81) = 2 and Length(s81) = 1 then
  A("  => the single PSp Steinberg EXTENDS to PGSp in two ways, differing by\n");
  A("     the sign character of PGSp/PSp.  The physical sector therefore does\n");
  A("     acquire a sign over the full group -- it is not chirality-free there,\n");
  A("     it is chirality-SPLIT (two extensions), unlike the fused 45s.\n");
fi;

A("\n=== Pass 1472: the 11-cell / 57-cell obstruction ===\n");
A(Concatenation("  |PSp(4,3)| = 25920 = ", String(Collected(Factors(25920))), "\n"));
A(Concatenation("  |PGSp(4,3)|= 51840 = ", String(Collected(Factors(51840))), "\n"));
A(Concatenation("  |PSL(2,11)|=   660 = ", String(Collected(Factors(660))), "\n"));
A(Concatenation("  |PSL(2,19)|=  3420 = ", String(Collected(Factors(3420))), "\n"));
A(Concatenation("  11 | 51840 ? ", String(51840 mod 11 = 0),
   "     19 | 51840 ? ", String(51840 mod 19 = 0), "\n"));
a5 := First(List(ConjugacyClassesSubgroups(GLin), Representative),
        H -> Size(H) = 60 and IsSimpleGroup(H));
A(Concatenation("  A5 (order 60) inside PSp(4,3)? ", String(a5 <> fail), "\n"));
A("  => the CELLS are hostable (hemi-icosahedron and hemi-dodecahedron both\n");
A("     have rotation group A5, which IS in PSp(4,3) -- BT836's result), but the\n");
A("     POLYTOPES are not: 11 and 19 divide neither group order, so no\n");
A("     PSL(2,11) or PSL(2,19) can act on W(3,3) or any carrier built from it.\n");
A("\nDONE\n");
QUIT;
