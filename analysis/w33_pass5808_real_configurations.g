# Pass 5808: the REAL Desargues and Mobius-Kantor configurations, and the sharp test --
# a point group with TWO block systems, where the conjecture predicts the kernel FAILS.
#
# Pass 5802 found my earlier Desargues/Mobius-Kantor incidence lists were fakes
# (|Aut| 4 and 1 against published 120 and 16).  Built properly here:
#   Desargues 10_3 : points = 2-subsets of {1..5}, lines = 3-subsets, incidence = subset
#   Mobius-Kantor  : points = Z8, lines = {i, i+1, i+3} mod 8
LoadPackage("grape");;

mk := function(n, blocks, name)
  local nb, adj, i, v, levi, A, S, act, bl;
  nb := Length(blocks);
  adj := List([1..n+nb], i -> []);
  for i in [1..nb] do
    for v in blocks[i] do
      Add(adj[v], n+i); Add(adj[n+i], v);
    od;
  od;
  levi := Graph(Group(()), [1..n+nb], OnPoints,
                function(x,y) return y in adj[x]; end, true);
  A := AutomorphismGroup(levi);
  S := Stabilizer(A, [1..n], OnSets);
  Print(name, ":  |Aut(Levi)| = ", Size(A), ", point group |S| = ", Size(S), "\n");
  if Size(S) = 1 then Print("   trivial point group\n"); return; fi;
  act := Action(S, [1..n], OnPoints);
  if not IsTransitive(act, [1..n]) then
    Print("   not transitive on points: orbits ",
          List(Orbits(act,[1..n]), Length), "\n");
    return;
  fi;
  bl := AllBlocks(act);
  Print("   transitive, primitive ", IsPrimitive(act,[1..n]),
        ", NONTRIVIAL BLOCK SYSTEMS = ", Length(bl),
        ", sizes ", Set(List(bl, Length)), "\n");
end;;

# Desargues: points are the 10 two-subsets of [1..5], lines the 10 three-subsets.
two := Combinations([1..5], 2);;
three := Combinations([1..5], 3);;
des := List(three, t -> Filtered([1..10], i -> IsSubset(t, two[i])));;
mk(10, des, "Desargues 10_3 (real)");

# Mobius-Kantor: points Z8, lines {i, i+1, i+3}.
mkl := List([0..7], i -> [ i mod 8, (i+1) mod 8, (i+3) mod 8 ] + 1);;
mk(8, mkl, "Mobius-Kantor 8_3 (real)");

# THE SHARP TEST: a configuration whose point group has TWO OR MORE block systems.
# AG(2,3) as 9_3 -- points of the affine plane, one parallel class removed.
ag := [];;
for i in [0..2] do for j in [0..2] do
  Add(ag, [ 3*i+j+1, 3*i+((j+1) mod 3)+1, 3*i+((j+2) mod 3)+1 ]);
od; od;
mk(9, ag, "three parallel triples on 9 points");

# The 8-point cube configuration: lines = the 4 antipodal pairs doubled is degenerate,
# use instead points Z8 with lines {i, i+2, i+4}.
c8 := List([0..7], i -> [ i mod 8, (i+2) mod 8, (i+4) mod 8 ] + 1);;
mk(8, c8, "Z8 with lines {i,i+2,i+4}");
QUIT;
