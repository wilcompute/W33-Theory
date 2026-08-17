# Pass 5816: the sharpest test of the surviving direction -- a point group with
# TWO OR MORE block systems.  The claim (kernel partition => UNIQUE system) predicts
# that any such configuration must LACK the kernel partition.
LoadPackage("grape");;
report := function(n, blocks, name)
  local nb, adj, i, v, levi, A, S, act, bl;
  nb := Length(blocks);
  adj := List([1..n+nb], i -> []);
  for i in [1..nb] do
    for v in blocks[i] do Add(adj[v], n+i); Add(adj[n+i], v); od;
  od;
  levi := Graph(Group(()), [1..n+nb], OnPoints,
                function(x,y) return y in adj[x]; end, true);
  A := AutomorphismGroup(levi);
  S := Stabilizer(A, [1..n], OnSets);
  Print(name, ": |Aut(Levi)|=", Size(A), " |point grp|=", Size(S));
  if Size(S) = 1 then Print("  trivial\n"); return; fi;
  act := Action(S, [1..n], OnPoints);
  if not IsTransitive(act,[1..n]) then Print("  intransitive\n"); return; fi;
  bl := AllBlocks(act);
  Print("  primitive=", IsPrimitive(act,[1..n]),
        "  SYSTEMS=", Length(bl), "  sizes=", Set(List(bl,Length)), "\n");
end;;
# cyclic 12-point configurations: C12 has block systems for every proper divisor
report(12, List([0..11], i -> [i, (i+1) mod 12, (i+4) mod 12] + 1), "Z12 {i,i+1,i+4}");
report(12, List([0..11], i -> [i, (i+2) mod 12, (i+6) mod 12] + 1), "Z12 {i,i+2,i+6}");
report(12, List([0..11], i -> [i, (i+3) mod 12, (i+6) mod 12] + 1), "Z12 {i,i+3,i+6}");
report(8,  List([0..7],  i -> [i, (i+1) mod 8, (i+4) mod 8] + 1),  "Z8  {i,i+1,i+4}");
report(10, List([0..9],  i -> [i, (i+1) mod 10, (i+5) mod 10] + 1),"Z10 {i,i+1,i+5}");
QUIT;
