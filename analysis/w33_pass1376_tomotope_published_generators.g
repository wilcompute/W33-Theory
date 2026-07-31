# Pass 1376 -- the tomotope from its PUBLISHED generators, and whether W(3,3)'s
# 540 frames are the facets of a rank-4 polytope.
#
# WHY THIS IS NOT A REDISCOVERY.  This repository has ~50 tomotope files
# (BT666, BT705, BT781-783, BT795, BT796, BT814, BT838, BT850, BT851, BT1363,
# BT1406, BT1527-1529, ...).  Every one of them works from DERIVED numbers --
# "order 96", "2^4:C3", "192 flags" -- restated from the literature.  A grep for
# the actual permutations
#
#     rho0 = (5,10)(6,9)(7,12)(8,11)      rho2 = (5,9)(6,10)(7,11)(8,12)
#     rho1 = (1,6)(2,5)(3,8)(4,7)         rho3 = (5,8)(6,7)(9,12)(10,11)
#
# published in Monson-Pellicer-Williams, "The Tomotope", Ars Math. Contemp. 5
# (2012), p. 9, returns NOTHING.  The group has been described here many times
# and never once constructed.  So every structural claim the corpus makes about
# Gamma(T) is currently uncorroborated, and this script corroborates or refutes
# them from the primary source.
#
# Five questions:
#   Q1  Does the published generating set reproduce |Gamma(T)| = 96?
#   Q2  Is Gamma(T)' = 2^4:C3 = SmallGroup[48,50], as BT781/BT783 assert?
#   Q3  Does Gamma(T) fail the intersection condition, as the literature says?
#       (This is WHY the tomotope is not an abstract polytope -- the single most
#       cited fact about it in this corpus, never once verified here.)
#   Q4  Gamma(T) has order 96; so does the 540-frame stabiliser in PGSp(4,3).
#       BT781 compared their order-48 halves.  Nobody has compared the 96s.
#   Q5  W(3,3)'s frame stabiliser is O_h = Aut(cube) = a string C-group {4,3}.
#       Does it extend to a rank-4 string C-group on all of PSp(4,3)?  If it
#       does, the 540 frames are the FACETS of an abstract 4-polytope.

LogTo();
out := "C:/Repos/Theory of Everything/data/w33_pass1376_tomotope.txt";
PrintTo(out, "Pass 1376: the tomotope from published generators\n\n");
A := function(s) AppendTo(out, s); end;

# ============================================================== Q1, Q2
r0 := (5,10)(6,9)(7,12)(8,11);
r1 := (1,6)(2,5)(3,8)(4,7);
r2 := (5,9)(6,10)(7,11)(8,12);
r3 := (5,8)(6,7)(9,12)(10,11);
rho := [r0, r1, r2, r3];
T := Group(rho);

A("=== Q1: the published generators ===\n");
A(Concatenation("|Gamma(T)|          = ", String(Size(T)),
   "   (literature: 96 -> ", String(Size(T) = 96), ")\n"));
A(Concatenation("IdGroup             = ", String(IdGroup(T)), "\n"));
A(Concatenation("StructureDescription= ", StructureDescription(T), "\n"));
A(Concatenation("transitive on 12?   = ", String(IsTransitive(T, [1..12])), "\n"));
A(Concatenation("orbits on 12        = ", String(List(Orbits(T,[1..12]), Length)), "\n"));
A(Concatenation("all rho_i involutions? ", String(ForAll(rho, x -> Order(x) = 2)), "\n"));

TD := DerivedSubgroup(T);
A("\n=== Q2: the derived subgroup ===\n");
A(Concatenation("|Gamma(T)'|         = ", String(Size(TD)), "\n"));
A(Concatenation("IdGroup             = ", String(IdGroup(TD)),
   "   (BT781/BT783 say 2^4:C3 = [48,50] -> ",
   String(IdGroup(TD) = [48,50]), ")\n"));
A(Concatenation("StructureDescription= ", StructureDescription(TD), "\n"));
A(Concatenation("centre order        = ", String(Size(Centre(TD))),
   "   (BT783 says 1 -> ", String(Size(Centre(TD)) = 1), ")\n"));
A(Concatenation("abelianisation      = ", String(AbelianInvariants(TD)),
   "   (BT783 says order 3)\n"));
