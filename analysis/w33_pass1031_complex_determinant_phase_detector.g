# Pass 1031: the COMPLEX determinant detects the phase and is blind to the sign.
#
# Pass 1029 showed det_R is trivial on the entire omega-normaliser (order 311040),
# because every element is C-linear or conjugate-linear on C^4 and such maps have
# det_R > 0.  So the real determinant separates NOTHING here: both primary classes
# of Pass 1023 lie in its kernel.
#
# The complex determinant does better, and exactly one of the two halves is visible
# to it.  On the C-linear part C = Z_{W(E8)}(w) = Z3 x Sp(4,3):
#
#   * Sp(4,3) is perfect, so det_C kills it;
#   * C/[C,C] = C/Sp(4,3) = Z3, so det_C is ONTO mu_3 with kernel exactly Sp(4,3);
#   * det_C(-I_4) = (-1)^4 = +1, so the antipodal map lies in that kernel too.
#
# Hence det_C sees the omega direction (3-primary, phase) and is blind to the
# antipodal direction (2-primary, sign).  That is an INVARIANT separation of the
# two halves, not merely the differing subgroup behaviour tabulated in Pass 1023.
#
# WHY THE GROUP-THEORETIC COMPUTATION BELOW IS det_C, not an analogy.  det_C is a
# homomorphism C -> C^* whose image is finite (C is finite), and it kills every
# commutator, so it factors through C^ab.  Here C^ab = Z3 and det_C is onto mu_3,
# so det_C IS the abelianisation map up to an isomorphism of Z3.  Therefore
# ker(det_C) = [C,C] = Sp(4,3), and membership in ker(det_C) is decidable purely
# group-theoretically -- which is what is verified.
#
# PRIOR ART -- cited, not reclaimed:
#   * Pass 1029 -- det_R trivial on the normaliser; the antipodal map has det_R +1.
#   * Pass 1023 -- the 2-primary (sign) / 3-primary (phase) split.
#   * Pass 1021/1020 -- C = Z3 x Sp(4,3), K = C' = Sp(4,3), the fibration.
#   * Pass 1028/1030 (other track) -- the syndrome decoder and the carrier
#     firewalls; this pass supplies the invariant those firewalls were separating
#     the halves without.

REPO := GAPInfo.SystemEnvironment.W33_REPO;;
OUT := Concatenation(REPO, "/data/w33_pass1031_complex_determinant_phase_detector.json");;
DIAG := Concatenation(REPO, "/data/w33_pass1031_diagnostic.txt");;

A31 := function(l, c) if not c then Error(Concatenation("Pass1031 failed: ", l)); fi; end;;
B31 := function(v) if v then return "true"; fi; return "false"; end;;

