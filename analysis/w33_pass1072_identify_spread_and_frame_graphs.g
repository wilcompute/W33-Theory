# Pass 1072: is the spread graph REALLY the U4(2) rank-3 graph, and what is the
# frame graph?
#
# Pass 1071 computed that the 36 spreads of W(3,3) carry a graph with parameters
# SRG(36,15,6,6) and asserted in its commit message that this "is the rank-3 U4(2)
# graph".  That assertion was NOT checked -- it was inferred from the parameters
# plus the existence of an index-36 maximal S6 in PSp(4,3).
#
# This session has retracted one pass for exactly that move (Pass 1043: matching a
# profile and declaring an identification), so the inference is checked here rather
# than left standing.  And the check is chosen to be TYPE-CORRECT: subdegrees are
# compared to subdegrees, and the graph is compared to an orbital of the group
# acting on the same 36 objects, not to a catalogue entry with matching numbers.
#
# There are several strongly regular graphs with parameters (36,15,6,6) -- the
# parameter set does not determine the graph -- so "SRG(36,15,6,6)" alone would not
# have settled it either way.
#
# PRIOR ART -- cited, not reclaimed:
#   * BT813 OWNS the subdegrees [1,15,20].  Its vacuum transition matrix records
#     the M36/G36 diagonal as exactly [1,15,20] and names it "the double-six
#     ranks", GAP-witnessed, with the classical identification (the 36 spreads of
#     W(3,3) are the 36 double-sixes of the 27 lines on a cubic surface).  The
#     rank-3 fact is BT813's, not this pass's, and this pass recomputes it only as
#     an internal consistency check.  It was found by the rediscovery guard, which
#     flagged [1,15,20] on the first run -- see the note below.
#   * Pass 1071 -- the 36 x 540 incidence and the SRG(36,15,6,6) parameters.
#   * Pass 1067 (parallel track) -- the 36-class / spread identification.
#   * Pass 1070 -- the retraction that motivates checking rather than inferring.
#
# WHAT IS ACTUALLY NEW HERE, stated narrowly:
#   (1) that the Pass 1071 graph -- built from SHARED FRAMES, with no group action
#       used in its construction -- is EQUAL AS AN EDGE SET to the group's
#       valency-15 orbital.  BT813 gives the orbit partition; it does not identify
#       any independently-built graph with it.  That gap is the whole point: there
#       are 32,548 strongly regular graphs with parameters (36,15,6,6), so matching
#       parameters identifies nothing, and matching a rank-3 profile is precisely
#       the inference Pass 1043 was retracted for.
#   (2) the FRAME side, which BT813's matrix does not cover: PSp(4,3) acts on the
#       540 frames at rank 32, and the frame graph is regular of degree 117 but is
#       NOT strongly regular.
#
# GUARD NOTE.  `scripts/check_rediscovery.py` flagged [1,15,20] -> BT813 the first
# time it was run on this file.  It had never run on it before, because the
# pre-commit hook's file filter was `\.(py|md)$` -- .g was excluded, so no GAP pass
# in this repository had ever been guarded.  That filter is fixed in the same
# commit as this pass.

REPO := GAPInfo.SystemEnvironment.W33_REPO;;
OUT := Concatenation(REPO, "/data/w33_pass1072_identify_spread_and_frame_graphs.json");;
DIAG := Concatenation(REPO, "/data/w33_pass1072_diagnostic.txt");;

A := function(l, c) if not c then Error(Concatenation("Pass1072 failed: ", l)); fi; end;;
B := function(v) if v then return "true"; fi; return "false"; end;;

# GAP's String() on a record emits `rec( k := 15, ... )`, which is NOT JSON.
# Emit the graph parameters explicitly instead.
GJ := function(r)
  return Concatenation("{\"n\": ", String(r.n), ", \"k\": ", String(r.k),
    ", \"lambda\": ", String(r.lambda), ", \"mu\": ", String(r.mu),
    ", \"strongly_regular\": ", B(r.ok), "}");
end;;

SRG := function(adj, n)
  local kk, lam, mu, i, j, common, ok;
  kk := Length(adj[1]); lam := fail; mu := fail; ok := true;
  for i in [1..n] do
    if Length(adj[i]) <> kk then ok := false; fi;
    for j in [1..n] do
      if i <> j then
        common := Length(Intersection(adj[i], adj[j]));
        if j in adj[i] then
          if lam = fail then lam := common; elif lam <> common then ok := false; fi;
        else
          if mu = fail then mu := common; elif mu <> common then ok := false; fi;
        fi;
      fi;
    od;
  od;
  return rec(ok := ok, n := n, k := kk, lambda := lam, mu := mu);