A(Concatenation("has index-2 subgroup? ",
   String(ForAny(ConjugacyClassesSubgroups(TD), c -> Index(TD, Representative(c)) = 2)),
   "   (BT783 says none)\n"));

# Schlafli-type data: orders of rho_i rho_{i+1}
A(Concatenation("\nSchlafli type {p,q,r} = {",
  String(Order(r0*r1)), ",", String(Order(r1*r2)), ",", String(Order(r2*r3)), "}\n"));
A("string relations (rho_i rho_j)^2=1 for |i-j|>=2:\n");
A(Concatenation("   (r0 r2)^2 = 1 ? ", String(Order(r0*r2) <= 2), "\n"));
A(Concatenation("   (r0 r3)^2 = 1 ? ", String(Order(r0*r3) <= 2), "\n"));
A(Concatenation("   (r1 r3)^2 = 1 ? ", String(Order(r1*r3) <= 2), "\n"));

# ============================================================== Q3  the IC
# For a string C-group: <rho_i : i in I> n <rho_j : j in J> = <rho_k : k in I n J>
SubI := function(G, gens, I)
  if Length(I) = 0 then return TrivialSubgroup(G); fi;
  return Subgroup(G, gens{I});
end;

A("\n=== Q3: the INTERSECTION CONDITION ===\n");
fails := 0; tested := 0;
for I in Combinations([1..4]) do
  for J in Combinations([1..4]) do
    tested := tested + 1;
    GI := SubI(T, rho, I); GJ := SubI(T, rho, J);
    GK := SubI(T, rho, Intersection(I, J));
    if Size(Intersection(GI, GJ)) <> Size(GK) then
      fails := fails + 1;
      if fails <= 6 then
        A(Concatenation("  FAILS  I=", String(I), " J=", String(J),
          " : |GI n GJ| = ", String(Size(Intersection(GI, GJ))),
          "  but |G_{I n J}| = ", String(Size(GK)), "\n"));
      fi;
    fi;
  od;
od;
A(Concatenation("  tested ", String(tested), " pairs (I,J);  FAILURES = ",
   String(fails), "\n"));
A(Concatenation("  intersection condition HOLDS? ", String(fails = 0),
   "   (literature: FAILS, which is why the tomotope is not a polytope)\n"));

# ============================================================== Q4  the 96s
A("\n=== Q4: Gamma(T) vs the 540-frame stabiliser in PGSp(4,3), both order 96 ===\n");
# Build W(3,3) and PGSp(4,3) = Aut(W(3,3)) as the line-nonedge ("frame") action.
SP4  := Sp(4,3);
pts  := Orbit(SP4, NormedRowVector([1,0,0,0]*Z(3)^0), OnLines);
Gp   := Action(SP4, pts, OnLines);
A(Concatenation("degree-40 image order = ", String(Size(Gp)), "\n"));
# totally isotropic lines: the 2-dim t.i. subspaces, each carrying 4 points.
# span of two collinear points, read back as a 4-set of point indices.
form := function(u,v)
  return u[1]*v[4] - u[4]*v[1] + u[2]*v[3] - u[3]*v[2];
end;
zero := Zero(GF(3));
adj := List([1..40], i -> Filtered([1..40],
        j -> j <> i and form(pts[i], pts[j]) = zero));
lines := [];
for i in [1..40] do
  for j in adj[i] do
    if j > i then
      sp := Filtered([1..40], m -> pts[m] in
              List(Filtered(Elements(VectorSpace(GF(3), [pts[i], pts[j]])),
                            v -> v <> Zero(pts[i])), NormedRowVector));
      AddSet(lines, Set(sp));
    fi;
  od;
od;
A(Concatenation("totally isotropic lines found: ", String(Length(lines)),
   "  all of size 4? ", String(ForAll(lines, L -> Length(L) = 4)), "\n"));

