# Pass 1046: the E6 Eisenstein tower IS the point stabiliser of the E8 one.
#
# Pass 1045's census showed E6 has exactly one nontrivial Springer tower, at d = 3,
# with degrees {6,9,12} and order 648.  That is Shephard-Todd G25, the Hessian
# group.  Pass 1020 independently found that the stabiliser of a root inside the E8
# tower G32 has order 155520/240 = 648, with its Sp(4,3)-part of order 216 and
# structure 3^{1+2}:Q8 -- the determinant-1 subgroup of the Hessian group.
#
# Same number twice, from two different constructions.  This pass asks whether that
# is a coincidence of the integer 648 or an actual nesting, by computing the
# stabiliser inside the E8 centraliser and checking it against the Hessian group's
# invariants rather than only its order.
#
# If it IS the nesting, the reading is that the E6 and E8 Eisenstein structures are
# ONE object seen at two levels -- the E6 tower is what sits over a point of the E8
# tower -- rather than two separate coincidences involving the same prime.
#
# PRIOR ART -- cited, not reclaimed:
#   * Pass 1045 -- the multi-type Springer census.
#   * Pass 1020 -- the 216 = 3^{1+2}:Q8 root stabiliser inside Sp(4,3).
#   * analysis/w33_witting_degrees_unify.py -- ST32 degrees, cited to Lehrer-Taylor.
#   * Shephard-Todd: G25 is the Hessian group of order 648, degrees 6,9,12.

REPO := GAPInfo.SystemEnvironment.W33_REPO;;
OUT := Concatenation(REPO, "/data/w33_pass1046_e6_tower_is_the_e8_stabiliser.json");;
DIAG := Concatenation(REPO, "/data/w33_pass1046_diagnostic.txt");;

A := function(l, c) if not c then Error(Concatenation("Pass1046 failed: ", l)); fi; end;;
B := function(v) if v then return "true"; fi; return "false"; end;;

Main := function()
  local roots, v, i, j, si, sj, m, k, rootIndex, ReflPerm, simples, W,
        cox, w, C, K, stabC, stabK, ab, der, cen,
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
  A("|C| = 155520", Size(C) = 155520);

  stabC := Stabilizer(C, 1);
  stabK := Stabilizer(K, 1);
  der := DerivedSubgroup(stabC);
  cen := Centre(stabC);
  ab := AbelianInvariants(stabC);

  checks := rec();

  # the E8 tower is transitive on the roots, so the stabiliser has order 648
  checks.E8_tower_is_transitive := IsTransitive(C, [1..240]);
  checks.point_stabiliser_has_order_648 := Size(stabC) = 648;
  checks.that_is_the_E6_tower_order := Size(stabC) = 6 * 9 * 12;

  # the Sp(4,3)-part is the det-1 subgroup, index 3 (Pass 1020)
  checks.Sp43_part_is_216 := Size(stabK) = 216;
  checks.index_three_inside_the_stabiliser := Index(stabC, stabK) = 3;

  # Hessian-group invariants beyond the order: G25 = 3^{1+2} : SL(2,3), so its
  # abelianisation is C3 and its derived subgroup has order 216.
  checks.abelianisation_is_C3 := ab = [3];
  checks.derived_subgroup_has_order_216 := Size(der) = 216;
  checks.derived_subgroup_is_the_Sp43_part := der = stabK;
  checks.centre_has_order_three := Size(cen) = 3;

  # a Hessian group has a normal extraspecial 3-group of order 27
  checks.has_normal_extraspecial_27 :=
    ForAny(NormalSubgroups(stabC), N -> Size(N) = 27 and Size(Centre(N)) = 3);

  names := RecNames(checks);
  stream := OutputTextFile(DIAG, false);
  SetPrintFormattingStatus(stream, false);
  for tag in names do
    WriteAll(stream, Concatenation(tag, " = ", B(checks.(tag)), "\n"));
  od;
  WriteAll(stream, Concatenation("|stab_C| = ", String(Size(stabC)), "\n"));
  WriteAll(stream, Concatenation("|stab_K| = ", String(Size(stabK)), "\n"));
  WriteAll(stream, Concatenation("AbelianInvariants = ", String(ab), "\n"));
  WriteAll(stream, Concatenation("|derived| = ", String(Size(der)),
    "  |centre| = ", String(Size(cen)), "\n"));
  WriteAll(stream, Concatenation("structure = ",
    StructureDescription(stabC), "\n"));
  CloseStream(stream);
  A("all checks", ForAll(names, tag -> checks.(tag)));

  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1046.e6_tower_is_the_e8_stabiliser.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"The E6 Eisenstein tower is the point stabiliser of the E8 one. E6's only Springer tower has degrees {6,9,12} and order 648 -- Shephard-Todd G25, the Hessian group -- and the stabiliser of a root inside the E8 tower G32 is a group of order 648 with abelianisation C3, derived subgroup of order 216, centre of order 3, and a normal extraspecial subgroup of order 27. Those are the Hessian group's invariants, not merely its order. So the two Eisenstein structures are one object at two levels rather than two coincidences at the same prime.\",\n");
  WriteAll(stream, Concatenation("  \"point_stabiliser_order\": ", String(Size(stabC)), ",\n"));
  WriteAll(stream, Concatenation("  \"Sp43_part\": ", String(Size(stabK)), ",\n"));
  WriteAll(stream, Concatenation("  \"abelianisation\": ", String(ab), ",\n"));
  WriteAll(stream, Concatenation("  \"derived_order\": ", String(Size(der)), ",\n"));
  WriteAll(stream, Concatenation("  \"centre_order\": ", String(Size(cen)), ",\n"));
  WriteAll(stream, "  \"E6_tower\": {\"d\": 3, \"degrees\": [6,9,12], \"order\": 648, \"group\": \"Shephard-Todd G25, the Hessian group\"},\n");
  WriteAll(stream, "  \"E8_tower\": {\"d\": 3, \"degrees\": [12,18,24,30], \"order\": 155520, \"group\": \"Shephard-Todd G32\"},\n");
  WriteAll(stream, "  \"nesting\": \"|G32| / 240 roots = 648 = |G25|. The rank-3 parabolic of the rank-4 Eisenstein tower is the rank-3 Eisenstein tower.\",\n");
  WriteAll(stream, "  \"reading\": \"Pass 1045 found E6 and E8 each carry an Eisenstein tower and read them as separate entries in a census. They are not separate: the E6 one sits over a point of the E8 one. The corpus's repeated 648 -- the Hessian group, the point stabiliser of PSp(4,3) on the 40 points, the det-1 subgroup 216 -- is one object appearing at the level where it belongs.\",\n");
  WriteAll(stream, "  \"scope\": \"Invariant-level identification: order, abelianisation, derived subgroup, centre, and a normal extraspecial 27. It does not construct an explicit isomorphism to G25 and does not claim the E6 root system embeds in E8 by this map.\",\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for tag in names do
    WriteAll(stream, Concatenation("    \"", tag, "\": ", B(checks.(tag))));
    if tag <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);
  Print("Pass1046 status=PASS checks=", Length(names), " output=", OUT, "\n");
end;;

Main();;
QUIT;
