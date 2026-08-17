# Pass 5848 (ITEM 1): n=12 and n=15 cyclic configs -- do any have TWO block systems
# AND a nonzero kernel?  That is the witness Pass 5833 asked for.
LoadPackage("grape");;
check := function(n, a, b)
  local blocks, nb, adj, i, v, levi, A, S, act, bl;
  blocks := List([0..n-1], i -> [ i, (i+a) mod n, (i+b) mod n ] + 1);
  nb := n;
  adj := List([1..2*n], i -> []);
  for i in [1..nb] do
    for v in blocks[i] do Add(adj[v], n+i); Add(adj[n+i], v); od;
  od;
  levi := Graph(Group(()), [1..2*n], OnPoints,
                function(x,y) return y in adj[x]; end, true);
  A := AutomorphismGroup(levi);
  S := Stabilizer(A, [1..n], OnSets);
  if Size(S) = 1 then return; fi;
  act := Action(S, [1..n], OnPoints);
  if not IsTransitive(act,[1..n]) then return; fi;
  bl := AllBlocks(act);
  if Length(bl) >= 2 then
    Print("  n=", n, " {0,", a, ",", b, "}: SYSTEMS=", Length(bl),
          " sizes=", Set(List(bl,Length)), " |G|=", Size(act), "\n");
  fi;
end;;
Print("n=12, kernel-nonzero triples with >=2 block systems:\n");
for a in [1..11] do for b in [a+1..11] do check(12,a,b); od; od;
Print("n=15:\n");
for a in [1..14] do for b in [a+1..14] do check(15,a,b); od; od;
QUIT;