end;;

Main := function()
  local S, J, pts, act, P, lines, sp, L, i, j, p, q, spreads, cur,
        FindSpreads, onpt, lineIdx, frames, frameIdx, spAct, spImg, spSub,
        orb15, adjSp, srgSp, myAdjSp, frAct, frImg, frSub, adjFr, srgFr,
        lineAct, PL,
        checks, names, stream, tag, rec1;

  S := Sp(4,3);
  J := InvariantBilinearForm(S).matrix;
  pts := NormedRowVectors(GF(3)^4);
  A("40 points", Length(pts) = 40);
  act := ActionHomomorphism(S, pts, OnLines);
  P := Image(act);
  A("PSp(4,3) order 25920", Size(P) = 25920);

  # totally isotropic lines as 4-point sets
  lines := [];
  for sp in Subspaces(GF(3)^4, 2) do
    L := BasisVectors(Basis(sp));
    if IsZero(L[1] * J * L[2]) then
      Add(lines, Set(Filtered([1..40], k -> pts[k] in sp)));
    fi;
  od;
  lines := Set(lines);
  A("40 lines", Length(lines) = 40);

  onpt := List([1..40], p2 -> Filtered([1..40], li -> p2 in lines[li]));

  # spreads: 10 pairwise disjoint lines covering all 40 points
  spreads := [];
  FindSpreads := function(chosen, used)
    local pmin, li;
    if Length(used) = 40 then Add(spreads, Set(chosen)); return; fi;
    pmin := First([1..40], x -> not (x in used));
    for li in onpt[pmin] do
      if IsEmpty(Intersection(lines[li], used)) then
        FindSpreads(Concatenation(chosen, [li]), Union(used, lines[li]));
      fi;
    od;
  end;;
  FindSpreads([], []);
  A("36 spreads", Length(spreads) = 36);

  # frames: unordered pairs of disjoint lines
  frames := [];
  for i in [1..40] do
    for j in [i+1..40] do
      if IsEmpty(Intersection(lines[i], lines[j])) then Add(frames, [i,j]); fi;
    od;
  od;
  A("540 frames", Length(frames) = 540);

  # ---- THE CHECK: PSp(4,3) on the 36 spreads -----------------------------
  # P permutes POINTS; spreads and frames are sets of LINE indices, so the induced
  # action on lines has to be taken first or the ActionHomomorphism is ill-defined.
  lineAct := ActionHomomorphism(P, lines, OnSets);
  PL := Image(lineAct);
  spAct := ActionHomomorphism(PL, spreads, OnSets);
  spImg := Image(spAct);
  spSub := SortedList(List(Orbits(Stabilizer(spImg, 1), [1..36]), Length));

  # my Pass 1071 graph: spreads adjacent iff they share >= 2 lines (a frame)
  myAdjSp := List([1..36], x -> Filtered([1..36], y ->
    y <> x and Length(Intersection(spreads[x], spreads[y])) >= 2));

  # the group's valency-15 orbital on the same 36 objects
  orb15 := First(Orbits(Stabilizer(spImg, 1), [1..36]), t -> Length(t) = 15);
  adjSp := [];
  if orb15 <> fail then
    adjSp := List([1..36], x -> Set(List(orb15, t ->
      t ^ RepresentativeAction(spImg, 1, x))));
  fi;
  srgSp := SRG(myAdjSp, 36);

  # ---- the frame graph, full parameters this time ------------------------
  # NB: `fi` is a GAP keyword (it closes `if`), so this cannot be named fi.
  frameIdx := function(a, b) return Position(frames, [Minimum(a,b), Maximum(a,b)]); end;
  adjFr := List([1..540], x -> []);
  for i in [1..36] do
    cur := [];
    for p in [1..Length(spreads[i])] do
      for q in [p+1..Length(spreads[i])] do
        Add(cur, frameIdx(spreads[i][p], spreads[i][q]));
      od;
    od;
    for p in cur do
      adjFr[p] := Union(adjFr[p], Difference(cur, [p]));
    od;
  od;
  srgFr := SRG(adjFr, 540);

  frAct := ActionHomomorphism(PL, frames, OnSets);
  frImg := Image(frAct);
  frSub := SortedList(List(Orbits(Stabilizer(frImg, 1), [1..540]), Length));

  checks := rec();

  checks.PSp43_on_36_spreads_is_rank_three := spSub = [1,15,20];
  checks.spread_graph_has_srg_36_15_6_6 :=
    srgSp.ok and srgSp.k = 15 and srgSp.lambda = 6 and srgSp.mu = 6;
  # THE IDENTIFICATION, checked not inferred: my graph IS the group's orbital
  checks.spread_graph_IS_the_group_orbital :=
    orb15 <> fail and adjSp = myAdjSp;
  checks.PSp43_transitive_on_spreads := IsTransitive(spImg, [1..36]);

  checks.frame_graph_is_regular_degree_117 := srgFr.k = 117;
  # EXPECTATION CORRECTED BY THE COMPUTATION.  I asserted the frame graph would be
  # strongly regular by analogy with the spread side.  It is not: lambda and mu
  # vary, and PSp(4,3) acts on the 540 frames at RANK 32, not rank 3.  The two
  # sides of the incidence are genuinely different in kind -- the spread side is a
  # rank-3 orbital, the frame side is not.
  checks.frame_graph_is_NOT_strongly_regular := not srgFr.ok;
  checks.frame_action_is_rank_32 := Length(frSub) = 32;
  checks.PSp43_transitive_on_frames := IsTransitive(frImg, [1..540]);

  names := RecNames(checks);
  stream := OutputTextFile(DIAG, false);
  SetPrintFormattingStatus(stream, false);
  for tag in names do
    WriteAll(stream, Concatenation(tag, " = ", B(checks.(tag)), "\n"));
  od;
  WriteAll(stream, Concatenation("spread SUBDEGREES = ", String(spSub), "\n"));
  WriteAll(stream, Concatenation("spread graph = ", String(srgSp), "\n"));
  WriteAll(stream, Concatenation("graph = group orbital : ",
    B(orb15 <> fail and adjSp = myAdjSp), "\n"));
  WriteAll(stream, Concatenation("frame SUBDEGREES = ", String(frSub), "\n"));
  WriteAll(stream, Concatenation("frame graph = ", String(srgFr), "\n"));
  CloseStream(stream);
  A("all checks", ForAll(names, tag -> checks.(tag)));

  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1072.identify_spread_and_frame_graphs.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"Pass 1071's identification is CHECKED, not inferred. The Pass 1071 spread graph -- built from shared frames, with no group action used in its construction -- is EQUAL AS AN EDGE SET to the valency-15 orbital of PSp(4,3) on the 36 spreads. So it really is the rank-3 graph and not merely a graph with matching parameters: 32,548 strongly regular graphs share (36,15,6,6), so the parameters identify nothing on their own. The subdegrees [1,15,20] are BT813's and are cited, not reclaimed. NEW on the frame side: PSp(4,3) acts on the 540 frames at RANK 32, and the frame graph is regular of degree 117 but NOT strongly regular -- the two sides of the incidence are different in kind.\",\n");
  WriteAll(stream, "  \"prior_art\": \"BT813 owns the subdegrees [1,15,20]: its vacuum transition matrix records the M36/G36 diagonal as [1,15,20] and names it the double-six ranks, GAP-witnessed, with the classical identification of the 36 spreads with the 36 double-sixes of the 27 lines on a cubic surface. This pass recomputes them only as an internal consistency check. The collision was found by scripts/check_rediscovery.py on its first ever run against a .g file: the pre-commit filter matched only (py|md), so no GAP pass in this repository had ever been guarded. That filter is fixed in the same commit.\",\n");
  WriteAll(stream, Concatenation("  \"spread_subdegrees\": ", String(spSub), ",\n"));
  WriteAll(stream, Concatenation("  \"spread_graph\": ", GJ(srgSp), ",\n"));
  WriteAll(stream, Concatenation("  \"frame_subdegrees\": ", String(frSub), ",\n"));
  WriteAll(stream, Concatenation("  \"frame_graph\": ", GJ(srgFr), ",\n"));
  WriteAll(stream, "  \"why_this_needed_checking\": \"Several strongly regular graphs share the parameter set (36,15,6,6), so the parameters alone do not determine the graph. Pass 1071's commit inferred the identification from the parameters plus the existence of an index-36 maximal S6 in PSp(4,3). This session retracted Pass 1043 for exactly that move, so the inference is verified here by equality of edge sets against the group's own orbital -- a type-correct comparison.\",\n");
  WriteAll(stream, "  \"scope\": \"Identification of the spread graph with the group orbital, and the frame graph's measured parameters. No catalogue lookup is performed and no claim is made about which named graph in the literature this is beyond its being the PSp(4,3) rank-3 orbital.\",\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for tag in names do
    WriteAll(stream, Concatenation("    \"", tag, "\": ", B(checks.(tag))));
    if tag <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);
  Print("Pass1072 status=PASS checks=", Length(names), " output=", OUT, "\n");
end;;

Main();;
QUIT;
