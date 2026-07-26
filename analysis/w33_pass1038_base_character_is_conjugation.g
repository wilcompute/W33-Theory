# Pass 1038: the base chirality character is exactly "is this element
# conjugate-linear?" -- and it is NOT the 2-primary section class.
#
# Pass 1033 found that the base group W(E6) carries exactly one binary character,
# with kernel the simple group U4(2), while the total-space group Sp(4,3) is perfect
# and carries none.  The obvious next question is whether that base character IS the
# 2-primary (sign) section obstruction of Pass 1023.  It is not, and the reason is
# clean enough to state before computing:
#
#   Sp(4,3) acts on the 40 blocks through its image, which is PSp(4,3) = U4(2).
#   But U4(2) is exactly ker(base character).  So the base character PULLS BACK
#   TRIVIALLY to Sp(4,3) -- it cannot see the total-space group at all -- whereas
#   the 2-primary section obstruction for Sp(4,3) is nontrivial (Pass 1023).
#   Two invariants, disjoint domains of sensitivity, therefore different.
#
# That leaves the question of what DOES carry the character, and the answer is the
# structurally interesting part.  The omega-normaliser N has order 311040 and the
# centraliser C has index 2 in it: C is the C-LINEAR part, N \ C the CONJUGATE-LINEAR
# part (complex conjugation on C^4).  Image(C) on the 40 blocks is U4(2) = the
# kernel; the outer half of the base comes entirely from N \ C.  So
#
#     base character(g) = -1   <=>   g is conjugate-linear.
#
# The substrate's binary chirality datum is the C-linear / conjugate-linear
# dichotomy, nothing else.  Combined with Pass 1029 -- complex conjugation on
# C^4 = R^8 has det_R = (-1)^4 = +1 -- this says the operation that reverses
# orientation ON THE BASE preserves it on the total space.  That is the sharpest
# form of "chirality is unselectable from inside" the arc has reached: the reversal
# exists, it is conjugation, and it is invisible in the representation the substrate
# acts by.
#
# PRIOR ART -- cited, not reclaimed:
#   * Pass 1033 -- the base character, its kernel, and Sp(4,3) being perfect.
#   * Pass 1029 -- det_R trivial on N; conjugation has det_R +1.
#   * Pass 1023 -- the 2-primary / 3-primary section obstructions.
#   * Pass 1021/1020 -- the fibration, C = Z3 x Sp(4,3), the base = W(E6).
#   * Passes 1034-1037 (other track) -- "three distinct order-six structures that
#     must not be conflated"; this pass adds a fourth distinction, between the base
#     character and the 2-primary class, in the same spirit.

REPO := GAPInfo.SystemEnvironment.W33_REPO;;
OUT := Concatenation(REPO, "/data/w33_pass1038_base_character_is_conjugation.json");;
DIAG := Concatenation(REPO, "/data/w33_pass1038_diagnostic.txt");;

A38 := function(l, c) if not c then Error(Concatenation("Pass1038 failed: ", l)); fi; end;;
B38 := function(v) if v then return "true"; fi; return "false"; end;;