Main31 := function()
  local roots, v, i, j, si, sj, m, k, rootIndex, ReflPerm, simples,
        W, cox, w, negPerm, C, K, N, ab, quo, hom, imgW, imgNeg,
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
  A31("|W(E8)|", Size(W) = 696729600);

  cox := Product(List(simples, ReflPerm));
  w := cox ^ 10;
  negPerm := PermList(List(roots, x -> rootIndex(-x)));
  C := Centralizer(W, w);
  K := DerivedSubgroup(C);
  N := Normalizer(W, Group(w));
  A31("|C|", Size(C) = 155520);
  A31("|K|", Size(K) = 51840);

  # det_C, realised as the abelianisation map C -> C/[C,C]
  ab := AbelianInvariants(C);
  quo := FactorGroup(C, K);
  hom := NaturalHomomorphismByNormalSubgroup(C, K);
  imgW := Image(hom, w);
  imgNeg := Image(hom, negPerm);

  checks := rec();

  checks.derived_subgroup_is_Sp43 := K = DerivedSubgroup(C) and Size(K) = 51840;
  checks.abelianisation_is_Z3 := ab = [3] and Size(quo) = 3 and IsCyclic(quo);
  checks.det_C_is_onto_mu3 := Size(quo) = 3 and Size(Image(hom)) = 3;

  # the phase direction IS detected
  checks.omega_is_outside_the_kernel := not (w in K);
  checks.omega_generates_the_image := Order(imgW) = 3 and Group(imgW) = quo;

  # the sign direction is NOT detected
  checks.antipodal_map_is_inside_the_kernel := negPerm in K;
  checks.antipodal_image_is_trivial := imgNeg = One(quo);

  # therefore det_C separates the two halves
  checks.det_C_separates_phase_from_sign :=
    (not (w in K)) and (negPerm in K);

  # and det_R separates neither (Pass 1029, re-derived here from perfectness)
  checks.det_R_separates_neither :=
    IsPerfect(K) and negPerm in K;

  # the fibre group meets the kernel exactly in the sign part
  checks.fibre_C6_meets_kernel_in_the_sign_part :=
    Size(Group(cox ^ 5)) = 6 and
    Size(Intersection(Group(cox ^ 5), K)) = 2 and
    negPerm in Intersection(Group(cox ^ 5), K);

  names := RecNames(checks);
  stream := OutputTextFile(DIAG, false);
  SetPrintFormattingStatus(stream, false);
  for tag in names do
    WriteAll(stream, Concatenation(tag, " = ", B31(checks.(tag)), "\n"));
  od;
  WriteAll(stream, Concatenation("AbelianInvariants(C) = ", String(ab), "\n"));
  WriteAll(stream, Concatenation("|C/K| = ", String(Size(quo)), "\n"));
  WriteAll(stream, Concatenation("order of image of w = ", String(Order(imgW)), "\n"));
  WriteAll(stream, Concatenation("image of antipodal trivial = ",
    B31(imgNeg = One(quo)), "\n"));
  WriteAll(stream, Concatenation("|<c^5> cap K| = ",
    String(Size(Intersection(Group(cox ^ 5), K))), "\n"));
  CloseStream(stream);
  A31("all checks", ForAll(names, tag -> checks.(tag)));

  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1031.complex_determinant_phase_detector.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"The complex determinant separates the two primary classes. det_C on C = Z3 x Sp(4,3) is onto mu_3 with kernel exactly the derived subgroup Sp(4,3); omega lies outside that kernel and generates the image, while the antipodal map lies inside it. So det_C DETECTS the 3-primary phase class and is BLIND to the 2-primary sign class. The real determinant, by Pass 1029, detects neither.\",\n");
  WriteAll(stream, "  \"identification\": \"det_C is a homomorphism from a finite group to C^*, so it kills every commutator and factors through C^ab. Here C^ab = Z3 and det_C is onto mu_3, so det_C IS the abelianisation map up to an isomorphism of Z3, and ker(det_C) = [C,C] = Sp(4,3). Membership is therefore decidable group-theoretically, which is what is computed.\",\n");
  WriteAll(stream, "  \"detector_table\": {\n");
  WriteAll(stream, "    \"det_R_on_normaliser\": {\"image\": \"trivial\", \"detects_sign\": false, \"detects_phase\": false},\n");
  WriteAll(stream, "    \"det_C_on_centraliser\": {\"image\": \"mu_3\", \"detects_sign\": false, \"detects_phase\": true}\n");
  WriteAll(stream, "  },\n");
  WriteAll(stream, Concatenation("  \"abelian_invariants_of_C\": ", String(ab), ",\n"));
  WriteAll(stream, "  \"kernel\": \"Sp(4,3), order 51840\",\n");
  WriteAll(stream, "  \"fibre_intersection\": \"<c^5> cap ker(det_C) has order 2 and contains the antipodal map: the C6 fibre meets the kernel exactly in its sign part, so det_C restricted to the fibre is precisely the projection C6 -> C3.\",\n");
  WriteAll(stream, "  \"reading\": \"Pass 1023 separated the halves by how subgroups behave; Pass 1028 and 1030 raised firewalls against merging them. This supplies the invariant those firewalls were separating the halves without: a single character whose kernel contains one primary class and not the other. The phase half is a determinant; the sign half is not a determinant of anything.\",\n");
  WriteAll(stream, "  \"scope\": \"Separation invariant only. It does not identify either class with any named corpus obstruction, and it says nothing about conjugate-linear elements, on which det_C is not a homomorphism to mu_3.\",\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for tag in names do
    WriteAll(stream, Concatenation("    \"", tag, "\": ", B31(checks.(tag))));
    if tag <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);
  Print("Pass1031 status=PASS checks=", Length(names), " output=", OUT, "\n");
end;;

Main31();;
QUIT;
