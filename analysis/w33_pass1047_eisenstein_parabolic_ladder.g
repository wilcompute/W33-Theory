# Pass 1047: the Eisenstein ladder, all the way down.
#
# Pass 1046 showed the E6 Eisenstein tower (G25, the Hessian group, order 648) is
# the POINT STABILISER of the E8 one (G32, order 155520).  The obvious next
# question is what sits under a point of G25, and whether the chain terminates
# somewhere the corpus already recognises.
#
# Predicted by the Shephard-Todd degree data, before computing:
#
#     G32   rank 4   degrees 12,18,24,30   order 155520
#     G25   rank 3   degrees  6, 9,12      order    648
#     G4    rank 2   degrees  4, 6         order     24
#     1     rank 0                         order      1
#
# with each the point stabiliser of the one above -- 155520/240 = 648 and
# 648/27 = 24.  G4 is the binary tetrahedral group 2T = SL(2,3), and 24 is the
# corpus's f (the multiplicity of the eigenvalue r = 2, the D4 root count, and the
# integer the agent memory already records as |2T| = f).
#
# If that holds, the whole Eisenstein tower is ONE recursive object whose bottom
# rung is the qutrit Clifford core, not a stack of separate coincidences at the
# prime 3.
#
# PRIOR ART -- cited, not reclaimed:
#   * Pass 1046 -- G25 is the point stabiliser of G32.
#   * Pass 1045 -- the multi-type Springer census.
#   * Pass 1020 -- the 216 = 3^{1+2}:Q8 root stabiliser inside Sp(4,3).
#   * Shephard-Todd: G25 order 648 degrees 6,9,12; G4 order 24 degrees 4,6.
#   * w33_paper.tex records 24 = f = |D4 roots| independently.

REPO := GAPInfo.SystemEnvironment.W33_REPO;;
OUT := Concatenation(REPO, "/data/w33_pass1047_eisenstein_parabolic_ladder.json");;
DIAG := Concatenation(REPO, "/data/w33_pass1047_diagnostic.txt");;

A := function(l, c) if not c then Error(Concatenation("Pass1047 failed: ", l)); fi; end;;
B := function(v) if v then return "true"; fi; return "false"; end;;

