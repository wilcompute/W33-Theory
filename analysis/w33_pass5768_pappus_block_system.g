# Pass 5768: is the Pappus kernel partition a block system of Aut(Pappus)?
# The Reye's is (Pass 5675). If Pappus's is too, the two-of-five is a real class.
LoadPackage("grape");;
d := EvalString(StringFile("c:/Repos/Theory of Everything/data/tmp_pappus.json"));;
blocks := d[1];; parts := d[2];;
n := 9;; nb := Length(blocks);;
adj := List([1..n+nb], i -> []);;
for i in [1..nb] do
  for v in blocks[i] do
    Add(adj[v+1], n+i); Add(adj[n+i], v+1);
  od;
od;;
levi := Graph(Group(()), [1..n+nb], OnPoints,
              function(x,y) return y in adj[x]; end, true);;
A := AutomorphismGroup(levi);;
Print("|Aut(Pappus Levi)| = ", Size(A), "\n");
orbs := Orbits(A, [1..n+nb]);;
Print("orbits: ", List(orbs, Length), "\n");
pts := First(orbs, o -> Length(o) = 9);;
if pts = fail then Print("no 9-orbit (Levi is point-line transitive)\n");
  pts := [1..9]; fi;
act := Action(A, [1..9], OnPoints);;
Print("action on the 9 points: order ", Size(act), ", transitive ",
      IsTransitive(act,[1..9]), ", primitive ", IsPrimitive(act,[1..9]), "\n");
bl := AllBlocks(act);;
Print("nontrivial block representatives: ", Length(bl), "\n");
Print("block sizes: ", Set(List(bl, Length)), "\n");
target := Set(List(parts, x -> Set(x)));;
Print("kernel partition (0-based): ", target, "\n");
found := false;;
for b in bl do
  sys := Orbit(act, b, OnSets);
  p0 := Set(List(sys, x -> Set(List(x, y -> y-1))));
  Print("   system sizes ", Length(sys), " x ", Length(b), " : ", p0, "\n");
  if p0 = target then found := true; Print("   ^^^ MATCHES THE KERNEL PARTITION\n"); fi;
od;
Print("\nPAPPUS KERNEL PARTITION IS A BLOCK SYSTEM : ", found, "\n");
QUIT;
