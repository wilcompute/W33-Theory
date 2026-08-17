# Pass 5675: the [12,4,6] code's weight-8 words complement to a partition of the Reye's
# 12 points into three 4-sets.  Q4's own geometry splits the 12 as SIX pairs (one per
# direction-pair of the 4-cube), NOT as three fours.  So where does the 3x4 come from?
# Test: is it a block system of the T12_165 action?
LoadPackage("grape");;

inc := EvalString(StringFile("c:/Repos/Theory of Everything/data/tmp_reye16_levi.json"));;
n := 28;;
adj := List([1..n], i -> []);;
for e in inc do
  Add(adj[e[1]+1], e[2]+17);
  Add(adj[e[2]+17], e[1]+1);
od;;
levi := Graph(Group(()), [1..n], OnPoints,
              function(x,y) return y in adj[x]; end, true);;
A := AutomorphismGroup(levi);;
orbs := Orbits(A, [1..28]);;
twelve := SortedList(First(orbs, o -> Length(o) = 12));;
act := Action(A, twelve, OnPoints);;
Print("action on the 12: order ", Size(act), ", T12_",
      TransitiveIdentification(act), ", primitive ", IsPrimitive(act, [1..12]), "\n");

# every block system
bl := AllBlocks(act);;
Print("nontrivial block representatives: ", Length(bl), "\n");
sizes := Set(List(bl, Length));;
Print("block sizes occurring: ", sizes, "\n");
for s in sizes do
  Print("   size ", s, ": ", Length(Filtered(bl, b -> Length(b) = s)), " representative(s)\n");
od;

# the code partition, in the SAME indexing (twelve[i] <-> code coordinate i-1)
codeparts := [ [0,5,8,11], [1,4,7,9], [2,3,6,10] ];;
Print("\ncode partition (0-based coordinates): ", codeparts, "\n");
allsys := AllBlocks(act);;
found := false;;
for b in allsys do
  if Length(b) = 4 then
    sys := Orbit(act, b, OnSets);
    if Length(sys) = 3 then
      p0 := SortedList(List(sys, x -> SortedList(List(x, y -> y-1))));
      Print("   a size-4 system: ", p0, "\n");
      if p0 = SortedList(List(codeparts, SortedList)) then
        found := true;
        Print("   ^^^ THIS IS THE CODE PARTITION\n");
      fi;
    fi;
  fi;
od;
Print("\nCODE PARTITION IS A BLOCK SYSTEM OF T12_165 : ", found, "\n");
QUIT;
