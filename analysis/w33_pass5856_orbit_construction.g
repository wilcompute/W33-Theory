# Pass 5856 -- BREAKTHROUGH ATTEMPT on alpha(W(3,9)).
#
# Every attempt so far searched the POINT SET for a large coclique and plateaued at 51
# across three local-search classes (Pass 5784).  A maximum partial ovoid of a classical
# polar space is far more likely to be a union of ORBITS of a subgroup than something a
# random walk finds.  So: search the SUBGROUP LATTICE of Sp(4,9) instead, and ask which
# orbits on the 820 points are partial ovoids.
#
# An orbit of size > 51 that is pairwise non-collinear beats every search so far,
# structurally rather than by more compute.

q := 9;;
G := Sp(4,q);;
V := GF(q)^4;;
Print("Sp(4,", q, ") order ", Size(G), "\n");

# The 820 projective points, as normalised row vectors.
pts := [];;
for v in Elements(V) do
  if v <> Zero(V) then
    Add(pts, v);
  fi;
od;;
norm := function(v)
  local c;
  for c in v do
    if c <> Zero(GF(q)) then return v * c^-1; fi;
  od;
  return v;
end;;
P := Set(List(pts, norm));;
Print("projective points: ", Length(P), "\n");

J := [[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]] * One(GF(q));;
form := function(u,v) return u * J * v; end;;

# Maximal subgroups of Sp(4,9) -- the natural place large structured orbits live.
mx := MaximalSubgroupClassReps(G);;
Print("maximal subgroup classes: ", Length(mx), "\n");
best := 0;;
for H in mx do
  local orbs, o, S, ok, i, j, sz;
  Print("  |H| = ", Size(H), "  index ", Index(G, H), "\n");
  orbs := Orbits(H, P, OnLines);
  for o in orbs do
    sz := Length(o);
    if sz > 51 and sz <= 82 then
      # is this orbit a partial ovoid?
      ok := true;
      for i in [1..sz] do
        for j in [i+1..sz] do
          if form(norm(o[i]), norm(o[j])) = Zero(GF(q)) then ok := false; break; fi;
        od;
        if not ok then break; fi;
      od;
      if ok then
        Print("    *** PARTIAL OVOID ORBIT of size ", sz, " ***\n");
        if sz > best then best := sz; fi;
      fi;
    fi;
  od;
  Print("    orbit sizes: ", Set(List(orbs, Length)), "\n");
od;
Print("\nbest partial-ovoid orbit found: ", best, "  (local search reaches 51)\n");
QUIT;
