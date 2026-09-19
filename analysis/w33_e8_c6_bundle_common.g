# Common deterministic constructor for Passes 1023--1027.
#
# Rebuilds the 240 E8 roots, W(E8), the regular order-3 centralizer,
# K = Sp(4,3), and the invariant block systems of sizes 2, 3, and 6.
# No optional GAP package or random search is used.

Bool102x := function(value)
  if value then return "true"; fi;
  return "false";
end;;

ConstituentBlocks102x := function(container, blocks)
  return Filtered(blocks, block -> ForAll(block, point -> point in container));
end;;

FixedPoints102x := function(group, points)
  local gens;
  gens := GeneratorsOfGroup(group);
  return Filtered(points, point -> ForAll(gens, g -> point ^ g = point));
end;;

FixedBlocks102x := function(group, blocks)
  local gens;
  gens := GeneratorsOfGroup(group);
  return Filtered(blocks, block -> ForAll(gens, g ->
    Set(List(block, point -> point ^ g)) = Set(block)));
end;;

AdmitsPointSection102x := function(group, baseBlocks)
  local orbit, base, stabilizer;
  for orbit in Orbits(group, baseBlocks, OnSets) do
    base := orbit[1];
    stabilizer := Stabilizer(group, base, OnSets);
    if Length(FixedPoints102x(stabilizer, base)) = 0 then return false; fi;
  od;
  return true;
end;;

AdmitsBlockSection102x := function(group, baseBlocks, subBlocks)
  local orbit, base, candidates, stabilizer;
  for orbit in Orbits(group, baseBlocks, OnSets) do
    base := orbit[1];
    candidates := ConstituentBlocks102x(base, subBlocks);
    stabilizer := Stabilizer(group, base, OnSets);
    if Length(FixedBlocks102x(stabilizer, candidates)) = 0 then return false; fi;
  od;
  return true;
end;;

OrderedFibre102x := function(fibre, unit)
  local root;
  root := Minimum(fibre);
  return List([0..5], power -> root ^ (unit ^ power));
end;;

BuildE8C6Bundle102x := function()
  local roots, v, i, j, si, sj, m, k, rootIndex, ReflPerm, simples,
        W, cox, omega, C, K, neg, unit, allBlocks,
        block2, block3, block6, pairs, triples, fibres, orderedFibres;

  roots := [];
  for i in [1..8] do
    for j in [i+1..8] do
      for si in [1,-1] do
        for sj in [1,-1] do
          v := ListWithIdenticalEntries(8, 0);
          v[i] := 2*si; v[j] := 2*sj;
          Add(roots, v);
        od;
      od;
    od;
  od;
  for m in [0..255] do
    v := List([0..7], k -> (-1)^(QuoInt(m, 2^k) mod 2));
    if Number(v, x -> x = -1) mod 2 = 0 then Add(roots, v); fi;
  od;

  rootIndex := function(x) return Position(roots, x); end;
  ReflPerm := function(r)
    return PermList(List(roots, x -> rootIndex(x - ((x * r) / 4) * r)));
  end;

  simples := [
    [ 1,-1,-1,-1,-1,-1,-1, 1], [ 2, 2, 0, 0, 0, 0, 0, 0],
    [-2, 2, 0, 0, 0, 0, 0, 0], [ 0,-2, 2, 0, 0, 0, 0, 0],
    [ 0, 0,-2, 2, 0, 0, 0, 0], [ 0, 0, 0,-2, 2, 0, 0, 0],
    [ 0, 0, 0, 0,-2, 2, 0, 0], [ 0, 0, 0, 0, 0,-2, 2, 0] ];

  W := Group(List(simples, ReflPerm));
  cox := Product(List(simples, ReflPerm));
  omega := cox ^ 10;
  C := Centralizer(W, omega);
  K := DerivedSubgroup(C);
  neg := PermList(List(roots, x -> rootIndex(-x)));
  unit := cox ^ 5;

  allBlocks := AllBlocks(K);
  block2 := First(allBlocks, block -> Length(block) = 2);
  block3 := First(allBlocks, block -> Length(block) = 3);
  block6 := First(allBlocks, block -> Length(block) = 6);
  pairs := Blocks(K, [1..240], block2);
  triples := Blocks(K, [1..240], block3);
  fibres := Blocks(K, [1..240], block6);
  orderedFibres := List(fibres, fibre -> OrderedFibre102x(fibre, unit));

  return rec(
    roots := roots,
    W := W,
    cox := cox,
    omega := omega,
    centralizer := C,
    K := K,
    center := Center(K),
    neg := neg,
    unit := unit,
    pairs := pairs,
    triples := triples,
    fibres := fibres,
    orderedFibres := orderedFibres
  );
end;;
