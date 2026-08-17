# Pass5703 (Track A support): staged TransitiveIdentification settling test.
# Track A reduced the tomotope-W33 bridge to one integer: the TransitiveIdentification
# of the q=5 design's action on its moving 12 points is 165 (equivariant bridge),
# 161 or 163 (isomorphic but inequivalent actions), or anything else (not W(F4)/Z).
#
# Stage 1 is self-contained and verifies the three candidates.
# Stage 2 is a template: load the q=5 design's 12-point action (needs the
# 325-vertex cover data from the Track A corpus) and type it.

# ---- Stage 1: the three candidates are exactly the faithful W(F4)/Z degree-12 actions
cand := [TransitiveGroup(12,161), TransitiveGroup(12,163), TransitiveGroup(12,165)];
Print("orders: ", List(cand, Size), "\n");               # expect [576, 576, 576]
Print("smallgroup ids: ", List(cand, g -> IdSmallGroup(g)), "\n");  # expect all [576, 8654]
wf4modZ := SmallGroup(576, 8654);
Print("all isomorphic to W(F4)/Z: ",
      List(cand, g -> IsomorphismGroups(g, wf4modZ) <> fail), "\n");
Print("pairwise abstract isomorphisms (expected true, true, true): ",
      [IsomorphismGroups(cand[1], cand[2]) <> fail,
       IsomorphismGroups(cand[1], cand[3]) <> fail,
       IsomorphismGroups(cand[2], cand[3]) <> fail], "\n");
# permutation inequivalence is what TransitiveIdentification distinguishes.

# ---- Stage 2: type the q=5 action (requires Track A data)
# G5 := < permutation group on the moving 12 of the q=5 design >;
# if IsTransitive(G5) and Size(G5) = 576 then
#   t := TransitiveIdentification(G5);
#   Print("settling integer: ", t, "\n");
#   if t = 165 then Print("BRIDGE EQUIVARIANT\n");
#   elif t in [161,163] then Print("ISOMORPHIC BUT INEQUIVALENT ACTIONS\n");
#   else Print("NOT W(F4)/Z -- order match only\n"); fi;
# fi;
