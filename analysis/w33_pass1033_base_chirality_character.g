# Pass 1033: the chirality character exists -- on the BASE, and only there.
#
# The arc so far.  Pass 1029: det_R is trivial on the entire omega-normaliser N
# (order 311040), because every element is C-linear or conjugate-linear on C^4 and
# such maps preserve orientation of R^8.  So the 8-dimensional E8 representation
# admits NO binary character at all on the tower.  Pass 1031: det_C on the
# C-linear part is onto mu_3 with kernel exactly Sp(4,3), detecting the 3-primary
# phase and blind to the 2-primary sign.
#
# That left the sign half with no detector anywhere, and one obvious place still
# unchecked.  Sp(4,3) is PERFECT, so it has no nontrivial character to any abelian
# group -- the total-space group cannot host a binary invariant even in principle.
# The BASE group is not perfect:
#
#     W(E6) = PGSp(4,3) = U4(2):2,   [W(E6),W(E6)] = U4(2),   W(E6)^ab = C2.
#
# So the base carries exactly one binary character, with kernel the simple group
# U4(2).  This pass asks whether that character is the chirality one, and whether
# it is genuinely different from det_R rather than a relabelling of it.
#
# The answer is that it is different, and the difference is representation-theoretic
# rather than subtle: W(E6) is a reflection group in its OWN 6-dimensional
# representation, where reflections have determinant -1 and the sign character is
# the determinant.  Pulled back to the ambient 8-dimensional E8 representation the
# same elements have det_R = +1, by Pass 1029.  One group, two representations, two
# different determinants -- and the corpus's chirality datum lives in the smaller
# one, which is invisible from inside the tower.
#
# PRIOR ART -- cited, not reclaimed:
#   * analysis/A_REFLECTION_GROUP_CANNOT_ORIENT_ITSELF.md -- the chirality
#     obstruction and the det(w) = -1 definition.  Entirely its result.
#   * Pass 1029 -- det_R trivial on N; Sp(4,3) perfect hence in ker(det).
#   * Pass 1031 -- det_C detects the phase; the detector table this extends.
#   * Pass 1021 -- the two-level fibration, and the normaliser image = W(E6).

REPO := GAPInfo.SystemEnvironment.W33_REPO;;
OUT := Concatenation(REPO, "/data/w33_pass1033_base_chirality_character.json");;
DIAG := Concatenation(REPO, "/data/w33_pass1033_diagnostic.txt");;

A33 := function(l, c) if not c then Error(Concatenation("Pass1033 failed: ", l)); fi; end;;
B33 := function(v) if v then return "true"; fi; return "false"; end;;

