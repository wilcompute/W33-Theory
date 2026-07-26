# Pass 1070: RETRACTION of Pass 1043.  Suborbits are not orbits.
#
# Pass 1043 concluded "the Springer construction lands on the Pass 117
# ordered-pair W(E6) embedding, not the code embedding."  That conclusion is
# WRONG and is withdrawn here.  The parallel track's Passes 1063-1069 reached the
# opposite answer -- the Pass 125 CODE embedding -- and they are right.
#
# THE ERROR, exactly.  w33_paper.tex thm:two-we6-embeddings distinguishes the two
# copies of W(E6) by their ORBITS on C^perp/C:
#
#     code embedding (Pass 125): 256 = 1 + 135 + 120
#         -- transitive on the 135 isotropic and on the 120 anisotropic classes;
#     Pass 117 embedding:        isotropic orbits 27,36,36,36
#                                anisotropic orbits 1,1,1,27,27,27,36
#         -- INTRANSITIVE on both.
#
# Pass 1043 computed
#
#     sub120 := SortedList(List(Orbits(Stabilizer(Q120, 1), [1..120]), Length));
#
# which is the orbit list of a POINT STABILISER -- the SUBDEGREES of a transitive
# action -- stored it in a field named "anisotropic_orbit_sizes", and compared it
# to the paper's ORBIT sizes.  Those are different invariants.  The numbers
# 1,1,1,27,27,27,36 do coincide, which is why the error survived review, but a
# suborbit profile and an orbit profile are not comparable quantities.
#
# THE CORRECT ANSWER is forced and needs no new machinery.  The tower is transitive
# on the 240 roots (Pass 1020) and the 120 antipodal pairs are a BLOCK SYSTEM, so
# the induced action on the 120 is transitive.  Transitive means the orbit list is
# [120] -- exactly the code fingerprint 256 = 1 + 135 + 120 -- and NOT the Pass 117
# fingerprint, which has three fixed points.  A group with a fixed point on the 120
# cannot be transitive on it.
#
# This pass verifies both numbers side by side so the distinction is on record as
# data rather than as prose.
#
# WHAT SURVIVES.  Pass 1041 is unaffected: it matched the SRG(120,63,30,36)
# axis-pairing graph, built from orthogonality rather than from any group action,
# and separately observed the subdegrees.  Only the EMBEDDING IDENTIFICATION in
# Pass 1043 is withdrawn.
#
# METHOD NOTE.  This is the same failure the corpus has recorded twice before under
# a different surface: Sp(4,3) versus W(E6) (equal orders, different groups) and
# Pass 338's selector frame (equal subdegrees, different groups).  Here it is equal
# NUMBERS attached to different INVARIANTS.  The lesson is narrower than "check the
# group": check that the two quantities being compared are the same kind of thing.
#
# PRIOR ART / CROSS-TRACK:
#   * w33_paper.tex thm:two-we6-embeddings owns both fingerprints.
#   * Passes 1063-1069 (parallel track) reached the correct answer first and are
#     credited with it; this pass supplies the retraction on my side.
#   * Pass 1020 -- transitivity of the tower on the 240 roots.

REPO := GAPInfo.SystemEnvironment.W33_REPO;;
OUT := Concatenation(REPO, "/data/w33_pass1070_retract_1043_suborbits_are_not_orbits.json");;
DIAG := Concatenation(REPO, "/data/w33_pass1070_diagnostic.txt");;

A := function(l, c) if not c then Error(Concatenation("Pass1070 failed: ", l)); fi; end;;
B := function(v) if v then return "true"; fi; return "false"; end;;

