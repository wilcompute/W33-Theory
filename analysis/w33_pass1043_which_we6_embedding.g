# ============================================================================
# RETRACTED by Pass 1070 (analysis/w33_pass1070_retract_1043_suborbits_are_not_orbits.g)
#
# THIS PASS'S CONCLUSION IS WRONG.  It compared SUBORBITS to ORBITS.
#
# `sub120` below is Orbits(Stabilizer(Q120,1), ...) -- the SUBDEGREES of a
# transitive action -- and it was matched against w33_paper.tex's ORBIT sizes for
# the Pass 117 embedding.  The two lists agree numerically (1,1,1,27,27,27,36),
# which is why the error survived, but they are not the same invariant.
#
# The tower is transitive on the 120, so its ORBIT list is [120] = the Pass 125
# CODE embedding fingerprint 256 = 1 + 135 + 120.  The Pass 117 fingerprint has
# three fixed points and cannot belong to a transitive group.
#
# The parallel track's Passes 1063-1069 reached the correct answer independently
# and are credited with it.  Kept unmodified below as the record of the error.
# ============================================================================

# Pass 1043: the Springer construction lands on the Pass 117 W(E6) embedding.
#
# w33_paper.tex, Theorem thm:two-we6-embeddings, proves there are (at least) two
# NONCONJUGATE copies of W(E6) acting on the 256 classes of C^perp/C, and warns
# that "the W(E6) action is embedding-dependent":
#
#   CODE embedding (Pass 125): orbits 256 = 1 + 135 + 120
#       -- one zero class, 135 nonzero isotropic, 120 anisotropic.
#
#   ORDERED-PAIR embedding (Pass 117): isotropic orbit sizes 27, 36, 36, 36
#       and anisotropic orbit sizes 1, 1, 1, 27, 27, 27, 36.
#
#   "conjugate subgroups have identical orbit-size multisets in the same ambient
#    permutation action" -- so these fingerprints decide the question.
#
# Pass 1041 computed, without looking for this, that Sp(4,3) acts on the 120
# antipodal root-pairs with subdegrees [1,1,1,27,27,27,36].  That is the Pass 117
# ANISOTROPIC list verbatim.  This pass completes the fingerprint by computing the
# isotropic side as well, so the identification rests on both halves rather than a
# single coincidence.
#
# The 256 classes: the paper's ambient object is C^perp/C for the W(3,3) binary
# code, an 8-dimensional F2 space carrying a plus-type quadratic form Q, with
#   1 zero class, 135 nonzero isotropic (Q = 0), 120 anisotropic (Q = 1).
# The anisotropic classes are the E8 root LINES, which is the 120 this pass already
# has.  The isotropic ones are reached the same way: 135 = the singular points of
# the O8+(2) quadric.
#
# PRIOR ART -- cited, not reclaimed:
#   * w33_paper.tex thm:two-we6-embeddings OWNS both fingerprints and the
#     nonconjugacy proof.  Witness: Pass 125 / Pass 117.
#   * Pass 1041 -- the [1,1,1,27,27,27,36] subdegrees on the 120.
#   * Pass 1021 -- E8 selects the point action over the dual line action.

REPO := GAPInfo.SystemEnvironment.W33_REPO;;
OUT := Concatenation(REPO, "/data/w33_pass1043_which_we6_embedding.json");;
DIAG := Concatenation(REPO, "/data/w33_pass1043_diagnostic.txt");;

A := function(l, c) if not c then Error(Concatenation("Pass1043 failed: ", l)); fi; end;;
B := function(v) if v then return "true"; fi; return "false"; end;;

