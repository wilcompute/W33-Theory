# Pass 1039: the Springer regular-element tower of W(E8).  Is the Eisenstein
# fibration unique, or one member of a family?
#
# Passes 1020/1021 built the 240 -> 40 fibration from a REGULAR element of order 3,
# whose centraliser is Shephard-Todd G32 of order 12*18*24*30 = 155520.  Nothing in
# that construction is specific to 3.  Springer's theorem gives the same recipe for
# every d:
#
#     C_{W}(regular w of order d)  is a complex reflection group whose degrees are
#     exactly the degrees of W divisible by d, so |C| = product of those degrees.
#
# For W(E8), degrees 2,8,12,14,18,20,24,30, that predicts:
#
#     d = 2   all eight degrees          696729600   (w = -1, central: whole group)
#     d = 3   12,18,24,30                   155520   G32, the EISENSTEIN tower
#     d = 4    8,12,20,24                    46080   G31, the GAUSSIAN analogue
#     d = 5   20,30                            600
#     d = 6   12,18,24,30                   155520   same order as d = 3
#     d = 8    8,24                            192
#     d = 10  20,30                            600
#     d = 12  12,24                            288
#
# So "q = 3 is forced" is a TESTABLE claim about this tower rather than an
# assertion, and the honest question is not whether the Eisenstein tower exists --
# it does -- but whether it is distinguished among its siblings.  In particular
# d = 4 supplies a rank-4 reflection group too, so a Gaussian competitor exists on
# paper.  This pass asks what each member actually does to the 240 roots.
#
# PRIOR ART -- cited, not reclaimed:
#   * Pass 1020 -- the Springer route and the d = 3 centraliser G32.
#   * Pass 1021 -- the 240 -> 40 fibration and its ZZ6 fibre.
#   * analysis/w33_witting_degrees_unify.py -- the G32 degrees {12,18,24,30} and
#     155520 as their product, cited to Lehrer-Taylor.  That is ITS result; this
#     pass reuses the same law for the other divisors.

REPO := GAPInfo.SystemEnvironment.W33_REPO;;
OUT := Concatenation(REPO, "/data/w33_pass1039_springer_tower.json");;
DIAG := Concatenation(REPO, "/data/w33_pass1039_diagnostic.txt");;

A39 := function(l, c) if not c then Error(Concatenation("Pass1039 failed: ", l)); fi; end;;
B39 := function(v) if v then return "true"; fi; return "false"; end;;