Main := function()
  local roots, v, i, j, si, sj, m, k, rootIndex, ReflPerm, simples, W,
        cox, w, C, K, N, b2, sys2, homK, QK, homN, QN,
        orbitsK, suborbK, orbitsN, suborbN,
        checks, names, stream, tag;

  roots := [];
  for i in [1..8] do
    for j in [i+1..8] do
      for si in [1,-1] do for sj in [1,-1] do
        v := ListWithIdenticalEntries(8, 0);
        v[i] := 2*si; v[j] := 2*sj; Add(roots, v);
      od; od;
    od;
  od;
  for m in [0..255] do
    v := List([0..7], k -> (-1)^(QuoInt(m, 2^k) mod 2));
    if Number(v, x -> x = -1) mod 2 = 0 then Add(roots, v); fi;
  od;
  rootIndex := function(x) return Position(roots, x); end;
  ReflPerm := function(r) return PermList(List(roots, x -> rootIndex(x - ((x*r)/4)*r))); end;
  simples := [
    [ 1,-1,-1,-1,-1,-1,-1, 1], [ 2, 2, 0, 0, 0, 0, 0, 0],
    [-2, 2, 0, 0, 0, 0, 0, 0], [ 0,-2, 2, 0, 0, 0, 0, 0],
    [ 0, 0,-2, 2, 0, 0, 0, 0], [ 0, 0, 0,-2, 2, 0, 0, 0],
    [ 0, 0, 0, 0,-2, 2, 0, 0], [ 0, 0, 0, 0, 0,-2, 2, 0] ];
  W := Group(List(simples, ReflPerm));
  cox := Product(List(simples, ReflPerm));
  w := cox ^ 10;
  C := Centralizer(W, w);
  K := DerivedSubgroup(C);
  N := Normalizer(W, Group(w));
  A("|K| = 51840", Size(K) = 51840);

  b2 := First(AllBlocks(K), b -> Length(b) = 2);
  sys2 := Blocks(K, [1..240], b2);
  A("120 antipodal blocks", Length(sys2) = 120);

  homK := ActionHomomorphism(K, sys2, OnSets);  QK := Image(homK);
  homN := ActionHomomorphism(N, sys2, OnSets);  QN := Image(homN);

  # THE TWO QUANTITIES, side by side.
  orbitsK := SortedList(List(Orbits(QK, [1..120]), Length));
  suborbK := SortedList(List(Orbits(Stabilizer(QK, 1), [1..120]), Length));
  orbitsN := SortedList(List(Orbits(QN, [1..120]), Length));
  suborbN := SortedList(List(Orbits(Stabilizer(QN, 1), [1..120]), Length));

  checks := rec();

  # the group IS transitive: orbit list is [120], the code fingerprint
  checks.tower_is_transitive_on_the_120 := IsTransitive(QK, [1..120]);
  checks.orbit_list_is_a_single_block_of_120 := orbitsK = [120];
  checks.normaliser_also_transitive := orbitsN = [120];

  # the number Pass 1043 quoted is the SUBORBIT list, a different invariant
  checks.suborbits_are_the_1043_numbers := suborbK = [1,1,1,27,27,27,36];
  checks.orbits_and_suborbits_differ := orbitsK <> suborbK;

  # therefore the Pass 117 fingerprint is EXCLUDED: it has fixed points
  checks.pass117_fingerprint_needs_fixed_points :=
    1 in [1,1,1,27,27,27,36];
  checks.transitive_action_has_no_fixed_points :=
    not (1 in orbitsK);
  checks.pass117_identification_is_refuted :=
    IsTransitive(QK, [1..120]) and orbitsK <> [1,1,1,27,27,27,36];

  # and the code fingerprint is the one that matches
  checks.code_embedding_is_the_correct_answer := orbitsK = [120];

  names := RecNames(checks);
  stream := OutputTextFile(DIAG, false);
  SetPrintFormattingStatus(stream, false);
  for tag in names do
    WriteAll(stream, Concatenation(tag, " = ", B(checks.(tag)), "\n"));
  od;
  WriteAll(stream, Concatenation("ORBITS   of K on 120 = ", String(orbitsK), "\n"));
  WriteAll(stream, Concatenation("SUBORBITS of K on 120 = ", String(suborbK), "\n"));
  WriteAll(stream, Concatenation("ORBITS   of N on 120 = ", String(orbitsN), "\n"));
  WriteAll(stream, Concatenation("SUBORBITS of N on 120 = ", String(suborbN), "\n"));
  CloseStream(stream);
  A("all checks", ForAll(names, tag -> checks.(tag)));

  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1070.retract_1043.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"retracts\": \"Pass 1043 (analysis/w33_pass1043_which_we6_embedding.g and its certificate)\",\n");
  WriteAll(stream, "  \"headline\": \"Pass 1043 is WITHDRAWN. It compared SUBORBITS to ORBITS. The tower is transitive on the 120 anisotropic classes, so its orbit list is [120] -- the Pass 125 CODE embedding fingerprint 256 = 1+135+120 -- and not the Pass 117 fingerprint, which has three fixed points and cannot belong to a transitive group. The parallel track's Passes 1063-1069 reached the correct answer and are credited with it.\",\n");
  WriteAll(stream, Concatenation("  \"orbits_on_120\": ", String(orbitsK), ",\n"));
  WriteAll(stream, Concatenation("  \"suborbits_on_120\": ", String(suborbK), ",\n"));
  WriteAll(stream, "  \"the_error\": \"Pass 1043 computed Orbits(Stabilizer(Q120,1), [1..120]) -- the subdegrees of a transitive action -- stored the result in a field named 'anisotropic_orbit_sizes', and matched it against the paper's ORBIT sizes for the Pass 117 embedding. The two lists agree numerically (1,1,1,27,27,27,36), which is why the error survived, but a suborbit profile and an orbit profile are not the same invariant and are not comparable.\",\n");
  WriteAll(stream, "  \"what_survives\": \"Pass 1041 is unaffected. It matched the SRG(120,63,30,36) axis-pairing graph, built from the orthogonality relation rather than from a group action, and only separately reported the subdegrees. Its identification of the Eisenstein fibre with the paper's axis-glue carrier stands. Only the embedding identification of Pass 1043 is withdrawn.\",\n");
  WriteAll(stream, "  \"method_note\": \"Third instance of one failure mode wearing a new surface. Sp(4,3) vs W(E6): equal orders, different groups. Pass 338's selector frame: equal subdegrees, different groups. Here: equal numbers attached to DIFFERENT INVARIANTS. The rule that would have caught all three is narrower than 'check the group' -- check that the two quantities being compared are the same kind of quantity before comparing them at all.\",\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for tag in names do
    WriteAll(stream, Concatenation("    \"", tag, "\": ", B(checks.(tag))));
    if tag <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);
  Print("Pass1070 status=PASS checks=", Length(names), " output=", OUT, "\n");
end;;

Main();;
QUIT;
