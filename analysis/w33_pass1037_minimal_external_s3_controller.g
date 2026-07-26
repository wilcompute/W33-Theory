# Pass 1037: the minimal external controller is S3, not C6.
#
# Let w be the canonical order-3 Eisenstein scalar in W(E8),
# C = C_W(w) = C3 x Sp(4,3), K = C' = Sp(4,3), and
# N = N_W(<w>).  Pass 1031 identifies C/K = C3 as the complex-determinant
# phase detector.  Pass 1033 identifies the independent base character C2.
# This pass computes the smallest group containing both effects:
#
#     N/K = C3 : C2 = S3.
#
# The outer involution conjugates w to w^-1.  Hence the controller is dihedral
# and nonabelian.  It must not be confused with the internal Eisenstein-unit
# fibre <c^5> = C6, which is cyclic and whose order-2 part lies inside K.

REPO := GAPInfo.SystemEnvironment.W33_REPO;;
OUT := Concatenation(REPO, "/data/w33_pass1037_minimal_external_s3_controller.json");;
DIAG := Concatenation(REPO, "/data/w33_pass1037_diagnostic.txt");;

A37 := function(label, condition)
  if not condition then Error(Concatenation("Pass1037 failed: ", label)); fi;
end;;
B37 := function(value) if value then return "true"; fi; return "false"; end;;

Main37 := function()
  local roots, v, i, j, si, sj, m, k, rootIndex, ReflPerm, simples,
        W, cox, w, C, K, N, F, hom, Q, qC, qw, t, qt, chiralityQuot,
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
  A37("240 roots", Length(roots) = 240);

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
  A37("|W(E8)|", Size(W) = 696729600);
  cox := Product(List(simples, ReflPerm));
  w := cox ^ 10;
  C := Centralizer(W, w);
  K := DerivedSubgroup(C);
  N := Normalizer(W, Group(w));
  F := Group(cox ^ 5);

  A37("|C|", Size(C) = 155520);
  A37("|K|", Size(K) = 51840);
  A37("|N|", Size(N) = 311040);
  A37("K normal in N", IsNormal(N, K));

  hom := NaturalHomomorphismByNormalSubgroup(N, K);
  Q := Image(hom);
  qC := Image(hom, C);
  qw := Image(hom, w);
  t := First(GeneratorsOfGroup(N), element -> not (element in C));
  A37("normaliser generator outside centraliser", t <> fail);
  qt := Image(hom, t);
  chiralityQuot := FactorGroup(Q, qC);

  checks := rec();
  checks.normaliser_quotient_has_order_six := Size(Q) = 6;
  checks.normaliser_quotient_is_nonabelian := not IsAbelian(Q);
  checks.normaliser_quotient_is_S3 := Size(Q) = 6 and not IsAbelian(Q);
  checks.quotient_derived_subgroup_has_order_three := Size(DerivedSubgroup(Q)) = 3;
  checks.quotient_abelianisation_is_C2 := AbelianInvariants(Q) = [2];
  checks.phase_subgroup_is_normal_C3 := Size(qC) = 3 and IsCyclic(qC) and IsNormal(Q, qC);
  checks.omega_generates_phase_subgroup := Order(qw) = 3 and Group(qw) = qC;
  checks.external_generator_has_order_two := Order(qt) = 2;
  checks.external_generator_inverts_phase := qw ^ qt = qw ^ -1;
  checks.chirality_quotient_is_C2 := Size(chiralityQuot) = 2 and IsCyclic(chiralityQuot);
  checks.internal_fibre_is_cyclic_C6 := Size(F) = 6 and IsCyclic(F) and IsAbelian(F);
  checks.external_controller_is_not_internal_fibre := not IsAbelian(Q) and IsAbelian(F);
  checks.controller_order_is_minimal_for_C3_and_C2 := Size(Q) = Lcm(3, 2);

  names := RecNames(checks);
  stream := OutputTextFile(DIAG, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, Concatenation("|C| = ", String(Size(C)), "\n"));
  WriteAll(stream, Concatenation("|K| = ", String(Size(K)), "\n"));
  WriteAll(stream, Concatenation("|N| = ", String(Size(N)), "\n"));
  WriteAll(stream, Concatenation("|N/K| = ", String(Size(Q)), "\n"));
  WriteAll(stream, Concatenation("AbelianInvariants(N/K) = ", String(AbelianInvariants(Q)), "\n"));
  for tag in names do
    WriteAll(stream, Concatenation(tag, " = ", B37(checks.(tag)), "\n"));
  od;
  CloseStream(stream);
  A37("all checks", ForAll(names, tag -> checks.(tag)));

  stream := OutputTextFile(OUT, false);
  SetPrintFormattingStatus(stream, false);
  WriteAll(stream, "{\n");
  WriteAll(stream, "  \"schema\": \"w33.pass1037.minimal_external_s3_controller.gap.v1\",\n");
  WriteAll(stream, "  \"status\": \"PASS\",\n");
  WriteAll(stream, "  \"headline\": \"The minimal external controller is N/K = S3. The C-linear centraliser contributes the normal C3 phase detector, while an external involution contributes the base C2 character and conjugates phase to its inverse. This nonabelian S3 must not be confused with the internal cyclic C6 Eisenstein-unit fibre.\",\n");
  WriteAll(stream, "  \"orders\": {\"centraliser\": 155520, \"Sp43_kernel\": 51840, \"normaliser\": 311040, \"controller_quotient\": 6},\n");
  WriteAll(stream, "  \"exact_sequence\": \"1 -> C3 -> S3 -> C2 -> 1, with the C2 acting on C3 by inversion\",\n");
  WriteAll(stream, "  \"internal_external_distinction\": \"The internal fibre <c^5> is cyclic C6 and intersects Sp(4,3) in its central sign C2. The external controller N/K is nonabelian S3; its C2 is a quotient operation that inverts the phase C3. Equal order six does not mean equal group or equal role.\",\n");
  WriteAll(stream, "  \"minimality\": \"Any controller containing an order-3 phase operation and an independent order-2 chirality operation has order divisible by 6. N/K realizes order 6 and the required inversion action, so S3 is minimal.\",\n");
  WriteAll(stream, Concatenation("  \"check_count\": ", String(Length(names)), ",\n"));
  WriteAll(stream, "  \"checks\": {\n");
  for tag in names do
    WriteAll(stream, Concatenation("    \"", tag, "\": ", B37(checks.(tag))));
    if tag <> names[Length(names)] then WriteAll(stream, ","); fi;
    WriteAll(stream, "\n");
  od;
  WriteAll(stream, "  }\n}\n");
  CloseStream(stream);
  Print("Pass1037 status=PASS checks=", Length(names), " output=", OUT, "\n");
end;;

Main37();;
QUIT;
