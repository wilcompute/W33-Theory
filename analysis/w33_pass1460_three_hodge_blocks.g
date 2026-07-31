# Pass 1460 -- signed characters of ALL THREE Hodge blocks.
# Pass 1455 showed the harmonic 81 is the Steinberg module under the SIGNED edge
# action. The same machinery applies to the other two blocks, and if each is a
# single irreducible the whole 240-dim signed module decomposes into exactly
# three named pieces -- a much stronger statement than the harmonic one alone.
LogTo();
out := "C:/Repos/Theory of Everything/data/w33_pass1460_three_blocks.txt";
PrintTo(out, "Pass 1460: signed characters of exact / harmonic / coexact\n\n");
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
for j in [1..nE] do d1[edges[j][1]][j] := -1; d1[edges[j][2]][j] := 1; od;
d2 := NullMat(nE, Length(tris));
for j in [1..Length(tris)] do
  t := tris[j];
  d2[Position(edges,[t[2],t[3]])][j] := d2[Position(edges,[t[2],t[3]])][j]+1;
  d2[Position(edges,[t[1],t[3]])][j] := d2[Position(edges,[t[1],t[3]])][j]-1;
  d2[Position(edges,[t[1],t[2]])][j] := d2[Position(edges,[t[1],t[2]])][j]+1;
od;
EXACT   := VectorSpace(Rationals, d1);   # ROW space of d1 inside Q^240
COEXACT := VectorSpace(Rationals, TransposedMat(d2));      # im d2 (as rows), 120
HARM    := Intersection(VectorSpace(Rationals, NullspaceMat(TransposedMat(d1))),
                        VectorSpace(Rationals, NullspaceMat(d2)));
A(Concatenation("dims: exact=", String(Dimension(EXACT)),
  "  harmonic=", String(Dimension(HARM)),
  "  coexact=", String(Dimension(COEXACT)),
  "   sum=", String(Dimension(EXACT)+Dimension(HARM)+Dimension(COEXACT)), "\n\n"));
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
tbl := CharacterTable(Gp); ccl := ConjugacyClasses(tbl);
Report := function(name, V)
  local bas,B,chi,dec,us;
  bas := BasisVectors(Basis(V)); B := Basis(V,bas);
  chi := List(ccl, function(c)
    local g,M,t,i,co;
    g := Representative(c); M := SignedMat(g); t := 0;
    for i in [1..Length(bas)] do
      co := Coefficients(B, bas[i]*M);
      if co = fail then return fail; fi;
      t := t + co[i];
    od;
    return t; end);
  if fail in chi then
    A(Concatenation(name, ": NOT signed-invariant\n")); return;
  fi;
  dec := MatScalarProducts(tbl, Irr(tbl), [ClassFunction(tbl,chi)])[1];
  us  := Filtered([1..Length(dec)], i -> dec[i]<>0);
  A(Concatenation(name, " (dim ", String(chi[1]), "): ",
     String(List(us, i -> [Irr(tbl)[i][1], dec[i]])),
     "   irreducible? ", String(Length(us)=1 and dec[us[1]]=1), "\n"));
end;
Report("EXACT   ", EXACT);
Report("HARMONIC", HARM);
Report("COEXACT ", COEXACT);
A("\nDONE\n");
QUIT;
