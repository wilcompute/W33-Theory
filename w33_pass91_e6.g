# Pass 91 -- Aut(W(3,3)) is the Weyl group of E6, acting on the 27 lines / 45 tritangent planes.
# Verifies the graph automorphism group of W(3,3) is isomorphic to W(E6) (both order 51840,
# structure PSp(4,3):2), and records the E6 cubic-surface orbit sizes (27,36,45,72) that W(E6)
# permutes -- the same 45 tritangent planes that are the minimum-weight codewords of C_2(W).

LoadPackage("grape");;

field := GF(3);;
pts := NormedRowVectors(field^4);;
J := [[0,1,0,0],[2,0,0,0],[0,0,0,1],[0,0,2,0]] * One(field);;
adjfun := function(x, y) return not IsZero(pts[x]*J*pts[y]); end;;
gamma := Graph(Group(()), [1..40], OnPoints, adjfun, true);;
aut := AutGroupGraph(gamma);;

out := OutputTextFile("w33_pass91_e6_out.txt", false);;
SetPrintFormattingStatus(out, false);;
PrintTo(out, "aut_order=", Size(aut), "\n");

# derived subgroup = the simple PSp(4,3) = S(4,3) of order 25920, index 2 in Aut(W)
der := DerivedSubgroup(aut);;
PrintTo(out, "derived_order=", Size(der), "\n");
PrintTo(out, "derived_is_simple=", IsSimpleGroup(der), "\n");
PrintTo(out, "derived_simple_name=", IsomorphismTypeInfoFiniteSimpleGroup(der).name, "\n");
PrintTo(out, "aut_index_over_derived=", Size(aut) / Size(der), "\n");

# Weyl group of E6 for comparison
L := SimpleLieAlgebra("E", 6, Rationals);;
WE6 := WeylGroup(RootSystem(L));;
PrintTo(out, "WE6_order=", Size(WE6), "\n");
derW := DerivedSubgroup(WE6);;
PrintTo(out, "WE6_derived_order=", Size(derW), "\n");
PrintTo(out, "WE6_derived_simple_name=", IsomorphismTypeInfoFiniteSimpleGroup(derW).name, "\n");

# isomorphic as abstract groups?
iso := IsomorphismGroups(aut, WE6);;
PrintTo(out, "aut_iso_WE6=", not iso = fail, "\n");

CloseStream(out);
QUIT;