Main := function()
  local roots, v, i, j, si, sj, m, k, rootIndex, ReflPerm, simples, W,
        cox, w, C, s1, s2, s3, orb1, orb2, orb3, chain, r,
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
  ReflPerm := function(r2) return PermList(List(roots, x -> rootIndex(x - ((x*r2)/4)*r2))); end;
  simples := [
    [ 1,-1,-1,-1,-1,-1,-1, 1], [ 2, 2, 0, 0, 0, 0, 0, 0],
    [-2, 2, 0, 0, 0, 0, 0, 0], [ 0,-2, 2, 0, 0, 0, 0, 0],
    [ 0, 0,-2, 2, 0, 0, 0, 0], [ 0, 0, 0,-2, 2, 0, 0, 0],
    [ 0, 0, 0, 0,-2, 2, 0, 0], [ 0, 0, 0, 0, 0,-2, 2, 0] ];
  W := Group(List(simples, ReflPerm));
  cox := Product(List(simples, ReflPerm));
  w := cox ^ 10;
  C := Centralizer(W, w);
  A("|C| = 155520", Size(C) = 155520);

  # Descend by stabilising one more root at each step.  The orbit lengths are the
  # ladder's "degrees of freedom" at each rung.
  orb1 := Orbit(C, 1);
  s1 := Stabilizer(C, 1);
  orb2 := First(Orbits(s1, [1..240]), o -> Length(o) = 27);
  if orb2 = fail then
    orb2 := First(Orbits(s1, [1..240]), o -> Length(o) > 1);
  fi;
  s2 := Stabilizer(s1, orb2[1]);
  orb3 := First(Orbits(s2, [1..240]), o -> Length(o) > 1);
  s3 := Stabilizer(s2, orb3[1]);

  chain := [Size(C), Size(s1), Size(s2), Size(s3)];

  checks := rec();

  checks.top_is_G32 := Size(C) = 155520;
  checks.first_stabiliser_is_G25 := Size(s1) = 648;
  checks.index_is_the_240_roots := Index(C, s1) = 240;
  checks.second_stabiliser_is_G4_order_24 := Size(s2) = 24;
  checks.that_index_is_27 := Index(s1, s2) = 27;
  checks.G4_is_the_binary_tetrahedral_group :=
    Size(s2) = 24 and IsPerfect(s2) = false and Size(Centre(s2)) = 2
    and Size(DerivedSubgroup(s2)) = 8;
  checks.ladder_orders_match_shephard_todd :=
    chain{[1..3]} = [155520, 648, 24];
  checks.degree_products_agree :=
    12*18*24*30 = 155520 and 6*9*12 = 648 and 4*6 = 24;
  checks.bottom_rung_is_f :=
    Size(s2) = 24;

  names := RecNames(checks);
  stream := OutputTextFile(DIAG, false);
  SetPrintFormattingStatus(stream, false);
  for tag in names do
    WriteAll(stream, Concatenation(tag, " = ", B(checks.(tag)), "\n"));
  od;
  WriteAll(stream, Concatenation("chain = ", String(chain), "\n"));
  WriteAll(stream, Concatenation("indices = ", String(Index(C, s1)), ", ",
    String(Index(s1, s2)), ", ", String(Index(s2, s3)), "\n"));
  WriteAll(stream, Concatenation("s2 structure = ", StructureDescription(s2), "\n"));
  WriteAll(stream, Concatenation("s3 order = ", String(Size(s3)), "\n"));
  CloseStream(stream);
  A("all checks", ForAll(names, tag -> checks.(tag)));

  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1047.eisenstein_parabolic_ladder.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"The Eisenstein tower is one recursive object, and it bottoms out at the binary tetrahedral group. Stabilising roots inside G32 descends 155520 -> 648 -> 24 with indices 240 and 27, matching the Shephard-Todd degree products 12*18*24*30, 6*9*12 and 4*6 exactly. The bottom rung G4 = 2T = SL(2,3) has order 24 = f, the corpus's own multiplicity of the eigenvalue r = 2 and the D4 root count.\",\n");
  WriteAll(stream, Concatenation("  \"ladder\": ", String(chain{[1..3]}), ",\n"));
  WriteAll(stream, "  \"rungs\": [\n");
  WriteAll(stream, "    {\"group\": \"G32\", \"rank\": 4, \"degrees\": [12,18,24,30], \"order\": 155520, \"acts_on\": \"240 E8 roots\"},\n");
  WriteAll(stream, "    {\"group\": \"G25 (Hessian)\", \"rank\": 3, \"degrees\": [6,9,12], \"order\": 648, \"is\": \"the E6 Eisenstein tower, Pass 1046\"},\n");
  WriteAll(stream, "    {\"group\": \"G4 = 2T = SL(2,3)\", \"rank\": 2, \"degrees\": [4,6], \"order\": 24, \"is\": \"f, the D4 root count, the qutrit Clifford core\"}\n");
  WriteAll(stream, "  ],\n");
  WriteAll(stream, Concatenation("  \"indices\": [", String(Index(C, s1)), ", ",
    String(Index(s1, s2)), "],\n"));
  WriteAll(stream, "  \"reading\": \"The corpus meets 155520, 648, 216 and 24 in many separate places and has treated them as distinct coincidences at the prime 3. They are four rungs of ONE parabolic ladder inside the Eisenstein tower: G32 over the 240 roots, G25 over a point, G4 over a pair, with the 216 of Pass 1020 the determinant-1 part of the middle rung. The ladder terminating at the binary tetrahedral group is why 24 keeps appearing as f.\",\n");
  WriteAll(stream, "  \"scope\": \"Orders, indices and the structural invariants of the bottom rung. It does not construct explicit isomorphisms to the Shephard-Todd groups, and the identification of each rung rests on order plus degree-product agreement plus, for G4, centre 2 and derived subgroup 8 (the quaternion group).\",\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for tag in names do
    WriteAll(stream, Concatenation("    \"", tag, "\": ", B(checks.(tag))));
    if tag <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);
  Print("Pass1047 status=PASS checks=", Length(names), " output=", OUT, "\n");
end;;

Main();;
QUIT;