Main33 := function()
  local roots, v, i, j, si, sj, m, k, rootIndex, ReflPerm, simples, S, Sinv, Det,
        W, cox, w, negPerm, C, K, N, sys6, b6, hom40, base, baseDer, baseAb,
        baseHom, baseQuo, witness, g, detWitness, imgWitness, tries,
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
  ReflPerm := function(r)
    return PermList(List(roots, x -> rootIndex(x - ((x * r) / 4) * r)));
  end;
  simples := [
    [ 1,-1,-1,-1,-1,-1,-1, 1], [ 2, 2, 0, 0, 0, 0, 0, 0],
    [-2, 2, 0, 0, 0, 0, 0, 0], [ 0,-2, 2, 0, 0, 0, 0, 0],
    [ 0, 0,-2, 2, 0, 0, 0, 0], [ 0, 0, 0,-2, 2, 0, 0, 0],
    [ 0, 0, 0, 0,-2, 2, 0, 0], [ 0, 0, 0, 0, 0,-2, 2, 0] ];
  W := Group(List(simples, ReflPerm));
  A33("|W(E8)|", Size(W) = 696729600);

  # det_R on the ambient 8-dimensional representation (Pass 1029's construction)
  S := simples;
  Sinv := S ^ -1;
  Det := function(g2)
    return Determinant(Sinv * List(simples, r -> roots[ rootIndex(r) ^ g2 ]));
  end;
  A33("det_R(reflection) = -1", Det(ReflPerm(simples[1])) = -1);

  cox := Product(List(simples, ReflPerm));
  w := cox ^ 10;
  negPerm := PermList(List(roots, x -> rootIndex(-x)));
  C := Centralizer(W, w);
  K := DerivedSubgroup(C);
  N := Normalizer(W, Group(w));
  A33("|K| = 51840", Size(K) = 51840);
  A33("|N| = 311040", Size(N) = 311040);

  # the base: N acting on the 40 Eisenstein lines
  b6 := First(AllBlocks(K), b -> Length(b) = 6);
  sys6 := Blocks(K, [1..240], b6);
  A33("40 blocks", Length(sys6) = 40);
  hom40 := ActionHomomorphism(N, sys6, OnSets);
  base := Image(hom40);
  A33("base is W(E6) of order 51840", Size(base) = 51840);

  baseDer := DerivedSubgroup(base);
  baseAb := AbelianInvariants(base);
  baseHom := NaturalHomomorphismByNormalSubgroup(base, baseDer);
  baseQuo := Image(baseHom);

  # A WITNESS: an element of N whose BASE character is -1 while det_R is +1.
  # Its existence is what makes the two characters different rather than the same
  # character seen twice.
  witness := fail; tries := 0;
  while witness = fail and tries < 20000 do
    tries := tries + 1;
    g := PseudoRandom(N);
    if not (Image(hom40, g) in baseDer) then
      witness := g;
    fi;
  od;
  A33("found an element outside the base derived subgroup", witness <> fail);
  detWitness := Det(witness);
  imgWitness := Image(baseHom, Image(hom40, witness));

  checks := rec();

  # (a) the total space cannot host a binary character AT ALL
  checks.total_space_group_is_perfect := IsPerfect(K);
  checks.perfect_means_no_binary_character :=
    IsPerfect(K) and AbelianInvariants(K) = [];

  # (b) the base can, and does: exactly one, with simple kernel
  checks.base_is_not_perfect := not IsPerfect(base);
  checks.base_abelianisation_is_C2 :=
    baseAb = [2] and Size(baseQuo) = 2;
  checks.base_character_kernel_is_simple_U42 :=
    Size(baseDer) = 25920 and IsSimple(baseDer);

  # (c) THE POINT: base character -1 while the ambient det_R is +1
  checks.witness_has_base_character_minus_one :=
    imgWitness <> One(baseQuo);
  checks.witness_has_ambient_det_plus_one :=
    detWitness = 1;
  checks.two_characters_are_genuinely_different :=
    imgWitness <> One(baseQuo) and detWitness = 1;

  # (d) and det_R is trivial on the whole tower, so this is not a relabelling
  checks.det_R_trivial_on_normaliser :=
    Set(List(GeneratorsOfGroup(N), Det)) = [1];

  names := RecNames(checks);
  stream := OutputTextFile(DIAG, false);
  SetPrintFormattingStatus(stream, false);
  for tag in names do
    WriteAll(stream, Concatenation(tag, " = ", B33(checks.(tag)), "\n"));
  od;
  WriteAll(stream, Concatenation("AbelianInvariants(base) = ", String(baseAb), "\n"));
  WriteAll(stream, Concatenation("AbelianInvariants(K) = ", String(AbelianInvariants(K)), "\n"));
  WriteAll(stream, Concatenation("|baseDer| = ", String(Size(baseDer)), "\n"));
  WriteAll(stream, Concatenation("det_R(witness) = ", String(detWitness), "\n"));
  WriteAll(stream, Concatenation("base char(witness) nontrivial = ",
    B33(imgWitness <> One(baseQuo)), "\n"));
  CloseStream(stream);
  A33("all checks", ForAll(names, tag -> checks.(tag)));

  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1033.base_chirality_character.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"The binary chirality character exists on the BASE and nowhere else. Sp(4,3) is perfect, so the total-space group has no nontrivial character to any abelian group and cannot host a binary invariant even in principle. W(E6) = U4(2):2 has abelianisation C2 with simple kernel U4(2). A witness element has base character -1 while its ambient det_R is +1, so the two are different characters, not one character seen twice.\",\n");
  WriteAll(stream, "  \"detector_table\": {\n");
  WriteAll(stream, "    \"det_R_on_normaliser\": {\"image\": \"trivial\", \"detects_sign\": false, \"detects_phase\": false},\n");
  WriteAll(stream, "    \"det_C_on_centraliser\": {\"image\": \"mu_3\", \"detects_sign\": false, \"detects_phase\": true},\n");
  WriteAll(stream, "    \"sign_character_on_base\": {\"image\": \"C2\", \"detects_sign\": true, \"detects_phase\": false}\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, Concatenation("  \"abelianisation_total_space\": ", String(AbelianInvariants(K)), ",\n"));
  WriteAll(stream, Concatenation("  \"abelianisation_base\": ", String(baseAb), ",\n"));
  WriteAll(stream, Concatenation("  \"base_character_kernel\": ", String(Size(baseDer)), ",\n"));
  WriteAll(stream, Concatenation("  \"witness_ambient_det\": ", String(detWitness), ",\n"));
  WriteAll(stream, "  \"reading\": \"W(E6) is a reflection group in its OWN 6-dimensional representation, where reflections have determinant -1 and the sign character IS that determinant. Pulled back to the ambient 8-dimensional E8 representation the same elements have det_R = +1. One group, two representations, two different determinants -- and the corpus's chirality datum lives in the smaller one. That is the precise sense in which chirality is real but unselectable from inside the tower: it is not absent, it is invisible in the representation the substrate actually acts by.\",\n");
  WriteAll(stream, "  \"closes\": \"Pass 1029 left the sign half with no detector anywhere. It has exactly one, on the base, and the total space provably cannot carry it because Sp(4,3) is perfect.\",\n");
  WriteAll(stream, "  \"scope\": \"Existence and distinctness of the character. It does NOT prove the base character equals the 2-primary section class of Pass 1023, and does not construct an equivariant orientation datum -- Pass 1029 shows none exists inside the tower.\",\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for tag in names do
    WriteAll(stream, Concatenation("    \"", tag, "\": ", B33(checks.(tag))));
    if tag <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);
  Print("Pass1033 status=PASS checks=", Length(names), " output=", OUT, "\n");
end;;

Main33();;
QUIT;