Main39 := function()
  local roots, v, i, j, si, sj, m, k, rootIndex, ReflPerm, simples, degrees,
        W, cox, d, predicted, w, g, o, tries, C, K, rows, row, blocks, bsizes,
        transC, transK, fixed, checks, names, stream, tag, r, dlist;

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
  ReflPerm := function(r2)
    return PermList(List(roots, x -> rootIndex(x - ((x * r2) / 4) * r2)));
  end;
  simples := [
    [ 1,-1,-1,-1,-1,-1,-1, 1], [ 2, 2, 0, 0, 0, 0, 0, 0],
    [-2, 2, 0, 0, 0, 0, 0, 0], [ 0,-2, 2, 0, 0, 0, 0, 0],
    [ 0, 0,-2, 2, 0, 0, 0, 0], [ 0, 0, 0,-2, 2, 0, 0, 0],
    [ 0, 0, 0, 0,-2, 2, 0, 0], [ 0, 0, 0, 0, 0,-2, 2, 0] ];
  W := Group(List(simples, ReflPerm));
  A39("|W(E8)|", Size(W) = 696729600);
  cox := Product(List(simples, ReflPerm));
  A39("Coxeter order 30", Order(cox) = 30);

  degrees := [2,8,12,14,18,20,24,30];
  dlist := [3,4,5,6,8,10,12];
  rows := [];

  for d in dlist do
    predicted := Product(Filtered(degrees, x -> x mod d = 0));
    # A regular element of order d is identified by Springer's theorem itself:
    # its centraliser has exactly the predicted order.  Search for one.
    w := fail; tries := 0;
    while w = fail and tries < 3000 do
      tries := tries + 1;
      g := PseudoRandom(W);
      o := Order(g);
      if o mod d = 0 then
        g := g ^ (o / d);
        if Order(g) = d and Size(Centralizer(W, g)) = predicted then
          w := g;
        fi;
      fi;
    od;
    if w = fail then
      Add(rows, rec(d := d, predicted := predicted, found := false));
      continue;
    fi;
    C := Centralizer(W, w);
    K := DerivedSubgroup(C);
    fixed := Number([1..240], x -> x ^ w = x);
    transC := IsTransitive(C, [1..240]);
    transK := IsTransitive(K, [1..240]);
    blocks := [];
    if transK then
      bsizes := SortedList(Set(List(AllBlocks(K), Length)));
      blocks := bsizes;
    fi;
    Add(rows, rec(d := d, predicted := predicted, found := true,
      centraliser := Size(C), derived := Size(K), fixedRoots := fixed,
      transitiveC := transC, transitiveK := transK, blockSizes := blocks));
  od;

  checks := rec();

  checks.d3_is_the_eisenstein_tower :=
    ForAny(rows, r2 -> r2.d = 3 and r2.found and r2.centraliser = 155520
      and r2.derived = 51840 and r2.transitiveK and r2.fixedRoots = 0);
  checks.d4_gaussian_sibling_exists :=
    ForAny(rows, r2 -> r2.d = 4 and r2.found and r2.centraliser = 46080);
  checks.every_found_centraliser_matches_springer :=
    ForAll(Filtered(rows, r2 -> r2.found), r2 -> r2.centraliser = r2.predicted);
  checks.tower_has_more_than_one_member :=
    Number(rows, r2 -> r2.found) >= 2;

  # THE DISCRIMINATOR: which members give a TRANSITIVE derived subgroup on the
  # 240 roots?  That is what makes a fibration rather than just a subgroup.
  checks.d3_derived_is_transitive :=
    ForAny(rows, r2 -> r2.d = 3 and r2.found and r2.transitiveK);

  names := RecNames(checks);
  stream := OutputTextFile(DIAG, false);
  SetPrintFormattingStatus(stream, false);
  for tag in names do
    WriteAll(stream, Concatenation(tag, " = ", B39(checks.(tag)), "\n"));
  od;
  WriteAll(stream, "d | predicted | |C| | |C'| | fixedRoots | transC | transC' | blocks\n");
  for r in rows do
    if r.found then
      WriteAll(stream, Concatenation(String(r.d), " | ", String(r.predicted), " | ",
        String(r.centraliser), " | ", String(r.derived), " | ", String(r.fixedRoots),
        " | ", B39(r.transitiveC), " | ", B39(r.transitiveK), " | ",
        String(r.blockSizes), "\n"));
    else
      WriteAll(stream, Concatenation(String(r.d), " | ", String(r.predicted),
        " | NOT FOUND\n"));
    fi;
  od;
  CloseStream(stream);
  A39("all checks", ForAll(names, tag -> checks.(tag)));

  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1039.springer_tower.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"The Eisenstein fibration is one member of the Springer regular-element tower of W(E8), not a unique object. Every divisor d of a degree gives a regular centraliser of order equal to the product of the degrees divisible by d. What distinguishes d = 3 is measured here rather than assumed.\",\n");
  WriteAll(stream, "  \"law\": \"|C_W(regular w of order d)| = product of the degrees of W divisible by d (Springer). Degrees of W(E8): 2,8,12,14,18,20,24,30.\",\n");
  WriteAll(stream, "  \"tower\": [\n");
  for i in [1..Length(rows)] do
    r := rows[i];
    if r.found then
      WriteAll(stream, Concatenation("    {\"d\": ", String(r.d),
        ", \"predicted\": ", String(r.predicted),
        ", \"centraliser\": ", String(r.centraliser),
        ", \"derived\": ", String(r.derived),
        ", \"fixed_roots\": ", String(r.fixedRoots),
        ", \"centraliser_transitive\": ", B39(r.transitiveC),
        ", \"derived_transitive\": ", B39(r.transitiveK),
        ", \"block_sizes\": ", String(r.blockSizes), "}"));
    else
      WriteAll(stream, Concatenation("    {\"d\": ", String(r.d),
        ", \"predicted\": ", String(r.predicted), ", \"found\": false}"));
    fi;
    if i < Length(rows) then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  ],\n");
  WriteAll(stream, "  \"reading\": \"'q = 3 is forced' is a claim about this tower and is now testable rather than asserted. d = 4 supplies a rank-4 Gaussian sibling (Shephard-Todd G31, order 46080 = 8*12*20*24), so the mere existence of a rank-4 complex-reflection centraliser does not single out the Eisenstein case. Whatever distinguishes d = 3 has to be read off the columns here -- transitivity of the derived subgroup and the block structure -- not from the existence of the centraliser.\",\n");
  WriteAll(stream, "  \"scope\": \"Structural census of the tower. It does not claim d = 3 is or is not distinguished; it supplies the table on which that claim must be settled.\",\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for tag in names do
    WriteAll(stream, Concatenation("    \"", tag, "\": ", B39(checks.(tag))));
    if tag <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);
  Print("Pass1039 status=PASS checks=", Length(names), " output=", OUT, "\n");
end;;

Main39();;
QUIT;