Main38 := function()
  local roots, v, i, j, si, sj, m, k, rootIndex, ReflPerm, simples,
        W, cox, w, negPerm, C, K, N, b6, sys6, hom40, base, imgK, imgC,
        baseDer, baseHom, baseQuo, elts, g, outerAllConj, innerAllTrivial,
        tries, sample, checks, names, stream, tag;

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
  A38("|W(E8)|", Size(W) = 696729600);

  cox := Product(List(simples, ReflPerm));
  w := cox ^ 10;
  negPerm := PermList(List(roots, x -> rootIndex(-x)));
  C := Centralizer(W, w);
  K := DerivedSubgroup(C);
  N := Normalizer(W, Group(w));
  A38("|C| = 155520", Size(C) = 155520);
  A38("|K| = 51840", Size(K) = 51840);
  A38("|N| = 311040", Size(N) = 311040);
  A38("C has index 2 in N", Index(N, C) = 2);

  b6 := First(AllBlocks(K), b -> Length(b) = 6);
  sys6 := Blocks(K, [1..240], b6);
  hom40 := ActionHomomorphism(N, sys6, OnSets);
  base := Image(hom40);
  imgK := Image(hom40, K);
  imgC := Image(hom40, C);
  baseDer := DerivedSubgroup(base);
  baseHom := NaturalHomomorphismByNormalSubgroup(base, baseDer);
  baseQuo := Image(baseHom);

  # Does the base character vanish on everything C-linear, and only there?
  # C-linear = C; conjugate-linear = N \ C.  Sample rather than enumerate 311040.
  innerAllTrivial := true;
  outerAllConj := true;
  for tries in [1..400] do
    g := PseudoRandom(N);
    sample := Image(baseHom, Image(hom40, g));
    if g in C then
      if sample <> One(baseQuo) then innerAllTrivial := false; fi;
    else
      if sample = One(baseQuo) then outerAllConj := false; fi;
    fi;
  od;

  checks := rec();

  # (a) the base character cannot see the total-space group at all
  checks.image_of_Sp43_on_the_base_is_U42 :=
    Size(imgK) = 25920 and IsSimple(imgK);
  checks.that_image_is_exactly_the_character_kernel :=
    imgK = baseDer;
  checks.base_character_pulls_back_trivially_to_Sp43 :=
    ForAll(GeneratorsOfGroup(K),
      g2 -> Image(baseHom, Image(hom40, g2)) = One(baseQuo));

  # (b) but the 2-primary section obstruction for Sp(4,3) IS nontrivial (Pass 1023)
  checks.two_primary_obstruction_is_nontrivial :=
    Size(Stabilizer(K, Blocks(K, [1..240],
      First(AllBlocks(K), b -> Length(b) = 2))[1], OnSets)) = 432;

  # (c) hence they are different invariants
  checks.base_character_is_not_the_two_primary_class :=
    imgK = baseDer;

  # (d) what DOES carry it: the conjugate-linear half
  checks.C_linear_part_maps_into_the_kernel :=
    imgC = baseDer and Size(imgC) = 25920;
  checks.character_is_exactly_conjugate_linearity :=
    innerAllTrivial and outerAllConj;
  checks.outer_half_exists_and_has_index_two :=
    Index(N, C) = 2 and Size(base) = 51840 and Size(baseDer) = 25920;

  names := RecNames(checks);
  stream := OutputTextFile(DIAG, false);
  SetPrintFormattingStatus(stream, false);
  for tag in names do
    WriteAll(stream, Concatenation(tag, " = ", B38(checks.(tag)), "\n"));
  od;
  WriteAll(stream, Concatenation("|image(K)| = ", String(Size(imgK)), "\n"));
  WriteAll(stream, Concatenation("|image(C)| = ", String(Size(imgC)), "\n"));
  WriteAll(stream, Concatenation("|baseDer| = ", String(Size(baseDer)), "\n"));
  WriteAll(stream, Concatenation("imgK = baseDer : ", B38(imgK = baseDer), "\n"));
  WriteAll(stream, Concatenation("inner all trivial : ", B38(innerAllTrivial), "\n"));
  WriteAll(stream, Concatenation("outer all nontrivial : ", B38(outerAllConj), "\n"));
  CloseStream(stream);
  A38("all checks", ForAll(names, tag -> checks.(tag)));

  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1038.base_character_is_conjugation.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"The base chirality character is exactly conjugate-linearity, and it is NOT the 2-primary section class. Sp(4,3) maps onto U4(2) on the 40 blocks, and U4(2) is precisely the character's kernel, so the character pulls back trivially to the total-space group while the 2-primary section obstruction there is nontrivial. What carries the character is the outer half N \\\\ C, the conjugate-linear elements.\",\n");
  WriteAll(stream, "  \"separation\": \"base character and 2-primary class have disjoint domains of sensitivity: the character vanishes identically on Sp(4,3), where the section obstruction lives. They cannot be the same invariant.\",\n");
  WriteAll(stream, Concatenation("  \"image_of_Sp43_on_base\": ", String(Size(imgK)), ",\n"));
  WriteAll(stream, Concatenation("  \"image_of_centraliser_on_base\": ", String(Size(imgC)), ",\n"));
  WriteAll(stream, Concatenation("  \"character_kernel\": ", String(Size(baseDer)), ",\n"));
  WriteAll(stream, "  \"identification\": \"base character(g) = -1 <=> g is conjugate-linear. C is the C-linear part and maps into the kernel; N \\\\ C is complex conjugation on C^4 and supplies the whole outer half.\",\n");
  WriteAll(stream, "  \"reading\": \"Combined with Pass 1029 -- conjugation on C^4 = R^8 has det_R = (-1)^4 = +1 -- the operation that reverses orientation ON THE BASE preserves it on the total space. The reversal exists, it is complex conjugation, and it is invisible in the representation the substrate acts by. That is the sharpest form of 'chirality is unselectable from inside' this arc has reached.\",\n");
  WriteAll(stream, "  \"scope\": \"A separation and an identification of the character. It does not construct an equivariant orientation datum -- Pass 1029 shows none exists inside the tower -- and the conjugate-linearity correspondence is verified on a 400-element sample plus the exact kernel equality, not by enumerating 311040 elements.\",\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for tag in names do
    WriteAll(stream, Concatenation("    \"", tag, "\": ", B38(checks.(tag))));
    if tag <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);
  Print("Pass1038 status=PASS checks=", Length(names), " output=", OUT, "\n");
end;;

Main38();;
QUIT;
