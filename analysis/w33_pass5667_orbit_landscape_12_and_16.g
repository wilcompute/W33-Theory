# Pass 5667: the COMPLETE orbit landscape of W(F4)/Z on the Reye 12 and 16.
#
# Not a hunt for a pattern -- an enumeration.  For every conjugacy class of subgroups,
# record the orbit partition on the 12 points and on the 16 blocks.  Then ask, once,
# whether 8+3+1 (the SM gauge-boson pattern) or any SM fermion pattern appears at all,
# and if so what subgroup produces it.  Enumerating first and asking second is the only
# way this does not become numerology.
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
twelve := First(orbs, o -> Length(o) = 12);;
sixteen := First(orbs, o -> Length(o) = 16);;
act12 := Action(A, twelve, OnPoints);;
act16 := Action(A, sixteen, OnPoints);;
Print("|G| = ", Size(A), ", acting faithfully on 12 and on 16\n");

cc := ConjugacyClassesSubgroups(act12);;
Print("conjugacy classes of subgroups: ", Length(cc), "\n\n");

# Build the same subgroup list inside act16 via the isomorphism A -> act16.
h12 := ActionHomomorphism(A, twelve, OnPoints);;
h16 := ActionHomomorphism(A, sixteen, OnPoints);;

seen12 := [];;
patterns := [];;
for c in cc do
  H := Representative(c);
  p12 := SortedList(List(Orbits(H, [1..12]), Length));
  # pull H back to A, push forward to the 16
  HA := PreImage(h12, H);
  H16 := Image(h16, HA);
  p16 := SortedList(List(Orbits(H16, [1..16]), Length));
  Add(patterns, [Size(H), p12, p16, StructureDescription(H)]);
od;

# distinct 12-patterns
d12 := Set(List(patterns, p -> p[2]));;
d16 := Set(List(patterns, p -> p[3]));;
Print("distinct orbit patterns on the 12: ", Length(d12), "\n");
for p in d12 do Print("   ", p, "\n"); od;
Print("\ndistinct orbit patterns on the 16: ", Length(d16), "\n");
for p in d16 do Print("   ", p, "\n"); od;

Print("\n--- the one question, asked AFTER the enumeration ---\n");
sm := [1,3,8];;
hit := Filtered(patterns, p -> p[2] = sm);;
Print("subgroups with orbits 1+3+8 on the 12 : ", Length(hit), "\n");
for p in hit do
  Print("   |H| = ", p[1], "  ", p[4], "   on the 16: ", p[3], "\n");
od;
# and the fermion-shaped ones on the 16
for target in [ [1,1,2,3,3,6], [1,3,4,8], [4,4,8], [1,1,6,8], [16] ] do
  h := Filtered(patterns, p -> p[3] = target);
  Print("subgroups with orbits ", target, " on the 16 : ", Length(h), "\n");
od;
QUIT;