if Length(lines) = 40 then
  lineAct := ActionHomomorphism(Gp, lines, OnSets);
  GLin := Image(lineAct);
  # frames = unordered pairs of DISJOINT lines
  frames := Filtered(Combinations([1..40], 2),
              p -> Intersection(lines[p[1]], lines[p[2]]) = []);
  A(Concatenation("frames (disjoint line pairs) = ", String(Length(frames)), "\n"));
  stabP := Stabilizer(GLin, frames[1], OnSets);
  A(Concatenation("frame stabiliser in PSp(4,3): |H| = ", String(Size(stabP)),
     "  IdGroup = ", String(IdGroup(stabP)),
     "  = ", StructureDescription(stabP), "\n"));
  A(Concatenation("  is it O_h = C2 x S4 = [48,48]? ",
     String(IdGroup(stabP) = [48,48]), "\n"));
  A(Concatenation("  Gamma(T)' = [48,50];  equal? ",
     String(IdGroup(stabP) = IdGroup(TD)), "\n"));
  # PGSp(4,3): the full automorphism group of the GQ, order 51840
  fullAut := Normalizer(SymmetricGroup(40), GLin);
  A(Concatenation("|Aut(W(3,3)) on lines| = ", String(Size(fullAut)), "\n"));
  stabF := Stabilizer(fullAut, frames[1], OnSets);
  A(Concatenation("frame stabiliser in PGSp(4,3): |H| = ", String(Size(stabF)),
     "  IdGroup = ", String(IdGroup(stabF)),
     "  = ", StructureDescription(stabF), "\n"));
  A(Concatenation("  ISOMORPHIC TO Gamma(T) (both order 96)? ",
     String(IdGroup(stabF) = IdGroup(T)), "\n"));
  A(Concatenation("  Gamma(T) IdGroup = ", String(IdGroup(T)),
     " vs frame-96 IdGroup = ", String(IdGroup(stabF)), "\n"));
  A(Concatenation("  derived subgroup of the frame-96 = ",
     String(IdGroup(DerivedSubgroup(stabF))), " = ",
     StructureDescription(DerivedSubgroup(stabF)), "\n"));

  # ========================================================== Q5 polytopality
  A("\n=== Q5: do the 540 frames form the facets of a rank-4 polytope? ===\n");
  A("Frame stabiliser O_h = Aut(cube) is the string C-group {4,3}.  If PSp(4,3)\n");
  A("admits rho3 with (rho0 rho3)^2 = (rho1 rho3)^2 = 1, <all> = PSp(4,3), and\n");
  A("the intersection condition, then the 540 cosets of O_h are the FACETS of a\n");
  A("rank-4 abstract regular polytope of type {4,3,r} with 25920 flags.\n");
  A("(Existence of SOME rank-4 polytope for U4(2) is published -- Leemans &\n");
  A(" Vauthier, atlas of abstract regular polytopes for small groups, 2006.\n");
  A(" The question here is whether the FRAME stabiliser is one of the facets.)\n\n");
  # standard generators of O_h as a string C-group {4,3}
  found := false;
  invs := Filtered(Elements(stabP), x -> Order(x) = 2);
  triples := [];
  for a in invs do for b in invs do for c in invs do
    if Order(a*c) = 2 and Order(a*b) = 4 and Order(b*c) = 3
       and Size(Subgroup(stabP, [a,b,c])) = 48 then
      Add(triples, [a,b,c]);
    fi;
  od; od; od;
  A(Concatenation("string C-group {4,3} generating triples in O_h: ",
     String(Length(triples)), "\n"));
  if Length(triples) > 0 then
    t := triples[1];
    C := Centralizer(GLin, Subgroup(GLin, [t[1], t[2]]));
    cand := Filtered(Elements(C), x -> Order(x) = 2);
    A(Concatenation("candidate rho3 (involutions centralising rho0,rho1): ",
       String(Length(cand)), "\n"));
    for x in cand do
      H := Subgroup(GLin, [t[1], t[2], t[3], x]);
      if Size(H) = Size(GLin) then
        g4 := [t[1], t[2], t[3], x];
        ok := true;
        for I in Combinations([1..4]) do
          for J in Combinations([1..4]) do
            GI := SubI(GLin, g4, I); GJ := SubI(GLin, g4, J);
            GK := SubI(GLin, g4, Intersection(I, J));
            if Size(Intersection(GI, GJ)) <> Size(GK) then ok := false; fi;
          od;
        od;
        A(Concatenation("  rho3 found: type {",
          String(Order(t[1]*t[2])), ",", String(Order(t[2]*t[3])), ",",
          String(Order(t[3]*x)), "}   generates PSp(4,3)=", String(Size(H)),
          "   IC holds = ", String(ok), "\n"));
        if ok then found := true; fi;
      fi;
    od;
  fi;
  A(Concatenation("  RANK-4 STRING C-GROUP ON THE FRAME CUBE EXISTS? ",
     String(found), "\n"));
fi;

A("\nDONE\n");
QUIT;