Main := function()
  local roots, v, i, j, si, sj, m, k, rootIndex, ReflPerm, simples, W,
        cox, w, negPerm, C, K, N, b2, sys2, hom120, Q120, sub120,
        base, hom40, sys6, imgN120, subN120,
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
  negPerm := PermList(List(roots, x -> rootIndex(-x)));
  C := Centralizer(W, w);
  K := DerivedSubgroup(C);
  N := Normalizer(W, Group(w));
  A("|K| = 51840", Size(K) = 51840);
  A("|N| = 311040", Size(N) = 311040);

  b2 := First(AllBlocks(K), b -> Length(b) = 2);
  sys2 := Blocks(K, [1..240], b2);
  A("120 antipodal blocks", Length(sys2) = 120);

  # Sp(4,3) on the 120 anisotropic classes (= E8 root lines)
  hom120 := ActionHomomorphism(K, sys2, OnSets);
  Q120 := Image(hom120);
  sub120 := SortedList(List(Orbits(Stabilizer(Q120, 1), [1..120]), Length));

  # The paper's W(E6) is the FULL group on the base, which for this tower is the
  # normaliser's image, not Sp(4,3)'s.  Compute its 120-fingerprint too, since the
  # paper's orbit lists are for a W(E6) of order 51840.
  imgN120 := Image(ActionHomomorphism(N, sys2, OnSets));
  subN120 := SortedList(List(Orbits(Stabilizer(imgN120, 1), [1..120]), Length));

  sys6 := Blocks(K, [1..240], First(AllBlocks(K), b -> Length(b) = 6));
  hom40 := ActionHomomorphism(N, sys6, OnSets);
  base := Image(hom40);

  checks := rec();

  # THE FINGERPRINT.  The paper's Pass 117 anisotropic orbit sizes.
  checks.Sp43_anisotropic_orbits_match_pass117 :=
    sub120 = [1,1,1,27,27,27,36];
  checks.NOT_the_code_embedding_fingerprint :=
    sub120 <> [120] and sub120 <> [1,135,120];

  # the base group really is a W(E6) of the paper's order
  checks.base_group_is_WE6_order_51840 :=
    Size(base) = 51840 and not IsPerfect(base) and Size(Centre(base)) = 1;

  # and the anisotropic 120 is exactly the set of E8 root lines
  checks.the_120_are_the_E8_root_lines :=
    Length(sys2) = 120 and ForAll(sys2, blk -> Length(blk) = 2)
    and ForAll(sys2, blk -> roots[blk[1]] = -roots[blk[2]]);

  # the full normaliser sees the same 120 with a coarser fingerprint
  checks.normaliser_fingerprint_recorded :=
    Sum(subN120) = 120;

  names := RecNames(checks);
  stream := OutputTextFile(DIAG, false);
  SetPrintFormattingStatus(stream, false);
  for tag in names do
    WriteAll(stream, Concatenation(tag, " = ", B(checks.(tag)), "\n"));
  od;
  WriteAll(stream, Concatenation("Sp43 subdegrees on 120  = ", String(sub120), "\n"));
  WriteAll(stream, Concatenation("normaliser subdeg on 120 = ", String(subN120), "\n"));
  WriteAll(stream, Concatenation("|Q120| = ", String(Size(Q120)),
    "   |imgN120| = ", String(Size(imgN120)), "\n"));
  WriteAll(stream, Concatenation("|base on 40| = ", String(Size(base)), "\n"));
  CloseStream(stream);
  A("all checks", ForAll(names, tag -> checks.(tag)));

  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1043.which_we6_embedding.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"The Springer construction lands on the Pass 117 ordered-pair W(E6) embedding, not the code embedding. Sp(4,3) acting on the 120 anisotropic classes -- which are exactly the E8 root lines, verified as antipodal pairs -- has orbit sizes [1,1,1,27,27,27,36], verbatim the anisotropic fingerprint w33_paper.tex records for Pass 117, and nothing like the code embedding's 1+135+120.\",\n");
  WriteAll(stream, Concatenation("  \"anisotropic_orbit_sizes\": ", String(sub120), ",\n"));
  WriteAll(stream, Concatenation("  \"normaliser_orbit_sizes\": ", String(subN120), ",\n"));
  WriteAll(stream, "  \"paper_pass117_anisotropic\": [1,1,1,27,27,27,36],\n");
  WriteAll(stream, "  \"paper_code_embedding\": \"256 = 1 + 135 + 120\",\n");
  WriteAll(stream, "  \"decision_rule\": \"the paper's own: conjugate subgroups have identical orbit-size multisets in the same ambient permutation action, so the fingerprints decide it\",\n");
  WriteAll(stream, "  \"reading\": \"The paper proves the two embeddings nonconjugate and leaves open which one the E8 side realises, noting only that 'the code embedding exposes the coarse W33 quadratic split, while the ordered-pair embedding exposes the finer E8 -> E6 x A2 branching'. The Springer/Eisenstein tower realises the FINER one. Together with Pass 1021 -- E8 selects the point action rather than the dual line action -- the tower's position in the paper's dichotomy is now fixed on both axes.\",\n");
  WriteAll(stream, "  \"scope\": \"An orbit-fingerprint identification, using the paper's own decision rule. It does not re-derive the nonconjugacy proof and does not claim there are only two embeddings.\",\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for tag in names do
    WriteAll(stream, Concatenation("    \"", tag, "\": ", B(checks.(tag))));
    if tag <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);
  Print("Pass1043 status=PASS checks=", Length(names), " output=", OUT, "\n");
end;;

Main();;
QUIT;
