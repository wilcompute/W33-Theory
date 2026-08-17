# Pass 5784: is the Pappus kernel partition a block system of Aut(Pappus)?
# Pass 5770 could not run this: Pappus is self-dual so its Levi is point-line
# transitive and Action(A,[1..9]) has no method.  Fix: act with the index-2
# point-preserving subgroup.
LoadPackage("grape");;

blocks := [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[1,5,6],[2,3,7]];;
parts  := [[0,5,7],[1,3,8],[2,4,6]];;
n := 9;; nb := 9;;

adj := List([1..n+nb], i -> []);;
for i in [1..nb] do
  for v in blocks[i] do
    Add(adj[v+1], n+i);
    Add(adj[n+i], v+1);
  od;
od;;
levi := Graph(Group(()), [1..n+nb], OnPoints,
              function(x,y) return y in adj[x]; end, true);;
A := AutomorphismGroup(levi);;
Print("|Aut(Pappus Levi)| = ", Size(A), "\n");
Print("orbits on the Levi : ", List(Orbits(A,[1..n+nb]), Length), "\n");

# The index-2 subgroup preserving the point side.
S := Stabilizer(A, [1..9], OnSets);;
Print("point-preserving subgroup |S| = ", Size(S), "\n");
act := Action(S, [1..9], OnPoints);;
Print("action on the 9 points: order ", Size(act),
      ", transitive ", IsTransitive(act,[1..9]),
      ", primitive ", IsPrimitive(act,[1..9]), "\n");
Print("TransitiveIdentification : ", TransitiveIdentification(act), "\n");

bl := AllBlocks(act);;
Print("nontrivial block representatives : ", Length(bl), "\n");
Print("block sizes occurring : ", Set(List(bl, Length)), "\n");

target := Set(List(parts, x -> Set(x)));;
Print("kernel partition (0-based) : ", target, "\n");
found := false;;
for b in bl do
  sys := Orbit(act, b, OnSets);
  p0 := Set(List(sys, x -> Set(List(x, y -> y-1))));
  Print("   system ", Length(sys), " x ", Length(b), " : ", p0, "\n");
  if p0 = target then
    found := true;
    Print("   ^^^ MATCHES THE KERNEL PARTITION\n");
  fi;
od;
Print("\nPAPPUS KERNEL PARTITION IS A BLOCK SYSTEM : ", found, "\n");
QUIT;
