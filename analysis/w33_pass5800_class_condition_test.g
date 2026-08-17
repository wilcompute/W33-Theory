# Pass 5800: is "unique nontrivial block system" the REAL condition, or a proxy?
# Test both properties independently on five configurations:
#   (a) does the GF(2) kernel's top-weight words complement to a partition?
#   (b) does the point-action have exactly one nontrivial block system?
# If (a) <=> (b) across all five, the class is characterised.  If they come apart,
# one of them is a proxy for something else.
LoadPackage("grape");;

configs := [
  [ "Fano 7_3", 7, [[0,1,3],[1,2,4],[2,3,5],[3,4,6],[4,5,0],[5,6,1],[6,0,2]] ],
  [ "Mobius-Kantor 8_3", 8, [[0,1,2],[1,3,4],[2,5,6],[3,5,7],[4,6,7],[0,3,6],[0,4,5],[1,6,7]] ],
  [ "Pappus 9_3", 9, [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[1,5,6],[2,3,7]] ],
  [ "Desargues 10_3", 10, [[0,1,2],[0,3,4],[0,5,6],[1,3,7],[1,5,8],[2,4,8],[2,6,7],[3,6,9],[4,5,9],[7,8,9]] ],
];;

for cfg in configs do
  name := cfg[1];; n := cfg[2];; blocks := cfg[3];; nb := Length(blocks);;
  adj := List([1..n+nb], i -> []);;
  for i in [1..nb] do
    for v in blocks[i] do
      Add(adj[v+1], n+i); Add(adj[n+i], v+1);
    od;
  od;
  levi := Graph(Group(()), [1..n+nb], OnPoints,
                function(x,y) return y in adj[x]; end, true);
  A := AutomorphismGroup(levi);
  S := Stabilizer(A, [1..n], OnSets);
  act := Action(S, [1..n], OnPoints);
  Print(name, ":\n");
  Print("   |Aut(Levi)| = ", Size(A), ", point-preserving |S| = ", Size(S), "\n");
  if Size(act) = 1 or not IsTransitive(act, [1..n]) then
    Print("   action not transitive on points; block systems undefined\n");
  else
    bl := AllBlocks(act);
    Print("   transitive, primitive ", IsPrimitive(act,[1..n]),
          ", nontrivial block representatives ", Length(bl),
          ", sizes ", Set(List(bl, Length)), "\n");
    Print("   UNIQUE BLOCK SYSTEM : ", Length(bl) = 1, "\n");
  fi;
od;
QUIT;
