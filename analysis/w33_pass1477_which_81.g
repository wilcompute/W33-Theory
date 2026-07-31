# Pass 1477 -- WHICH extension of the Steinberg does the harmonic sector carry?
# The 81 splits into two PGSp-irreducibles differing by the sign character. The
# harmonic space is a concrete subspace of the SIGNED edge module, so extend the
# signed action to PGSp and read its character there.
LogTo();
out := "C:/Repos/Theory of Everything/data/w33_pass1477_which_81.txt";
PrintTo(out, "Pass 1477: which degree-81 extension the harmonic sector carries\n\n");
A := function(s) AppendTo(out, s); end;
SP4  := Sp(4,3);
pts  := Orbit(SP4, NormedRowVector([1,0,0,0]*Z(3)^0), OnLines);
Gp   := Action(SP4, pts, OnLines);
form := function(u,v) return u[1]*v[4]-u[4]*v[1]+u[2]*v[3]-u[3]*v[2]; end;
zero := Zero(GF(3));
adj  := List([1..40], i -> Filtered([1..40], j -> j<>i and form(pts[i],pts[j])=zero));
edges := Filtered(Combinations([1..40],2), e -> e[2] in adj[e[1]]);
tris  := Filtered(Combinations([1..40],3),
           t -> ForAll(Combinations(t,2), e -> e[2] in adj[e[1]]));
nE := Length(edges);
d1 := NullMat(40, nE);
for j in [1..nE] do d1[edges[j][1]][j]:=-1; d1[edges[j][2]][j]:=1; od;
d2 := NullMat(nE, Length(tris));
for j in [1..Length(tris)] do
  t := tris[j];
  d2[Position(edges,[t[2],t[3]])][j] := d2[Position(edges,[t[2],t[3]])][j]+1;
  d2[Position(edges,[t[1],t[3]])][j] := d2[Position(edges,[t[1],t[3]])][j]-1;
  d2[Position(edges,[t[1],t[2]])][j] := d2[Position(edges,[t[1],t[2]])][j]+1;
od;
H := Intersection(VectorSpace(Rationals, NullspaceMat(TransposedMat(d1))),
                  VectorSpace(Rationals, NullspaceMat(d2)));
A(Concatenation("dim harmonic = ", String(Dimension(H)), "\n"));
# the FULL automorphism group, acting on POINTS
FullPts := Normalizer(SymmetricGroup(40), Gp);
A(Concatenation("|Aut on points| = ", String(Size(FullPts)),
   "   (expect 51840)\n"));
SignedMat := function(g)
  local M,j,a,b,k;
  M := NullMat(nE,nE);
  for j in [1..nE] do
    a := edges[j][1]^g; b := edges[j][2]^g;
    if a<b then k:=Position(edges,[a,b]); M[j][k]:=1;
    else       k:=Position(edges,[b,a]); M[j][k]:=-1; fi;
  od;
  return M;
end;
A(Concatenation("harmonic invariant under the FULL group? ",
  String(ForAll(GeneratorsOfGroup(FullPts),
    g -> ForAll(BasisVectors(Basis(H)), v -> v*SignedMat(g) in H))), "\n"));
tblF := CharacterTable(FullPts); cclF := ConjugacyClasses(tblF);
bas := BasisVectors(Basis(H)); B := Basis(H,bas);
chi := List(cclF, function(c)
  local g,M,t,i,co;
  g := Representative(c); M := SignedMat(g); t := 0;
  for i in [1..Length(bas)] do
    co := Coefficients(B, bas[i]*M);
    if co = fail then return fail; fi;
    t := t + co[i];
  od; return t; end);
A(Concatenation("full-group harmonic character computable: ",
  String(not fail in chi), "\n"));
if not fail in chi then
  dec := MatScalarProducts(tblF, Irr(tblF), [ClassFunction(tblF, chi)])[1];
  us := Filtered([1..Length(dec)], i -> dec[i] <> 0);
  A(Concatenation("  decomposition over PGSp: ",
    String(List(us, i -> [Irr(tblF)[i][1], dec[i]])), "\n"));
  A(Concatenation("  a SINGLE degree-81 extension? ",
    String(Length(us)=1 and Irr(tblF)[us[1]][1]=81), "\n"));
  if Length(us)=1 then
    A(Concatenation("  which one: irreducible #", String(us[1]),
      " of the PGSp table\n"));
  fi;
fi;
A("\nDONE\n");
QUIT;
