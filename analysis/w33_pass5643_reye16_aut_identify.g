# Pass 5643: is Aut(the 16-face graph of BT1413's Reye configuration) really W(F4),
# or is 1152 = |S4 wr S2| an order coincidence?  Decide by IsomorphismGroups.
LoadPackage("grape");;

edges := EvalString(StringFile("c:/Repos/Theory of Everything/data/tmp_reye16_edges.json"));;

n := 16;;
G := Group(());;
adj := List([1..n], i -> []);;
for e in edges do
  Add(adj[e[1]+1], e[2]+1);
  Add(adj[e[2]+1], e[1]+1);
od;;

gamma := Graph(Group(()), [1..n], OnPoints,
               function(x,y) return y in adj[x]; end, true);;
A := AutomorphismGroup(gamma);;
Print("16-face graph |Aut| = ", Size(A), "\n");
Print("  structure     = ", StructureDescription(A), "\n");

# The two order-1152 candidates.
W := WeylGroup(RootSystem(SimpleLieAlgebra("F",4,Rationals)));;
Print("|W(F4)|       = ", Size(W), "\n");
Print("  structure   = ", StructureDescription(W), "\n");

S4wrS2 := WreathProduct(SymmetricGroup(4), SymmetricGroup(2));;
Print("|S4 wr S2|    = ", Size(S4wrS2), "\n");
Print("  structure   = ", StructureDescription(S4wrS2), "\n");

Print("Aut =~ W(F4)     : ", IsomorphismGroups(A, W) <> fail, "\n");
Print("Aut =~ S4 wr S2  : ", IsomorphismGroups(A, S4wrS2) <> fail, "\n");
Print("W(F4) =~ S4wrS2  : ", IsomorphismGroups(W, S4wrS2) <> fail, "\n");

# Is the graph's complement the 4x4 rook's graph (= L(4,4) = K4 x K4)?
comp := ComplementGraph(gamma);;
Print("complement is regular of degree ", Length(Adjacency(comp,1)), "\n");
rook := Graph(Group(()), Cartesian([1..4],[1..4]), OnPairs,
   function(x,y) return x<>y and (x[1]=y[1] or x[2]=y[2]); end, true);;
Print("complement =~ rook 4x4 : ", IsIsomorphicGraph(comp, rook), "\n");
Print("|Aut(rook 4x4)| = ", Size(AutomorphismGroup(rook)), "\n");
QUIT;
